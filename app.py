import streamlit as st
import google.generativeai as genai
import time
import os

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(
    page_title="Viral Partner AI",
    page_icon="🚀",
    layout="centered"
)

# ----------------------------
# Clean Visible UI
# ----------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #141E30, #243B55);
    color: white;
}

h1, h2, h3, p, label {
    color: white !important;
}

.result-card {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(12px);
    padding: 25px;
    border-radius: 15px;
    border: 1px solid rgba(255,255,255,0.15);
    margin-top: 20px;
}

.stButton>button {
    background: linear-gradient(45deg, #ff00cc, #3333ff);
    color: white;
    border: none;
    padding: 12px 25px;
    border-radius: 25px;
    font-weight: bold;
    font-size: 16px;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 15px #ff00cc;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Header
# ----------------------------
st.title("🚀 Viral Partner AI")
st.subheader("Turn your reels into viral content")
st.write("Upload your reel and let AI analyze its viral potential.")

# ----------------------------
# API Setup
# ----------------------------
api_key = st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("GOOGLE_API_KEY not found in Streamlit Secrets.")
    st.stop()

genai.configure(api_key=api_key)

# 🔥 Stable Working Model
model = genai.GenerativeModel("models/gemini-1.5-flash-001")

# ----------------------------
# File Upload
# ----------------------------
uploaded_file = st.file_uploader(
    "Upload your Reel (MP4, MOV, AVI)",
    type=["mp4", "mov", "avi"]
)

if uploaded_file:

    st.video(uploaded_file)

    if st.button("✨ Audit My Reel"):

        try:
            with st.spinner("AI is analyzing your video..."):

                # Save temporary file
                temp_path = "temp_video.mp4"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.read())

                # Upload to Gemini
                video = genai.upload_file(path=temp_path)

                # Wait for processing
                while video.state.name == "PROCESSING":
                    time.sleep(2)
                    video = genai.get_file(video.name)

                if video.state.name == "FAILED":
                    st.error("Video processing failed.")
                    st.stop()

                prompt = """
                Analyze this Instagram reel.

                Give:
                1. Viral score out of 100
                2. Hook analysis (first 3 seconds)
                3. Retention feedback
                4. 3 viral caption ideas
                5. 5 hashtag suggestions
                """

                response = model.generate_content([video, prompt])

                os.remove(temp_path)

            st.markdown(f"""
            <div class="result-card">
                <h2>📊 Viral Audit Report</h2>
                <p style="line-height:1.6;">{response.text}</p>
            </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error: {str(e)}")

# ----------------------------
# Footer
# ----------------------------
st.markdown("---")
st.caption("Powered by Gemini 1.5 Flash 001 • Created by MC Sairaj 🚀")
