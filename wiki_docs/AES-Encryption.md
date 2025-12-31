# AES Encryption

## Overview

The **AES Encryption** module provides military-grade file encryption using **AES-256-CBC** (Advanced Encryption Standard with 256-bit keys in Cipher Block Chaining mode). It uses **PBKDF2-HMAC-SHA256** for key derivation from passwords.

---

## 🔬 AES Algorithm

### What is AES?

**AES (Advanced Encryption Standard)** is a symmetric encryption algorithm adopted by the U.S. government in 2001 (FIPS 197). It replaced DES and is now the global standard for data encryption.

**Key Properties**:
- **Symmetric**: Same key encrypts and decrypts
- **Block cipher**: Processes data in 128-bit blocks
- **Key sizes**: 128, 192, or 256 bits (ByteBastion uses 256-bit)
- **Speed**: Hardware-accelerated on modern CPUs (AES-NI instruction set)

### AES-256 Security

**Brute Force Resistance**:
```
Key space: 2^256 = 1.16 × 10^77 possible keys
Atoms in universe: ~10^80

At 1 trillion keys/second:
Time to crack: 3.67 × 10^51 years
(Age of universe: 1.38 × 10^10 years)

Conclusion: AES-256 is unbreakable by brute force with current technology
```

**NSA Classification**: AES-256 approved for TOP SECRET documents

---

## 🔐 Cipher Block Chaining (CBC)

### Why Block Chaining?

**Problem with ECB** (Electronic Codebook):
```
Plaintext:  [Block1] [Block2] [Block1] [Block2]
Encrypted:  [Enc1]   [Enc2]   [Enc1]   [Enc2]
                ↑                 ↑
         Same plaintext = Same ciphertext (patterns visible!)
```

**Solution: CBC Mode**:
```
Block1: Encrypt(Plaintext1 ⊕ IV)
Block2: Encrypt(Plaintext2 ⊕ Ciphertext1)
Block3: Encrypt(Plaintext3 ⊕ Ciphertext2)
...

Result: Same plaintext encrypts differently (due to chaining)
```

### Initialization Vector (IV)

**IV**: 128-bit random value that initializes CBC chaining

**Properties**:
- Must be **unpredictable** (cryptographically random)
- Must be **unique** per encryption (never reuse with same key)
- Not secret (stored with ciphertext)

**Generation**:
```python
import os

iv = os.urandom(16)  # 16 bytes = 128 bits
```

---

## 🔑 Key Derivation (PBKDF2-HMAC-SHA256)

### Why Not Use Password Directly?

**Problem**: User passwords are weak and variable-length

```
Password: "hello123"
Not suitable for AES-256 (needs exactly 256 bits = 32 bytes)
```

**Solution**: Key Derivation Function (KDF)

### PBKDF2 Algorithm

**PBKDF2** (Password-Based Key Derivation Function 2) strengthens passwords through iterative hashing.

**Formula**:
```
Key = PBKDF2(password, salt, iterations, key_length)
    = Hash(Hash(Hash(...Hash(password + salt)...)))
    ↑
    Repeated 'iterations' times
```

**Parameters**:
```python
password:   User-provided password (any length)
salt:       16-byte random value (prevents rainbow tables)
iterations: 100,000+ (makes brute force slower)
key_length: 32 bytes (256 bits for AES-256)
hash:       SHA-256
```

### Implementation

```python
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os

def derive_key(password: str, salt: bytes) -> bytes:
    """Derive 256-bit encryption key from password"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,              # 256 bits
        salt=salt,
        iterations=100_000,     # OWASP recommendation
    )
    key = kdf.derive(password.encode())
    return key

# Generate random salt
salt = os.urandom(16)
key = derive_key("MyPassword123!", salt)
# key is now 32 bytes, suitable for AES-256
```

---

## 📖 Usage Guide

### Encrypting a File

```bash
# Launch ByteBastion
./run.sh

# Select option 6 (AES Encryption/Decryption)
# Choose option 1 (Encrypt file)
# Enter file path: /path/to/secret.txt
# Enter password: ************
# Confirm password: ************
```

**Output**:
```
╭─────────────────────────────────────────────────────────╮
│                 AES-256 File Encryption                 │
├─────────────────────────────────────────────────────────┤
│ Original File:  secret.txt                              │
│ Encrypted File: secret.txt.enc                          │
│ Algorithm:      AES-256-CBC                             │
│ Key Derivation: PBKDF2-HMAC-SHA256 (100,000 iterations)│
│ Original Size:  1,048,576 bytes                         │
│ Encrypted Size: 1,048,592 bytes (16-byte padding)       │
│                                                         │
│ ✓ File encrypted successfully                          │
│                                                         │
│ ⚠ IMPORTANT:                                            │
│ • Keep your password secure                             │
│ • Losing password = permanent data loss                 │
│ • Store .enc file safely                                │
╰─────────────────────────────────────────────────────────╯
```

### Decrypting a File

```bash
# Select option 2 (Decrypt file)
# Enter file path: /path/to/secret.txt.enc
# Enter password: ************
```

**Correct Password**:
```
╭─────────────────────────────────────────────────────────╮
│                 AES-256 File Decryption                 │
├─────────────────────────────────────────────────────────┤
│ Encrypted File: secret.txt.enc                          │
│ Decrypted File: secret.txt                              │
│ Size:           1,048,576 bytes                         │
│                                                         │
│ ✓ File decrypted successfully                          │
╰─────────────────────────────────────────────────────────╯
```

