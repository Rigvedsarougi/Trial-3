import streamlit as st
from ur_audio_sub import subGen_path, read_txt

def generate_subtitle(mp3_file_path):
    # Set up the subtitle file path
    subtitle_file_path = mp3_file_path.replace('.mp3', '.txt')

    # Generate subtitle
    subGen_path(mp3_file_path)

    # Read subtitle content
    subtitle_content = read_txt(subtitle_file_path)

    return subtitle_content

def main():
    st.title("Audio Subtitle Generator")

    # File upload
    mp3_file = st.file_uploader("Upload an MP3 file")

    if mp3_file is not None:
        # Save the uploaded file to a temporary location
        with open("temp.mp3", "wb") as f:
            f.write(mp3_file.getvalue())

        # Generate subtitle
        subtitle_content = generate_subtitle("temp.mp3")

        # Display subtitle content
        st.header("Generated Subtitle:")
        st.text(subtitle_content)

if __name__ == "__main__":
    main()
