import http.server
import socketserver
import webbrowser

PORT = 8000

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>IntervAi - AI Mock Interview</title>

<style>
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: Arial, sans-serif;
    min-height: 100vh;
    color: #ffffff;
    background: linear-gradient(135deg, #080b20, #21154b, #063b48);
}

button,
input {
    font-family: inherit;
}

button {
    cursor: pointer;
}

.nav {
    height: 70px;
    padding: 0 6%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: rgba(0, 0, 0, 0.28);
    border-bottom: 1px solid rgba(255,255,255,0.12);
}

.logo {
    font-size: 23px;
    font-weight: bold;
}

.logo b {
    color: #a78bfa;
}

.nav button {
    padding: 10px 15px;
    margin-left: 7px;
    border: 0;
    border-radius: 9px;
    background: #7c3aed;
    color: white;
}

.page {
    display: none;
}

.page.active {
    display: block;
}

.container {
    width: 92%;
    max-width: 1150px;
    margin: auto;
    padding: 42px 0;
}

.auth {
    min-height: calc(100vh - 70px);
    display: flex;
    align-items: center;
    justify-content: center;
}

.authbox,
.panel {
    padding: 35px;
    border-radius: 24px;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.15);
    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
}

.authbox {
    width: 410px;
}

.authbox h1 {
    font-size: 36px;
    margin-bottom: 12px;
}

.muted {
    color: #b8bfd3;
    margin-bottom: 22px;
}

.input {
    width: 100%;
    padding: 14px;
    margin: 7px 0;
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.18);
    background: rgba(255,255,255,0.08);
    color: white;
    outline: none;
}

.input::placeholder {
    color: #aeb6ca;
}

.primary,
.action {
    border: 0;
    border-radius: 10px;
    padding: 13px 18px;
    background: #7c3aed;
    color: white;
    font-weight: bold;
}

.primary {
    width: 100%;
    margin-top: 12px;
}

.link {
    color: #c4b5fd;
    cursor: pointer;
    font-weight: bold;
}

.cards {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    margin-top: 30px;
}

.card {
    padding: 26px;
    border-radius: 18px;
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.12);
    transition: 0.3s;
}

.card:hover {
    transform: translateY(-5px);
    background: rgba(255,255,255,0.11);
}

.icon {
    font-size: 40px;
    margin-bottom: 14px;
}

.card p {
    color: #b8bfd3;
    line-height: 1.5;
    margin-top: 8px;
}

.start {
    margin-top: 18px;
    padding: 11px 18px;
    border: 0;
    border-radius: 9px;
    background: #7c3aed;
    color: white;
}

.interview {
    display: grid;
    grid-template-columns: 1.05fr 0.95fr;
    gap: 22px;
    margin-top: 22px;
}

.videoWrap {
    position: relative;
}

video {
    width: 100%;
    height: 360px;
    object-fit: cover;
    border-radius: 15px;
    background: #020617;
    transform: scaleX(-1);
}

.overlay {
    position: absolute;
    left: 15px;
    right: 15px;
    top: 15px;
    display: flex;
    justify-content: space-between;
    pointer-events: none;
}

.badge {
    padding: 8px 12px;
    border-radius: 20px;
    background: rgba(0,0,0,0.65);
    font-size: 13px;
}

.green {
    color: #4ade80;
}

.red {
    color: #f87171;
}

.metrics {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin-top: 14px;
}

.metric {
    padding: 13px;
    text-align: center;
    background: rgba(255,255,255,0.06);
    border-radius: 11px;
}

.metric strong {
    display: block;
    font-size: 24px;
    color: #c4b5fd;
}

.metric small {
    color: #b8bfd3;
}

.question {
    font-size: 28px;
    line-height: 1.4;
    min-height: 150px;
}

.answerBox {
    min-height: 110px;
    padding: 16px;
    border-radius: 13px;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.14);
    color: white;
    line-height: 1.5;
}

.actions {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin-top: 15px;
}

.action.secondary {
    background: #334155;
}

.action.stop {
    background: #dc2626;
}

.listening {
    margin-top: 15px;
    color: #4ade80;
    font-weight: bold;
}

.result {
    text-align: center;
}

.score {
    font-size: 72px;
    font-weight: 800;
    color: #c4b5fd;
    margin: 25px;
}

