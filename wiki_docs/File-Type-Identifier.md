# File Type Identifier

## Overview

The **File Type Identifier** uses **magic bytes analysis** to determine the true type of a file, independent of its extension. This is critical for detecting malware disguised with misleading extensions (e.g., `invoice.pdf.exe` appearing as `invoice.pdf` on Windows).

---

## 🔬 Technical Deep Dive

### What Are Magic Bytes?

**Magic bytes** (file signatures) are specific byte sequences at the beginning of files that identify their format. Operating systems use these to determine how to handle files.

### Magic Bytes Examples

| File Type | Magic Bytes (Hex) | Magic Bytes (ASCII) | Offset |
|-----------|-------------------|---------------------|--------|
| **JPEG** | `FF D8 FF` | `ÿØÿ` | 0 |
| **PNG** | `89 50 4E 47 0D 0A 1A 0A` | `‰PNG....` | 0 |
| **PDF** | `25 50 44 46` | `%PDF` | 0 |
| **ZIP** | `50 4B 03 04` | `PK..` | 0 |
| **GIF** | `47 49 46 38` | `GIF8` | 0 |
| **EXE (Windows)** | `4D 5A` | `MZ` | 0 |
| **ELF (Linux)** | `7F 45 4C 46` | `.ELF` | 0 |
| **MP3** | `FF FB` or `49 44 33` | `ÿû` or `ID3` | 0 |
| **MP4** | `66 74 79 70` | `ftyp` | 4 |
| **RAR** | `52 61 72 21` | `Rar!` | 0 |

