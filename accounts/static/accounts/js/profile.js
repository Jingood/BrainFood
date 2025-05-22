document.addEventListener("DOMContentLoaded", () => {
    const nicknameEl = document.getElementById("user-nickname");
    const gridEl = document.getElementById("sessions-container");
    const tmpl = document.getElementById("session-template");
    const noSessionMsg = document.getElementById("no-sessions-message");

    const PAGE_SIZE = 15;
    let sessions = [];
    let currentPage = 1;

    function makeSessionCard(session) {
        const node = tmpl.content.cloneNode(true);
        const link = node.querySelector(".session-button");
        const date = node.querySelector(".session-date");
        const info = node.querySelector(".session-info");

        link.href = `/chat/${session.id}/`;
        date.textContent = new Date(session.created_at)
            .toLocaleString("ko-KR", { dateStyle: "short", timeStyle: "short" });

        info.textContent = session.title || session.last_message || "(제목 없음)";
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