document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("login-form");
    const signupLink = document.querySelector(".signup-link");
    const statusBox = document.createElement("p");
    statusBox.className = "login-status";
    form.appendChild(statusBox);

    if (signupLink) {
        signupLink.setAttribute("href", "/accounts/signup/");
    }

    loginForm.addEventListener("submit", async function (e) {
        e.preventDefault();
        statusBox.textContent = "";
        const btn = form.querySelector(".login-button");
        btn.disabled = true;

        const payload = {
            username: loginForm.username.value.trim(),
            password: loginForm.password.value,
        };

        try {
            await axios.post("/accounts/api/login/", payload);
            window.location.href = "/";
        } catch (err) {
            if (err.response) {
                if (err.response.status === 401) {
                    statusBox.textContent = "아이디 또는 비밀번호가 올바르지 않습니다.";
                } else {
                    statusBox.textContent = `오류(${err.response.status})가 발생했습니다.`;
                }
            } else if (err.request) {
                statusBox.textContent = "네트워크 오류: 서버에 연결할 수 없습니다.";
            } else {
                statusBox.textContent = "알 수 없는 오류가 발생했습니다.";
            }
        } finally {
            btn.disabled = false;
        }
    });
});