.scoregrid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 15px;
    margin-top: 25px;
}

.scorebox {
    padding: 20px;
    background: rgba(255,255,255,0.07);
    border-radius: 14px;
}

.scorebox strong {
    display: block;
    font-size: 30px;
    color: #c4b5fd;
    margin-top: 8px;
}

.feedback {
    text-align: left;
    margin-top: 25px;
    padding: 25px;
    border-radius: 16px;
    background: rgba(255,255,255,0.07);
}

.feedback li {
    margin: 10px 0;
    color: #d7dbea;
}

.brand {
    color: #a78bfa;
}

@media(max-width:850px) {
    .cards,
    .interview,
    .scoregrid {
        grid-template-columns: 1fr;
    }

    .container {
        width: 94%;
    }

    .authbox {
        width: 94%;
    }

    .question {
        font-size: 22px;
    }
}
</style>

<script src="https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/face_mesh.js"></script>

</head>

<body>

<div class="nav">

    <div class="logo">
        🤖 <b>IntervAi</b>
    </div>

    <div id="navRight"></div>

</div>


<!-- LOGIN -->

<section id="login" class="page active">

<div class="auth">

<div class="authbox">

<h1>Welcome Back 👋</h1>

<p class="muted">
Practice smarter with <span class="brand">IntervAi</span>.
</p>

<input
id="loginEmail"
class="input"
type="email"
placeholder="Email"
>

<input
id="loginPass"
class="input"
type="password"
placeholder="Password"
>

<button class="primary" onclick="login()">
Login
</button>

<p style="margin-top:20px;text-align:center">

New user?

<span class="link" onclick="showPage('register')">
Create account
</span>

</p>

</div>
</div>

</section>


<!-- REGISTER -->

<section id="register" class="page">

<div class="auth">

<div class="authbox">

<h1>Create Account 🚀</h1>

<p class="muted">
Join IntervAi and practice interviews with AI.
</p>

<input
id="regName"
class="input"
placeholder="Full Name"
>

<input
id="regEmail"
class="input"
type="email"
placeholder="Email"
>

<input
id="regPass"
class="input"
type="password"
placeholder="Password"
>

<button class="primary" onclick="registerUser()">
Create Account
</button>

<p style="margin-top:20px;text-align:center">

Already registered?

<span class="link" onclick="showPage('login')">
Login
</span>

</p>

</div>
</div>

</section>


<!-- DASHBOARD -->

<section id="dashboard" class="page">

<div class="container">

<h1>
Hello, <span id="name"></span> 👋
</h1>

<p class="muted">
Welcome to <span class="brand">IntervAi</span>.
Choose your interview type.
</p>

<div class="cards">

<div class="card">

<div class="icon">💻</div>

<h2>Technical</h2>

<p>
Python, AI, ML and programming questions.
</p>

<button
class="start"
onclick="startInterview('Technical')"
>
Start →
</button>

</div>


<div class="card">

<div class="icon">👔</div>

<h2>HR Interview</h2>

<p>
Communication, confidence and HR questions.
</p>

<button
class="start"
onclick="startInterview('HR')"
>
Start →
</button>

</div>


<div class="card">

<div class="icon">🧠</div>

<h2>Aptitude</h2>

<p>
Logical and quantitative questions.
</p>

<button
class="start"
onclick="startInterview('Aptitude')"
>
Start →
</button>

</div>

</div>

</div>

</section>


<!-- INTERVIEW -->

<section id="interview" class="page">

<div class="container">

<h1>🤖 IntervAi Interviewer</h1>

<div class="interview">


<div class="panel">

<h2>Live Camera & Behaviour</h2>

<br>

<div class="videoWrap">

<video
id="camera"
autoplay
muted
playsinline
></video>

<div class="overlay">

<span id="cameraBadge" class="badge">
Camera starting...
</span>

<span id="faceBadge" class="badge">
Face: --
</span>

</div>

</div>


<p id="status" class="listening">
Requesting camera + microphone...
</p>


<div class="metrics">

<div class="metric">

<strong id="eye">--</strong>

<small>
Eye Contact
</small>

</div>


<div class="metric">

<strong id="posture">--</strong>

<small>
Position/Posture
</small>

</div>


<div class="metric">

