from flask import Flask, request, render_template_string
import requests
import os

app = Flask(__name__)

# Groq API Key from environment variable
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Function to call Groq AI
def generate_groq_caption(topic, audience, emotion, platform):
    prompt = f"""
You are a social media assistant.
Generate:
1. A catchy caption
2. 5 relevant hashtags
3. Short feedback about this video topic

Video Topic: {topic}
Target Audience: {audience}
Emotion: {emotion}
Platform: {platform}
"""
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt,
        "max_tokens": 150
    }

    url = "https://api.groq.ai/v1/engines/groq-2.5-flash-lite/completions"

    try:
        response = requests.post(url, json=data, headers=headers, timeout=15)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["text"].strip()
    except Exception as e:
        return f"Error contacting Groq AI: {e}"

# HTML template
HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
<title>Your Viral Partner 🚀</title>
<style>
body { font-family: Arial; background:#1e1e2f; color:#fff; padding:20px; }
input, select { width:100%; padding:10px; margin:10px 0; border-radius:5px; border:none; }
button { padding:10px 20px; margin:10px 0; border-radius:5px; background:#ff007f; color:#fff; border:none; cursor:pointer; }
button:hover { background:#ff3399; }
.result { background: rgba(255,255,255,0.1); padding:15px; border-radius:10px; white-space: pre-wrap; }
</style>
</head>
<body>
<h1>Your Viral Partner 🚀 (Groq AI)</h1>

{% if not result %}
<form method="POST">
<label>Video Topic:</label>
<input name="topic" value="{{topic}}">
<label>Target Audience:</label>
<input name="audience" value="{{audience}}">
<label>Emotion:</label>
<input name="emotion" value="{{emotion}}">
<label>Platform:</label>
<select name="platform">
<option {% if platform=='Instagram' %}selected{% endif %}>Instagram</option>
<option {% if platform=='TikTok' %}selected{% endif %}>TikTok</option>
<option {% if platform=='YouTube Shorts' %}selected{% endif %}>YouTube Shorts</option>
</select>
<button type="submit">Generate 🚀</button>
</form>
{% else %}
<h2>📊 Generated Result:</h2>
<div class="result">{{ result }}</div>
<form method="GET">
<button type="submit">Start New Analysis</button>
</form>
{% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET","POST"])
def index():
    topic = request.form.get("topic","")
    audience = request.form.get("audience","")
    emotion = request.form.get("emotion","")
    platform = request.form.get("platform","Instagram")
    result = None

    if request.method=="POST":
        result = generate_groq_caption(topic, audience, emotion, platform)

    return render_template_string(
        HTML_TEMPLATE,
        topic=topic,
        audience=audience,
        emotion=emotion,
        platform=platform,
        result=result
    )

if __name__=="__main__":
    app.run(host="0.0.0.0", port=8080)
