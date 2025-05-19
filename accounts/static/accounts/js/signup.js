document.addEventListener("DOMContentLoaded", function () {
    const signupForm = document.getElementById("signup-form");

    signupForm.addEventListener("submit", async function (e) {
        e.preventDefault();

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
            console.error(err);
        }
    });
});