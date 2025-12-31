# Data Deletion Utility

## Overview

The **Data Deletion Utility** securely erases files using the **DoD 5220.22-M standard**, making data recovery forensically infeasible. Unlike simple file deletion, this tool performs multiple overwrite passes to prevent data remnant recovery.

---

## 🔬 Why Standard Deletion is Insufficient

### How File Systems "Delete" Files

When you delete a file normally:

```
1. Operating system marks directory entry as "deleted"
2. Disk blocks are marked as "available"
3. File data remains on disk until overwritten

Result: File appears deleted, but data is fully recoverable
```

**Recovery Tools**: Recuva, PhotoRec, TestDisk can easily recover "deleted" files

---

## 🛠️ DoD 5220.22-M Standard

### Overview

**DoD 5220.22-M** is a data sanitization standard issued by the U.S. Department of Defense for clearing and sanitizing storage media.

**Standard**: DoD 5220.22-M, ECE (National Industrial Security Program Operating Manual)

### 3-Pass Overwrite Algorithm

**Pass 1**: Write zeros (`0x00`) to all sectors
```
Original data: 01101011 10110101 11010011
After Pass 1:  00000000 00000000 00000000
```

**Pass 2**: Write ones (`0xFF`) to all sectors
```
After Pass 1:  00000000 00000000 00000000
After Pass 2:  11111111 11111111 11111111
```

**Pass 3**: Write random data to all sectors
```
After Pass 2:  11111111 11111111 11111111
After Pass 3:  10010110 01101001 11100010 (random)
```

**Final Step**: Verify overwrites and unlink file

### Why 3 Passes?

**Theory**: Magnetic storage retains "ghost" data from previous writes. Multiple passes overwrite magnetic domains to eliminate data remnants.

**Modern Reality**:
- SSDs: 1 pass sufficient (wear leveling makes multi-pass unnecessary)
- HDDs: 1 pass is likely sufficient with modern drives
- Paranoid security: 3-7 passes provides psychological assurance

---

## 📖 Usage Guide

### Securely Deleting a File

```bash
# Launch ByteBastion
./run.sh

# Select option 5 (Data Deletion Utility)
# Enter file path: /path/to/sensitive_file.txt
# Confirm deletion: yes
```

**Output**:
```
╭─────────────────────────────────────────────────────────╮
│           Secure File Deletion (DoD 5220.22-M)         │
├─────────────────────────────────────────────────────────┤
│ File: sensitive_file.txt                                │
│ Size: 1,048,576 bytes                                   │
│                                                         │
│ [▓▓▓▓▓▓▓▓▓▓] Pass 1/3: Writing zeros... 100%           │
│ [▓▓▓▓▓▓▓▓▓▓] Pass 2/3: Writing ones... 100%            │
│ [▓▓▓▓▓▓▓▓▓▓] Pass 3/3: Writing random... 100%          │
│ [✓] Verifying overwrites... Complete                   │
│ [✓] Unlinking file... Complete                         │
│                                                         │
│ ✓ File securely deleted (3 passes completed)           │
│                                                         │
│ Data recovery is forensically infeasible               │
╰─────────────────────────────────────────────────────────╯
```

---

## 🔍 Technical Implementation

### Overwrite Algorithm

```python
import os
import secrets

def secure_delete_dod(file_path):
    """Securely delete file using DoD 5220.22-M standard"""
    
    # Get file size
    file_size = os.path.getsize(file_path)
    
    with open(file_path, 'rb+') as f:
        # Pass 1: Write zeros
        f.seek(0)
        f.write(b'\x00' * file_size)
        f.flush()
        os.fsync(f.fileno())  # Force write to disk
        
        # Pass 2: Write ones
        f.seek(0)
        f.write(b'\xFF' * file_size)
        f.flush()
        os.fsync(f.fileno())
        
        # Pass 3: Write random data
        f.seek(0)
        f.write(secrets.token_bytes(file_size))
        f.flush()
        os.fsync(f.fileno())
    
    # Unlink file (remove from file system)
    os.remove(file_path)
```

### Key Implementation Details

**1. `os.fsync()`**: Forces OS to write buffered data to physical disk
```python
f.flush()              # Flush Python buffer to OS
os.fsync(f.fileno())   # Force OS to write to disk
```

**2. Chunk Processing** (for large files):
```python
CHUNK_SIZE = 4096  # 4KB chunks

def secure_delete_chunked(file_path):
    file_size = os.path.getsize(file_path)
    
    with open(file_path, 'rb+') as f:
        for pass_num in range(3):
            f.seek(0)
            bytes_written = 0
            
            while bytes_written < file_size:
                chunk_size = min(CHUNK_SIZE, file_size - bytes_written)
                
                if pass_num == 0:
                    f.write(b'\x00' * chunk_size)
                elif pass_num == 1:
                    f.write(b'\xFF' * chunk_size)
                else:
                    f.write(secrets.token_bytes(chunk_size))
                
                bytes_written += chunk_size
            
            f.flush()
            os.fsync(f.fileno())
    
    os.remove(file_path)
```

---

## 🔒 SSD Considerations

### Why SSDs Are Different

