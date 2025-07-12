import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

load_dotenv()

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")

class AudioGenerator:
    def __init__(self):
        self.elevenlabs = ElevenLabs(
            api_key=os.getenv("ELEVENLABS_API_KEY"),
        )

    def generate(self, content, topic, style, custom_style, age_group, voice_id, model_id="eleven_multilingual_v2", output_format="mp3_44100_128"):
        audio = self.elevenlabs.text_to_speech.convert(
            text=content,
            voice_id=voice_id,
            model_id=model_id,
            output_format=output_format,
        )

        # Use the correct output directory
        output_dir = os.path.join(OUTPUT_DIR, "audio")
        os.makedirs(output_dir, exist_ok=True)
        filename = f"{topic.replace(' ', '_')}_audio.mp3"
        audio_path = os.path.join(output_dir, filename)
        with open(audio_path, "wb") as f:
            f.write(audio)
        return audio_path