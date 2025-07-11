import os

class AudioGenerator:
    def __init__(self, elevenlabs_client):
        self.client = elevenlabs_client
        # Save audio in output/audio
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.output_dir = os.path.join(project_root, "output", "content")
        os.makedirs(self.output_dir, exist_ok=True)

    def text_to_speech(self, text, topic, voice_id):
        """Convert text to speech using ElevenLabs API and save as MP3"""
        try:
            audio_generator = self.client.text_to_speech.convert(
                text=text,
                voice_id=voice_id,
                model_id="eleven_multilingual_v2",
                output_format="mp3_44100_128",
            )
            audio_content = b''.join(chunk for chunk in audio_generator)
            audio_file_path = os.path.join(self.output_dir, f"{topic.replace(' ', '_')}_audio.mp3")
            with open(audio_file_path, "wb") as f:
                f.write(audio_content)
            return audio_file_path
        except Exception as e:
            print(f"Error creating audio file with ElevenLabs: {e}")
            return False