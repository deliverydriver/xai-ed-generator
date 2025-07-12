import os
import json
import datetime
import logging
from elevenlabs.client import ElevenLabs
from educational_content_generator import EducationalContentGenerator
from image_generator import ImageGenerator
from audio_generator import AudioGenerator

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")
LOG_FILE = os.path.join(OUTPUT_DIR, "request_log.jsonl")

# Setup logging
LOGGING_PATH = os.path.join(OUTPUT_DIR, "main.log")
os.makedirs(OUTPUT_DIR, exist_ok=True)
logging.basicConfig(
    filename=LOGGING_PATH,
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s"
)

def init_output_dirs():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIR, "content"), exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIR, "images"), exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIR, "audio"), exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIR, "video"), exist_ok=True)

init_output_dirs()

def log_request(action, params, result_path=None):
    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "action": action,
        "params": params,
        "result_path": result_path
    }
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")

def build_prompt(topic, style, custom_style, age_group):
    logging.info(f"Building prompt with topic={topic}, style={style}, custom_style={custom_style}, age_group={age_group}")
    style_part = style
    if style == "Agentic" and custom_style:
        style_part += f" ({custom_style})"
    prompt = (
        f"Generate {style_part} educational content for the topic '{topic}' "
        f"targeted at {age_group}."
    )
    logging.debug(f"Prompt built: {prompt}")
    return prompt

def generate_content(topic, style, custom_style, age_group):
    logging.info("Starting generate_content")
    try:
        prompt = build_prompt(topic, style, custom_style, age_group)
        content_generator = EducationalContentGenerator(prompt)
        educational_content = content_generator.generate_content()
        os.makedirs(os.path.join(OUTPUT_DIR, "content"), exist_ok=True)
        content_file_path = os.path.join(OUTPUT_DIR, "content", f"{topic.replace(' ', '_')}_content.txt")
        with open(content_file_path, "w", encoding="utf-8") as content_file:
            content_file.write(educational_content)
        log_request(
            "generate_content",
            {"topic": topic, "style": style, "custom_style": custom_style, "age_group": age_group, "prompt": prompt},
            content_file_path
        )
        logging.info(f"Content generated and saved to {content_file_path}")
        return educational_content, content_file_path
    except Exception as e:
        logging.error(f"Error in generate_content: {e}", exc_info=True)
        raise

def generate_image(educational_content, topic, style, custom_style, age_group):
    logging.info("Starting generate_image")
    try:
        os.makedirs(os.path.join(OUTPUT_DIR, "images"), exist_ok=True)
        image_generator = ImageGenerator()
        image_path = image_generator.generate_image(educational_content, topic)
        log_request(
            "generate_image",
            {"topic": topic, "style": style, "custom_style": custom_style, "age_group": age_group, "educational_content": educational_content[:100] + "..."},
            image_path
        )
        logging.info(f"Image generated and saved to {image_path}")
        return image_path
    except Exception as e:
        logging.error(f"Error in generate_image: {e}", exc_info=True)
        raise

def generate_audio(content, topic, style, custom_style, age_group, voice_id):
    logging.info("Starting generate_audio")
    try:
        audio_generator = AudioGenerator()
        audio_path = audio_generator.generate(content, topic, style, custom_style, age_group, voice_id)
        log_request(
            "generate_audio",
            {"topic": topic, "style": style, "custom_style": custom_style, "age_group": age_group, "voice_id": voice_id},
            audio_path
        )
        logging.info(f"Audio generated and saved to {audio_path}")
        return audio_path
    except Exception as e:
        logging.error(f"Error in generate_audio: {e}", exc_info=True)
        raise

def generate_video(educational_content, topic, style, custom_style, age_group, voice_id=None, callback=None):
    logging.info("Starting generate_video")
    try:
        from runway import generate_video as runway_generate_video
        os.makedirs(os.path.join(OUTPUT_DIR, "video"), exist_ok=True)
        video_path = os.path.join(OUTPUT_DIR, "video", f"{topic.replace(' ', '_')}_video.mp4")
        prompt = f"Educational video: {educational_content[:200]}"
        runway_generate_video(prompt, video_path, topic, callback=callback)
        log_request(
            "generate_video",
            {
                "topic": topic,
                "style": style,
                "custom_style": custom_style,
                "age_group": age_group,
                "prompt": prompt,
                "voice_id": voice_id
            },
            video_path
        )
        logging.info(f"Video generated and saved to {video_path}")
        return video_path
    except Exception as e:
        logging.error(f"Error in generate_video: {e}", exc_info=True)
        raise

def main():
    logging.info("Starting main function")
    try:
        init_output_dirs()
        topic = input("Enter the educational topic: ")
        style = input("Enter the style (e.g., 'Agentic'): ")
        custom_style = input("Enter custom style (optional): ")
        age_group = input("Enter the target age group: ")

        educational_content, content_file_path = generate_content(topic, style, custom_style, age_group)
        print(f"Educational content saved to: {content_file_path}")

        image_path = generate_image(educational_content, topic, style, custom_style, age_group)
        print(f"Image generated and saved to: {image_path}")

        audio_path = generate_audio(educational_content, topic, style, custom_style, age_group, voice_id="FFj9mArDv2wVzs5iXpea")
        print(f"Audio generated and saved to: {audio_path}")

        video_path = generate_video(educational_content, topic, style, custom_style, age_group)
        print(f"Video generated and saved to: {video_path}")
    except Exception as e:
        logging.critical(f"Unhandled exception in main: {e}", exc_info=True)
        print("An error occurred. Check main.log for details.")

if __name__ == "__main__":
    main()