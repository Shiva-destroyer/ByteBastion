# File Integrity Checker

## Overview

The **File Integrity Checker** uses **SHA-256 cryptographic hashing** to verify file authenticity and detect unauthorized modifications. This tool is essential for security auditing, forensic analysis, and ensuring data integrity.

---

## 🔬 SHA-256 Hashing Algorithm

### What is SHA-256?

**SHA-256** (Secure Hash Algorithm 256-bit) is a cryptographic hash function that produces a unique 256-bit (32-byte) fingerprint for any input data. It is part of the SHA-2 family designed by the NSA.

### Key Properties

1. **Deterministic**: Same input always produces same hash
2. **Fast Computation**: Efficient to compute hash for any input
3. **Avalanche Effect**: Small input change completely changes output
4. **One-Way Function**: Computationally infeasible to reverse
5. **Collision Resistant**: Near-impossible to find two inputs with same hash

### Mathematical Representation

```
H: {0,1}* → {0,1}^256
Where H is the hash function mapping arbitrary length input to 256-bit output
```

### Hash Format

A SHA-256 hash is 64 hexadecimal characters:
```
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

Each hex character represents 4 bits (64 chars × 4 = 256 bits).

---

## 🛠️ Technical Implementation

### Hashing Process

```python
import hashlib

def calculate_hash(file_path):
    """Calculate SHA-256 hash of a file"""
    sha256_hash = hashlib.sha256()
    
    # Read file in chunks to handle large files
    with open(file_path, 'rb') as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    
    return sha256_hash.hexdigest()
```

### Why Chunk Reading?

Large files (GB+) cannot fit in RAM. Chunk reading:
- Processes file in 4KB blocks
- Updates hash progressively
- Memory-efficient for files of any size

---

## 📖 Usage Guide

### Adding Files to Database

```bash
# Launch ByteBastion
./run.sh

# Select option 1 (File Integrity Checker)
# Choose option 1 (Add file to database)
# Enter file path: /path/to/important_file.pdf
```

The tool will:
1. Calculate SHA-256 hash of the file
2. Store hash in `integrity_database.json`
3. Display confirmation with hash value

### Verifying File Integrity

```bash
# Select option 2 (Verify file integrity)
# Enter file path: /path/to/important_file.pdf
```

**Possible Outcomes:**

✅ **Match**: File is authentic and unmodified
```
Status: ✓ VERIFIED
Current Hash:  a1b2c3d4...
Stored Hash:   a1b2c3d4...
Result: File integrity verified successfully
```

❌ **Mismatch**: File has been modified
```
Status: ⚠ MODIFIED
Current Hash:  x9y8z7w6...
Stored Hash:   a1b2c3d4...
Result: WARNING - File has been modified!
```

⚠️ **Not Found**: File not in database
```
Status: File not found in database
Action: Add file to database first
```

---

## 🔍 Use Cases

### 1. Software Distribution Verification

**Scenario**: Download Ubuntu ISO from mirror

```bash
# Official hash from ubuntu.com
Expected: 45a8e8a6e5c8e4f2b7c9d3a1f6e2b4c8...

# Calculate downloaded file hash
./run.sh → File Integrity Checker → Add file
File: ubuntu-22.04-desktop-amd64.iso
Hash:  45a8e8a6e5c8e4f2b7c9d3a1f6e2b4c8...

Result: ✓ Hashes match - download is authentic
```

### 2. Detecting Ransomware Modifications

**Scenario**: Monitor critical system files

```bash
# Before attack
Add to database: /etc/passwd
Hash: 5f4dcc3b5aa765d61d8327deb882cf99...

# After attack (verify)
Verify: /etc/passwd
Current Hash:  9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d...
Stored Hash:   5f4dcc3b5aa765d61d8327deb882cf99...

Result: ⚠ FILE MODIFIED - Possible ransomware activity!
```

### 3. Forensic Evidence Chain of Custody

Document evidence integrity in legal investigations:

```
Timeline:
09:00 - Evidence collected: stolen_data.zip
        Hash: c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6...

14:30 - Pre-analysis verification
        Hash: c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6... ✓

16:45 - Post-analysis verification
        Hash: c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6... ✓

