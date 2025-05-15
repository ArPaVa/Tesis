# Tesis

## Setup

Add the variable: HF_ACCESS_TOKEN to a .env file

Prepare for the download of the whisper model. (medium=1.42 GB small=461MB)
Prepare for the download of the pyannote model. (30MB)

## Installation

```
sudo apt install ffmpeg
```

```bash
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

### llama-cpp requirements https://pypi.org/project/llama-cpp-python/
Install a C compiler:  https://winlibs.com/#download-release
- Linux: gcc or clang
- Windows: Visual Studio or MinGW
- MacOS: Xcode
<!-- 

Add `gcc` to PATH. 
 TODO

Set environment variables to specify the compiler and generator.

    In **Command Prompt** (cmd.exe), run:
    ```cmd
    set CC=C:\mingw64\bin\gcc.exe
    set CXX=C:\mingw64\bin\g++.exe
    set CMAKE_GENERATOR=MinGW Makefiles

    set CMAKE_MAKE_PROGRAM=C:\mingw64\bin\mingw32-make.exe
    ```

    In **PowerShell**, run:
    ```powershell
    $env:CC = "C:\mingw64\bin\gcc.exe"
    $env:CXX = "C:\mingw64\bin\g++.exe"
    $env:CMAKE_GENERATOR = "MinGW Makefiles"
    $env:CMAKE_MAKE_PROGRAM = "C:\mingw64\bin\mingw32-make.exe"
    $env:CMAKE_ARGS = "-DGGML_OPENBLAS=on -DCMAKE_C_COMPILER=C:\mingw64\bin\gcc.exe -DCMAKE_CXX_COMPILER=C:\mingw64\bin\g++.exe"
    ``` -->

```bash
pip install --upgrade --force-reinstall --no-cache-dir llama-cpp-python
```

## Execution

To execute just execute main, it will ask for the path of the file you want to work with, the path needs to have the full path including the format (example.mp3), or just the name of the file (including format), if the file is on the same folder as main.

```bash
python3 main.py
```

## LLM used:

https://huggingface.co/Open-Orca/Mistral-7B-OpenOrca

```bash
python3 llm.py
```

## 
Read in a paper that for lower end pcs, cuting the audios in 5 minutes pieces helps to reduce memory usage and speeds up processing. Wich is something we really need

## Whisper
medium 1.42 GB download
