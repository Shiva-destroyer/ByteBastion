# Educational Keylogger

## ⚠️ CRITICAL LEGAL WARNING

**STOP AND READ THIS FIRST**

The **Educational Keylogger** is designed **EXCLUSIVELY** for:
- ✅ Authorized security research in controlled environments
- ✅ Educational demonstrations with explicit consent
- ✅ Personal device monitoring (your own hardware only)
- ✅ Penetration testing with written authorization

### Legal Consequences of Misuse

Unauthorized keylogging is a **FEDERAL CRIME** in most jurisdictions:

**United States**:
- **Computer Fraud and Abuse Act (CFAA)** - 18 U.S.C. § 1030
  - Up to 10 years imprisonment
  - Fines up to $250,000
- **Electronic Communications Privacy Act (ECPA)** - 18 U.S.C. § 2510
  - Wiretapping charges
  - Civil liability for damages

**European Union**:
- **GDPR Article 6** - Unlawful processing of personal data
  - Fines up to €20 million or 4% of annual revenue
- **Member state criminal laws** - Vary by country

**United Kingdom**:
- **Computer Misuse Act 1990**
  - Up to 2 years imprisonment
- **Data Protection Act 2018**
  - Criminal and civil penalties

**Other Countries**: Similar laws exist globally (Canada - Criminal Code, Australia - Cybercrime Act, etc.)

**DO NOT USE THIS TOOL WITHOUT EXPLICIT AUTHORIZATION**

---

## 🔬 Technical Deep Dive

### How Keyloggers Work

Keyloggers operate by intercepting keyboard events at various levels of the system stack:

```
┌─────────────────────────────────────┐
│  Application Layer (e.g., Browser)  │  ← Application-level logging
├─────────────────────────────────────┤
│  Operating System (User Space)      │  ← User-space API hooks (pynput)
├─────────────────────────────────────┤
│  Kernel Space                        │  ← Kernel-level drivers
├─────────────────────────────────────┤
│  Hardware Layer (Keyboard)           │  ← Hardware keyloggers
└─────────────────────────────────────┘
```

ByteBastion's keylogger operates at the **User-space API level** using the `pynput` library.

---

## 🛠️ pynput Library Implementation

### Architecture

`pynput` uses platform-specific APIs:

**Linux**: X11 / XInput / evdev
```python
from Xlib import X, display
# Hooks into X Window System events
```

**Windows**: Win32 API
```python
import ctypes
from ctypes import wintypes
# Uses SetWindowsHookEx with WH_KEYBOARD_LL
```

**macOS**: Quartz Event Services
```python
from Quartz import CGEventTapCreate
# Hooks into Core Graphics event stream
```

### Event Hook Mechanism

```python
from pynput import keyboard

def on_press(key):
    """Callback triggered on key press"""
    try:
        # Handle character keys
        char = key.char
        log_key(char)
    except AttributeError:
        # Handle special keys (Enter, Shift, etc.)
        log_key(f'[{key.name}]')

# Create listener with callback
listener = keyboard.Listener(on_press=on_press)
listener.start()  # Non-blocking
listener.join()   # Block until stopped
```

### Key Event Types

1. **on_press**: Triggered when key is pressed down
2. **on_release**: Triggered when key is released
3. **on_click**: (Mouse) Triggered on mouse button events

---

## 📖 Usage Guide

### Starting the Keylogger

```bash
# Launch ByteBastion
./run.sh

# Select option 2 (Educational Keylogger)
# Choose option 1 (Start keylogger)
```

**Important**: The keylogger runs in the foreground and displays captured keys in real-time.

### Stopping the Keylogger

Press **Escape** key to gracefully stop logging.

```
Output:
[+] Keylogger started. Press ESC to stop...
h e l l o [space] w o r l d [enter]
[ESC]
[!] Keylogger stopped.
```

### Log File Format

Captured keystrokes are saved to `keylog.txt`:

```
2025-12-31 10:30:15 - h
2025-12-31 10:30:16 - e
2025-12-31 10:30:17 - l
2025-12-31 10:30:17 - l
2025-12-31 10:30:18 - o
2025-12-31 10:30:19 - [space]
2025-12-31 10:30:20 - w
2025-12-31 10:30:21 - o
2025-12-31 10:30:22 - r
2025-12-31 10:30:23 - l
2025-12-31 10:30:24 - d
2025-12-31 10:30:25 - [enter]
```

---

## 🔍 Detection & Prevention

### How to Detect Keyloggers

#### 1. Process Monitoring

```bash
# Linux: Check for suspicious processes
ps aux | grep -i key
lsof | grep -i keyboard

# Windows: Task Manager or PowerShell
Get-Process | Where-Object {$_.Name -like "*key*"}
```

#### 2. Network Traffic Analysis

Advanced keyloggers exfiltrate data over network:

```bash
# Monitor outbound connections
netstat -an | grep ESTABLISHED
tcpdump -i eth0 -n
```

#### 3. File System Monitoring

Watch for log files:

```bash
# Linux: inotify watches
inotifywait -m -r /home/user/ -e create -e modify

# Look for hidden log files
find / -name "*keylog*" 2>/dev/null
find / -name ".*log" 2>/dev/null
```

### Protection Strategies

#### 1. Use Virtual Keyboards

On-screen keyboards bypass hardware/software keyloggers:

**Linux**: `onboard`, `florence`
**Windows**: Windows On-Screen Keyboard
**macOS**: Accessibility Keyboard

#### 2. Two-Factor Authentication (2FA)

