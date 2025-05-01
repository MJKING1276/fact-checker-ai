import os
from dotenv import load_dotenv
import re
import requests
from flask import Flask, request, render_template_string
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# ---- API KEY SETUP ----
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
GENAI_API_KEY = os.getenv("GENAI_API_KEY")

# Configure Google Generative AI
genai.configure(api_key=GENAI_API_KEY)
model = genai.GenerativeModel(model_name="models/gemini-2.0-flash")
# ---- HTML TEMPLATE ----
HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>FACT CHECKER AI AGENT</title>
  <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
  <style>
    body {
      font-family: 'Press Start 2P', cursive;
      background: black;
      color: #00f7ff;
      margin: 0;
      overflow: auto;
      font-size: 0.9rem;
    }

    .snake {
      position: absolute;
      top: 50%;
      left: 0;
      width: 100%;
      height: 10px;
      background: linear-gradient(90deg, #ff00ff, #00f7ff);
      animation: snakeMove 1.0s linear infinite;
    }

    @keyframes snakeMove {
      0% { transform: translateX(-100%); }
      100% { transform: translateX(100%); }
    }

    .formula-bg {
      position: fixed;
      width: 100%;
      height: 100%;
      z-index: -1;
      pointer-events: none;
      background-image: url('https://i.imgur.com/tH7e7Vk.png');
      background-size: contain;
      opacity: 0.08;
      animation: floatFormulas 10s infinite linear alternate;
    }

    @keyframes floatFormulas {
      0% { transform: translateY(0); }
      100% { transform: translateY(-20px); }
    }

    .morphing-shape {
      position: fixed;
      width: 150px;
      height: 150px;
      background: radial-gradient(circle at center, #00f7ff, #004f7a);
      opacity: 0.2;
      z-index: 0;
      animation: morph 10s infinite ease-in-out;
      filter: blur(30px);
    }

    .morphing-shape.left { top: 20%; left: 5%; animation-delay: 0s; }
    .morphing-shape.right { bottom: 20%; right: 5%; animation-delay: 5s; }

    @keyframes morph {
      0% { border-radius: 50% 50% 40% 60% / 60% 50% 50% 40%; transform: scale(1) translate(0, 0); }
      25% { border-radius: 60% 40% 50% 50% / 50% 60% 40% 50%; transform: scale(1.1) translate(10px, -10px); }
      50% { border-radius: 50% 60% 50% 40% / 60% 50% 40% 50%; transform: scale(1) translate(0, 10px); }
      75% { border-radius: 40% 50% 60% 50% / 50% 40% 60% 50%; transform: scale(0.9) translate(-10px, -5px); }
      100% { border-radius: 50% 50% 40% 60% / 60% 50% 50% 40%; transform: scale(1) translate(0, 0); }
    }

    .welcome-text {
      position: absolute;
      top: 45%;
      left: 50%;
      transform: translate(-50%, -50%);
      font-size: 1.2rem;
      text-shadow: 0 0 10px #00f7ff;
      animation: fadeIn 2s ease-in-out;
    }

    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

    .container {
      display: none;
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      background: rgba(0,0,0,0.8);
      padding: 20px;
      border-radius: 20px;
      box-shadow: 0 0 30px #00f7ff;
      max-width: 500px;
      width: 90%;
      text-align: center;
    }

    h1 {
      margin-bottom: 15px;
      font-size: 1.2rem;
      text-shadow: 0 0 10px #00f7ff;
    }

    textarea {
      display: block;
      box-sizing: border-box;
      width: 100%;
      padding: 10px;
      font-size: 0.75rem;
      background: #111;
      color: #00f7ff;
      border: 2px solid #00f7ff;
      border-radius: 8px;
      margin-bottom: 15px;
      resize: vertical;
    }

    button {
      background: #00f7ff;
      color: black;
      border: none;
      padding: 10px 20px;
      font-size: 0.9rem;
      border-radius: 10px;
      cursor: pointer;
      transition: 0.3s;
    }

    button:hover {
      background: #ff00ff;
      color: white;
      box-shadow: 0 0 15px #ff00ff;
    }

    .result-box {
      margin-top: 20px;
      padding: 12px;
      line-height: 1.4;
      background: rgba(255,255,255,0.1);
      border-radius: 15px;
      border: 1px solid #00f7ff;
      text-align: left;
      white-space: pre-wrap;
      max-height: 250px;
      overflow-y: auto;
      overflow-x: hidden;
    }

    .loading-overlay {
      display: none;
      position: absolute;
      top: 0; left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.9);
      z-index: 10;
      align-items: center;
      justify-content: center;
      flex-direction: column;
      color: #00f7ff;
      font-size: 1rem;
      text-align: center;
    }

    .infinity-loader {
      width: 80px;
      height: 80px;
      border: 8px solid #00f7ff;
      border-top: 8px solid transparent;
      border-radius: 50%;
      animation: rotate 2s linear infinite;
    }

    @keyframes rotate { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

    .footer {
      position: absolute;
      bottom: 10px;
      font-size: 0.9rem;
      color: #00f7ff;
      text-align: center;
    }

    .footer a {
      text-decoration: none;
      color: #00f7ff;
      font-weight: 700;
    }
  </style>
</head>
<body>
  <div class="snake" id="snake"></div>
  <div class="formula-bg"></div>
  <div class="morphing-shape left"></div>
  <div class="morphing-shape right"></div>
  <div class="welcome-text" id="welcome">FACT CHECKER AI AGENT</div>

  <div class="container" id="main-container">
    <h1>FACT CHECKER AI AGENT</h1>
    <form id="factForm">
      <textarea name="claim" rows="4" placeholder="Enter a fact or claim to verify..." required></textarea>
      <button type="submit">Check Fact</button>
    </form>
    {% if result %}
    <div class="result-box" id="result-box">
      <strong>Claim:</strong> {{ claim }}

      <br><br><strong>Result:</strong> {{ result }}
    </div>
    {% endif %}
  </div>

  <div class="loading-overlay" id="loading">
    <div class="infinity-loader"></div>
    <p>Verifying your claim...</p>
  </div>

  <script>
    window.onload = () => {
      setTimeout(() => {
        document.getElementById('welcome').style.display = 'none';
        document.getElementById('snake').style.display = 'none';
        document.getElementById('main-container').style.display = 'block';
      }, 2000);
    };

    document.getElementById('factForm').addEventListener('submit', function(event) {
      event.preventDefault();
      const claim = document.querySelector('textarea[name="claim"]').value;

      document.getElementById("main-container").style.display = "none";
      const loader = document.getElementById("loading");
      loader.style.display = "flex";

      fetch("/", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: "claim=" + encodeURIComponent(claim)
      })
      .then(response => response.text())
      .then(html => {
        document.open();
        document.write(html);
        document.close();
      });
    });

    document.querySelector('textarea[name="claim"]').addEventListener('keydown', function(event) {
      if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        document.querySelector('button[type="submit"]').click();
      }
    });
  </script>
