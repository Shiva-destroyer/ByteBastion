# Hidden File Detector

## Overview

The **Hidden File Detector** discovers concealed files using dotfile detection, attribute checking, and heuristic analysis. It identifies potentially malicious files that bypass casual inspection.

---

## 🔬 What Are Hidden Files?

### Platform-Specific Hiding Methods

**Linux/macOS**: Dotfiles (filename starts with `.`)
```bash
.hidden_file.txt        # Hidden
normal_file.txt         # Visible

ls                      # Doesn't show .hidden_file.txt
ls -a                   # Shows all files including hidden
```

**Windows**: Hidden attribute flag
```cmd
attrib +h secret.txt    # Hide file
attrib -h secret.txt    # Unhide file

dir                     # Doesn't show hidden files
dir /a:h                # Shows hidden files
```

**Cross-Platform**: Alternate Data Streams (NTFS), Extended Attributes, Steganography

---

## 🛠️ Detection Techniques

### 1. Dotfile Detection (Unix-like Systems)

```python
import os

def find_dotfiles(directory):
    """Find all hidden files starting with dot"""
    hidden_files = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.startswith('.') and file not in ['.', '..']:
                full_path = os.path.join(root, file)
                hidden_files.append(full_path)
    
    return hidden_files

# Example output:
# /home/user/.bash_history (legitimate)
# /home/user/.evil_script.sh (suspicious)
```

### 2. Windows Hidden Attribute

```python
import ctypes
from ctypes import wintypes

def is_hidden_windows(file_path):
    """Check if file has hidden attribute on Windows"""
    FILE_ATTRIBUTE_HIDDEN = 0x02
    
    attrs = ctypes.windll.kernel32.GetFileAttributesW(file_path)
    return bool(attrs & FILE_ATTRIBUTE_HIDDEN)

# Check file
if is_hidden_windows("C:\\secret.txt"):
    print("File is hidden")
```

### 3. Extended Attributes (macOS)

```python
import xattr

def check_hidden_flag_macos(file_path):
    """Check macOS hidden flag in extended attributes"""
    try:
        attrs = xattr.xattr(file_path)
        # Check for com.apple.FinderInfo hidden flag
        finder_info = attrs.get('com.apple.FinderInfo', b'')
        if len(finder_info) >= 9:
            # Byte 8 contains visibility flags
            return bool(finder_info[8] & 0x40)  # kIsInvisible flag
    except:
        return False
```

### 4. Heuristic Analysis

Identify suspicious characteristics:

```python
def analyze_suspiciousness(file_path):
    """Calculate suspicion score based on heuristics"""
    score = 0
    
    # 1. Hidden file in user directory
    if file_path.startswith(os.path.expanduser('~')):
        if os.path.basename(file_path).startswith('.'):
            score += 2
    
    # 2. Executable hidden file
    if os.access(file_path, os.X_OK):
        score += 3
    
    # 3. Recently created (< 24 hours)
    age = time.time() - os.path.getctime(file_path)
    if age < 86400:  # 24 hours
        score += 2
    
    # 4. Non-standard name (random characters)
    name = os.path.basename(file_path)
    if sum(c.isalnum() for c in name) / len(name) < 0.5:
        score += 2
    
    # 5. Common malware extensions
    malware_exts = ['.exe', '.bat', '.cmd', '.vbs', '.ps1', '.sh']
    if any(file_path.endswith(ext) for ext in malware_exts):
        score += 3
    
    return score  # 0-12 scale

# Interpretation:
# 0-3:  Likely benign (config files)
# 4-6:  Potentially suspicious
# 7-9:  Highly suspicious
# 10+:  Critical threat
```

---

## 📖 Usage Guide

### Scanning for Hidden Files

```bash
# Launch ByteBastion
./run.sh

# Select option 9 (Hidden File Detector)
# Choose scan directory: /home/user
# Scan recursively? (y/n): y
# Show only suspicious files? (y/n): y
```