Even if password is captured, 2FA prevents unauthorized access.

#### 3. Regular Security Scans

```bash
# Linux: rkhunter, chkrootkit
sudo rkhunter --check
sudo chkrootkit

# Windows: Windows Defender, Malwarebytes
```

#### 4. Physical Security

Hardware keyloggers require physical access:
- Inspect USB ports for unknown devices
- Check PS/2 keyboard connector for inline devices
- Secure physical access to workstations

---

## 🧪 Ethical Use Cases

### 1. Parental Monitoring (Legal Requirements)

**United States**: Legal to monitor minor children's devices you own

**Requirements**:
- Device must be owned by parent/guardian
- Child must be under 18 (varies by state)
- Cannot violate wiretapping laws in two-party consent states

**Best Practice**: Inform children of monitoring (transparency builds trust)

### 2. Employee Monitoring (with Disclosure)

**Legal Requirements**:
- Written notice to employees
- Company-owned devices only
- Compliance with labor laws
- Privacy policy disclosure

**Example Policy**:
```
NOTICE: Computer systems provided by [Company Name] may be
monitored for security and productivity purposes. By using
these systems, you consent to such monitoring.
```

### 3. Security Research

**Authorized Scenarios**:
- Analyzing malware behavior in sandboxed environment
- Testing anti-keylogger software effectiveness
- Demonstrating attack vectors in security training

**Requirements**:
- Isolated lab environment
- No production systems
- Documented research purpose

### 4. Forensic Investigation

**Law Enforcement**:
- Requires court warrant
- Chain of custody documentation
- Admissible evidence procedures

**Corporate Investigation**:
- Written authorization from management
- Legal counsel review
- HR involvement

---

## 🛡️ Security & Privacy

### ByteBastion Keylogger Safeguards

1. **Local Storage Only**: Logs saved to local file, never transmitted
2. **User Consent**: Explicit disclaimer before execution
3. **Visible Operation**: Runs in foreground, not hidden
4. **Easy Termination**: ESC key immediately stops logging
5. **No Stealth Features**: No rootkit, no persistence mechanisms

### Responsible Disclosure

If you discover vulnerabilities in keylogging defenses:

1. **DO NOT** exploit vulnerabilities on systems you don't own
2. Follow responsible disclosure guidelines (90-day disclosure window)
3. Report to vendor security teams first
4. Provide proof-of-concept (not weaponized exploits)

---

## 🔧 Advanced Topics

### Bypassing Detection

**Educational Theory Only** - Understanding attacker techniques improves defense

#### Technique 1: Process Hiding

```python
# Rename process to innocuous name
import sys
sys.argv[0] = 'system_daemon'

# Linux: Hide from ps
import setproctitle
setproctitle.setproctitle('kernel_worker')
```

**Defense**: Monitor by PID, not name. Use `lsof` to check file handles.

#### Technique 2: Memory-Only Operation

```python
# Don't write to disk (RAM only)
log_buffer = []  # Store in memory
# Exfiltrate periodically via network
```

**Defense**: Memory forensics tools (Volatility, Rekall)

#### Technique 3: Kernel-Level Hooking

Low-level hooks bypass user-space monitoring:

```c
// Linux Kernel Module (LKM) example
#include <linux/input.h>
#include <linux/keyboard.h>

int keyboard_notifier(struct notifier_block *nb, unsigned long action, void *data) {
    struct keyboard_notifier_param *param = data;
    if (action == KBD_KEYSYM && param->down)
        log_key(param->value);
    return NOTIFY_OK;
}
```

**Defense**: Kernel integrity checking (IMA/EVM, Secure Boot)

---

## 🐛 Troubleshooting

### Issue: "Permission denied" on Linux

**Cause**: X11 display access restricted

**Solution**:
```bash
# Allow local connections (temporary)
xhost +local:

# Or run as user who owns display
sudo -u $USER ./run.sh
```

### Issue: Keylogger captures nothing

**Cause**: Wrong keyboard input method

**Solution**:
```bash
# Check if pynput detects your keyboard
python3 -c "from pynput import keyboard; keyboard.Listener(on_press=lambda k: print(k)).start()"

# If no output, try:
# - Check X11 vs Wayland (Wayland has restrictions)
# - Verify input device permissions
ls -l /dev/input/event*
```

### Issue: Special keys not logged correctly

**Cause**: Key mappings differ by keyboard layout

**Solution**:
```python
# Enhance key detection
from pynput.keyboard import Key

special_keys = {
    Key.enter: '[ENTER]',
    Key.tab: '[TAB]',
    Key.space: '[SPACE]',
    Key.backspace: '[BACKSPACE]',
    Key.shift: '[SHIFT]',
    Key.ctrl: '[CTRL]',
    Key.alt: '[ALT]',
}
```

---

## 📚 Further Reading

- [CFAA Full Text](https://www.law.cornell.edu/uscode/text/18/1030)
- [ECPA Legal Guide](https://www.justice.gov/jm/criminal-resource-manual-1050-synopsis-electronic-surveillance-laws)
- [pynput Documentation](https://pynput.readthedocs.io/)
- [OWASP Input Validation](https://owasp.org/www-community/controls/Input_Validation)

---

## 🔗 Related Tools

- [[Hidden-File-Detector]] - Discover hidden keylogger log files
- [[Directory-Sync-Monitor]] - Monitor for suspicious file creation
- [[File-Integrity-Checker]] - Verify system files haven't been modified by malware

---

**Developer**: Sai Srujan Murthy | **Contact**: saisrujanmurthy@gmail.com