</body>
</html>

"""

# ---- Flask App ----
app = Flask(__name__)

def query_sources(claim):
    sources = {'news': [], 'wikidata': [], 'gdelt': []}
    try:
        news_response = requests.get(
            "https://newsapi.org/v2/everything",
            params={"q": claim, "apiKey": NEWSAPI_KEY, "language": "en", "pageSize": 5},
            timeout=10
        ).json()
        if news_response.get("status") == "ok":
            sources['news'] = [f"{a['title']} ({a['source']['name']})" for a in news_response.get("articles", [])]
    except: pass
    return sources

def fact_check(claim):
    if len(claim.strip()) < 5 or len(claim.split()) < 2:
        return {
            'accuracy': 0,
            'verdict': 'INVALID',
            'explanation': 'Please provide a complete factual statement.'
        }

    sources = query_sources(claim)
    prompt = f"""You are a senior fact-checker. Analyze the following claim:

    "{claim}"

    Sources:
    - News: {sources['news'] or 'None'}

    Respond in this format:
    Accuracy: [0-100]%
    Verdict: [CORRECT, WRONG, UNVERIFIABLE]
    Explanation: Detailed reasoning with evidence if any."""

    try:
        response = model.generate_content(prompt)
        raw_text = response.text.strip()
        accuracy = re.search(r'Accuracy:\s*(\d+)%', raw_text)
        verdict = re.search(r'Verdict:\s*(CORRECT|WRONG|UNVERIFIABLE)', raw_text)
        explanation = re.search(r'Explanation:\s*(.+)', raw_text, re.DOTALL)

        verdict_text = verdict.group(1) if verdict else "UNVERIFIABLE"
        verdict_map = {
            "CORRECT": "CORRECT ✅",
            "WRONG": "WRONG ❌",
            "UNVERIFIABLE": "NOT VERIFIABLE ❓ Not shown in public/media."
        }

        return {
            'accuracy': int(accuracy.group(1)) if accuracy else 50,
            'verdict': verdict_map.get(verdict_text, "NOT VERIFIABLE ❓"),
            'explanation': explanation.group(1).strip() if explanation else "No explanation."
        }

    except Exception as e:
        return {
            'accuracy': 0,
            'verdict': 'ERROR ❌',
            'explanation': f'Error verifying: {str(e)}'
        }

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    claim = ""
    accuracy = 0
    if request.method == "POST":
        claim = request.form.get("claim", "").strip()
        if claim:
            check = fact_check(claim)
            result = f"{check['verdict']}\n\nAccuracy: {check['accuracy']}%\n\nExplanation:\n{check['explanation']}"
    return render_template_string(HTML, result=result, claim=claim)

if __name__ == "__main__":
    app.run(debug=True)
