<img src="https://raw.githubusercontent.com/deliverydriver/xai-ed-generator/refs/heads/master/Screenshot%20from%202025-11-04%2013-27-46.png" alt="Screenshot" width="300" height="300">
# xAI Educational Generator

for questions or help direct messages to allow.multi.0f@icloud.com

for business development use azures.accents.0z@icloud.com

reach me on IG, FB, TG @goodfamilia

<img src="https://raw.githubusercontent.com/deliverydriver/xai-ed-generator/refs/heads/master/output/images/Disney's_Rivers_of_America_8e5dff22.jpg" alt="Disney's Rivers of America" width="300" height="300">

## Overview
The xAI Educational Generator is a Python application designed to create educational content on any topic. It leverages the xAI API for text generation, ElevenLabs for lifelike speech synthesis, and can generate images and videos to provide a comprehensive, multi-format learning experience. The application includes both a command-line and graphical user interface (GUI). — also included is a monitoring application that when you open it, it is a list of all inputs and outputs that can be exported as a report

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
