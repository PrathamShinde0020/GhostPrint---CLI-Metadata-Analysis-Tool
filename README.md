<div align="center">
<img width="1026" height="765" alt="image" src="https://github.com/user-attachments/assets/fb5f79fc-a5b2-4db1-8c34-5566365c6286" alt="GhostPrint Banner" width="200" />

👻 GhostPrint 🕵️‍♂️
A Command-Line Metadata Extraction Tool for Cybersecurity, Forensics & OSINT
Reveal the invisible. Extract the undeniable.
</div>

GhostPrint is a powerful, user-friendly CLI tool built in Python for extracting and analyzing hidden metadata from various file types. It is tailored for cybersecurity analysts, digital forensic investigators, and OSINT practitioners who need to quickly uncover digital traces left behind in files.

This tool can reveal critical insights such as file authorship, device details, software versions, timestamps, and even GPS locations, supporting investigations, detecting content manipulation, and aiding in threat actor reconnaissance.

✨ Key Features
1. 🖥️ Rich CLI Interface: Utilizes the rich library to provide a clean, colorful, and highly readable user experience with styled tables and interactive prompts.

2. ⚙️ Dual-Analysis Engine: Employs a hybrid approach, using native Python libraries (Pillow, PyPDF2) for quick, human-readable summaries and integrating the industry-standard exiftool for comprehensive, deep-dive forensic analysis.

3. 🛡️ OSINT Risk Assessment: Automatically analyzes and flags high-risk metadata, providing instant context on potential data leaks (e.g., "Could reveal location," "Device fingerprint").

4. 📂 Multi-Format Support: Natively parses metadata from common image formats (JPEG, PNG, etc.) and PDF documents, with fallback support for dozens of other file types via exiftool.

5. 💾 Flexible Export Options: Allows users to export the extracted metadata to structured formats like JSON or CSV for further analysis, reporting, or integration with other tools.

6. 📦 Standalone Executable: Packaged with PyInstaller into a single .exe file, allowing it to run on any Windows system without requiring Python or any dependencies to be installed.
   
🛠️ Technology Stack
Language: Python 3

Core Libraries:
rich - For the rich text user interface.
Pillow - For native image metadata parsing.
PyPDF2 - For native PDF metadata parsing.

External Dependency:
exiftool - For advanced and fallback metadata extraction (optional, but recommended for full functionality).

Packaging:
PyInstaller - For creating the standalone executable.

🚀 Getting Started
You can run GhostPrint in two ways: by using the pre-built executable (easiest) or by running the source code directly.
Method 1: Using the Executable (Recommended)
1. Navigate to the Releases page of this repository.
2. Download the GhostPrint.exe file from the latest release.
3. Open your command prompt (CMD) or PowerShell, navigate to the directory where you downloaded the file, and run it:
   .\GhostPrint.exe
4. Follow the on-screen prompts to provide the path to the file you wish to analyze.

Method 2: Running from Source Code
Prerequisites
Python 3.8 or newer

pip (Python package installer)

(Optional but Recommended) ExifTool installed and added to your system's PATH.

Installation
Clone the repository:

git clone https://github.com/PrathamShinde0020/GhostPrint---CLI-Metadata-Analysis-Tool.git
cd GhostPrint---CLI-Metadata-Analysis-Tool
Install the required Python packages:

pip install -r requirements.txt
Run the application:

python ghostprint.py
🔮 Future Enhancements
[ ] Reverse Geolocation: Integrate an API to convert GPS coordinates into physical addresses.
[ ] Metadata Anonymizer: Add a feature to strip and remove metadata from files.
[ ] Bulk Processing: Enable metadata extraction from all files within a specified folder.
[ ] Web Interface: Develop a simple web-based version of the tool.

📄 License
This project is licensed under the MIT License. See the LICENSE file for details.





