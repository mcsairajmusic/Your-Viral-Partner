import streamlit as st
import time
import os
from google import genai

# --------------------
# Page Config
# --------------------
st.set_page_config(page_title="Viral Partner AI", page_icon="🚀")

st.title("🚀 Viral Partner AI")
st.write("Upload your reel and let AI analyze its viral potential.")

# --------------------
# API Key
# --------------------
api_key = st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("Add GOOGLE_API_KEY in Streamlit Secrets.")
    st.stop()

client = genai.Client(api_key=api_key)

# --------------------
# Upload Video
# --------------------
uploaded_file = st.file_uploader("Upload Reel (MP4)", type=["mp4", "mov", "avi"])

if uploaded_file:
    st.video(uploaded_file)

    if st.button("✨ Audit My Reel"):
        try:
            with st.spinner("Analyzing video..."):

                # Save temporary file
                temp_path = "temp_video.mp4"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.read())

                # Upload file
                video_file = client.files.upload(file=temp_path)

                # Wait until ready
                while video_file.state == "PROCESSING":
                    time.sleep(2)
                    video_file = client.files.get(name=video_file.name)

                prompt = """
                Analyze this Instagram reel.

                Give:
                1. Viral score (out of 100)
                2. Hook feedback
                3. Retention feedback
                4. 3 viral captions
                5. 5 hashtags
                """

                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=[video_file, prompt],
                )

                os.remove(temp_path)

            st.success("Audit Complete ✅")
            st.write(response.text)

        except Exception as e:
            st.error(f"Error: {str(e)}")
