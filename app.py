import streamlit as st
import google.generativeai as genai
import os
import time

# 1. Page Configuration
st.set_page_config(page_title="Your Viral Partner", page_icon="🚀", layout="centered")
st.title("🚀 Your Viral Partner: Global Audit")
st.markdown("### Stop Guessing. Start Trending.")

# 2. API Configuration (2026 Stable)
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("Please add your GOOGLE_API_KEY to the app secrets/env variables.")
    st.stop()

genai.configure(api_key=api_key)

# 3. File Uploader
uploaded_file = st.file_uploader("Upload your MP4 Reel (Max 60s)", type=['mp4', 'mov'])

if uploaded_file is not None:
    # Save file locally to bypass buffer errors
    with open("temp_video.mp4", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.video("temp_video.mp4")

    if st.button("Analyze Viral Potential"):
        try:
            with st.status("AI is watching your video...", expanded=True) as status:
                # STEP 1: Upload to Gemini File API
                st.write("Uploading to Google Cloud...")
                video_file = genai.upload_file(path="temp_video.mp4")
                
                # STEP 2: The 'Anti-Error' Loop (Critical for 2026)
                # This prevents the 404/Processing error you saw before
                while video_file.state.name == "PROCESSING":
                    time.sleep(2)
                    video_file = genai.get_file(video_file.name)
                
                if video_file.state.name == "FAILED":
                    st.error("Video processing failed at Google's end.")
                    st.stop()

                st.write("Analyzing hooks and global trends...")
                
                # STEP 3: Generate Content using Gemini 2.0 Flash
                model = genai.GenerativeModel(model_name="gemini-1.5-flash")
                
                prompt = """
                Perform a global viral audit on this video. 
                Return the following sections:
                1. VIRAL SCORE: A percentage (0-100%) based on 2026 retention algorithms.
                2. HOOK AUDIT: Analyze the first 2.8 seconds. What works? What doesn't?
                3. GLOBAL CAPTIONS: Provide 3 captions (1 English, 1 Hinglish, 1 Short-Mystery).
                4. HASHTAG STRATEGY: 5 tags for Global reach and 5 for Local reach.
                5. EDITING FIX: One specific change to increase watch time.
                """
                
                response = model.generate_content([prompt, video_file])
                
                status.update(label="Analysis Complete!", state="complete", expanded=False)

            # Display Results
            st.success("✅ Your Viral Audit is Ready!")
            st.markdown(response.text)
            
            # Cleanup Google Cloud Storage
            genai.delete_file(video_file.name)

        except Exception as e:
            st.error(f"Business Logic Error: {e}")
            st.info("Tip: If you see a 404, check if your API Key has 'Gemini 2.0 Flash' enabled in Google AI Studio.")

# 4. Footer
st.divider()
st.caption("Powered by Your Viral Partner © 2026")