Conclusion: Evidence integrity maintained throughout analysis
```

---

## 🧮 Collision Probability

### How Secure is SHA-256?

**Number of possible hashes**: 2^256 ≈ 1.16 × 10^77

**Comparison**:
- Atoms in observable universe: ~10^80
- SHA-256 hash space: ~10^77

**Birthday Paradox Attack**:
- To find a collision with 50% probability
- Need to hash ~2^128 files
- At 1 billion hashes/second: **10^22 years**

**Conclusion**: SHA-256 collisions are astronomically improbable for practical purposes.

---

## 🛡️ Security Best Practices

### 1. Store Hashes Securely

❌ **Bad**: Store database on same system as files
```
/var/important_files/
├── document.pdf
└── integrity_database.json  ← Attacker can modify this too!
```

✅ **Good**: Store database on separate, secured system
```
Protected Server:
└── integrity_database.json

File Server:
└── /var/important_files/document.pdf
```

### 2. Use Read-Only Storage for Reference Hashes

Store trusted hashes on write-once media:
- CD-R/DVD-R
- WORM (Write Once Read Many) drives
- Blockchain (for distributed verification)

### 3. Automate Regular Verification

```bash
#!/bin/bash
# cron job: 0 2 * * * /path/to/verify_critical_files.sh

CRITICAL_FILES=(
    "/etc/passwd"
    "/etc/shadow"
    "/boot/vmlinuz"
)

for file in "${CRITICAL_FILES[@]}"; do
    python3 -c "from modules.file_checker import FileIntegrityChecker; \
                checker = FileIntegrityChecker(); \
                checker.verify_file('$file')" || \
    echo "ALERT: $file modified!" | mail -s "Security Alert" admin@example.com
done
```

---

## 🔧 Advanced Features

### Database Structure

```json
{
    "/path/to/file1.txt": {
        "hash": "a1b2c3d4e5f6...",
        "size": 1024,
        "added": "2025-12-31T10:30:00",
        "algorithm": "SHA-256"
    },
    "/path/to/file2.pdf": {
        "hash": "f6e5d4c3b2a1...",
        "size": 524288,
        "added": "2025-12-31T11:45:00",
        "algorithm": "SHA-256"
    }
}
```

### Listing All Monitored Files

```bash
# Select option 3 (List all monitored files)
```

Output:
```
╭───────────────────────────────────────────────────────╮
│            Monitored Files Database                    │
├───────────────────────────────────────────────────────┤
│ 1. /home/user/document.pdf                            │
│    Hash: a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6...          │
│                                                        │
│ 2. /etc/passwd                                        │
│    Hash: 5f4dcc3b5aa765d61d8327deb882cf99...          │
│                                                        │
│ Total: 2 files monitored                              │
╰───────────────────────────────────────────────────────╯
```

---

## 🐛 Troubleshooting

### Issue: "Permission denied"

**Cause**: Insufficient permissions to read file

**Solution**:
```bash
# Run with sudo (use cautiously)
sudo ./run.sh

# Or change file permissions
chmod +r /path/to/file
```

### Issue: "File not found in database"

**Cause**: File hasn't been added to integrity database

**Solution**:
```bash
# Add file first (option 1)
# Then verify (option 2)
```

### Issue: Hash mismatch on unchanged file

**Possible Causes**:
1. File system timestamps causing metadata changes
2. Opened file was auto-saved by editor
3. Symbolic links pointing to different targets
4. Cloud sync modifying file metadata

**Verification**:
```bash
# Check file modification time
ls -l /path/to/file

# Recalculate hash manually
sha256sum /path/to/file
```

---

## 📚 Further Reading

- [NIST SHA-2 Specification (FIPS 180-4)](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf)
- [SHA-256 Implementation Guide](https://en.wikipedia.org/wiki/SHA-2)
- [Tripwire: Commercial Integrity Checker](https://www.tripwire.com/)
- [AIDE: Advanced Intrusion Detection Environment](https://aide.github.io/)

---

## 🔗 Related Tools

- [[AES-Encryption]] - Protect files with encryption after verifying integrity
- [[Data-Deletion-Utility]] - Securely delete files that fail integrity checks
- [[Hidden-File-Detector]] - Find unauthorized hidden files that bypass monitoring

---

**Developer**: Sai Srujan Murthy | **Contact**: saisrujanmurthy@gmail.com
