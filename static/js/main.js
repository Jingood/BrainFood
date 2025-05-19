document.addEventListener("DOMContentLoaded", function() {
    const chatBtn = document.querySelector(".start-btn");

    startBtn.addEventListener("click", function (e) {
        e.preventDefault();

        axios.get("/accounts/api/user/")
        .then(response => {
            window.location.href = "/chatbot/";
        })
        .catch(error => {
            window.location.href = "/accounts/login/";
        });
    });
});