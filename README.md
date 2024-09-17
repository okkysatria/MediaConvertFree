# Media Convert Free

A versatile media conversion application for Windows that allows you to convert various media files using GPU acceleration. The application provides both an executable file and a Python script for ease of use.

<div align="center">
  <img src="https://github.com/user-attachments/assets/e56e3d75-bb01-4a6c-a6bd-b3ecdbcb7f6d" alt="ss" width="500"/>
</div>


## Requirements

- **Windows 10/11**
- **Python 3.11.x** (Required only for the Python script, not for the executable)
- **FFmpeg** (Make sure FFmpeg is installed and accessible from the command line)

## Download and Installation

### Option 1: Using the Executable

1. **Download the Executable:**
   - [Download](https://github.com/okkysatria/MediaConvertFree/releases/download/v1/MCF.exe)

2. **Run the Executable:**
   - Double-click the downloaded file to launch the application. The GUI will allow you to select folders, filter files, and start the conversion process.
   - Use the following features:
     - **Browse:** Select the folder containing media files.
     - **Apply Filter:** Filter files by type.
     - **Select All:** Select all files for conversion.
     - **Start Conversion:** Begin converting the selected files.
     - **Stop:** Halt the conversion process if needed.
     - **Save to Original Path:** Choose whether to save converted files in their original directory or a specified folder.

### Option 2: Using the Python Script

1. **Download the Repository:**
   - [Download ZIP](https://github.com/okkysatria/MediaConvertFree/archive/refs/heads/main.zip) (Replace with actual link)

2. **Extract the ZIP File:**
   - Extract the ZIP file to a location of your choice.

3. **Install Python:**
   - Ensure Python 3.11.x is installed on your system. Download it from the [official Python website](https://www.python.org/ftp/python/3.11.1/python-3.11.1-amd64.exe).

4. **Install Dependencies:**
   - Open a command prompt or terminal, navigate to the extracted directory, and install the required libraries with:
     ```bash
     pip install -r requirements.txt
     ```

5. **Run the Script:**
   - Execute the script by running `python media_convert.py` in your terminal.

6. **Interactive Commands:**
   - Press `e` to exit the script.
   - Press `s` to start the conversion process.

7. **Specify Save File Path:**
   - Provide the path where the converted files will be saved, if not using the original path.

## Features

- **GPU Acceleration:** Detects and uses available GPU codecs (NVIDIA, AMD, Intel) for enhanced performance.
- **File Filtering:** Filter media files by type before conversion.
- **Progress Monitoring:** Track conversion progress with a progress bar.
- **File Handling:** Option to delete original files after conversion.
