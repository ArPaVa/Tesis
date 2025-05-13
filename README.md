## Installation
```
python3 -m venv venv
source venv/bin/activate
pip install openai-whisper
pip install pyannote.audio
pip install pydub
pip install llama-cpp-python
```

```
sudo apt install ffmpeg
```

### llama-cpp requirements https://pypi.org/project/llama-cpp-python/
Install a C compiler:  https://winlibs.com/#download-release
- Linux: gcc or clang
- Windows: Visual Studio or MinGW
- MacOS: Xcode


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
    ```

    ```
    pip install --upgrade --force-reinstall --no-cache-dir llama-cpp-python
    ```

## LLM used:

https://huggingface.co/Open-Orca/Mistral-7B-OpenOrca

## 
Read in a paper that for lower end pcs, cuting the audios in 5 minutes pieces helps to reduce memory usage and speeds up processing. Wich is something we really need

## Whisper
medium 1.42 GB download
