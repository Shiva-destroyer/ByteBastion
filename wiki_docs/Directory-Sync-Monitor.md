# Directory Sync Monitor

## Overview

The **Directory Sync Monitor** provides real-time file system monitoring using the `watchdog` library. It detects file creation, modification, deletion, and movement events instantly, making it ideal for security monitoring and backup synchronization.

---

## 🔬 Event-Driven Architecture

### Traditional vs Event-Driven Monitoring

**Traditional Polling**:
```python
# ❌ Inefficient approach
while True:
    current_state = scan_directory()
    if current_state != previous_state:
        detect_changes()
    time.sleep(5)  # Check every 5 seconds

Problems:
- High CPU usage (constant scanning)
- Delayed detection (5-second intervals)
- Misses rapid changes
```

**Event-Driven (watchdog)**:
```python
# ✅ Efficient approach
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        print(f"File created: {event.src_path}")

observer = Observer()
observer.schedule(MyHandler(), "/path/to/watch", recursive=True)
observer.start()  # Non-blocking, event-driven

Benefits:
- Low CPU usage (OS notifies changes)
- Instant detection (0-ms latency)
- Captures all events
```

---

## 🛠️ watchdog Library

### Platform-Specific Implementations

`watchdog` uses native OS APIs for efficient monitoring:

**Linux**: `inotify`
```python
# Kernel-level file system notifications
import inotify.adapters
i = inotify.adapters.Inotify()
i.add_watch('/path/to/watch')
# Receives events: IN_CREATE, IN_MODIFY, IN_DELETE, IN_MOVE
```

**macOS**: `FSEvents`
```python
# File System Events API
from fsevents import Observer
# Monitors directory changes at kernel level
```

**Windows**: `ReadDirectoryChangesW`
```python
# Win32 API directory monitoring
import win32file
# Receives notifications: FILE_NOTIFY_CHANGE_*
```

### Event Types

| Event Type | Description | Example |
|------------|-------------|---------|
| **created** | New file/directory created | `touch newfile.txt` |
| **modified** | File content or metadata changed | `echo "data" >> file.txt` |
| **deleted** | File/directory removed | `rm file.txt` |
| **moved** | File/directory renamed or moved | `mv file.txt newname.txt` |

### Event Object Structure

```python
class FileSystemEvent:
    event_type:  str   # 'created', 'modified', 'deleted', 'moved'
    src_path:    str   # Full path to affected file
    is_directory: bool # True if directory, False if file
    
class FileMovedEvent(FileSystemEvent):
    dest_path: str     # Destination path (for move events)
```

---

## 📖 Usage Guide

### Starting Directory Monitor

```bash
# Launch ByteBastion
./run.sh

# Select option 7 (Directory Sync Monitor)
# Enter directory to monitor: /home/user/Documents
# Monitor recursively? (y/n): y
```

**Output**:
```
╭─────────────────────────────────────────────────────────╮
│            Directory Sync Monitor Active                │
├─────────────────────────────────────────────────────────┤
│ Watching: /home/user/Documents                          │
│ Recursive: Yes (includes subdirectories)                │
│                                                         │
│ Press Ctrl+C to stop monitoring...                      │
╰─────────────────────────────────────────────────────────╯

[2025-12-31 10:30:15] ✓ Created:  /home/user/Documents/report.txt
[2025-12-31 10:30:22] ✎ Modified: /home/user/Documents/report.txt
[2025-12-31 10:31:05] ➜ Moved:    /home/user/Documents/report.txt
                                   → /home/user/Documents/final_report.txt
[2025-12-31 10:31:30] ✗ Deleted:  /home/user/Documents/draft.txt
[2025-12-31 10:32:10] ✓ Created:  /home/user/Documents/subfolder/
```

---

## 🔍 Use Cases

### 1. Ransomware Detection

**Scenario**: Detect mass file encryption by ransomware

```python
from collections import Counter
from datetime import datetime, timedelta

class RansomwareDetector(FileSystemEventHandler):
    def __init__(self):
        self.recent_modifications = []
    
    def on_modified(self, event):
        now = datetime.now()
        self.recent_modifications.append(now)
        
        # Remove events older than 60 seconds
        self.recent_modifications = [
            t for t in self.recent_modifications 
            if now - t < timedelta(seconds=60)
        ]
        
        # Alert if > 100 files modified in 60 seconds
        if len(self.recent_modifications) > 100:
            alert("⚠ RANSOMWARE ALERT: Mass file modifications detected!")
            # Immediately disconnect from network
            os.system("nmcli networking off")
```

### 2. Automated Backup Trigger

**Scenario**: Sync critical directory to backup when changes occur

```python
import shutil

class BackupTrigger(FileSystemEventHandler):
    def __init__(self, source, backup):
        self.source = source
        self.backup = backup
    
    def on_modified(self, event):
        # Delay 5 seconds (debounce rapid changes)
        time.sleep(5)
        
        # Incremental backup
        relative_path = event.src_path.replace(self.source, '')
        dest = self.backup + relative_path
        
        if not event.is_directory:
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.copy2(event.src_path, dest)
            print(f"✓ Backed up: {relative_path}")

# Usage
handler = BackupTrigger("/home/user/critical", "/backup/critical")
observer.schedule(handler, "/home/user/critical", recursive=True)
```

### 3. Intrusion Detection

**Scenario**: Monitor system directories for unauthorized changes

