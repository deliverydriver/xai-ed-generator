import os
import base64
from openai import OpenAI

class ImageGenerator:
    def __init__(self):
        self.xai_api_key = os.environ.get(
            "XAI_API_KEY",
            "***"
        )
        self.client = OpenAI(
            api_key=self.xai_api_key,
            base_url="https://api.x.ai/v1"
        )
        # Save images in output/images
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.output_dir = os.path.join(project_root, "output", "images")
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_image(self, paragraph_text, topic):
        """Generate an image based on a paragraph of educational content."""
        try:
            # Get a brief scene description from the paragraph
            scene_response = self.client.chat.completions.create(
                model="grok-3-mini",
                messages=[
                    {"role": "system", "content": "Create a vivid visual description based on the following educational content. Make it suitable for image generation."},
                    {"role": "user", "content": paragraph_text}
                ],
                max_tokens=100
            )
            scene_description = scene_response.choices[0].message.content.strip()
            print(f"Generating image for scene: {scene_description[:50]}...")

            # Generate the image using the correct endpoint
            response = self.client.images.generate(
                model="grok-3-mini-image",
                prompt=f"Educational illustration: {scene_description}",
                n=1,
                response_format="b64_json"
            )

            image_b64 = response.data[0].b64_json
            image_filename = f"{topic.replace(' ', '_')}_{os.urandom(4).hex()}.jpg"
            image_path = os.path.join(self.output_dir, image_filename)
            with open(image_path, "wb") as img_file:
                img_file.write(base64.b64decode(image_b64))
            return image_path

        except Exception as e:
            print(f"Error generating image: {e}")
            return None