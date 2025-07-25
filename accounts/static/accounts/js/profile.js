document.addEventListener("DOMContentLoaded", () => {
    const nicknameEl = document.getElementById("user-nickname");
    const gridEl = document.getElementById("sessions-container");
    const tmpl = document.getElementById("session-template");
    const noSessionMsg = document.getElementById("no-sessions-message");
    const changeBtn = document.querySelector(".password-change-button");
    const deleteBtn = document.querySelector(".account-delete-button");

    changeBtn.addEventListener("click", function() {
        window.location.href = "/accounts/password_change/";
    })

    deleteBtn.addEventListener("click", async (e) => {
        e.preventDefault()

        const ok = confirm("정말로 계정을 삭제하시겠습니까? 이 작업은 되돌릴 수 없습니다.");
        if (!ok) return;

        try {
            await axios.delete("/accounts/api/delete/");
            window.location.href = "/";
        } catch (err) {
            console.error(err);
        }
    })

    const chatBtn = document.querySelector(".new-chat-button");

    chatBtn.addEventListener("click", function (e) {
        e.preventDefault()

        axios.post("/chat/api/sessions/", { title: "", first_message: "" })
            .then(res => {
                const newId = res.data.id;
                window.location.href = `/chat/${newId}`;
            });
    })

    const PAGE_SIZE = 15;
    let sessions = [];
    let currentPage = 1;

    function makeSessionCard(session) {
        const node = tmpl.content.cloneNode(true);

        const card = node.querySelector(".session-card");
        card.id = `session-${session.id}`;

        const link = node.querySelector(".session-button");
        link.href = `/chat/${session.id}/`;

        node.querySelector(".session-date").textContent =
            new Date(session.created_at).toLocaleString("ko-KR", 
                { dateStyle: "short", timeStyle: "short" });
        
        node.querySelector(".session-info").textContent =
            session.title || session.last_message || "(제목 없음)";
        
        const delBtn = node.querySelector(".session-delete-btn");
        delBtn.onclick = async (e) => {
            e.stopPropagation();
            const ok = confirm("세션을 삭제하시겠습니까?");
            if (!ok) return;
            try {
                await axios.delete(`/chat/api/sessions/${session.id}/delete/`);
                document.getElementById(`session-${session.id}`).remove();
                sessions = sessions.filter(s => s.id !== session.id);
                if (sessions.length === 0) renderPage(1);
            } catch (err) {
                console.error(err);
            }
        };
        return node;
    }

    function renderPage(page = 1) {
        gridEl.innerHTML = "";
        const start = (page - 1) * PAGE_SIZE;
        const pageItems = sessions.slice(start, start + PAGE_SIZE);

        if (pageItems.length === 0) {
            noSessionMsg.style.display = "block";
            return;
        }
        noSessionMsg.style.display = "none";

        pageItems.forEach(s => gridEl.appendChild(makeSessionCard(s)));

        drawPaginator(page);
    }

    function drawPaginator(active) {
        const old = document.querySelector(".paginator");
        old && old.remove();

        const totalPages = Math.ceil(sessions.length / PAGE_SIZE);
        if (totalPages <= 1) return;

        const pag = document.createElement("div");
        pag.className = "paginator";

        for (let p = 1; p <= totalPages; p++) {
            const btn = document.createElement("button");
            btn.textContent = p;
            btn.className = p === active ? "page-btn active" : "page-btn";
            btn.onclick = () => {
                currentPage = p;
                renderPage(p);
            };
            pag.appendChild(btn);
        }
        gridEl.after(pag);
    }

    axios.get("/accounts/api/profile/")
    .then(res => {
        nicknameEl.textContent = res.data.nickname;
        sessions = res.data.sessions || [];
        renderPage(1);
    })
    .catch(err => {
        console.error(err);
        window.location.href = "/accounts/login/";
    });
});