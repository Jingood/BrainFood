document.addEventListener("DOMContentLoaded", function() {
    const chatBtn = document.querySelector(".start-btn");

    chatBtn.addEventListener("click", function (e) {
        e.preventDefault();

        axios.get("/accounts/api/user/")
        .then(response => {
            axios.post("/chat/api/sessions/", { title: "", first_message: "" })
            .then(res => {
                const newId = res.data.id;
                window.location.href = `/chat/${newId}/`;
            });
        })
        .catch(error => {
            window.location.href = "/accounts/login/";
        });
    });
});