**Output**:
```
╭─────────────────────────────────────────────────────────╮
│            Hidden File Detection Report                 │
├─────────────────────────────────────────────────────────┤
│ Scanned: /home/user                                     │
│ Files analyzed: 1,234                                   │
│ Hidden files found: 47                                  │
│ Suspicious files: 3                                     │
│                                                         │
│ 🔴 CRITICAL THREAT (Score: 11/12)                      │
│ Path: /home/user/.evil_backdoor.sh                     │
│ Reason:                                                 │
│   • Hidden file (dotfile)                               │
│   • Executable permissions                              │
│   • Created 2 hours ago                                 │
│   • Suspicious extension (.sh)                          │
│ Action: QUARANTINE IMMEDIATELY                          │
│                                                         │
│ 🟠 HIGHLY SUSPICIOUS (Score: 8/12)                     │
│ Path: /home/user/.cache/.X19dGF0                       │
│ Reason:                                                 │
│   • Hidden file in cache directory                      │
│   • Base64-encoded name                                 │
│   • Executable permissions                              │
│ Action: INVESTIGATE                                     │
│                                                         │
│ 🟡 POTENTIALLY SUSPICIOUS (Score: 5/12)                │
│ Path: /home/user/.local/share/.tmpfile                 │
│ Reason:                                                 │
│   • Hidden file                                         │
│   • Recently modified                                   │
│ Action: MONITOR                                         │
╰─────────────────────────────────────────────────────────╯
```

---

## 🔍 Common Hidden File Locations

### Benign Hidden Files

```
~/.bashrc               # Shell configuration
~/.ssh/                 # SSH keys and config
~/.gitconfig            # Git configuration
~/.vimrc                # Vim configuration
~/.mozilla/             # Firefox profile
~/.cache/               # Application caches
```

### Suspicious Locations

```
~/.config/autostart/    # Auto-start malware
~/.local/share/         # User data (check for unusual files)
/tmp/.hidden/           # Temporary malware staging
/var/tmp/.X11-unix/     # Fake X11 socket names
~/.ICE-unix/            # Suspicious hidden directory
```

---

## 🛡️ Attack Scenarios

### Scenario 1: Persistence Mechanism

**Attack**: Malware creates hidden startup script

```bash
# Attacker creates hidden autostart entry
mkdir -p ~/.config/autostart/
cat > ~/.config/autostart/.evil_updater.desktop << EOF
[Desktop Entry]
Type=Application
Exec=/home/user/.local/bin/.backdoor
Hidden=true
NoDisplay=true
X-GNOME-Autostart-enabled=true
EOF

# Script remains hidden from casual inspection
ls ~/.config/autostart/  # Doesn't show .evil_updater.desktop
```

**Detection**: ByteBastion scans autostart directories

```
Found: ~/.config/autostart/.evil_updater.desktop
Score: 10/12 (Critical)
Reason: Hidden autostart entry with executable
```

### Scenario 2: Data Exfiltration

**Attack**: Malware hides stolen data in hidden directory

```bash
# Create hidden directory
mkdir ~/.cache/.firefox_backup  # Looks legitimate

# Copy sensitive data
cp ~/.ssh/id_rsa ~/.cache/.firefox_backup/.key
cp ~/Documents/passwords.txt ~/.cache/.firefox_backup/.data

# Exfiltrate later via cron job
(crontab -l; echo "0 3 * * * /tmp/.upload_data.sh") | crontab -
```

**Detection**: Heuristic analysis flags unusual hidden directories

```
Found: ~/.cache/.firefox_backup/.key
Score: 9/12 (Highly suspicious)
Reason: 
  - Hidden file in hidden directory
  - Recently created
  - Unusual location for SSH key
```

### Scenario 3: Rootkit Concealment

**Attack**: Kernel rootkit hides files from ls/find

```c
// Kernel module hook example (simplified)
int fake_getdents(unsigned int fd, struct linux_dirent *dirp, unsigned int count) {
    int ret = real_getdents(fd, dirp, count);
    
    // Remove entries starting with .evil from directory listing
    struct linux_dirent *d;
    for (d = dirp; d < dirp + ret; ) {
        if (strncmp(d->d_name, ".evil", 5) == 0) {
            // Skip this entry (hide from user)
            memmove(d, d + d->d_reclen, ret - (d - dirp));
            ret -= d->d_reclen;
        } else {
            d += d->d_reclen;
        }
    }
    return ret;
}
```

**Detection**: Direct disk scanning bypasses kernel hooks

