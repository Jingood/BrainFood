document.addEventListener("DOMContentLoaded", () => {
    axios.defaults.withCredentials = true;
    axios.defaults.xsrfHeaderName = "X-CSRFToken";
    axios.defaults.xsrfCookieName = "csrftoken";

    function getCookie(name) {
    const match = document.cookie.match(new RegExp('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)'));
    return match ? decodeURIComponent(match[2]) : null;
    }

    axios.interceptors.request.use(config => {
    const method = config.method.toUpperCase();
    if (!["GET", "HEAD", "OPTIONS", "TRACE"].includes(method)) {
        config.headers["X-CSRFToken"] = getCookie("csrftoken");
    }
    return config;
    });

    let isRefreshing = false;
    let refreshSubscribers = [];

    function subscribeTokenRefresh(cb) { refreshSubscribers.push(cb); }
    function onRefreshed() { refreshSubscribers.forEach(cb => cb()); refreshSubscribers = []; }

    axios.interceptors.response.use(
    res => res,
    arr => {
        const { config, response } = err;
        if (!response || response.status !== 401 || config.__isRetry) return Promise.reject(err);
        
        if (isRefreshing) {
            return new Promise(resolve => {
                subscribeTokenRefresh(() => {
                    config.__isRetry = true;
                    resolve(axios(config));
                });
            });
        }

        isRefreshing = true;
        return axios.post("/accounts/api/refresh/", {}, {
            withCredentials: true,
        })
        .then(() => {
            isRefreshing = false;
            onRefreshed();
            config.__isRetry = true;
            return axios(config);
        })
        .catch(refreshErr => {
            isRefreshing = false;
            window.location.href = "/accounts/login/";
            return Promise.reject(refreshErr);
        });
    }
    );

    const logoBtn = document.querySelector(".logo")
    const profileBtn = document.getElementById("profile-signup-btn");
    const profileText = document.getElementById("profile-signup-text");
    const logoutBtn = document.getElementById("logout-login-btn");
    const logoutText = document.getElementById("logout-login-text");

    if (logoBtn) {
        logoBtn.style.cursor = "pointer";
        logoBtn.addEventListener("click", () => {
            window.location.href = "/";
        });
    }

    function renderLoggedIn(username = "프로필") {
    profileText.textContent = "프로필";
    profileBtn.setAttribute("href", "/accounts/profile/");

    logoutText.textContent = "로그아웃";
    logoutBtn.setAttribute("href", "#");
    logoutBtn.onclick = (e) => {
        e.preventDefault();
        axios.post("/accounts/api/logout/", {}, { withCredentials: true })
        .finally(() => {
            window.location.reload();
        });
    };
    }

    function renderLoggedOut() {
    profileText.textContent = "회원가입";
    profileBtn.setAttribute("href", "/accounts/signup/");
    profileBtn.onclick = null;

    logoutText.textContent = "로그인";
    logoutBtn.setAttribute("href", "/accounts/login/");
    logoutBtn.onclick = null;
    }

    const SKIP_USERINFO_PATHS = ["/", "/accounts/signup/", "/accounts/login/"];

    if (!SKIP_USERINFO_PATHS.some(p => location.pathname.startsWith(p))) {
        axios.get("/accounts/api/user/")
        .then((res) => renderLoggedIn(res.data.username))
        .catch(renderLoggedOut);
    }
});
