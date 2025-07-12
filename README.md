# xAI Educational Generator

## Overview
The xAI Educational Generator is a Python application designed to create educational content on any topic. It leverages the xAI API for text generation, ElevenLabs for lifelike speech synthesis, and can generate images and videos to provide a comprehensive, multi-format learning experience. The application includes both a command-line and graphical user interface (GUI).

## xai-educational-gen 
├── src
│   
├── main.py                        # Entry point for CLI and backend logic
│   
├── gui.py                         # Tkinter-based graphical user interface
│   
├── educational_content_generator.py # EducationalContentGenerator class
│  
├── image_generator.py              # ImageGenerator class for visuals
│   
├── audio_generator.py              # AudioGenerator class using ElevenLabs API
│   
├── runway.py                      # Video generation integration
│   
├── admin_log_viewer.py             # Admin log viewer utility
│   
├── voices.json                     # Voice definitions for audio generation
│   
└── output 
│       
├── content                     # Generated educational content text files
│       
├── images                     # Generated images
│       
└── audio                       # Generated audio files
├── requirements.txt                    # Project dependencies 
├── .env.example                        # Template for environment variables (API keys, etc.) 
└── README.md

# Project documentation for the project
## Installation
1. Clone the repository:git clone https://github.com/deliverydriver/xai-ed-generator.git2. Navigate to the project directory:cd xai-educational-generator3. Install the required dependencies:pip install -r requirements.txt
## Usage
1. Set up your environment variables in a `.env` file based on the `.env.example` template.
2. Run the application:python src/main.py3. Follow the prompts to enter a topic for which you want to generate educational content.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.