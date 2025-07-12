import os
import requests
import time
import base64
import mimetypes

RUNWAY_API_KEY = "key_8238c8edd2b9e276bc0171e90d44a7223e9b93ffcf3ecf3cabbe635a7db7ea03b6395c4cfd88d05e3015b3c872bfece7591051a8ad3fc5b3bdd5386bf6627faf"
RUNWAY_API_URL = "https://api.dev.runwayml.com/v1/image_to_video"

def read_content(content_path):
    with open(content_path, "r", encoding="utf-8") as f:
        return f.read().strip()

def find_image_for_topic(images_dir, topic):
    topic_prefix = topic.replace(' ', '_').lower()
    for fname in os.listdir(images_dir):
        if fname.lower().startswith(topic_prefix) and fname.lower().endswith(('.png', '.jpg', '.jpeg')):
            return os.path.join(images_dir, fname)
    for fname in os.listdir(images_dir):
        if fname.lower().endswith(('.png', '.jpg', '.jpeg')):
            return os.path.join(images_dir, fname)
    return None

def generate_video(prompt, output_path, topic, callback=None):
    images_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output", "images")
    image_path = find_image_for_topic(images_dir, topic)
    if not image_path:
        raise FileNotFoundError("No image found in the images folder for video generation.")

    # Read and encode the image as base64 data URL
    with open(image_path, "rb") as img_file:
        mime_type, _ = mimetypes.guess_type(image_path)
        if not mime_type:
            mime_type = "image/jpeg"
        encoded_string = base64.b64encode(img_file.read()).decode("utf-8")
        data_url = f"data:{mime_type};base64,{encoded_string}"

    headers = {
        "Authorization": f"Bearer {RUNWAY_API_KEY}",
        "X-Runway-Version": "2024-11-06",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gen4_turbo",
        "prompt": prompt,
        "promptImage": data_url,
        "num_frames": 210,
        "fps": 30,
        "seed": 42,
        "motion": "cinematic",
        "ratio": '832:1104'
    }
    print(f"Sending base64 data URL image and prompt to Runway API...")
    response = requests.post(RUNWAY_API_URL, headers=headers, json=data)
    print("RESPONSE:", response.status_code, response.text)  # For debugging
    if response.status_code != 200:
        raise Exception(f"Runway API error: {response.status_code} {response.text}")
    result = response.json()
    video_id = result["id"]

    # Poll for video completion
    status_url = f"https://api.dev.runwayml.com/v1/tasks/{video_id}"
    downloaded = False
    max_retries = 5
    retries = 0
    while True:
        while retries < max_retries:
            try:
                status_resp = requests.get(status_url, headers=headers, timeout=10)
                status_resp.raise_for_status()
                break
            except requests.exceptions.ConnectionError as e:
                print("Connection error, retrying in 10 seconds...")
                time.sleep(10)
                retries += 1
        else:
            raise Exception("Failed to connect to Runway API after multiple attempts.")
        
        status_data = status_resp.json()
        print("STATUS POLL RESPONSE:", status_data)  # Debug print
        if callback is not None:
            callback(status_data)
        if status_data["status"].upper() == "SUCCEEDED":
            video_url = None
            if "output" in status_data and status_data["output"]:
                video_url = status_data["output"][0]
            elif "outputs" in status_data and status_data["outputs"]:
                video_url = status_data["outputs"][0]
            if not video_url:
                raise Exception("No video URL found in status response.")
            if not downloaded:
                print("Downloading video from:", video_url)
                video_resp = requests.get(video_url)
                print("Video download response:", video_resp.status_code)
                video_resp.raise_for_status()
                with open(output_path, "wb") as f:
                    f.write(video_resp.content)
                print(f"Video saved to: {output_path}")
                downloaded = True
            break  # <-- Ensure you break after download!
        elif status_data["status"].upper() == "FAILED":
            raise Exception("Video generation failed.")
        time.sleep(3)

if __name__ == "__main__":
    topic = "Being an Educational Assistant"
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    content_path = os.path.join(project_root, "output", "content", f"{topic.replace(' ', '_')}_content.txt")
    video_dir = os.path.join(project_root, "output", "video")
    os.makedirs(video_dir, exist_ok=True)
    video_path = os.path.join(video_dir, f"{topic.replace(' ', '_')}_video.mp4")

    with open(content_path, "r", encoding="utf-8") as f:
        content = f.read().strip()
    prompt = f"Educational video: {content[:200]}"
    generate_video(prompt, video_path, topic)