<strong id="expression">--</strong>

<small>
Expression
</small>

</div>

</div>


<p style="margin-top:14px;color:#aeb6ca;font-size:13px">

Live computer-vision estimates.
Keep your face visible and look toward the camera.

</p>

</div>


<div class="panel">

<p id="counter" class="muted">
Question 1 / 5
</p>

<div id="question" class="question"></div>


<div id="answerBox" class="answerBox">

Your spoken answer will appear here automatically...

</div>


<div class="actions">

<button
class="action"
onclick="repeatQuestion()"
>
🔊 Repeat
</button>

<button
class="action secondary"
onclick="startListening()"
>
🎙️ Speak Answer
</button>

<button
class="action stop"
onclick="finishInterview()"
>
Finish
</button>

</div>


<p id="listening" class="listening">
Preparing voice interview...
</p>

<p
id="feedback"
style="margin-top:15px"
></p>

</div>

</div>

</div>

</section>


<!-- RESULT -->

<section id="result" class="page">

<div class="container result">

<h1>
🎯 Interview Completed
</h1>

<p class="muted">
Your IntervAi performance report
</p>


<div id="overall" class="score">
0/100
</div>


<div class="scoregrid">

<div class="scorebox">
Answer Quality
<strong id="s1">0</strong>
</div>

<div class="scorebox">
Communication
<strong id="s2">0</strong>
</div>

<div class="scorebox">
Confidence
<strong id="s3">0</strong>
</div>

<div class="scorebox">
Eye Contact
<strong id="s4">0</strong>
</div>

<div class="scorebox">
Position/Posture
<strong id="s5">0</strong>
</div>

<div class="scorebox">
Expression
<strong id="s6">0</strong>
</div>

</div>


<div class="feedback">

<h2>
💡 Improvement Suggestions
</h2>

<ul>

<li id="tipEye">
Maintain eye contact with the camera.
</li>

<li id="tipPosture">
Keep your face centered and posture steady.
</li>

<li>
Speak clearly and confidently.
</li>

<li>
Give structured answers with examples.
</li>

<li>
Avoid unnecessary pauses and filler words.
</li>

</ul>

</div>


<button
class="primary"
style="max-width:300px"
onclick="showPage('dashboard')"
>
Back to Dashboard
</button>

</div>

</section>


<script>

const QUESTIONS = {

Technical: [
"What is Python?",
"What is Artificial Intelligence?",
"What is Machine Learning?",
"What is the difference between a list and a tuple?",
"Explain one project you have developed."
],

HR: [
"Tell me about yourself.",
"What are your strengths?",
"What are your weaknesses?",
"Why should we hire you?",
"Where do you see yourself in five years?"
],

Aptitude: [
"What is 20 percent of 500?",
"What is the average of 10, 20 and 30?",
"What is the next number: 2, 4, 8, 16?",
"A train travels 60 km in 2 hours. What is its speed?",
"What is 25 percent of 800?"
]

};


let interviewType = "";
let questionIndex = 0;
let totalScore = 0;

let cameraStream = null;
let recognition = null;
let interviewActive = false;

let visual = {
    eye: 0,
    posture: 0,
    expression: 0,
    count: 0
};


function showPage(id) {

    document
        .querySelectorAll(".page")
        .forEach(function(page) {
            page.classList.remove("active");
        });

    document
        .getElementById(id)
        .classList.add("active");

    updateNavbar();
}


function updateNavbar() {

    const user = localStorage.getItem("mockUser");

    const nav = document.getElementById("navRight");

    if (user) {

        nav.innerHTML =
        '<button onclick="showPage(\'dashboard\')">Dashboard</button>' +
        '<button onclick="logout()">Logout</button>';

    } else {

        nav.innerHTML = "";

    }
}


function registerUser() {

    const name =
        document.getElementById("regName").value.trim();

    const email =
        document.getElementById("regEmail").value.trim();

    const password =
        document.getElementById("regPass").value;


    if (!name || !email || !password) {

        alert("Please fill all fields.");

        return;
    }


    if (password.length < 4) {

        alert("Password must contain at least 4 characters.");

        return;
    }


    let users =
        JSON.parse(
            localStorage.getItem("mockUsers") || "[]"
        );


    const exists =
        users.some(function(user) {

            return user.email.toLowerCase()
                === email.toLowerCase();

        });


    if (exists) {

        alert("This email is already registered.");

        return;
    }


    users.push({
        name: name,
        email: email,
        password: password
    });


    localStorage.setItem(
        "mockUsers",
        JSON.stringify(users)
    );


    document.getElementById("regName").value = "";
    document.getElementById("regEmail").value = "";
    document.getElementById("regPass").value = "";


    alert(
        "Account created successfully! Now login."
    );


    showPage("login");
}


