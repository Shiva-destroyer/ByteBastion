# Temporary File Cleaner

## Overview

The **Temporary File Cleaner** safely identifies and removes temporary files based on age, pattern matching, and safety checks. It helps reclaim disk space while avoiding deletion of important files.

---

## 🔬 What Are Temporary Files?

### Common Temporary File Locations

**Linux/macOS**:
```
/tmp/                    # System-wide temp (cleared on reboot)
/var/tmp/                # Persistent temp (survives reboot)
~/.cache/                # User application caches
~/.local/share/Trash/    # User trash/recycle bin
/var/log/                # Rotated log files
```

**Windows**:
```
C:\Windows\Temp\         # System temp
C:\Users\<user>\AppData\Local\Temp\  # User temp
%TEMP%                   # Environment variable
Recycle Bin              # Deleted files
```

### Temporary File Patterns

Common file extensions and patterns:
```
*.tmp                    # Generic temp files
*.temp                   # Alternate temp extension
*.bak                    # Backup files
*.cache                  # Cache files
*.log                    # Log files
*.old                    # Old versions
~*                       # Editor backup files (vim, emacs)
.~lock.*                 # LibreOffice lock files
core.*                   # Core dumps
*.swp                    # Vim swap files
thumbs.db                # Windows thumbnail cache
.DS_Store                # macOS folder metadata
```

---

## 🛠️ Safe Deletion Strategy

### Age-Based Filtering

**Problem**: Some temp files are actively in use

```
File: /tmp/firefox_profile.tmp
Age:  5 minutes (ACTIVE - don't delete!)

File: /tmp/old_installer.tmp
Age:  90 days (SAFE to delete)
```

**Solution**: Only delete files older than threshold (default: 7 days)

```python
import os
import time

def is_old_enough(file_path, days_threshold=7):
    """Check if file is older than threshold"""
    file_mtime = os.path.getmtime(file_path)  # Last modified time
    age_seconds = time.time() - file_mtime
    age_days = age_seconds / 86400  # Convert to days
    
    return age_days > days_threshold
```

### Safety Checks

**1. Whitelist Protected Directories**
```python
PROTECTED_DIRS = [
    "/home/",
    "/root/",
    "/etc/",
    "/usr/",
    "/bin/",
    "/sbin/",
    "/boot/",
    "/dev/",
    "/sys/",
    "/proc/"
]

def is_safe_location(path):
    """Only allow cleanup in designated temp directories"""
    SAFE_DIRS = ["/tmp/", "/var/tmp/", "~/.cache/"]
    return any(path.startswith(safe) for safe in SAFE_DIRS)
```

**2. Ignore Active Files**
```python
import fcntl

def is_file_locked(file_path):
    """Check if file is currently in use"""
    try:
        with open(file_path, 'r') as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)
            return False  # Not locked
    except IOError:
        return True  # File is locked (in use)
```

**3. Dry-Run Mode**
```python
def clean_temp_files(directory, age_days=7, dry_run=True):
    """
    Scan and optionally delete temp files
    
    Args:
        directory: Path to scan
        age_days: Minimum age in days
        dry_run: If True, only list files (don't delete)
    """
    files_to_delete = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file)
            
            if is_old_enough(path, age_days) and not is_file_locked(path):
                files_to_delete.append(path)
    
    if dry_run:
        print(f"Would delete {len(files_to_delete)} files:")
        for f in files_to_delete:
            print(f"  {f}")
    else:
        for f in files_to_delete:
            os.remove(f)
            print(f"Deleted: {f}")
    
    return files_to_delete
```

---

## 📖 Usage Guide

### Cleaning Temporary Files

```bash
# Launch ByteBastion
./run.sh

# Select option 8 (Temporary File Cleaner)
# Choose scan directory:
#   1. System temp (/tmp)
#   2. User cache (~/.cache)
#   3. Custom directory
# Minimum age (days): 7
# Dry run (preview only)? (y/n): y
```

