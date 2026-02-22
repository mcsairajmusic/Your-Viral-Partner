import streamlit as st
import google.generativeai as genai
import time
import os

# -----------------------------
# 1️⃣ Page Config
# -----------------------------
st.set_page_config(
    page_title="Viral Partner AI",
    page_icon="🚀",
    layout="centered"
)

# -----------------------------
# 2️⃣ Premium CSS (Improved Visibility)
# -----------------------------
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(135deg, #141E30, #243B55);
    color: #ffffff;
}

/* Make ALL text bright white */
html, body, [class*="css"] {
    color: #ffffff !important;
}

/* Header Styling */
h1, h2, h3 {
    color: #ffffff !important;
    font-weight: 700;
}

/* Glass Card */
.result-card {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(15px);
    border-radius: 18px;
    padding: 30px;
    border: 1px solid rgba(255, 255, 255, 0.15);
    margin-top: 25px;
    box-shadow: 0 0 25px rgba(0,0,0,0.4);
}

/* Upload Box */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.05);
    padding: 15px;
    border-radius: 15px;
}

/* Button */
.stButton>button {
    background: linear-gradient(45deg, #ff00cc, #3333ff);
    color: white;
    border: none;
    padding: 12px 28px;
    border-radius: 30px;
    font-weight: bold;
    font-size: 16px;
    transition: 0.3s ease;
}

.stButton>button:hover {
    transform: scale(1.07);
    box-shadow: 0px 0px 20px #ff00cc;
}

/* Footer */
footer {visibility: hidden;}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# 3️⃣ Header
# -----------------------------
st.title("🚀 Viral Partner AI")
st.subheader("Turn your reels into viral sensations")
st.write("Upload your reel and let AI analyze your hook, pacing & viral potential.")

# -----------------------------
# 4️⃣ API Setup
# -----------------------------
api_key = st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("⚠ Please add your GOOGLE_API_KEY in Streamlit Secrets.")
    st.stop()

genai.configure(api_key=api_key)

# Stable model
model = genai.GenerativeModel("gemini-1.5-flash")

# -----------------------------
# 5️⃣ File Upload
# -----------------------------
uploaded_file = st.file_uploader("📂 Upload your Reel (MP4, MOV, AVI)", type=["mp4", "mov", "avi"])

if uploaded_file:

    st.video(uploaded_file)

    if st.button("✨ Audit My Reel"):

        with st.spinner("🤖 AI is analyzing your video..."):

            try:
                # Save temporary file
                temp_path = "temp_video.mp4"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.read())

                # Upload to Gemini
                video_file = genai.upload_file(path=temp_path)

                # Wait until processed
                while video_file.state.name == "PROCESSING":
                    time.sleep(2)
                    video_file = genai.get_file(video_file.name)

                if video_file.state.name == "FAILED":
                    st.error("❌ Video processing failed. Try another file.")
                    st.stop()

                prompt = """
                Analyze this Instagram reel for viral potential.

                Give:
                1. Overall Viral Score (out of 100)
                2. First 3-second Hook Analysis
                3. Pacing & Retention Feedback
                4. 3 High-Converting Viral Captions
                5. 5 Hashtag Suggestions
                """

                response = model.generate_content([video_file, prompt])

                # Delete temp file
                os.remove(temp_path)

                st.markdown(f"""
                <div class="result-card">
                    <h2>📊 Viral Audit Report</h2>
                    <p style="font-size:16px; line-height:1.6;">
                    {response.text}
                    </p>
                </div>
                """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"⚠ Error: {str(e)}")

# -----------------------------
# 6️⃣ Footer
# -----------------------------
st.markdown("---")
st.caption("Powered by Gemini 1.5 Flash • Created by MC Sairaj 🚀")
