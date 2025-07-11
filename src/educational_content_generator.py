import os
import requests

class EducationalContentGenerator:
    def __init__(self, topic):
        self.topic = topic
        self.xai_api_key = "xai-KMRpmonf6OOd6fRmvmcBTNI3DcxuNC1nmLEUDFNQzWkcYNFuXRs1mE0YhMtYREBfKPOhsEeB9JJK6SLi"  # Replace with actual API key
        self.base_url = "https://api.x.ai/v1/chat/completions"

    def generate_content(self):
        """Generate educational content based on the specified topic using xAI API."""
        try:
            response = requests.post(
                self.base_url,
                headers={
                    "Authorization": f"Bearer {self.xai_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "grok-2",
                    "messages": [
                        {"role": "system", "content": "You are an educational content generator. Write a clear, engaging, and accurate explanation for the following topic."},
                        {"role": "user", "content": self.topic}
                    ],
                    "max_tokens": 512
                }
            )
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"]
            return content
        except Exception as e:
            print(f"Error generating content for topic '{self.topic}': {e}")
            return "Content generation failed."

    def save_content_to_file(self, content, output_dir):
        """Save the generated content to a text file."""
        safe_title = self.safe_filename(self.topic)
        file_path = os.path.join(output_dir, f"{safe_title}.txt")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return file_path

    def safe_filename(self, title):
        """Create a safe filename from the topic."""
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        return safe_title[:50].replace(' ', '_')