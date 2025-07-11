# xAI Educational Generator

## Overview
The xAI Educational Generator is a Python application designed to create educational content on any topic. It utilizes the xAI API to generate informative text, complemented by images and audio files. The application aims to provide a comprehensive learning experience by making educational material accessible in multiple formats.

## Project Structure
```
xai-educational-generator
├── src
│   ├── main.py                # Entry point of the application
│   ├── educational_content_generator.py  # Contains the EducationalContentGenerator class
│   ├── image_generator.py      # Contains the ImageGenerator class for generating visuals
│   ├── audio_generator.py      # Contains the AudioGenerator class for converting text to speech
│   ├── utils
│   │   ├── __init__.py        # Initializes the utils module
│   │   ├── text_processor.py   # Utility functions for processing text
│   │   └── file_handler.py     # Utility functions for file operations
│   └── config
│       ├── __init__.py        # Initializes the config module
│       └── settings.py         # Configuration settings including API keys and output paths
├── output
│   ├── content                 # Directory for generated educational content text files
│   ├── images                  # Directory for generated images related to the content
│   └── audio                   # Directory for generated audio files that read the content
├── requirements.txt            # Lists project dependencies
├── .env.example                # Template for environment variables
└── README.md                   # Documentation for the project
```

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/xai-educational-generator.git
   ```
2. Navigate to the project directory:
   ```
   cd xai-educational-generator
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
1. Set up your environment variables in a `.env` file based on the `.env.example` template.
2. Run the application:
   ```
   python src/main.py
   ```
3. Follow the prompts to enter a topic for which you want to generate educational content.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.