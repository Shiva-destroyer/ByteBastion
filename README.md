# ByteBastion - Comprehensive Security Suite

A modular cybersecurity toolkit designed for security professionals and students. ByteBastion provides 10 essential security tools in a single, easy-to-use interface.

## 🛡️ Features

ByteBastion includes the following security tools:

1. **File Integrity Checker** - Verify file integrity using cryptographic hashes
2. **Educational Keylogger** - Learn about keystroke logging (educational purposes only)
3. **File Type Identifier** - Identify file types using magic bytes analysis
4. **Secure Password Generator** - Generate cryptographically secure passwords
5. **Data Deletion Utility** - Securely wipe files beyond recovery
6. **AES Encryption/Decryption** - Encrypt and decrypt files using AES
7. **Directory Sync Monitor** - Monitor directories for changes in real-time
8. **Temporary File Cleaner** - Clean temporary files from your system
9. **Hidden File Detector** - Scan directories for hidden files
10. **Disk Space Analyzer** - Analyze disk usage with smart alerts

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

### Setup

1. **Clone or navigate to the repository:**
   ```bash
   cd "/home/shivansh/Vs Code/Github projects/ByteBastion"
   ```

2. **Create and activate virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Linux/Mac
   # or
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Usage

Run the application:
```bash
cd src
python main.py
```

Navigate the menu by entering the number corresponding to the tool you want to use.

## 📦 Dependencies

- **rich** - Professional terminal UI and tables
- **pyfiglet** - ASCII art banner generation
- **cryptography** - AES encryption and hashing
- **pynput** - Keyboard and mouse monitoring
- **watchdog** - File system event monitoring
- **psutil** - System and process utilities
- **schedule** - Task scheduling
- **python-magic** - File type identification

## 🏗️ Project Structure

```
ByteBastion/
├── src/
│   ├── main.py                    # Main application entry point
│   ├── __init__.py
│   └── modules/                   # Security tool modules
│       ├── __init__.py
│       ├── file_checker.py        # File integrity verification
│       ├── keylogger.py           # Educational keylogger
│       ├── file_type_identifier.py
│       ├── password_generator.py
│       ├── data_deletion.py
│       ├── aes_crypto.py
│       ├── directory_monitor.py
│       ├── temp_cleaner.py
│       ├── hidden_detector.py
│       └── disk_analyzer.py
├── venv/                          # Virtual environment
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## 🔒 Security Notice

**IMPORTANT:** This toolkit is designed for educational and authorized security research purposes only. 

- Always obtain proper authorization before testing on systems you don't own
- The keylogger module is strictly for educational purposes
- Misuse of these tools may violate laws and regulations
- Use responsibly and ethically

## 👨‍💻 Development

### Adding New Tools

1. Create a new module file in `src/modules/`
2. Implement a class with a `run()` method
3. Import and add the tool to `main.py`
4. Update the menu table with the new tool

### Code Standards

- Follow PEP 8 style guidelines
- Use docstrings for all classes and functions
- Keep modules independent and modular
- Handle errors gracefully

## 🤝 Contributing

Contributions are welcome! Please ensure:
- Code follows PEP 8 standards
- All tools include proper error handling
- Documentation is updated accordingly

## 📧 Contact

**Developer:** Sai Srujan Murthy

For questions, suggestions, or bug reports, please reach out via email.

## 📝 License

This project is created for educational purposes. Use at your own risk and ensure compliance with local laws and regulations.

## 🎯 Implementation Status

- [x] ~~Implement File Integrity Checker functionality~~ ✅ **COMPLETE**
- [x] ~~Implement Educational Keylogger (with warnings)~~ ✅ **COMPLETE**
- [x] ~~Add File Type Identifier logic~~ ✅ **COMPLETE**
- [x] ~~Build Password Generator with customization~~ ✅ **COMPLETE**
- [x] ~~Create secure file wiping utility~~ ✅ **COMPLETE**
- [x] ~~Implement AES encryption/decryption~~ ✅ **COMPLETE**
- [x] ~~Build directory monitoring system~~ ✅ **COMPLETE**
- [x] ~~Add temp file cleaning capabilities~~ ✅ **COMPLETE**
- [x] ~~Develop hidden file detection~~ ✅ **COMPLETE**
- [x] ~~Create disk space analyzer with alerts~~ ✅ **COMPLETE**

**All 10 security tools are fully implemented and production-ready! 🎉**

## 🙏 Acknowledgments

Built with modern Python libraries:
- Rich Console for beautiful terminal UI
- Cryptography library for security features
- Watchdog for file system monitoring
- And many more amazing open-source tools

---

**Stay Secure! 🔒**