```python
class IntrusionDetector(FileSystemEventHandler):
    PROTECTED_DIRS = [
        "/etc/passwd",
        "/etc/shadow",
        "/etc/sudoers",
        "/boot/",
        "/usr/bin/"
    ]
    
    def on_any_event(self, event):
        for protected in self.PROTECTED_DIRS:
            if event.src_path.startswith(protected):
                alert(f"⚠ SECURITY ALERT: {event.event_type} on {event.src_path}")
                log_to_siem(event)
                send_email_alert(event)
                
# Requires root to monitor system directories
observer.schedule(IntrusionDetector(), "/etc", recursive=True)
observer.schedule(IntrusionDetector(), "/boot", recursive=True)
```

### 4. Developer Hot-Reload

**Scenario**: Auto-restart application when code changes

```python
import subprocess
import signal

class HotReload(FileSystemEventHandler):
    def __init__(self, command):
        self.command = command
        self.process = None
        self.restart()
    
    def restart(self):
        if self.process:
            self.process.send_signal(signal.SIGTERM)
        self.process = subprocess.Popen(self.command.split())
        print("✓ Application restarted")
    
    def on_modified(self, event):
        if event.src_path.endswith('.py'):
            print(f"✎ Code changed: {event.src_path}")
            self.restart()

# Usage: Auto-restart Flask app on code changes
handler = HotReload("python3 app.py")
observer.schedule(handler, "./src", recursive=True)
```

---

## 🔧 Advanced Features

### Filtering Events

```python
class FilteredHandler(FileSystemEventHandler):
    def __init__(self, extensions):
        self.extensions = extensions
    
    def on_modified(self, event):
        # Only monitor specific file types
        if any(event.src_path.endswith(ext) for ext in self.extensions):
            print(f"Tracked file modified: {event.src_path}")

# Monitor only Python files
handler = FilteredHandler(['.py', '.pyx'])
```

### Event Debouncing

**Problem**: Text editors trigger multiple events per save

```
[10:30:15.001] Modified: file.txt
[10:30:15.012] Modified: file.txt
[10:30:15.023] Modified: file.txt  ← 3 events for 1 save!
```

**Solution**: Debounce events

```python
from threading import Timer

class DebouncedHandler(FileSystemEventHandler):
    def __init__(self, delay=1.0):
        self.delay = delay
        self.timers = {}
    
    def on_modified(self, event):
        # Cancel previous timer for this file
        if event.src_path in self.timers:
            self.timers[event.src_path].cancel()
        
        # Set new timer
        timer = Timer(self.delay, self.process_event, [event])
        self.timers[event.src_path] = timer
        timer.start()
    
    def process_event(self, event):
        print(f"File modified (debounced): {event.src_path}")
        del self.timers[event.src_path]
```

### Recursive vs Non-Recursive

```python
# Non-recursive: Only watch immediate directory
observer.schedule(handler, "/path/to/dir", recursive=False)
# Monitors: /path/to/dir/file.txt
# Ignores:  /path/to/dir/subdir/file.txt

# Recursive: Watch all subdirectories
observer.schedule(handler, "/path/to/dir", recursive=True)
# Monitors: /path/to/dir/file.txt
# Monitors: /path/to/dir/subdir/file.txt
# Monitors: /path/to/dir/subdir/subdir2/file.txt
```

---

## 🛡️ Security Considerations

### 1. Monitor Sensitive Directories

```bash
# High-value targets for monitoring
/etc/          # System configuration
/var/log/      # Log files (detect tampering)
/home/user/.ssh/  # SSH keys
/boot/         # Bootloader (rootkit detection)
~/.config/     # Application configs
```

### 2. Avoid Monitoring Temp Directories

```bash
# High-churn directories waste resources
/tmp/
/var/tmp/
/var/cache/
~/.cache/

# Exclude these from monitoring
```

### 3. Audit Trail

```python
import json
from datetime import datetime

class AuditLogger(FileSystemEventHandler):
    def __init__(self, log_file):
        self.log_file = log_file
    
    def log_event(self, event):
        entry = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event.event_type,
            'path': event.src_path,
            'is_directory': event.is_directory,
            'user': os.getlogin(),
            'pid': os.getpid()
        }
        
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(entry) + '\n')
    
    def on_any_event(self, event):
        self.log_event(event)
```

---

## 🐛 Troubleshooting

### Issue: "No module named 'watchdog'"

**Solution**:
```bash
pip install watchdog
```

### Issue: Too many events (high CPU usage)

**Causes**:
- Monitoring high-churn directory (`/tmp/`, `/var/log/`)
- No event filtering

**Solutions**:
```python
# 1. Add debouncing
# 2. Filter file types
# 3. Exclude high-churn directories
```

### Issue: Events not detected

**Possible Causes**:
1. Insufficient permissions
2. Network file systems (NFS, SMB) don't support inotify
3. Reached inotify watch limit (Linux)

**Solutions**:
```bash
# Check inotify limit
cat /proc/sys/fs/inotify/max_user_watches
# Output: 8192 (default)

# Increase limit
echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

---

## 📚 Further Reading

- [watchdog Documentation](https://python-watchdog.readthedocs.io/)
- [Linux inotify Manual](https://man7.org/linux/man-pages/man7/inotify.7.html)
- [macOS FSEvents](https://developer.apple.com/documentation/coreservices/file_system_events)
- [Windows ReadDirectoryChangesW](https://docs.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-readdirectorychangesw)

---

## 🔗 Related Tools

- [[File-Integrity-Checker]] - Verify modified files haven't been tampered with
- [[Hidden-File-Detector]] - Scan for newly created hidden files
- [[Temporary-File-Cleaner]] - Auto-clean detected temporary files

---

**Developer**: Sai Srujan Murthy | **Contact**: saisrujanmurthy@gmail.com
