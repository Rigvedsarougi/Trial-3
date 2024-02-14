import websockets
import asyncio
import base64
import json
import pyaudio
from streamlit_lottie import st_lottie
import requests
from streamlit_webrtc import WebRtcMode, webrtc_streamer

import streamlit as st

if 'run' not in st.session_state:
    st.session_state['run'] = False

Frames_per_buffer = 3200
Format = pyaudio.paInt16
Channels = 1
Rate = 16000
p = pyaudio.PyAudio()

# starts recording
stream = p.open(
    format=Format,
    channels=Channels,
    rate=Rate,
    input=True,
    frames_per_buffer=Frames_per_buffer
)

webrtc_ctx = webrtc_streamer(
        key="speech-to-text",
        mode=WebRtcMode.SENDONLY,
        audio_receiver_size=1024,
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
        media_stream_constraints={"video": False, "audio": True},
    )

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code!= 200:
        return None
    return r.json()

voice_animation = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_owkzfxim.json")

st.title('Create real_time transcription from your microphone')

start, stop = st.columns(2)    

def stop_listening():
    st.session_state['run'] = False
    

def start_listening():
    st.session_state['run'] = True
    st_lottie(voice_animation, height=200)


start.button('Start Listening', on_click= start_listening)


stop.button('Stop Listening', on_click= stop_listening)


endpoint_url = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"

async def send_receive():

    print(f'Connecting websocket to url ${endpoint_url}')

    async with websockets.connect(
        endpoint_url,
        extra_headers=(("Authorization", st.secrets.key),),
        ping_interval=5,
        ping_timeout=20
    ) as _ws:

        r = await asyncio.sleep(0.1)
        print("Receiving SessionBegins ...")

        session_begins = await _ws.recv()
        print(session_begins)
        print("Sending messages ...")

        async def send():
            while st.session_state['run']:
                try:
                    audio_frames = webrtc_ctx.audio_receiver.get_frames(timeout=1)
                    data = stream.read(Frames_per_buffer)
                    data = base64.b64encode(data).decode("utf-8")
                    json_data = json.dumps({"audio_data":str(data)})
                    r = await _ws.send(json_data)

                except websockets.exceptions.ConnectionClosedError as e:
                    print(e)
                    assert e.code == 4008
                    break

                except Exception as e:
                    assert False, "Not a websocket 4008 error"

                r = await asyncio.sleep(0.01)

            return True


        async def receive():
            while st.session_state['run']:
                try:
                    result_str = await _ws.recv()
                    if json.loads(result_str)['message_type'] == 'FinalTranscript':
                        print(json.loads(result_str)['text'])
                        st.markdown(json.loads(result_str)['text'])

                except websockets.exceptions.ConnectionClosedError as e:
                    print(e)
                    assert e.code == 4008
                    break

                except Exception as e:
                    assert False, "Not a websocket 4008 error"

        send_result, receive_result = await asyncio.gather(send(), receive())

asyncio.run(send_receive())     













