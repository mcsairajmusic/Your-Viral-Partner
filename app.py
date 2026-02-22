import streamlit as st
import google.generativeai as genai
import time

# 1. Page Configuration (The tab title and icon)
st.set_page_config(page_title="Viral Partner AI", page_icon="🚀", layout="centered")

# 2. Custom CSS for a "Premium" Look
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: white;
    }
    
    /* Glassmorphism Card for Results */
    .result-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-top: 20px;
    }
    
    /* Custom Button */
    .stButton>button {
        background: linear-gradient(45deg, #ff00cc, #3333ff);
        color: white;
        border: none;
        padding: 10px 24px;
        border-radius: 25px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0px 0px 15px #ff00cc;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Header Section
st.title("🚀 Viral Partner AI")
st.subheader("Turn your reels into viral sensations.")
st.write("Upload your video and let the AI audit your hook, lighting, and pacing.")

# 4. API Key Setup
api_key = st.secrets.get("GOOGLE_API_KEY")
if not api_key:
    st.error("Please add your GOOGLE_API_KEY in Streamlit Secrets.")
else:
    genai.configure(api_key=api_key)
    # Using the most stable 2026 model name
    model = genai.GenerativeModel(model_name="gemini-1.5-flash-001")
   # 5. File Uploader
    uploaded_file = st.file_uploader("📂 Upload your Reel (MP4)", type=["mp4", "mov", "avi"])

    if uploaded_file is not None:
        st.video(uploaded_file)
        
        if st.button("✨ Audit My Reel"):
            with st.status("🤖 AI is watching your video...", expanded=True) as status:
                # Save temp file
                with open("temp_video.mp4", "wb") as f:
                    f.write(uploaded_file.read())
                
                # Upload to Google
                video_file = genai.upload_file(path="temp_video.mp4")
                
                # Wait for processing
                while video_file.state.name == "PROCESSING":
                    time.sleep(2)
                    video_file = genai.get_file(video_file.name)
                
                # Prompt
                prompt = "Analyze this video for viral potential. Give a score out of 100, analyze the first 3-second hook, and suggest 3 viral captions."
                response = model.generate_content([video_file, prompt])
                status.update(label="✅ Audit Complete!", state="complete")

            # 6. Display Results in a Beautiful Card
            st.markdown(f"""
                <div class="result-card">
                    <h2>📊 Viral Audit Report</h2>
                    <p>{response.text}</p>
                </div>
            """, unsafe_allow_html=True)

# 7. Footer
st.markdown("---")
st.caption("Powered by Gemini 1.5 Flash • Created by mcsairajmusic")
