# README

## Requirements

**Operating System**

- Linux is recommended for best compatibility and performance.

**Python**

- Python version 3.10 or higher is required.

**External Dependencies**

- **FFmpeg**: Required for audio processing.
  - **Installation on Linux:**
    ```bash
    sudo apt install ffmpeg
    ```

- **C Compiler**: Required for llama-cpp-python.
  - **Linux:** It should come installed, if not: Install `gcc` or `clang`.
    ```bash
    sudo apt install build-essential
    ```

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/ArPaVa/Tesis.git
   cd Tesis
   ```

2. **Create and Activate Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install llama-cpp-python**
   ```bash
   pip install --upgrade --force-reinstall --no-cache-dir llama-cpp-python
   ```

5. **Set Environment Variables**
   - Add your Hugging Face access token to a `.env` file in the project root:
     ```
     HF_ACCESS_TOKEN=your_huggingface_token
     ```
    For this yu must have an account in [Hugging Face](https://huggingface.co)

## Model Downloads and Setup

**Whisper Model**

- The application supports several Whisper models:
  - `medium` (1.42 GB)
  - `small` (461 MB)
  - `base` (138 MB)
  - `tiny` (73 MB)
- The model will be downloaded automatically as needed. Ensure you have sufficient disk space and internet connection.

**LLM Model [Mistral-7B-OpenOrca](https://huggingface.co/Open-Orca/Mistral-7B-OpenOrca)**

- Download the GGUF file `mistral-7b-openorca.Q4_K_M.gguf` from [TheBloke/Mistral-7B-OpenOrca-GGUF](https://huggingface.co/TheBloke/Mistral-7B-OpenOrca-GGUF?show_file_info=mistral-7b-openorca.Q4_K_M.gguf). Or download directly from this link (https://huggingface.co/TheBloke/Mistral-7B-OpenOrca-GGUF/resolve/main/mistral-7b-openorca.Q4_K_M.gguf?download=true).
- Place the downloaded `.gguf` file into the `/models` directory in the project root.
- The model file size is approximately 4.10 GB.
- Max RAM required: 6.87 GB.

## Running the Application

- Start the web application with Streamlit:
  ```bash
  streamlit run src/app.py
  ```

## Audacity

**What is Audacity?**

Audacity is a free, open-source audio editor and recorder. It is widely used for recording, editing, and processing audio files.

**Important:**  
Audacity must be running to use this module. If you have multiple Audacity windows open, the code will operate on the last Audacity window opened. You cannot select which window the macros are sent to.

### Enable mod-script-pipe

The `mod-script-pipe` module is not enabled by default in Audacity and must be enabled to allow external scripting.

**To enable mod-script-pipe:**

1. **Run Audacity.**
2. Go to **Edit > Preferences > Modules**.
3. Locate `mod-script-pipe` (it should show as "New") and change its status to **Enabled**.
4. **Restart Audacity**.
5. Return to **Edit > Preferences > Modules** and check that `mod-script-pipe` now shows as **Enabled**.

This confirms that Audacity is finding the mod-script-pipe module and that the version is compatible.

**Note:**  
Audacity must remain open while using this project to enable automatic project generation and scripting integration.
