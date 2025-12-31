# Welcome to ByteBastion

**ByteBastion** is a comprehensive, modular security toolkit designed for educational purposes, penetration testing, and security research. Built with Python, it provides 10 powerful security tools in a unified, easy-to-use interface.

---

## 🎯 Project Architecture

ByteBastion follows a modular design pattern where each security tool operates independently as a Python module. The main application (`src/main.py`) serves as a central hub that orchestrates tool execution through a Rich-powered terminal interface.

### Architecture Overview

```
ByteBastion/
├── src/
│   ├── main.py              # Central application hub
│   └── modules/             # Individual security tools
│       ├── file_checker.py
│       ├── keylogger.py
│       ├── file_type_identifier.py
│       └── ... (10 tools total)
├── tests/                   # Automated test suite
└── requirements.txt         # Dependencies
```

### Design Principles

1. **Modularity**: Each tool is self-contained and can be used independently
2. **Extensibility**: New tools can be added without modifying existing code
3. **User-Friendly**: Rich terminal UI provides clear feedback and error handling
4. **Educational Focus**: Comprehensive documentation explains the "why" behind each tool

---

## 🔐 Security Tools Suite

ByteBastion includes 10 specialized security tools:

### 1. [[File-Integrity-Checker]]
Verifies file authenticity using SHA-256 cryptographic hashing to detect unauthorized modifications.

### 2. [[Educational-Keylogger]]
Monitors keyboard input for security research and ethical penetration testing.

### 3. [[File-Type-Identifier]]
Analyzes magic bytes to detect file type mismatches and identify disguised malware.

### 4. [[Secure-Password-Generator]]
Generates cryptographically secure passwords with configurable entropy levels.

### 5. [[Data-Deletion-Utility]]
Securely wipes files using DoD 5220.22-M standard 3-pass overwriting algorithm.

### 6. [[AES-Encryption]]
Encrypts and decrypts files using AES-256-CBC with PBKDF2-HMAC-SHA256 key derivation.

### 7. [[Directory-Sync-Monitor]]
Real-time monitoring of file system changes using event-driven architecture.

### 8. [[Temporary-File-Cleaner]]
Safely identifies and removes temporary files with age-based filtering.

### 9. [[Hidden-File-Detector]]
Discovers hidden files and identifies potentially malicious content using heuristic analysis.

### 10. [[Disk-Space-Analyzer]]
Analyzes disk usage across partitions with color-coded warnings for storage thresholds.

---

## ⚖️ Legal & Ethical Disclaimer

**IMPORTANT**: ByteBastion is developed strictly for **educational purposes** and **authorized security testing**.

### Authorized Use Cases
✅ Learning cybersecurity concepts  
✅ Authorized penetration testing  
✅ Security research in controlled environments  
✅ Educational demonstrations  

### Prohibited Use Cases
❌ Unauthorized access to systems  
❌ Malicious activities or data theft  
❌ Violating privacy laws (GDPR, CCPA, etc.)  
❌ Corporate espionage or illegal surveillance  

**Legal Warning**: Unauthorized use of keyloggers, file access tools, or monitoring software may violate:
- Computer Fraud and Abuse Act (CFAA) - U.S.
- Computer Misuse Act - UK
- GDPR - European Union
- Local privacy and cybercrime laws

**The developer assumes no liability for misuse of this software. Users are solely responsible for ensuring compliance with applicable laws.**

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/Shiva-destroyer/ByteBastion.git
cd ByteBastion

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Launch ByteBastion
./run.sh
```

### Basic Usage

1. **Launch the application**: `./run.sh`
2. **Select a tool**: Enter the tool number (1-10)
3. **Follow prompts**: Each tool provides interactive guidance
4. **Return to menu**: Press Enter after tool completion

---

## 🧪 Quality Assurance

ByteBastion includes a comprehensive automated test suite:

- **25 Test Cases** covering all 10 modules
- **100% Pass Rate** validated through continuous testing
- **Integration Tests** ensure module interoperability
- **Mock Testing** for safe execution without side effects

Run tests:
```bash
python tests/system_test.py
```

---

## 📊 Technology Stack

| Component | Technology |
|-----------|-----------|
| **Language** | Python 3.10+ |
| **UI Framework** | Rich (terminal UI) |
| **Cryptography** | `cryptography`, `hashlib` |
| **File System** | `watchdog`, `psutil` |
| **Input Monitoring** | `pynput` |
| **Type Detection** | `python-magic` |

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Write tests for new functionality
4. Ensure all tests pass: `python tests/system_test.py`
5. Submit a pull request with detailed description

---

## 📞 Contact & Support

Have questions or found a bug? Reach out:

**Developer**: Sai Srujan Murthy | **Contact**: saisrujanmurthy@gmail.com