function login() {

    const email =
        document.getElementById("loginEmail").value.trim();

    const password =
        document.getElementById("loginPass").value;


    if (!email || !password) {

        alert("Please enter email and password.");

        return;
    }


    const users =
        JSON.parse(
            localStorage.getItem("mockUsers") || "[]"
        );


    const user =
        users.find(function(user) {

            return (
                user.email.toLowerCase()
                === email.toLowerCase()
                &&
                user.password === password
            );

        });


    if (!user) {

        alert(
            "Invalid email or password. Create an account first."
        );

        return;
    }


    localStorage.setItem(
        "mockUser",
        user.name
    );


    document.getElementById("name").textContent =
        user.name;


    showPage("dashboard");
}


function logout() {

    stopMedia();

    localStorage.removeItem("mockUser");

    showPage("login");
}


async function startInterview(type) {

    interviewType = type;

    questionIndex = 0;

    totalScore = 0;

    visual = {
        eye: 0,
        posture: 0,
        expression: 0,
        count: 0
    };


    interviewActive = true;


    showPage("interview");

    showQuestion();


    try {

        if (!navigator.mediaDevices ||
            !navigator.mediaDevices.getUserMedia) {

            throw new Error(
                "Camera API not supported"
            );

        }


        cameraStream =
            await navigator.mediaDevices.getUserMedia({
                video: true,
                audio: true
            });


        document.getElementById("camera")
            .srcObject = cameraStream;


        document.getElementById("cameraBadge")
            .textContent = "● Camera ON";

        document.getElementById("cameraBadge")
            .className = "badge green";


        document.getElementById("status")
            .textContent = "● Camera + Microphone ON";


        startFaceAnalysis();

        speakAndThenListen();

    }

    catch (error) {

        console.error(error);


        document.getElementById("cameraBadge")
            .textContent = "Camera blocked";


        document.getElementById("cameraBadge")
            .className = "badge red";


        document.getElementById("status")
            .textContent =
            "Camera/Microphone permission required. Click Speak Answer to continue.";

    }

}


function showQuestion() {

    document.getElementById("counter")
        .textContent =
        "Question " +
        (questionIndex + 1) +
        " / 5";


    document.getElementById("question")
        .textContent =
        QUESTIONS[interviewType][questionIndex];


    document.getElementById("answerBox")
        .textContent =
        "Your spoken answer will appear here automatically...";


    document.getElementById("feedback")
        .textContent = "";

}


function speakAndThenListen() {

    if (!interviewActive) {
        return;
    }


    const text =
        document.getElementById("question")
        .textContent;


    if ("speechSynthesis" in window) {

        const speech =
            new SpeechSynthesisUtterance(text);


        speech.lang = "en-IN";

        speech.rate = 0.88;


        speech.onend = function() {

            setTimeout(
                startListening,
                400
            );

        };


        window.speechSynthesis.cancel();

        window.speechSynthesis.speak(speech);

    }

    else {

        startListening();

    }

}


function repeatQuestion() {

    if (!interviewActive) {
        return;
    }


    if ("speechSynthesis" in window) {
        window.speechSynthesis.cancel();
    }


    speakAndThenListen();
}


function getRecognition() {

    const SpeechRecognition =
        window.SpeechRecognition ||
        window.webkitSpeechRecognition;


    if (!SpeechRecognition) {
        return null;
    }


    const recognition =
        new SpeechRecognition();


    recognition.lang = "en-IN";

    recognition.continuous = false;

    recognition.interimResults = true;

    recognition.maxAlternatives = 1;


    return recognition;
}


