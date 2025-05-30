document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("change-password-form");
    const cancelLink = document.querySelector(".cancel-link");
    const statusBox = document.createElement("p");
    statusBox.className = "change-status";
    form.appendChild(statusBox);

    if (cancelLink) {
        cancelLink.setAttribute("href", "/accounts/profile/");
    }

    form.addEventListener("submit", async function (e) {
        e.preventDefault();
        statusBox.textContent = "";
        const btn = document.querySelector(".change-password-button");
        btn.disabled = true;

        const payload = {
            old_password: form.current_password.value,
            new_password1: form.new_password.value,
            new_password2: form.confirm_password.value,
        };

        try {
            await axios.post("/accounts/api/password_change/", payload);
            window.location.href = "/accounts/profile/";
        } catch (err) {
            if (err.response) {
                const msg = 
                    err.response.status === 400 && typeof err.response.data == "object"
                        ? Object.values(err.response.data).flat().join(" / ")
                        : `오류(${err.response.status})가 발생했습니다.`;
                statusBox.textContent = msg;
            } else if (err.request) {
                statusBox.textContent = "네트워크 오류: 서버에 연결할 수 없습니다.";
            } else {
                statusBox.textContent = "알 수 없는 오류입니다."
            }
        } finally {
            btn.disabled = false;
        }
    })
})