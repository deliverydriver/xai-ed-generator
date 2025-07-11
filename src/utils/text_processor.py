def clean_text(text):
    """Remove unwanted characters and format the text for better readability."""
    # Replace multiple spaces with a single space
    cleaned_text = ' '.join(text.split())
    # Optionally, you can add more formatting rules here
    return cleaned_text

def format_educational_content(content):
    """Format the educational content for presentation."""
    # Example formatting: adding headings or bullet points
    formatted_content = f"**Educational Topic:** {content['topic']}\n\n"
    formatted_content += f"**Content:**\n{content['text']}\n"
    return formatted_content

def generate_audio_filename(topic):
    """Create a safe filename for the audio file based on the topic."""
    safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).rstrip()
    return f"{safe_topic[:50].replace(' ', '_')}.mp3"