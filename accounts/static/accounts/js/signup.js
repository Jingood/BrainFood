document.addEventListener("DOMContentLoaded", function () {
    const signupForm = document.getElementById("signup-form");
    const loginLink = document.querySelector(".login-link")
    const statusBox = document.createElement("p");
    statusBox.className = "signup-status";
    signupForm.appendChild(statusBox);

    if (loginLink) {
        loginLink.setAttribute("href", "/accounts/login/");
    }

    signupForm.addEventListener("submit", async function (e) {
        e.preventDefault();
        statusBox.textContent = "";
        const btn = signupForm.querySelector(".signup-button");
        btn.disabled = true;

        const payload = {
            username: signupForm.username.value.trim(),
            password: signupForm.password.value,
            nickname: signupForm.nickname.value.trim(),
            email: signupForm.email.value.trim(),
        };

        try {
            await axios.post("/accounts/api/signup/", payload);
            window.location.href = "/accounts/login/";
        } catch (err) {
            if (err.response) {
                if (err.response.status === 400) {
                    const errors = err.response.data;
                    const msg = Object.values(errors).flat().join(" / ");
                    statusBox.textContent = `회원가입 실패: ${msg}`;
                } else {
                    statusBox.textContent = `오류 (${err.response.status})가 발생했습니다.`;
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