# Disk Space Analyzer

## Overview

The **Disk Space Analyzer** provides comprehensive storage analysis using the `psutil` library. It reports disk usage per partition with color-coded warnings for critical thresholds.

---

## 🔬 Storage Analysis Fundamentals

### File System Hierarchy

```
┌─────────────────────────────────────────┐
│  Partition (/dev/sda1)                  │
├─────────────────────────────────────────┤
│  ├─ Total Size: 500 GB                  │
│  ├─ Used: 350 GB (70%)                  │
│  ├─ Free: 150 GB (30%)                  │
│  └─ Mountpoint: /                       │
└─────────────────────────────────────────┘
```

### Key Metrics

**Total Space**: Physical capacity of partition  
**Used Space**: Data currently stored  
**Free Space**: Available for new data  
**Usage Percentage**: (Used / Total) × 100

**Danger Thresholds**:
```
 0-75%:  Safe (green)
75-90%:  Warning (yellow) - Monitor closely
90-95%:  Critical (orange) - Take action soon
95-100%: Emergency (red) - Immediate action required
```

---

## 🛠️ psutil Library

### Platform-Independent Disk APIs

`psutil` provides cross-platform disk information:

**Linux**: Reads `/proc/partitions` and uses `statvfs` syscall  
**Windows**: Uses `GetDiskFreeSpaceEx` Win32 API  
**macOS**: Uses `statfs` syscall

### Implementation

```python
import psutil

def get_disk_info():
    """Get all disk partitions and usage"""
    partitions = psutil.disk_partitions()
    
    disk_info = []
    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            
            disk_info.append({
                'device': partition.device,
                'mountpoint': partition.mountpoint,
                'fstype': partition.fstype,
                'total': usage.total,        # bytes
                'used': usage.used,          # bytes
                'free': usage.free,          # bytes
                'percent': usage.percent     # percentage
            })
        except PermissionError:
            # Skip inaccessible partitions
            continue
    
    return disk_info

# Example output:
# [
#   {
#     'device': '/dev/sda1',
#     'mountpoint': '/',
#     'fstype': 'ext4',
#     'total': 500000000000,    # 500 GB
#     'used': 350000000000,     # 350 GB
#     'free': 150000000000,     # 150 GB
#     'percent': 70.0
#   }
# ]
```

---

## 📖 Usage Guide

### Analyzing Disk Space

```bash
# Launch ByteBastion
./run.sh

# Select option 10 (Disk Space Analyzer with Alerts)
# Scan all partitions? (y/n): y
```

**Output**:
```
╭─────────────────────────────────────────────────────────╮
│              Disk Space Analysis Report                 │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ 🟢 Partition: / (Root)                                 │
│    Device:    /dev/sda1                                 │
│    Type:      ext4                                      │
│    Total:     500.0 GB                                  │
│    Used:      350.0 GB (70%)                            │
│    Free:      150.0 GB (30%)                            │
│    Status:    ✓ HEALTHY                                 │
│                                                         │
│    [▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░] 70%                          │
│                                                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ 🟡 Partition: /home                                    │
│    Device:    /dev/sda2                                 │
│    Type:      ext4                                      │
│    Total:     1.0 TB                                    │
│    Used:      850.0 GB (85%)                            │
│    Free:      150.0 GB (15%)                            │
│    Status:    ⚠ WARNING - Running low on space         │
│                                                         │
│    [▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░] 85%                          │
│                                                         │
│    Recommendations:                                     │
│    • Run [[Temporary-File-Cleaner]] to free space      │
│    • Move old files to external storage                 │
│    • Review large directories with du -sh /*            │
│                                                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ 🔴 Partition: /var                                     │
│    Device:    /dev/sda3                                 │
│    Type:      ext4                                      │
│    Total:     50.0 GB                                   │
│    Used:      48.5 GB (97%)                             │
│    Free:      1.5 GB (3%)                               │
│    Status:    🚨 CRITICAL - Immediate action required   │
│                                                         │
│    [▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓] 97%                          │
│                                                         │
│    URGENT Actions:                                      │
│    • Delete old log files: journalctl --vacuum-size=1G │
│    • Clear package cache: apt clean                     │
│    • Remove unused packages: apt autoremove             │
│    • Check largest files: du -ah /var | sort -rh | head│
│                                                         │
╰─────────────────────────────────────────────────────────╯

Summary:
--------
Total Disks: 3
🟢 Healthy: 1
🟡 Warning: 1
🔴 Critical: 1

Overall System Storage: 1.53 TB total, 1.25 TB used (81%)
```