**Wrong Password**:
```
╭─────────────────────────────────────────────────────────╮
│                    Decryption Failed                    │
├─────────────────────────────────────────────────────────┤
│ ✗ Invalid password or corrupted file                    │
│                                                         │
│ Possible causes:                                        │
│ • Incorrect password                                    │
│ • File corrupted during storage/transfer                │
│ • Wrong .enc file                                       │
│                                                         │
│ No data recovered                                       │
╰─────────────────────────────────────────────────────────╯
```

---

## 🔧 Encrypted File Structure

### File Format

ByteBastion's `.enc` files have this structure:

```
╔═══════════════════════════════════════════════════════╗
║  [Salt: 16 bytes]                                     ║  ← Key derivation
║  [IV: 16 bytes]                                       ║  ← CBC initialization
║  [Encrypted Data: variable length]                    ║  ← Actual ciphertext
║  [Padding: 0-15 bytes]                                ║  ← PKCS7 padding
╚═══════════════════════════════════════════════════════╝
```

**Size Overhead**: 32 bytes (salt + IV) + up to 15 bytes (padding)

### Why Store Salt and IV?

**Salt**: Required to derive key from password (unique per file)
**IV**: Required for CBC decryption (unique per encryption)

**Security**: Salt and IV are not secret (attackers are assumed to have them)

---

## 🛡️ Security Best Practices

### 1. Use Strong Passwords

```
❌ Weak:   "password123"
   Entropy: ~40 bits (minutes to crack)

✅ Strong: "correct-horse-battery-staple-giraffe-mountain"
   Entropy: ~77 bits (millions of years to crack)
```

See [[Secure-Password-Generator]] for password creation guidance.

### 2. Store Encrypted Files Securely

```
✅ Good Storage:
- Encrypted external drive (defense-in-depth)
- Cloud storage with 2FA (Google Drive, Dropbox)
- Offline USB in safe location

❌ Bad Storage:
- Same computer as plaintext version
- Unencrypted cloud storage without 2FA
- Sent via email (no encryption in transit)
```

### 3. Verify Integrity After Encryption

```bash
# Calculate hash of encrypted file
sha256sum secret.txt.enc > checksum.txt

# After transfer/storage, verify
sha256sum -c checksum.txt
# Output: secret.txt.enc: OK ✓
```

Use [[File-Integrity-Checker]] to monitor encrypted files.

### 4. Secure Key Management

**Option 1**: Use hardware security module (HSM)
```bash
# Example: YubiKey
ykman oath add "MyEncryptionPassword"
ykman oath code "MyEncryptionPassword"
```

**Option 2**: Split key across multiple parties (Shamir's Secret Sharing)
```python
# Require 3 out of 5 key holders to decrypt
from secretsharing import PlaintextToHexSecretSharer

key = "MyEncryptionPassword"
shares = PlaintextToHexSecretSharer.split_secret(key, 3, 5)
# Distribute shares to 5 different people
# Any 3 can reconstruct key
```

---

## 🧪 Attack Scenarios

### Scenario 1: Brute Force Attack

**Attacker**: Has encrypted file, tries all passwords

```
Weak Password: "password"
Keyspace: 26^8 = 208 billion
PBKDF2 (100K iterations): 208 billion × 100,000 = 2.08 × 10^16 hashes
GPU (1B hashes/sec): 2.08 × 10^16 / 10^9 = 2.08 × 10^7 seconds = 240 days ❌

Strong Password: "correct-horse-battery-staple"
Keyspace: 2048^4 = 17 trillion (from 2048-word list)
PBKDF2: 1.76 × 10^18 hashes
GPU: 1.76 × 10^18 / 10^9 = 1.76 × 10^9 seconds = 55,000 years ✅
```

**Defense**: PBKDF2 iterations slow down brute force significantly

### Scenario 2: Known-Plaintext Attack

**Attacker**: Has both plaintext and ciphertext of same file

**AES-256 Resistance**: Known-plaintext attacks are ineffective against AES-256. Even knowing plaintext/ciphertext pairs, deriving the key is infeasible.

### Scenario 3: Chosen-Ciphertext Attack

**Attacker**: Can decrypt chosen ciphertexts (oracle access)

**CBC Padding Oracle**: Vulnerability if padding errors leak information

**ByteBastion Protection**: Uses proper exception handling (no padding oracle leakage)

---

## 🐛 Troubleshooting

### Issue: "Decryption failed - invalid password"

**Solutions**:
```bash
# 1. Verify password (common mistakes)
#    - Caps Lock enabled
#    - Typo in password
#    - Wrong password used

# 2. Check file corruption
sha256sum original.txt.enc
# Compare with known-good checksum

# 3. Verify file format
file secret.txt.enc
# Should show: data

# 4. Check file size
ls -l secret.txt.enc
# Should be > 32 bytes (salt + IV)
```

### Issue: Encrypted file larger than expected

**Cause**: PKCS7 padding adds 1-16 bytes

**Explanation**:
```
Original: 1000 bytes
Block size: 16 bytes
Padding needed: 16 - (1000 % 16) = 16 - 8 = 8 bytes
Encrypted: 32 (salt+IV) + 1000 + 8 = 1040 bytes
```

This is normal and expected.

---

## 📚 Further Reading

- [FIPS 197: AES Specification](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.197.pdf)
- [NIST SP 800-38A: CBC Mode](https://csrc.nist.gov/publications/detail/sp/800-38a/final)
- [RFC 2898: PBKDF2 Specification](https://tools.ietf.org/html/rfc2898)
- [Cryptography Library Documentation](https://cryptography.io/)

---

## 🔗 Related Tools

- [[Secure-Password-Generator]] - Generate strong encryption passwords
- [[File-Integrity-Checker]] - Verify encrypted files haven't been tampered with
- [[Data-Deletion-Utility]] - Securely delete plaintext after encryption

---

**Developer**: Sai Srujan Murthy | **Contact**: saisrujanmurthy@gmail.com