**HDDs** (Hard Disk Drives):
- Data written to specific physical sectors
- Overwriting same sector replaces data
- Multi-pass overwriting effective

**SSDs** (Solid State Drives):
- Use **wear leveling** to distribute writes evenly
- Writing to "same" location may write to different physical cells
- Overwritten data may remain in unmapped cells

### SSD-Specific Deletion

**TRIM Command**: Marks blocks as deleted, allowing SSD to erase internally
```bash
# Linux: Enable TRIM
sudo fstrim -v /

# Automatic TRIM (add to fstab)
/dev/sda1  /  ext4  defaults,discard  0  1
```

**ATA Secure Erase**: Hardware-level full-drive erase
```bash
# Check if supported
hdparm -I /dev/sda | grep "Erase"

# Execute secure erase (DESTRUCTIVE!)
hdparm --user-master u --security-set-pass password /dev/sda
hdparm --user-master u --security-erase password /dev/sda
```

**Recommendation**: For SSDs, 1-pass overwrite + TRIM is sufficient

---

## 🛡️ Security Considerations

### 1. Encrypted Volumes

If file is on encrypted volume (LUKS, BitLocker, FileVault):

```
Original data: [sensitive content] (encrypted)
On-disk storage: [encrypted gibberish]
After deletion: [different encrypted gibberish]

Conclusion: Encryption already protects data remnants
Action: 1-pass overwrite or standard deletion sufficient
```

### 2. File System Journaling

**Issue**: Journaling file systems (ext4, NTFS) may log file contents

```
File: /home/user/secret.txt
Journal: Copy of file metadata and possibly data blocks
```

**Mitigation**:
- Disable journaling for sensitive partitions
- Securely wipe free space to clear journal remnants

### 3. Backups

**Critical**: Secure deletion only affects current copy

```
File: sensitive.doc
Locations:
- ✓ Primary drive (securely deleted)
- ❌ Backup drive (still exists!)
- ❌ Cloud backup (still exists!)
- ❌ Previous USB transfer (still exists!)

Action: Trace and delete ALL copies
```

### 4. Swap/Hibernation Files

**Risk**: Sensitive data may be written to swap/hibernation

```
# Linux: Check swap
swapon --show

# Disable swap temporarily
sudo swapoff -a

# Securely delete swap partition
sudo dd if=/dev/urandom of=/dev/sda2 bs=1M

# Re-enable swap
sudo swapon -a
```

---

## 🧪 Forensic Recovery Attempts

### Scenario: Recovery After 3-Pass Overwrite

**Before Secure Deletion**:
```
Sector 12345: "SSN: 123-45-6789" (original data)
```

**After Pass 1** (zeros):
```
Sector 12345: 00 00 00 00 00 00 00 00 00
Magnetic trace: Faint remnants of original bits
```

**After Pass 2** (ones):
```
Sector 12345: FF FF FF FF FF FF FF FF FF
Magnetic trace: Previous zeros detectable via microscopy (theory)
```

**After Pass 3** (random):
```
Sector 12345: A7 3C D5 8B 2F E1 94 6A B2
Magnetic trace: No pattern, no remnants
```

**Forensic Analysis**:
- Visual inspection: Random data, no patterns
- Magnetic force microscopy: No detectable remnants
- Data carving: No file signatures found
- **Conclusion**: Recovery infeasible

---

## 🐛 Troubleshooting

### Issue: "Permission denied"

**Cause**: Insufficient permissions to overwrite file

**Solution**:
```bash
# Check file permissions
ls -l /path/to/file

# Add write permission
chmod u+w /path/to/file

# Or run as owner
sudo -u owner ./run.sh
```

### Issue: Deletion fails on SSD

**Cause**: SSD firmware preventing direct overwrites

**Solution**:
```bash
# Use native TRIM support
sudo fstrim -v /

# For whole-drive wipe, use ATA Secure Erase
```

### Issue: File still recoverable

**Possible Causes**:
1. Backup copies exist elsewhere
2. File system journaling preserved data
3. Swap file contains data
4. Cloud sync created copies

**Verification**:
```bash
# Search for file remnants
sudo grep -a "sensitive_string" /dev/sda

# Use forensic tools
foremost -i /dev/sda -o recovered/
photorec /dev/sda
```

---

## 📚 Further Reading

- [DoD 5220.22-M Standard (NISPOM)](https://www.dss.mil/is/odaa/)
- [NIST SP 800-88: Guidelines for Media Sanitization](https://csrc.nist.gov/publications/detail/sp/800-88/rev-1/final)
- [Gutmann Method (35-pass)](https://en.wikipedia.org/wiki/Gutmann_method)
- [Understanding SSD Wear Leveling](https://www.crucial.com/support/articles-faq-ssd/how-do-ssds-work)

---

## 🔗 Related Tools

- [[AES-Encryption]] - Encrypt files before deletion for defense-in-depth
- [[File-Integrity-Checker]] - Verify overwrites were successful
- [[Hidden-File-Detector]] - Find hidden copies of sensitive files

---

**Developer**: Sai Srujan Murthy | **Contact**: saisrujanmurthy@gmail.com