```python
# ByteBastion reads disk directly (forensic mode)
import os

def forensic_scan(partition):
    """Scan disk directly, bypassing kernel filters"""
    with open(partition, 'rb') as disk:
        # Read raw disk sectors
        # Parse file system structures manually
        # Detect hidden files kernel is concealing
        pass
```

---

## 🔧 Advanced Detection

### 1. Alternate Data Streams (NTFS)

Windows NTFS allows hidden data in streams:

```cmd
# Create file with hidden stream
echo "visible content" > file.txt
echo "secret data" > file.txt:hidden_stream

# Main file appears normal
type file.txt
# Output: visible content

# Hidden stream not visible
dir
# Output: file.txt (size appears as main stream only)

# Access hidden stream
more < file.txt:hidden_stream
# Output: secret data
```

**Detection**:
```python
import os

def find_ads_windows(file_path):
    """Find Alternate Data Streams on Windows"""
    try:
        # Use PowerShell to enumerate streams
        import subprocess
        result = subprocess.run(
            ['powershell', '-Command', f'Get-Item "{file_path}" -Stream *'],
            capture_output=True, text=True
        )
        
        streams = result.stdout.split('\n')
        # Filter out default :$DATA stream
        hidden_streams = [s for s in streams if ':$DATA' not in s and s.strip()]
        
        if hidden_streams:
            print(f"⚠ Hidden streams found in {file_path}:")
            for stream in hidden_streams:
                print(f"  {stream}")
    except:
        pass
```

### 2. Steganography Detection

Data hidden inside image files:

```python
from PIL import Image
import numpy as np

def detect_steganography(image_path):
    """Detect LSB steganography in images"""
    img = Image.open(image_path)
    pixels = np.array(img)
    
    # Extract Least Significant Bits
    lsb_data = pixels & 1
    
    # Calculate entropy (randomness)
    from scipy.stats import entropy
    lsb_entropy = entropy(lsb_data.flatten())
    
    # High entropy suggests hidden data
    if lsb_entropy > 0.95:
        return True, "High LSB entropy suggests steganography"
    
    return False, "No steganography detected"
```

### 3. Process Hollowing Detection

Malware injecting into legitimate processes:

```python
import psutil

def detect_process_hollowing():
    """Detect suspicious process memory regions"""
    for proc in psutil.process_iter(['pid', 'name', 'memory_maps']):
        try:
            for mmap in proc.memory_maps():
                # Detect executable memory not backed by file
                if 'rwx' in mmap.perms and not mmap.path:
                    print(f"⚠ Suspicious memory in {proc.name()} (PID {proc.pid})")
                    print(f"  Address: {mmap.addr}, Permissions: {mmap.perms}")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
```

---

## 🐛 Troubleshooting

### Issue: Too many false positives

**Cause**: Legitimate hidden config files flagged

**Solution**: Whitelist common directories
```python
WHITELIST = [
    '~/.config/',
    '~/.local/share/',
    '~/.cache/',
    '~/.mozilla/',
    '~/.ssh/',
]

def is_whitelisted(path):
    return any(path.startswith(os.path.expanduser(wl)) for wl in WHITELIST)
```

### Issue: Missing rootkit-hidden files

**Cause**: Kernel-level hiding bypasses user-space detection

**Solution**: Use forensic tools
```bash
# Use chkrootkit
sudo chkrootkit

# Use rkhunter
sudo rkhunter --check

# Mount filesystem externally (live USB)
sudo mount /dev/sda1 /mnt
ls -la /mnt/home/user/  # Rootkit can't hide when OS isn't running
```

---

## 📚 Further Reading

- [Rootkit Detection Techniques](https://www.sans.org/reading-room/whitepapers/malicious/detecting-rootkits-33458)
- [NTFS Alternate Data Streams](https://docs.microsoft.com/en-us/windows/win32/fileio/file-streams)
- [Steganography Detection](https://medium.com/@codeblue_79/steganography-detection-using-deep-learning-b5e22e9b8e5)

---

## 🔗 Related Tools

- [[File-Integrity-Checker]] - Verify hidden files haven't been modified
- [[Directory-Sync-Monitor]] - Monitor for new hidden file creation
- [[File-Type-Identifier]] - Verify hidden files aren't disguised malware

---

**Developer**: Sai Srujan Murthy | **Contact**: saisrujanmurthy@gmail.com