---

## 🔍 Finding Large Files

### Directory Space Analysis

```python
import os

def analyze_directory(path):
    """Find largest directories and files"""
    dir_sizes = {}
    
    for root, dirs, files in os.walk(path):
        total_size = 0
        
        for file in files:
            try:
                file_path = os.path.join(root, file)
                total_size += os.path.getsize(file_path)
            except (OSError, PermissionError):
                continue
        
        dir_sizes[root] = total_size
    
    # Sort by size (largest first)
    sorted_dirs = sorted(dir_sizes.items(), key=lambda x: x[1], reverse=True)
    
    return sorted_dirs[:20]  # Top 20 largest directories

# Example output:
# [
#   ('/home/user/.cache', 15000000000),     # 15 GB
#   ('/var/log', 5000000000),               # 5 GB
#   ('/home/user/Videos', 3000000000),      # 3 GB
# ]
```

### Largest Files

```bash
# Linux/macOS command-line
find /home/user -type f -exec du -h {} + | sort -rh | head -20

# Output:
# 5.0G    /home/user/Videos/movie.mp4
# 2.5G    /home/user/.cache/chrome/cache.db
# 1.2G    /home/user/VirtualBox/Ubuntu.vdi
```

### Duplicate File Detection

```python
import hashlib
from collections import defaultdict

def find_duplicates(directory):
    """Find duplicate files by hash"""
    hashes = defaultdict(list)
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            
            try:
                # Calculate file hash
                with open(file_path, 'rb') as f:
                    file_hash = hashlib.md5(f.read()).hexdigest()
                
                hashes[file_hash].append(file_path)
            except (OSError, PermissionError):
                continue
    
    # Find hashes with multiple files (duplicates)
    duplicates = {h: paths for h, paths in hashes.items() if len(paths) > 1}
    
    return duplicates

# Example output:
# {
#   'a1b2c3d4...': [
#       '/home/user/Documents/photo.jpg',
#       '/home/user/Backup/photo.jpg',  # Same file, duplicate!
#   ]
# }
```

---

## 🛡️ Storage Management Best Practices

### 1. Maintain 20% Free Space

**Why**: File system performance degrades when > 80% full

```
< 80% full:  Normal performance
80-90%:      Slight slowdown (fragmentation increases)
90-95%:      Noticeable slowdown
> 95%:       Severe performance issues
100%:        System instability (logs can't write, updates fail)
```

### 2. Regular Cleanup Routine

```bash
#!/bin/bash
# Weekly cleanup script

# 1. Package manager cache
sudo apt clean                  # Debian/Ubuntu
sudo yum clean all              # RedHat/CentOS
brew cleanup                    # macOS

# 2. Old log files
sudo journalctl --vacuum-time=7d  # Keep last 7 days
sudo find /var/log -name "*.log.*" -mtime +30 -delete

# 3. Temporary files
sudo find /tmp -type f -atime +7 -delete
sudo find /var/tmp -type f -atime +30 -delete

# 4. Thumbnail cache
rm -rf ~/.cache/thumbnails/*

# 5. Browser cache
rm -rf ~/.cache/google-chrome/Default/Cache/*
rm -rf ~/.mozilla/firefox/*.default/cache2/*
```

### 3. Monitor Growth Trends

