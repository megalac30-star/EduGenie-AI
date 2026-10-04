const API_BASE_URL = "http://127.0.0.1:8000";

const userInput = document.getElementById("userInput");
const runBtn = document.getElementById("runBtn");
const runText = document.getElementById("runText");
const spinner = document.getElementById("spinner");
const result = document.getElementById("result");
const errorBox = document.getElementById("errorBox");
const clearBtn = document.getElementById("clearBtn");
const copyBtn = document.getElementById("copyBtn");
const charCount = document.getElementById("charCount");

const modeLabel = document.getElementById("modeLabel");
const modeTitle = document.getElementById("modeTitle");
const inputLabel = document.getElementById("inputLabel");

let currentTask = "qa";

const taskNames = {
    qa: {
        label: "ASK A QUESTION",
        title: "What would you like to learn?",
        input: "Your Question",
        button: "Ask EduGenie",
        placeholder: "Example: What is Artificial Intelligence?"
    },

    explain: {
        label: "EXPLAIN A TOPIC",
        title: "Which topic should I explain?",
        input: "Topic",
        button: "Explain Topic",
        placeholder: "Example: Explain machine learning"
    },

    quiz: {
        label: "GENERATE QUIZ",
        title: "What topic should I create a quiz about?",
        input: "Topic",
        button: "Generate Quiz",
        placeholder: "Example: Python programming"
    },

    summarize: {
        label: "SUMMARIZE",
        title: "What should I summarize?",
        input: "Text",
        button: "Summarize",
        placeholder: "Paste your notes here..."
    },

    learn: {
        label: "LEARNING PATH",
        title: "What would you like to learn?",
        input: "Topic",
        button: "Create Learning Path",
        placeholder: "Example: Learn Python from beginner to advanced"
    }
};


// ===============================
// API CALL
// ===============================

async function callAPI(endpoint, text) {

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            text: text
        })
    });

    let data;

    try {
        data = await response.json();
    } catch {
        throw new Error("Backend returned an invalid response.");
    }

    if (!response.ok) {
        throw new Error(
            data.detail ||
            data.message ||
            "Something went wrong."
        );
    }

    return data.result || data.answer || data.response || data;
}


// ===============================
// ASK QUESTION
// ===============================

async function askQuestion(text) {
    return await callAPI("/qa", text);
}


// ===============================
// EXPLAIN
// ===============================

async function explainTopic(text) {
    return await callAPI("/explain", text);
}


// ===============================
// QUIZ
// ===============================

async function generateQuiz(text) {
    return await callAPI("/quiz", text);
}


// ===============================
// SUMMARY
// ===============================

async function summarizeText(text) {
    return await callAPI("/summarize", text);
}


// ===============================
// LEARNING PATH
// ===============================

async function learningPath(text) {
    return await callAPI("/learn", text);
}


// ===============================
// RUN BUTTON
// ===============================

runBtn.addEventListener("click", async function () {

    const text = userInput.value.trim();

    if (!text) {
        showError("Please enter your question or topic.");
        userInput.focus();
        return;
    }

    clearError();

    runBtn.disabled = true;
    spinner.classList.remove("hidden");

    const originalText = runText.textContent;
    runText.textContent = "Thinking...";

    result.classList.remove("empty");
    result.innerHTML = "<p>EduGenie is thinking...</p>";

    try {

        let answer;

        if (currentTask === "qa") {
            answer = await askQuestion(text);

        } else if (currentTask === "explain") {
            answer = await explainTopic(text);

        } else if (currentTask === "quiz") {
            answer = await generateQuiz(text);

        } else if (currentTask === "summarize") {
            answer = await summarizeText(text);

        } else if (currentTask === "learn") {
            answer = await learningPath(text);
        }

        displayResult(answer);

    } catch (error) {

        console.error("EDUGENIE ERROR:", error);

        result.classList.add("empty");
        result.innerHTML = `
            <div>⚠</div>
            <p>Unable to get a response.</p>
        `;

        showError(error.message);

    } finally {

        runBtn.disabled = false;
        spinner.classList.add("hidden");
        runText.textContent = originalText;
    }
});


// ===============================
// TASK BUTTONS
// ===============================

document.querySelectorAll(".task").forEach(button => {

    button.addEventListener("click", function () {

        document.querySelectorAll(".task").forEach(btn => {
            btn.classList.remove("active");
        });

        this.classList.add("active");

        currentTask = this.dataset.task;

        const settings = taskNames[currentTask];

        modeLabel.textContent = settings.label;
        modeTitle.textContent = settings.title;
        inputLabel.textContent = settings.input;

        runText.textContent = settings.button;
        userInput.placeholder = settings.placeholder;

        clearInput();
    });
});


// ===============================
// CLEAR BUTTON
// ===============================

clearBtn.addEventListener("click", function () {
    clearInput();
});

function clearInput() {

    userInput.value = "";
    charCount.textContent = "0 characters";

    clearError();

    result.className = "result empty";

    result.innerHTML = `
        <div>✦</div>
        <p>Your result will appear here.</p>
    `;

    copyBtn.classList.add("hidden");
}


// ===============================
// CHARACTER COUNT
// ===============================

userInput.addEventListener("input", function () {

    const length = userInput.value.length;

    charCount.textContent =
        `${length} character${length === 1 ? "" : "s"}`;
});


// ===============================
// CTRL + ENTER
// ===============================

userInput.addEventListener("keydown", function (event) {

    if (event.ctrlKey && event.key === "Enter") {
        runBtn.click();
    }
});


// ===============================
// DISPLAY RESULT
// ===============================

function displayResult(data) {

    let text;

    if (typeof data === "string") {
        text = data;
    } else {
        text = JSON.stringify(data, null, 2);
    }

    result.className = "result";

    result.innerHTML = `
        <div style="white-space: pre-wrap;">${escapeHTML(text)}</div>
    `;

    copyBtn.classList.remove("hidden");
}


// ===============================
// COPY RESULT
// ===============================

copyBtn.addEventListener("click", async function () {

    const text = result.innerText;

    try {

        await navigator.clipboard.writeText(text);

        copyBtn.textContent = "Copied!";

        setTimeout(() => {
            copyBtn.textContent = "Copy";
        }, 1500);

    } catch (error) {
        console.error("Copy failed:", error);
    }
});


// ===============================
// ERROR
// ===============================

function showError(message) {

    errorBox.textContent = message;
    errorBox.classList.remove("hidden");
}

function clearError() {

    errorBox.textContent = "";
    errorBox.classList.add("hidden");
}


// ===============================
// HTML SAFETY
// ===============================

function escapeHTML(text) {

    return String(text)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}


console.log("EduGenie app.js loaded successfully.");