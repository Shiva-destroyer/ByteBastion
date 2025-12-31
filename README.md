# ByteBastion

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-Educational-green)
![Status](https://img.shields.io/badge/Status-Production--Ready-brightgreen)

```text
 ____        _       ____            _   _             
| __ ) _   _| |_ ___| __ )  __ _ ___| |_(_) ___  _ __  
|  _ \| | | | __/ _ \  _ \ / _` / __| __| |/ _ \| '_ \ 
| |_) | |_| | ||  __/ |_) | (_| \__ \ |_| | (_) | | | |
|____/ \__, |\__\___|____/ \__,_|___/\__|_|\___/|_| |_|
       |___/                                            
```

**A Comprehensive Security Toolkit for Cybersecurity Professionals & Researchers**

---

## 📚 **[Read the Full Documentation in the Wiki →](https://github.com/Shiva-destroyer/ByteBastion/wiki)**

For complete technical documentation, usage guides, security best practices, and deep-dive explanations of all tools, visit the **[ByteBastion Wiki](https://github.com/Shiva-destroyer/ByteBastion/wiki)**.

---

## 🎯 Overview

**ByteBastion** is a production-grade security suite combining **10 powerful tools** into a unified interface. Designed for penetration testers, security researchers, and system administrators.

### 🛡️ Security Tools

1. **[File Integrity Checker](https://github.com/Shiva-destroyer/ByteBastion/wiki/File-Integrity-Checker)** - SHA-256 hash verification
2. **[Educational Keylogger](https://github.com/Shiva-destroyer/ByteBastion/wiki/Educational-Keylogger)** - Input monitoring (authorized use only)
3. **[File Type Identifier](https://github.com/Shiva-destroyer/ByteBastion/wiki/File-Type-Identifier)** - Magic bytes analysis
4. **[Secure Password Generator](https://github.com/Shiva-destroyer/ByteBastion/wiki/Secure-Password-Generator)** - Cryptographic password creation
5. **[Data Deletion Utility](https://github.com/Shiva-destroyer/ByteBastion/wiki/Data-Deletion-Utility)** - DoD 5220.22-M secure wipe
6. **[AES Encryption](https://github.com/Shiva-destroyer/ByteBastion/wiki/AES-Encryption)** - AES-256-CBC file encryption
7. **[Directory Sync Monitor](https://github.com/Shiva-destroyer/ByteBastion/wiki/Directory-Sync-Monitor)** - Real-time file system monitoring
8. **[Temporary File Cleaner](https://github.com/Shiva-destroyer/ByteBastion/wiki/Temporary-File-Cleaner)** - Safe cache cleanup
9. **[Hidden File Detector](https://github.com/Shiva-destroyer/ByteBastion/wiki/Hidden-File-Detector)** - Malicious file discovery
10. **[Disk Space Analyzer](https://github.com/Shiva-destroyer/ByteBastion/wiki/Disk-Space-Analyzer)** - Storage analysis with alerts

---

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/Shiva-destroyer/ByteBastion.git
cd ByteBastion

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Launch ByteBastion
./run.sh
```

### Basic Usage

```bash
# Run ByteBastion
./run.sh

# Select tool by number (1-10)
# Follow interactive prompts
# Press Ctrl+C to exit
```

---

## ⚖️ Legal Notice

**IMPORTANT**: ByteBastion is for **authorized security testing and educational purposes ONLY**.

Unauthorized use of certain tools (keylogger, file access, monitoring) may violate:
- Computer Fraud and Abuse Act (CFAA) - U.S.
- Computer Misuse Act - UK  
- GDPR - European Union
- Local cybercrime and privacy laws

**The developer assumes NO liability for misuse. Users are responsible for legal compliance.**

---

## 🔐 Features

### Cryptography & Privacy
✅ AES-256-CBC encryption with PBKDF2-HMAC-SHA256  
✅ Cryptographically secure password generation  
✅ DoD 5220.22-M 3-pass file wiping  

### Analysis & Detection
✅ SHA-256 file integrity verification  
✅ Magic bytes file type identification  
✅ Hidden file and malware detection  
✅ Real-time disk usage analysis  

### Monitoring & Maintenance
✅ Event-driven directory monitoring (watchdog)  
✅ Intelligent temporary file cleanup  
✅ Keyboard input logging (ethical use only)  

---

## 🧪 Quality Assurance

- **25 Automated Tests** - 100% pass rate
- **PEP 8 Code Style** - Clean, maintainable code
- **Comprehensive Documentation** - Full technical wiki
- **Production-Ready** - Battle-tested implementation

```bash
# Run test suite
python tests/system_test.py
```

---

## 🏗️ Architecture

```
ByteBastion/
├── src/
│   ├── main.py          # Application entry point
│   └── modules/         # 10 security tools
├── tests/               # Automated test suite
├── wiki_docs/           # Wiki documentation
└── requirements.txt     # Dependencies
```

**Technology Stack**: Python 3.10+, Rich (UI), cryptography, watchdog, psutil, pynput, python-magic

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Write tests for new functionality
4. Ensure all tests pass
5. Submit pull request with detailed description

---

## 📄 License

MIT License - See [LICENSE](LICENSE) for details

---

## 📞 Contact

**Developer**: Sai Srujan Murthy  
**Email**: saisrujanmurthy@gmail.com  
**Repository**: [github.com/Shiva-destroyer/ByteBastion](https://github.com/Shiva-destroyer/ByteBastion)  
**Wiki**: [ByteBastion Wiki](https://github.com/Shiva-destroyer/ByteBastion/wiki)

---

## 🙏 Acknowledgments

Built with powerful open-source libraries:
- **Rich** - Terminal UI framework
- **cryptography** - Cryptographic recipes
- **watchdog** - File system monitoring
- **psutil** - System utilities
- **pynput** - Input monitoring
- **python-magic** - File type detection

---

<div align="center">

**Secure by Design • Educational by Purpose • Professional by Standard**

⭐ Star this repository if ByteBastion helps your security work!

</div>
