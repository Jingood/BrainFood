document.addEventListener("DOMContentLoaded", () => {
    const SESSION_ID = window.location.pathname.match(/\/chat\/(\d+)\/*/)[1];
    const MSG_AREA = document.getElementById("chat-messages");
    const FORM = document.getElementById("chat-form");
    const INPUT = document.getElementById("chat-input");

    function appendMessage(text, side) {
        const wrap = document.createElement("div");
        wrap.className = `message ${side === "user" ? "user-message" : "bot-message"}`;

        const bubble = document.createElement("div");
        bubble.className = "message-bubble";
        bubble.textContent = text;

        wrap.appendChild(bubble);
        MSG_AREA.appendChild(wrap);
        MSG_AREA.scrollTop = MSG_AREA.scrollHeight;
    }

    axios.get(`/chat/api/sessions/${SESSION_ID}/`)
        .then(res => {
            const msgs = res.data.messages || [];
            msgs.forEach(m => appendMessage(m.content, m.role === "user" ? "user" : "bot"));
        })
        .catch(() => appendMessage("이전 대화를 불러오지 못했습니다.", "bot"));
    
    const wsProto = location.protocol === "https:" ? "wss" : "ws";
    const socket = new WebSocket(`${wsProto}://${location.host}/ws/chat/${SESSION_ID}/`);

    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.type === "assistant_message") {
            appendMessage(data.content, "bot");
        }
    };

    socket.onclose = () => console.warn("웹소켓 연결이 종료되었습니다.");

    FORM.addEventListener("submit", async (e) => {
        e.preventDefault();
        const text = INPUT.value.trim();
        if (!text) return;

        appendMessage(text, "user");
        INPUT.value = "";

        try {
            await axios.post(`/chat/api/sessions/${SESSION_ID}/messages/`, { content: text });
        } catch (err) {
            appendMessage("메시지 전송 실패, 다시 시도해 주세요.", "bot");
            console.error(err);
        }
    });
});