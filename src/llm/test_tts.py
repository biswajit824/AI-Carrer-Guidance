from src.llm.tts import generate_speech


text = """
Welcome to your personalized career guidance.

You have a strong foundation in Python and Machine Learning.

You should focus on improving your SQL,
statistics and deployment skills.
"""


audio = generate_speech(
    text,
    "Hindi"
)


with open("test_output.wav", "wb") as f:
    f.write(audio)


print("Audio generated successfully!")
print(f"Audio size: {len(audio)} bytes")