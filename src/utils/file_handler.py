def save_content_to_file(content_text, topic, output_dir):
    content_filename = f"{output_dir}/content/{topic.replace(' ', '_')}.txt"
    with open(content_filename, "w", encoding='utf-8') as content_file:
        content_file.write(content_text)
    return content_filename

def save_image(image_data, image_name, output_dir):
    image_filename = f"{output_dir}/images/{image_name}.jpg"
    with open(image_filename, "wb") as img_file:
        img_file.write(image_data)
    return image_filename

def save_audio(audio_data, audio_name, output_dir):
    audio_filename = f"{output_dir}/audio/{audio_name}.mp3"
    with open(audio_filename, "wb") as audio_file:
        audio_file.write(audio_data)
    return audio_filename

def ensure_output_directories(output_dir):
    os.makedirs(f"{output_dir}/content", exist_ok=True)
    os.makedirs(f"{output_dir}/images", exist_ok=True)
    os.makedirs(f"{output_dir}/audio", exist_ok=True)