```python
import json
from datetime import datetime

def log_disk_usage(log_file='/var/log/disk_usage.json'):
    """Log disk usage over time for trend analysis"""
    usage = psutil.disk_usage('/')
    
    entry = {
        'timestamp': datetime.now().isoformat(),
        'total_gb': usage.total / (1024**3),
        'used_gb': usage.used / (1024**3),
        'free_gb': usage.free / (1024**3),
        'percent': usage.percent
    }
    
    with open(log_file, 'a') as f:
        f.write(json.dumps(entry) + '\n')

# Run daily via cron:
# 0 0 * * * python3 /path/to/script.py
```

**Analyze trends**:
```python
import pandas as pd
import matplotlib.pyplot as plt

# Load log
df = pd.read_json('/var/log/disk_usage.json', lines=True)
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Plot usage over time
plt.plot(df['timestamp'], df['percent'])
plt.xlabel('Date')
plt.ylabel('Disk Usage (%)')
plt.title('Disk Usage Trend')
plt.axhline(y=90, color='r', linestyle='--', label='Critical threshold')
plt.legend()
plt.show()
```

### 4. Set Up Alerts

```python
import subprocess

def check_and_alert():
    """Send alert if disk usage exceeds threshold"""
    usage = psutil.disk_usage('/')
    
    if usage.percent > 90:
        # Send email
        subprocess.run([
            'mail',
            '-s', 'DISK SPACE ALERT',
            'admin@example.com'
        ], input=f'Disk usage at {usage.percent}%!'.encode())
        
        # Send desktop notification
        subprocess.run([
            'notify-send',
            'Disk Space Alert',
            f'Partition / is {usage.percent}% full!'
        ])
```

---

## 🔧 Platform-Specific Considerations

### Linux: Inode Exhaustion

**Problem**: Out of inodes (file metadata) even with free space

```bash
# Check inode usage
df -i

# Output:
# Filesystem     Inodes  IUsed  IFree IUse% Mounted on
# /dev/sda1      3276800 3276800  0   100%  /

# Each file consumes 1 inode, even if file is empty!
```

**Solution**: Delete unnecessary files or recreate filesystem with more inodes

### Windows: Disk Compression

```powershell
# Enable NTFS compression to save space
Compact /C /S:C:\CompressMe

# Check compression ratio
Compact /Q C:\CompressMe
```

### macOS: APFS Snapshots

**Issue**: Time Machine snapshots consume space

```bash
# List snapshots
tmutil listlocalsnapshots /

# Delete specific snapshot
tmutil deletelocalsnapshots 2025-12-31-103015

# Disable local snapshots
sudo tmutil disablelocal
```

---

## 🐛 Troubleshooting

### Issue: "Disk full" but df shows free space

**Cause 1**: Reserved blocks (Linux)
```bash
# Check reserved space (default 5% for root)
tune2fs -l /dev/sda1 | grep "Reserved block count"

# Reduce reserved space to 1%
sudo tune2fs -m 1 /dev/sda1
```

**Cause 2**: Open deleted files
```bash
# Process holding deleted file open
lsof | grep deleted

# Restart process to release space
sudo systemctl restart apache2
```

### Issue: Disk usage doesn't match file sizes

**Cause**: Sparse files or filesystem overhead

```bash
# Check actual disk usage vs apparent size
du -sh /path/  # Disk usage
ls -lh /path/  # Apparent size

# Sparse file example:
# Apparent size: 10 GB
# Actual disk usage: 100 MB (holes in file)
```

---

## 📚 Further Reading

- [psutil Documentation](https://psutil.readthedocs.io/)
- [Linux File Systems Explained](https://www.kernel.org/doc/html/latest/filesystems/index.html)
- [Disk Space Management Best Practices](https://www.redhat.com/sysadmin/disk-space-management)

---

## 🔗 Related Tools

- [[Temporary-File-Cleaner]] - Free disk space by removing temp files
- [[Data-Deletion-Utility]] - Securely delete large unnecessary files
- [[Directory-Sync-Monitor]] - Monitor directories for rapid growth

---

**Developer**: Sai Srujan Murthy | **Contact**: saisrujanmurthy@gmail.com
