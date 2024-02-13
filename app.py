import streamlit as st
from ur_audio_sub import generate_subtitle

def main():
    st.title("Audio Subtitle Generator")

    # File upload section
    st.subheader("Upload Audio File")
    uploaded_file = st.file_uploader("Choose an audio file", type=["mp3"])

    if uploaded_file is not None:
        st.audio(uploaded_file, format='audio/mp3', start_time=0)

        # Generate subtitle
        subtitle_content = generate_subtitle(uploaded_file)

        # Display subtitle content
        st.subheader("Generated Subtitle:")
        st.write(subtitle_content)

if __name__ == "__main__":
    main()
