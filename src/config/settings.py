# filepath: /xai-educational-generator/xai-educational-generator/src/config/settings.py

XAI_API_KEY = "your_xai_api_key_here"
ELEVENLABS_API_KEY = "your_elevenlabs_api_key_here"
OUTPUT_DIR = "output"
CONTENT_OUTPUT_DIR = f"{OUTPUT_DIR}/content"
IMAGE_OUTPUT_DIR = f"{OUTPUT_DIR}/images"
AUDIO_OUTPUT_DIR = f"{OUTPUT_DIR}/audio"
DEFAULT_CONTENT_LENGTH = 5  # Default number of paragraphs for the educational content
IMAGE_MODEL = "grok-2-image"  # Model to be used for image generation
AUDIO_VOICE_ID = "your_voice_id_here"  # Voice ID for ElevenLabs text-to-speech
AUDIO_MODEL_ID = "eleven_multilingual_v2"  # Model ID for ElevenLabs audio generation
AUDIO_OUTPUT_FORMAT = "mp3_44100_128"  # Desired audio output format