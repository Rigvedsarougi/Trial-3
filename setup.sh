#!/bin/bash

# Install Python dependencies
pip install git+https://github.com/openai/whisper.git -q
pip install ur_audio_sub

# Install system dependencies
sudo apt update && sudo apt install ffmpeg
