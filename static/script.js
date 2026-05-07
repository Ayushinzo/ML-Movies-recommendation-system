let chatHistory = [];

const recommendBtn = document.getElementById("recommendBtn");

function toggleChat() {
    const chatWindow = document.getElementById("chatWindow");
    chatWindow.classList.toggle("active");
}

function addMessage(text, sender) {
    const chatMessages = document.getElementById("chatMessages");
    const msgDiv = document.createElement("div");

    msgDiv.className = `message ${sender}`;

    if (text === "typing") {
        msgDiv.id = "typingIndicator";
        msgDiv.innerHTML = `
            <div class="typing-dots">
                <span></span><span></span><span></span>
            </div>
        `;
    } else {
        msgDiv.innerText = text;
    }

    chatMessages.appendChild(msgDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function displayMovies(list) {
    const container = document.getElementById("moviesContainer");
    container.innerHTML = "";

    list.forEach((movie) => {
        const card = document.createElement("div");
        card.className = "movie";

        const poster = movie.poster_url && movie.poster_url !== movie.movie_id
            ? movie.poster_url
            : "https://picsum.photos/300/450";

        card.innerHTML = `
            <div class="ask-icon">✨</div>

            <img class="poster" src="${poster}" alt="${movie.title}">

            <div class="content">
                <div class="title">${movie.title}</div>
                <div class="overview">${shortText(movie.overview, 140)}</div>

                <div class="meta">
                    Genres: ${movie.genres}<br>
                    Runtime: ${movie.runtime} min<br>
                    Release Date: ${movie.release_date}<br>
                    Director: ${movie.director}<br>
                    Vote Count: ${movie.vote_count}<br>
                </div>
            </div>
        `;

        card.querySelector(".ask-icon").addEventListener("click", () => {
            askMovieBot(movie.title);
        });

        const overviewEl = card.querySelector(".overview");

        overviewEl.addEventListener("mouseenter", (e) => {
            if (movie.overview && movie.overview.length > 140) {
                showOverviewToast(e, movie.overview);
            }
        });

        overviewEl.addEventListener("mousemove", moveOverviewToast);

        overviewEl.addEventListener("mouseleave", hideOverviewToast);

        container.appendChild(card);
    });
}

recommendBtn.addEventListener("click", async () => {
    const query = document.getElementById("searchInput").value.trim();

    if (!query) return;

    const btnText = document.getElementById("btnText");
    const loader = document.getElementById("btnLoader");

    // start loading
    recommendBtn.disabled = true;
    btnText.innerText = "Finding...";
    btnText.classList.add("loading-text");
    loader.classList.remove("hidden");

    try {
        const response = await fetch(`/query/${encodeURIComponent(query)}`, {
            method: "GET",
            headers: {
                "Accept": "application/json"
            }
        });

        if (!response.ok) {
            throw new Error("Request failed: " + response.status);
            console.log(response.message)
        }

        const data = await response.json();

        displayMovies(data);

    } catch (error) {
        console.error("Error fetching movies:", error);
    } finally {
        // stop loading
        recommendBtn.disabled = false;
        btnText.innerText = "Recommend";
        btnText.classList.remove("loading-text");
        loader.classList.add("hidden");
    }
});

async function askMovieBot(movieTitle) {
    const chatWindow = document.getElementById("chatWindow");

    if (!chatWindow.classList.contains("active")) {
        toggleChat();
    }

    const message = `Write a punchy, one-paragraph, spoiler-free summary of movie "${movieTitle}" covering its premise, tone, and central conflict.`;
    const placeholder = "Summary of " + movieTitle;
    addMessage(placeholder, "user");
    sendToBot(message);
}

async function sendToBot(userMessage) {
    try {
        addMessage("typing", "bot");

        chatHistory.push({
            role: "user",
            content: userMessage
        });

        const response = await fetch("/chatbot", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            body: JSON.stringify({
                messages: chatHistory
            })
        });

        if (!response.ok) {
            throw new Error("Chatbot request failed: " + response.status);
        }

        const data = await response.json();

        document.getElementById("typingIndicator")?.remove();

        addMessage(data.reply, "bot");

        chatHistory.push({
            role: "assistant",
            content: data.reply
        });
    } catch (error) {
        document.getElementById("typingIndicator")?.remove();
        console.error("Chatbot error:", error);
        addMessage("System error. Please try again.", "bot");
    }
}

function handleManualChat() {
    const input = document.getElementById("userInput");
    const message = input.value.trim();
    if (!message) return;
    addMessage(message, "user");
    sendToBot(message);
    input.value = "";
}

function shortText(text, limit = 140) {
    if (!text) return "No overview available.";

    if (text.length <= limit) {
        return text;
    }

    return text.substring(0, limit) + ` <span class="more-text">...more</span>`;
}

function showOverviewToast(event, fullText) {
    let toast = document.getElementById("overviewToast");

    if (!toast) {
        toast = document.createElement("div");
        toast.id = "overviewToast";
        toast.className = "overview-toast";
        document.body.appendChild(toast);
    }

    toast.innerText = fullText;

    const x = event.clientX + 18;
    const y = event.clientY + 18;

    toast.style.left = x + "px";
    toast.style.top = y + "px";

    toast.classList.add("show");
}

function moveOverviewToast(event) {
    const toast = document.getElementById("overviewToast");
    if (!toast) return;

    toast.style.left = event.clientX + 18 + "px";
    toast.style.top = event.clientY + 18 + "px";
}

function hideOverviewToast() {
    const toast = document.getElementById("overviewToast");
    if (!toast) return;
    toast.classList.remove("show");
}