**Output (Dry Run)**:
```
╭─────────────────────────────────────────────────────────╮
│          Temporary File Cleaner (Dry Run)              │
├─────────────────────────────────────────────────────────┤
│ Scanning: /home/user/.cache                             │
│ Age threshold: 7 days                                   │
│                                                         │
│ Files identified for deletion:                          │
│                                                         │
│  1. /home/user/.cache/chrome/cache_data.bin            │
│     Age: 45 days | Size: 125 MB                        │
│                                                         │
│  2. /home/user/.cache/thumbnails/large/abc123.png      │
│     Age: 90 days | Size: 2.3 MB                        │
│                                                         │
│  3. /home/user/.cache/pip/http/cache.db                │
│     Age: 120 days | Size: 50 MB                        │
│                                                         │
│ Total: 3 files, 177.3 MB                               │
│                                                         │
│ ⚠ This is a dry run - no files deleted                 │
│ Run again without dry-run to delete                     │
╰─────────────────────────────────────────────────────────╯
```

**Output (Actual Deletion)**:
```
╭─────────────────────────────────────────────────────────╮
│          Temporary File Cleaner (Active)                │
├─────────────────────────────────────────────────────────┤
│ Deleting old temporary files...                         │
│                                                         │
│ [▓▓▓▓▓▓▓▓▓▓] 1/3 ✓ Deleted: cache_data.bin             │
│ [▓▓▓▓▓▓▓▓▓▓] 2/3 ✓ Deleted: abc123.png                 │
│ [▓▓▓▓▓▓▓▓▓▓] 3/3 ✓ Deleted: cache.db                   │
│                                                         │
│ ✓ Cleanup complete                                      │
│ Deleted: 3 files                                        │
│ Space reclaimed: 177.3 MB                               │
╰─────────────────────────────────────────────────────────╯
```

---

## 🔍 Advanced Cleanup Strategies

### 1. Intelligent Cache Management

```python
class CacheManager:
    def __init__(self, cache_dir, max_size_gb=5):
        self.cache_dir = cache_dir
        self.max_size_gb = max_size_gb
    
    def get_total_size(self):
        """Calculate total cache size in GB"""
        total = 0
        for root, dirs, files in os.walk(self.cache_dir):
            total += sum(os.path.getsize(os.path.join(root, f)) for f in files)
        return total / (1024**3)  # Convert to GB
    
    def cleanup_if_needed(self):
        """Delete oldest caches if size exceeds limit"""
        current_size = self.get_total_size()
        
        if current_size > self.max_size_gb:
            print(f"Cache size ({current_size:.2f} GB) exceeds limit ({self.max_size_gb} GB)")
            
            # Get all files sorted by age
            files = []
            for root, dirs, filenames in os.walk(self.cache_dir):
                for f in filenames:
                    path = os.path.join(root, f)
                    mtime = os.path.getmtime(path)
                    size = os.path.getsize(path)
                    files.append((mtime, path, size))
            
            # Sort by age (oldest first)
            files.sort()
            
            # Delete oldest files until under limit
            for mtime, path, size in files:
                os.remove(path)
                current_size -= size / (1024**3)
                print(f"Deleted: {path}")
                
                if current_size <= self.max_size_gb:
                    break
```

### 2. Log Rotation Management

```python
def cleanup_rotated_logs(log_dir, keep_count=5):
    """Keep only N most recent log files"""
    import glob
    
    log_patterns = ['*.log', '*.log.*', '*.log.gz']
    
    for pattern in log_patterns:
        logs = glob.glob(os.path.join(log_dir, pattern))
        # Sort by modification time (newest first)
        logs.sort(key=os.path.getmtime, reverse=True)
        
        # Delete logs beyond keep_count
        for log in logs[keep_count:]:
            os.remove(log)
            print(f"Deleted old log: {log}")
```

### 3. Browser Cache Cleanup

