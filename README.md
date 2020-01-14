# Rubik's Timing
## Ethos
This software is being created because I am a studying data science student and I want more ways to analyze my solve. This is being written to be dynamic with a config file.

## Requirements
- Python 3.8 + (I used python 3.8 but older versions may work)
- 

## Installation
1. [Install Python3.8+](https://www.python.org/downloads/)

2. Download Code
    - Click 'Clone or download'
    - Click 'Download ZIP
    - Go to download location and extract

3. Create Virtual Environment
    - Windows:
    - Press SHIFT and RIGHT CLICK in folder
    - LEFT CLICK 'Open PowerShell window here'
    - run:
    ```
    py -m venv venv
    ```
    
    - Linux/IOS:
    - In terminal:
    ```
    cd LOCATION OF CODE
    python -m venv venv
    ```

4. Activate Virtual Environment
    - Windows:   run venv\Scripts\activate.bat
    - Linux/IOS: run source venv/bin/activate

5. Install required modules
```
pip install -r requirements.txt
```

6. Run Application
    - Windows:   *double click* launch.bat
    - Linux/IOS: run 'bash launch.sh'


# Update log
- v0.1 Create project
    - Shows scramble in terminal
    - Shows scrambled state
    - Basic Hotkeys

- v0.2 Scamble on Screen
    - Shows scramble on screen
    - Slight refactor

- v0.3 Timer
    - Added timer functionality
    - Optimize a bit

- v0.4 Data
    - Refactor some code
    - Added Config
    - Added launch scripts
    - Created Readme

- v0.5 Support
    - Added windows support
    - Added a zip for venv