function startListening() {

    if (!interviewActive) {
        return;
    }


    recognition = getRecognition();


    if (!recognition) {

        document.getElementById("listening")
            .textContent =
            "Voice recognition is not supported. Please use Google Chrome.";

        return;
    }


    let finalText = "";


    document.getElementById("listening")
        .textContent =
        "🎙️ Listening... Speak your answer now.";


    recognition.onresult = function(event) {

        let text = "";


        for (
            let i = event.resultIndex;
            i < event.results.length;
            i++
        ) {

            text +=
                event.results[i][0].transcript;

        }


        document.getElementById("answerBox")
            .textContent = text;


        if (
            event.results[
                event.results.length - 1
            ].isFinal
        ) {

            finalText = text;

        }

    };


    recognition.onerror = function(event) {

        document.getElementById("listening")
            .textContent =
            "Microphone error: " +
            event.error +
            ". Click Speak Answer again.";

    };


    recognition.onend = function() {

        if (finalText.trim()) {

            document.getElementById("answerBox")
                .textContent = finalText;


            setTimeout(
                function() {
                    submitVoiceAnswer(finalText);
                },
                500
            );

        }

        else {

            document.getElementById("listening")
                .textContent =
                "No speech detected. Click Speak Answer again.";

        }

    };


    try {

        recognition.start();

    }

    catch (error) {

        console.log(error);

    }

}


function submitVoiceAnswer(answer) {

    if (!interviewActive) {
        return;
    }


    const words =
        answer
        .trim()
        .split(/\s+/)
        .filter(Boolean)
        .length;


    let marks;


    if (words >= 30) {
        marks = 20;
    }

    else if (words >= 20) {
        marks = 17;
    }

    else if (words >= 10) {
        marks = 14;
    }

    else if (words >= 5) {
        marks = 10;
    }

    else {
        marks = 5;
    }


    totalScore += marks;


    document.getElementById("feedback")
        .innerHTML =
        "<b>Answer Score: " +
        marks +
        "/20</b> — " +
        (
            marks >= 17
            ? "Excellent answer."
            : marks >= 14
            ? "Good answer. Add examples."
            : "Give a longer and clearer answer."
        );


    questionIndex++;


    if (questionIndex < 5) {

        setTimeout(function() {

            showQuestion();

            speakAndThenListen();

        }, 1300);

    }

    else {

        setTimeout(
            showResult,
            1300
        );

    }

}


function finishInterview() {

    if (!interviewActive) {
        return;
    }


    interviewActive = false;


    if (recognition) {

        try {
            recognition.abort();
        }

        catch (error) {}

    }


    if ("speechSynthesis" in window) {

        window.speechSynthesis.cancel();

    }


    showResult();
}


function stopMedia() {

    interviewActive = false;


    if (recognition) {

        try {
            recognition.abort();
        }

        catch (error) {}

    }


    if ("speechSynthesis" in window) {

        window.speechSynthesis.cancel();

    }


    if (cameraStream) {

        cameraStream
            .getTracks()
            .forEach(function(track) {

                track.stop();

            });


        cameraStream = null;

    }

}


function startFaceAnalysis() {

    if (typeof FaceMesh === "undefined") {

        document.getElementById("faceBadge")
            .textContent =
            "Face AI unavailable";

        return;
    }


    const video =
        document.getElementById("camera");


    const faceMesh =
        new FaceMesh({

            locateFile: function(file) {

                return (
                    "https://cdn.jsdelivr.net/npm/" +
                    "@mediapipe/face_mesh/" +
                    file
                );

            }

        });


    faceMesh.setOptions({

        maxNumFaces: 1,

        refineLandmarks: true,

        minDetectionConfidence: 0.5,

        minTrackingConfidence: 0.5

    });


    faceMesh.onResults(function(results) {

        if (!interviewActive) {
            return;
        }


        if (
            !results.multiFaceLandmarks ||
            results.multiFaceLandmarks.length === 0
        ) {

            document.getElementById("faceBadge")
                .textContent =
                "Face: Not detected";

            return;
        }


        const lm =
            results.multiFaceLandmarks[0];


        const nose = lm[1];

        const mouthTop = lm[13];

        const mouthBottom = lm[14];


        const faceX = nose.x;

        const faceY = nose.y;


        let eyeScore =
            100 -
            Math.min(
                100,
                Math.abs(faceX - 0.5) * 220
            );


        let positionScore =
            100 -
            Math.min(
                100,
                Math.abs(faceY - 0.50) * 180
            );


        const mouthOpen =
            Math.abs(
                mouthBottom.y -
                mouthTop.y
            );


        let expressionScore =
            70 +
            Math.min(
                25,
                mouthOpen * 300
            );


        eyeScore =
            Math.round(
                Math.max(
                    0,
                    Math.min(100, eyeScore)
                )
            );


        positionScore =
            Math.round(
                Math.max(
                    0,
                    Math.min(100, positionScore)
                )
            );


        expressionScore =
            Math.round(
                Math.max(
                    0,
                    Math.min(100, expressionScore)
                )
            );


        visual.eye += eyeScore;

        visual.posture += positionScore;

        visual.expression += expressionScore;

        visual.count++;


        document.getElementById("eye")
            .textContent = eyeScore;


        document.getElementById("posture")
            .textContent = positionScore;


        document.getElementById("expression")
            .textContent = expressionScore;


        document.getElementById("faceBadge")
            .textContent =
            "Face: Detected";

    });


    async function loop() {

        if (!interviewActive) {
            return;
        }


        if (video.readyState >= 2) {

            try {

                await faceMesh.send({
                    image: video
                });

            }

            catch (error) {

                console.log(error);

            }

        }


        requestAnimationFrame(loop);

    }


    loop();
}


