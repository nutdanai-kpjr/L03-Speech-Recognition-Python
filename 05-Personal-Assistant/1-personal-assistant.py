import pyaudio
import websockets
import asyncio
import base64
import json
from open_ai_services import askOpenAiBot
from secret_api_key import ASSEMBLY_AI_API_KEY

# Notes: This project requires a upgrade plan of AssemblyAI


# Record Microphone Input
FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

p = pyaudio.PyAudio()

# starts recording
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=FRAMES_PER_BUFFER,
)

print(" 🎙️ Recording on", p.get_default_input_device_info())

# Real Time Speech Recognition via AssemblyAI (Websocket)
URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"


async def realTimeVoiceChat():
    print(f"🔗 Connecting websocket to Assembly API ${URL}")
    async with websockets.connect(  # type: ignore
        URL,
        extra_headers=(("Authorization", ASSEMBLY_AI_API_KEY),),
        ping_interval=5,
        ping_timeout=20,
    ) as _ws:
        await asyncio.sleep(0.1)
        # print("Receiving Session Begins ...")
        session_begins = await _ws.recv()
        print(session_begins)
        print(" 🤖 Robot: Ask me anything ...")

        async def send():  # Send audio data to AssemblyAI
            while True:
                try:
                    data = stream.read(FRAMES_PER_BUFFER, exception_on_overflow=False)
                    data = base64.b64encode(data).decode("utf-8")
                    json_data = json.dumps({"audio_data": str(data)})
                    await _ws.send(json_data)
                except websockets.exceptions.ConnectionClosedError as e:  # type: ignore
                    print(e)
                    assert e.code == 4008
                    break
                except Exception as e:
                    assert False, "Not a websocket 4008 error"
                await asyncio.sleep(0.01)

            return True

        async def receive():  # Receive Transcript, then we will send it to OpenAI to give a proper response
            while True:
                try:
                    result_str = await _ws.recv()
                    result = json.loads(result_str)
                    prompt = result["text"]
                    if prompt and result["message_type"] == "FinalTranscript":
                        print(" 😉 Human:", prompt)
                        answer = askOpenAiBot(prompt)
                        print(" 🤖 Robot:", answer)
                except websockets.exceptions.ConnectionClosedError as e:  # type: ignore
                    print(e)
                    assert e.code == 4008
                    break
                except Exception as e:
                    assert False, "Not a websocket 4008 error"

        send_result, receive_result = await asyncio.gather(send(), receive())


asyncio.run(realTimeVoiceChat())