```python
def clean_browser_caches(age_days=30):
    """Clean browser caches across multiple browsers"""
    browsers = {
        'Chrome': '~/.cache/google-chrome/Default/Cache/',
        'Firefox': '~/.cache/mozilla/firefox/*.default/cache2/',
        'Chromium': '~/.cache/chromium/Default/Cache/'
    }
    
    for browser, cache_path in browsers.items():
        expanded_path = os.path.expanduser(cache_path)
        if os.path.exists(expanded_path):
            print(f"Cleaning {browser} cache...")
            clean_temp_files(expanded_path, age_days)
```

---

## 🛡️ Safety Guidelines

### What NOT to Delete

**System Files**:
```
❌ /var/run/         # Runtime system state
❌ /var/lock/        # Lock files for active processes
❌ /proc/            # Virtual file system (kernel)
❌ /sys/             # Virtual file system (devices)
```

**Active Application Files**:
```
❌ Database temp files during backup
❌ Compiler intermediate files during build
❌ Video editor temp files during render
```

**User Data Disguised as Temp**:
```
❌ ~/Downloads/*.tmp (could be incomplete download)
❌ ~/.config/*.bak (could be only backup of config)
```

### Pre-Deletion Checklist

✅ **1. Verify file age** (default: 7+ days old)  
✅ **2. Check file locks** (not currently open)  
✅ **3. Confirm location** (in designated temp dir)  
✅ **4. Run dry-run first** (preview before delete)  
✅ **5. Exclude system files** (check against whitelist)  

---

## 🧹 Automation

### Cron Job (Linux/macOS)

```bash
# Add to crontab
crontab -e

# Clean temp files daily at 2 AM
0 2 * * * cd /path/to/ByteBastion && ./run.sh --clean-temp --age 7 --auto

# Or use system cleanup
0 2 * * * /usr/bin/find /tmp -type f -atime +7 -delete
```

### Systemd Timer (Linux)

```ini
# /etc/systemd/system/temp-cleaner.service
[Unit]
Description=ByteBastion Temp File Cleaner

[Service]
Type=oneshot
ExecStart=/usr/bin/python3 /path/to/ByteBastion/src/modules/temp_cleaner.py

# /etc/systemd/system/temp-cleaner.timer
[Unit]
Description=Run temp cleaner daily

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
```

Activate:
```bash
sudo systemctl enable temp-cleaner.timer
sudo systemctl start temp-cleaner.timer
```

---

## 🐛 Troubleshooting

### Issue: "Permission denied"

**Cause**: Insufficient permissions to delete files

**Solution**:
```bash
# Option 1: Run as user who owns files
sudo -u username ./run.sh

# Option 2: Change permissions (use cautiously)
chmod -R u+w /tmp/target_dir
```

### Issue: Disk space not reclaimed

**Cause**: Files open by running processes

**Solution**:
```bash
# Find processes with deleted files still open
lsof | grep deleted

# Example output:
# chrome 1234 user 50r /tmp/deleted_file.tmp (deleted)

# Kill process or restart to reclaim space
kill 1234
```

### Issue: Important files deleted

**Prevention**:
1. **Always run dry-run first**
2. Use conservative age threshold (30+ days)
3. Exclude directories with important data

**Recovery**:
```bash
# Some file systems support undeletion
extundelete /dev/sda1 --restore-file /tmp/important.tmp

# Or restore from backup
```

---

## 📚 Further Reading

- [Linux Filesystem Hierarchy](https://www.pathname.com/fhs/)
- [Tmpfs and Temp File Management](https://www.kernel.org/doc/Documentation/filesystems/tmpfs.txt)
- [BleachBit: Open-Source Cleaner](https://www.bleachbit.org/)

---

## 🔗 Related Tools

- [[Disk-Space-Analyzer]] - Identify large temp files consuming space
- [[Hidden-File-Detector]] - Find hidden temp files
- [[Data-Deletion-Utility]] - Securely wipe sensitive temp files

---

**Developer**: Sai Srujan Murthy | **Contact**: saisrujanmurthy@gmail.com