function showResult() {

    const count =
        Math.max(
            1,
            visual.count
        );


    const eye =
        Math.round(
            visual.eye / count
        );


    const posture =
        Math.round(
            visual.posture / count
        );


    const expression =
        Math.round(
            visual.expression / count
        );


    const communication =
        Math.min(
            100,
            Math.max(
                0,
                totalScore * 5 + 5
            )
        );


    const confidence =
        Math.min(
            100,
            Math.max(
                0,
                Math.round(
                    (
                        eye +
                        posture +
                        expression
                    ) / 3
                )
            )
        );


    const answerQuality =
        Math.min(
            100,
            totalScore * 5
        );


    const overall =
        Math.round(
            (
                answerQuality +
                communication +
                confidence +
                eye +
                posture +
                expression
            ) / 6
        );


    stopMedia();


    document.getElementById("overall")
        .textContent =
        overall + "/100";


    document.getElementById("s1")
        .textContent =
        answerQuality;


    document.getElementById("s2")
        .textContent =
        communication;


    document.getElementById("s3")
        .textContent =
        confidence;


    document.getElementById("s4")
        .textContent =
        eye;


    document.getElementById("s5")
        .textContent =
        posture;


    document.getElementById("s6")
        .textContent =
        expression;


    document.getElementById("tipEye")
        .textContent =
        eye < 70
        ? "Improve eye contact: look toward the camera more often."
        : "Eye contact is good. Keep it consistent.";


    document.getElementById("tipPosture")
        .textContent =
        posture < 70
        ? "Improve position: keep your face centered and sit straight."
        : "Your position/posture is good.";


    showPage("result");
}


updateNavbar();


const savedUser =
    localStorage.getItem("mockUser");


if (savedUser) {

    document.getElementById("name")
        .textContent = savedUser;

    showPage("dashboard");

}

</script>

</body>
</html>
"""


class Handler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path == "/" or self.path.startswith("/?"):

            data = HTML.encode("utf-8")

            self.send_response(200)

            self.send_header(
                "Content-Type",
                "text/html; charset=utf-8"
            )

            self.send_header(
                "Content-Length",
                str(len(data))
            )

            self.end_headers()

            self.wfile.write(data)

        else:

            self.send_response(404)

            self.end_headers()


    def log_message(self, format, *args):
        pass


def main():

    print("======================================")
    print("          INTERVAI")
    print("       AI MOCK INTERVIEW")
    print("======================================")
    print()
    print("Starting IntervAi...")
    print()
    print("Open in Chrome:")
    print("http://localhost:8000")
    print()
    print("Camera + microphone are required.")
    print("Use Google Chrome for voice recognition.")
    print()
    print("Press Ctrl+C to stop.")
    print()


    with socketserver.ThreadingTCPServer(
        ("", PORT),
        Handler
    ) as server:

        webbrowser.open(
            "http://localhost:8000"
        )

        server.serve_forever()


if __name__ == "__main__":
    main()