**Full Database**: [List of File Signatures (Wikipedia)](https://en.wikipedia.org/wiki/List_of_file_signatures)

---

## 🛠️ libmagic & python-magic

### How libmagic Works

ByteBastion uses **python-magic**, which wraps the `libmagic` C library (same technology as Unix `file` command).

**Detection Process**:
1. Read first N bytes of file (typically 4KB)
2. Match against magic byte database (`/usr/share/misc/magic.mgc` on Linux)
3. Apply heuristic analysis if no exact match
4. Return MIME type and description

### MIME Type System

MIME (Multipurpose Internet Mail Extensions) types follow format: `type/subtype`

**Categories**:
- `text/*` - Text documents (`text/plain`, `text/html`)
- `image/*` - Images (`image/jpeg`, `image/png`)
- `video/*` - Videos (`video/mp4`, `video/mpeg`)
- `audio/*` - Audio (`audio/mpeg`, `audio/wav`)
- `application/*` - Binary data (`application/pdf`, `application/zip`)

### Implementation

```python
import magic
import os

# Detect MIME type
mime = magic.Magic(mime=True)
mime_type = mime.from_file('/path/to/file.jpg')
# Returns: 'image/jpeg'

# Get human-readable description
descriptor = magic.Magic()
description = descriptor.from_file('/path/to/file.jpg')
# Returns: 'JPEG image data, JFIF standard 1.01, resolution (DPI), density 72x72'
```

---

## 📖 Usage Guide

### Analyzing a File

```bash
# Launch ByteBastion
./run.sh

# Select option 3 (File Type Identifier)
# Enter file path: /path/to/suspicious_file.pdf
```

### Interpreting Results

#### ✅ Safe File (Extension Matches)

```
╭─────────────────────────────────────────────────────────╮
│            ✓ File Type Analysis                         │
├─────────────────────────────────────────────────────────┤
│ Filename:         report.pdf                            │
│ Extension:        .pdf                                  │
│ Actual MIME Type: application/pdf                       │
│ Expected MIME:    application/pdf                       │
│ Description:      PDF document, version 1.7             │
│ Size:             524,288 bytes                         │
│                                                         │
│ ✓ File extension matches the actual file type          │
╰─────────────────────────────────────────────────────────╯
```

#### ⚠️ Suspicious File (Extension Mismatch)

```
╭─────────────────────────────────────────────────────────╮
│       ⚠ WARNING: Extension Mismatch Detected!          │
├─────────────────────────────────────────────────────────┤
│ Filename:         invoice.pdf                           │
│ Extension:        .pdf                                  │
│ Actual MIME Type: application/x-dosexec                 │
│ Expected MIME:    application/pdf                       │
│ Description:      PE32 executable (GUI) Intel 80386     │
│ Size:             1,048,576 bytes                       │
╰─────────────────────────────────────────────────────────╯

╭─────────────────────────────────────────────────────────╮
│                    Security Alert                       │
├─────────────────────────────────────────────────────────┤
│ SECURITY WARNING:                                       │
│ The file extension '.pdf' does not match the actual     │
│ file type!                                              │
│                                                         │
│ This could indicate:                                    │
│   • File renamed to hide its true nature               │
│   • Potential malware disguised with fake extension    │
│   • Social engineering attempt                         │
│   • Accidental file renaming                           │
│                                                         │
│ Exercise caution before opening this file!              │
╰─────────────────────────────────────────────────────────╯
```

---

## 🔍 Attack Scenarios

### Scenario 1: Disguised Executable

**Attack**: Attacker emails `document.pdf` (actually `malware.exe`)

```
Expected: application/pdf (PDF document)
Actual:   application/x-dosexec (Windows executable)

Risk: User double-clicks, executes malware
```

**Why it works**:
- Windows hides known extensions by default
- Users trust PDF icon
- No technical knowledge required

**Defense**: ByteBastion detects mismatch immediately

### Scenario 2: Polyglot Files

**Advanced Attack**: File valid as BOTH PDF and executable

```python
# Polyglot structure
[PDF Header: %PDF-1.7]
[PDF content...]
[Malicious payload at specific offset]
[PE executable header at different offset]
```

**Behavior**:
- PDF reader: Opens as legitimate PDF
- OS executor: Runs as executable

**Detection**: ByteBastion identifies conflicting signatures

### Scenario 3: Double Extension Trick

**Attack**: `invoice.pdf.exe` (Windows hides `.exe`)

```
Displayed:  invoice.pdf
Full name:  invoice.pdf.exe
True type:  application/x-dosexec
```

**Why it works**:
- Windows Explorer: "Hide extensions for known file types" (default ON)
- User sees PDF icon
- Clicking executes .exe

**Defense**: ByteBastion analyzes actual file type, not extension

### Scenario 4: Embedded Malware in Images

**Attack**: JPEG with embedded PHP webshell

```
File: profile_pic.jpg
Magic bytes: FF D8 FF (valid JPEG)
Embedded:    <?php system($_GET['cmd']); ?>
```

**Behavior**:
- Image viewer: Displays valid image
- PHP interpreter: Executes malicious code

**Detection**: ByteBastion may flag as `text/x-php` if PHP code is prominent

---

## 🛡️ Security Best Practices

### 1. Always Verify Downloaded Files

```bash
# Before opening ANY downloaded file
./run.sh → File Type Identifier → Analyze file

# Especially for:
- Email attachments
- Files from USB drives
- Downloads from untrusted websites
```

### 2. Enable Full Extensions in OS

**Windows**:
```
File Explorer → View → Options → View tab
☐ Hide extensions for known file types (UNCHECK)
```

**macOS**:
```
Finder → Preferences → Advanced
☑ Show all filename extensions (CHECK)
```

**Linux**: Extensions shown by default in most file managers

### 3. Sandbox Unknown Files

```bash
# Open in isolated environment
firejail --private firefox suspicious_file.pdf

# Or use virtual machine
VirtualBox → Snapshot → Open file → Revert if malicious
```

### 4. Automate Scanning

```bash
#!/bin/bash
# Scan downloads directory automatically

inotifywait -m ~/Downloads -e create |
while read path action file; do
    echo "New file: $file"
    python3 -c "
from modules.file_type_identifier import FileTypeIdentifier
fti = FileTypeIdentifier()
result = fti.analyze_file('$path$file')
if result.get('mismatch'):
    print('⚠ WARNING: Extension mismatch detected!')
    notify-send 'Security Alert' 'Suspicious file detected in Downloads'
"
done
```

---

## 🔧 Technical Implementation

### Magic Database Location

**Linux**:
- Database: `/usr/share/misc/magic.mgc` (compiled binary)
- Text source: `/usr/share/misc/magic` (human-readable)

**macOS**:
- Database: `/usr/share/file/magic.mgc`

**Windows**:
- Bundled with python-magic installation

### Custom Magic Patterns

Create custom detection rules:

```bash
# /etc/magic.custom
0       string          \x89PNG\r\n\x1a\n       PNG image
0       string          %PDF                     PDF document
0       string          MZ                       DOS/Windows executable
```

Compile custom database:
```bash
file -C -m /etc/magic.custom
```

### ByteBastion Detection Logic

```python
class FileTypeIdentifier:
    def analyze_file(self, file_path):
        # Get actual MIME type from magic bytes
        mime = magic.Magic(mime=True)
        actual_mime = mime.from_file(file_path)
        
        # Get expected MIME from extension
        extension = os.path.splitext(file_path)[1].lower()
        expected_mime = self.extension_mapping.get(extension)
        
        # Detect mismatch (with fuzzy matching)
        mismatch = False
        if expected_mime and expected_mime != actual_mime:
            # Handle MIME type variations
            if not (expected_mime in actual_mime or actual_mime in expected_mime):
                mismatch = True
        
        return {
            'actual_mime': actual_mime,
            'expected_mime': expected_mime,
            'mismatch': mismatch,
            'description': mime_desc.from_file(file_path)
        }
```

---

## 🐛 Troubleshooting

### Issue: "python-magic not installed"

**Solution**:
```bash
# Install Python package
pip install python-magic

# Install libmagic library
# Debian/Ubuntu:
sudo apt-get install libmagic1

# RedHat/CentOS:
sudo yum install file-libs

# macOS:
brew install libmagic
```

### Issue: "Unable to open magic database"

**Solution**:
```bash
# Reinstall magic database
sudo apt-get install --reinstall libmagic-mgc

# Or specify custom path
export MAGIC=/usr/share/misc/magic.mgc
```

### Issue: Incorrect MIME type detection

**Causes**:
- Corrupted file
- Proprietary format not in database
- Encrypted/compressed data masking signature

**Solution**:
```bash
# Try multiple detection methods
file -b --mime-type suspicious_file
mimetype suspicious_file
python3 -c "import magic; print(magic.from_file('suspicious_file', mime=True))"
```

---

## 📚 Further Reading

- [File Format Specifications](https://www.fileformat.info/)
- [Magic Byte Database](https://en.wikipedia.org/wiki/List_of_file_signatures)
- [libmagic Source Code](https://github.com/file/file)
- [MIME Types RFC 2045](https://tools.ietf.org/html/rfc2045)

---

## 🔗 Related Tools

- [[File-Integrity-Checker]] - Verify file hasn't been tampered with after type verification
- [[Hidden-File-Detector]] - Find hidden malicious files
- [[Directory-Sync-Monitor]] - Monitor for suspicious new files

---

**Developer**: Sai Srujan Murthy | **Contact**: saisrujanmurthy@gmail.com
