# Secure Password Generator

## Overview

The **Secure Password Generator** creates cryptographically secure passwords using Python's `secrets` module. Unlike pseudo-random generators, `secrets` is designed specifically for security-critical applications like password generation.

---

## 🔬 Cryptographic Randomness

### secrets vs random

Python provides two randomness libraries with critical differences:

| Feature | `random` | `secrets` |
|---------|----------|-----------|
| **Algorithm** | Mersenne Twister (MT19937) | OS-provided CSPRNG |
| **Predictable** | ✅ Yes (deterministic) | ❌ No (truly random) |
| **Cryptographic** | ❌ Not secure | ✅ Cryptographically secure |
| **Seeding** | `random.seed(value)` | OS entropy pool |
| **Use Case** | Simulations, games | Passwords, tokens, keys |

### Why random is INSECURE for Passwords

```python
import random

# INSECURE: Mersenne Twister is predictable
random.seed(12345)
password1 = ''.join(random.choices('abc', k=10))
# Output: 'cbabcabcab'

random.seed(12345)
password2 = ''.join(random.choices('abc', k=10))
# Output: 'cbabcabcab' (SAME PASSWORD!)

# Attacker who observes a few outputs can predict future values
```

### Why secrets is SECURE

```python
import secrets

# SECURE: Uses OS-level entropy
password1 = ''.join(secrets.choice('abc') for _ in range(10))
# Output: 'bcaacbcbaa'

password2 = ''.join(secrets.choice('abc') for _ in range(10))
# Output: 'acbbccabac' (DIFFERENT - truly random)

# Each call reads from /dev/urandom (Linux) or CryptGenRandom (Windows)
```

**Entropy Sources**:
- Linux: `/dev/urandom` (kernel entropy pool)
- Windows: `CryptGenRandom()` (CSPRNG API)
- macOS: `getentropy()` (system call)

---

## 📊 Password Entropy

### What is Entropy?

**Entropy** measures password unpredictability in bits. Higher entropy = harder to crack.

**Formula**:
```
Entropy = log₂(charset_size^password_length)
        = password_length × log₂(charset_size)
```

### Character Set Sizes

| Character Set | Size | log₂(size) |
|---------------|------|------------|
| Digits (0-9) | 10 | 3.32 bits/char |
| Lowercase (a-z) | 26 | 4.70 bits/char |
| Uppercase (A-Z) | 26 | 4.70 bits/char |
| Letters (a-z, A-Z) | 52 | 5.70 bits/char |
| Alphanumeric (a-z, A-Z, 0-9) | 62 | 5.95 bits/char |
| Alphanumeric + Symbols | 94 | 6.55 bits/char |

### Entropy Examples

```python
# Example 1: 8-character lowercase password
Password: "abcdefgh"
Entropy:  8 × log₂(26) = 8 × 4.70 = 37.6 bits
Time to crack (1B attempts/sec): 0.14 seconds ❌

# Example 2: 12-character alphanumeric password
Password: "aB3dE5gH9jK2"
Entropy:  12 × log₂(62) = 12 × 5.95 = 71.4 bits
Time to crack (1B attempts/sec): 74 years ✅

# Example 3: 16-character full-symbol password
Password: "aB3#dE5@gH9!jK2%"
Entropy:  16 × log₂(94) = 16 × 6.55 = 104.8 bits
Time to crack (1B attempts/sec): 64 trillion years ✅✅✅
```

### Entropy Requirements by Use Case

| Use Case | Minimum Entropy | Example |
|----------|----------------|---------|
| **Weak** | < 28 bits | 6-digit PIN |
| **Fair** | 28-35 bits | 8-char lowercase |
| **Good** | 36-59 bits | 10-char alphanumeric |
| **Strong** | 60-79 bits | 12-char with symbols |
| **Very Strong** | 80-127 bits | 16-char with symbols |
| **Paranoid** | 128+ bits | 20+ char with symbols |

**NIST Recommendation**: Minimum 80 bits for sensitive systems

---

## 🛠️ Implementation

### Character Sets

```python
import string

lowercase = string.ascii_lowercase    # 'abcdefghijklmnopqrstuvwxyz'
uppercase = string.ascii_uppercase    # 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
digits = string.digits                # '0123456789'
symbols = string.punctuation          # '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'

# Combined charset (94 characters)
full_charset = lowercase + uppercase + digits + symbols
```

### Generation Algorithm

```python
import secrets
import string

def generate_password(length=16, use_uppercase=True, use_digits=True, use_symbols=True):
    """Generate cryptographically secure password"""
    
    # Build character set based on options
    charset = string.ascii_lowercase
    if use_uppercase:
        charset += string.ascii_uppercase
    if use_digits:
        charset += string.digits
    if use_symbols:
        charset += string.punctuation
    
    # Generate password
    password = ''.join(secrets.choice(charset) for _ in range(length))
    
    return password

# Calculate entropy
def calculate_entropy(length, charset_size):
    import math
    return length * math.log2(charset_size)
```

---

## 📖 Usage Guide

### Generating a Password

```bash
# Launch ByteBastion
./run.sh

# Select option 4 (Secure Password Generator)
# Follow prompts:

Password length (8-128): 16
Include uppercase letters? (y/n): y
Include digits? (y/n): y
Include symbols? (y/n): y
```

**Example Output**:
```
╭─────────────────────────────────────────────────────────╮
│             Generated Secure Password                   │
├─────────────────────────────────────────────────────────┤
│ Password: Kj9#mT2@pL5!wX8%                              │
│ Length:   16 characters                                 │
│ Entropy:  104.8 bits                                    │
│ Strength: Very Strong                                   │
│                                                         │
│ Estimated Time to Crack:                                │
│   1B attempts/sec:    641,180,000,000 years            │
│   1T attempts/sec:    641,180,000 years                │
╰─────────────────────────────────────────────────────────╯
```

---

## 🔍 Password Strength Guidelines

### Length vs Complexity

**Misconception**: Complexity > Length

**Reality**: Length is more important than complexity

```
# 8-char with all character types (entropy: 52.4 bits)
Password: aB3#dE5@
Time to crack: 142 days

# 16-char lowercase only (entropy: 75.2 bits)
Password: abcdefghijklmnop
Time to crack: 1.1 million years

Conclusion: Longer passwords win, even with simpler character sets
```

**Recommendation**: Prioritize length (16+ characters) over complexity

### Passphrases vs Random Passwords

**Random Password**: `Kj9#mT2@pL5!`
- **Pros**: High entropy, short
- **Cons**: Hard to remember, prone to weak storage (sticky notes)

**Passphrase**: `correct-horse-battery-staple`
- **Pros**: Easier to remember, high entropy if long
- **Cons**: Longer, may be in dictionaries

**xkcd 936 Analysis**:
```
Passphrase: "correct horse battery staple" (4 random common words)
Entropy: log₂(2048^4) = 44 bits (if from 2048-word list)

# Better: 6-word passphrase from 7776-word list (EFF wordlist)
Entropy: log₂(7776^6) = 77.5 bits
Example: "giraffe-envelope-stapler-mountain-velvet-keyboard"
```

---

## 🛡️ Best Practices

### 1. Unique Passwords Per Account

❌ **Bad**: Reusing passwords
```
Facebook: MyPassword123!
Gmail:    MyPassword123!
Bank:     MyPassword123!

Risk: One breach compromises all accounts
```

✅ **Good**: Unique passwords + password manager
```
Facebook: Kj9#mT2@pL5!wX8%
Gmail:    pQ4$nB7&fR2@hY9^
Bank:     zW6!cM3#vT8@dX1%

Solution: Use password manager (Bitwarden, KeePassXC)
```

### 2. Avoid Common Patterns

❌ **Predictable Patterns**:
- Sequential: `abc123`, `qwerty`
- Keyboard patterns: `1qaz2wsx`, `zxcvbnm`
- Substitutions: `P@ssw0rd`, `M!ch@3l`
- Personal info: `John1985`, `Fluffy2024`

✅ **True Randomness**:
- No patterns discernible
- Generated by cryptographic RNG

### 3. Password Storage

**Never Store Plain Text**:
```python
# ❌ NEVER DO THIS
with open('passwords.txt', 'w') as f:
    f.write(f"Gmail: {password}")
```

**Use Password Managers**:
```
✅ Recommended Managers:
- Bitwarden (open-source, audited)
- KeePassXC (offline, encrypted database)
- 1Password (commercial, well-audited)

Features:
- AES-256 encryption
- Zero-knowledge architecture
- PBKDF2/Argon2 key derivation
- Auto-fill (reduces phishing risk)
```

### 4. Enable Two-Factor Authentication (2FA)

Even strong passwords can be phished. 2FA adds a second layer:

```
Login = Password (something you know) + TOTP (something you have)

Example:
Password: Kj9#mT2@pL5!wX8%
2FA Code: 683491 (from authenticator app)

Attacker needs BOTH to gain access
```

**2FA Options** (by security):
1. **Hardware tokens** (YubiKey) - Most secure
2. **Authenticator apps** (Authy, Google Authenticator) - Secure
3. **SMS codes** - Better than nothing, but vulnerable to SIM swapping

---

## 🧮 Crack Time Calculations

### Brute Force Assumptions

**Online Attack** (rate-limited):
- Speed: 1,000 attempts/second
- Limited by server throttling

**Offline Attack** (stolen hash database):
- Modern GPU: 10 billion attempts/second (bcrypt)
- High-end GPU: 100 billion attempts/second (bcrypt)
- Custom ASIC: 1 trillion attempts/second (SHA-256)

### Calculation Formula

```
Time to crack = (charset_size^password_length) / (attempts_per_second * 2)

# Divide by 2 for average case (50% chance to find password before exhausting space)
```

### Example Scenarios

```python
# Scenario 1: 8-char alphanumeric (52.4 bits)
Keyspace: 62^8 = 218,340,105,584,896
GPU (10B/s): 218,340,105,584,896 / (10,000,000,000 × 2) = 10,917 seconds = 3 hours ❌

# Scenario 2: 12-char alphanumeric (71.4 bits)
Keyspace: 62^12 = 3.2 × 10^21
GPU (10B/s): 3.2 × 10^21 / (10,000,000,000 × 2) = 1.6 × 10^11 seconds = 5,070 years ✅

# Scenario 3: 16-char full charset (104.8 bits)
Keyspace: 94^16 = 5.6 × 10^31
ASIC (1T/s): 5.6 × 10^31 / (1,000,000,000,000 × 2) = 2.8 × 10^19 seconds = 888 billion years ✅✅✅
```

---

## 🐛 Troubleshooting

### Issue: Generated password rejected by website

**Cause**: Password policy restrictions (e.g., "no symbols", "max 16 chars")

**Solution**:
```bash
# Generate without symbols
Password length: 16
Include uppercase: y
Include digits: y
Include symbols: n  ← Disable symbols
```

### Issue: Can't remember complex password

**Solution**: Use password manager, not your memory

```bash
# Install KeePassXC (Linux)
sudo apt install keepassxc

# Create encrypted database
keepassxc --create MyPasswords.kdbx

# Set one STRONG master password
Master Password: correct-horse-battery-staple-giraffe-envelope-mountain
```

---

## 📚 Further Reading

- [NIST Password Guidelines (SP 800-63B)](https://pages.nist.gov/800-63-3/sp800-63b.html)
- [EFF Dice-Generated Passphrases](https://www.eff.org/dice)
- [xkcd 936: Password Strength](https://xkcd.com/936/)
- [Python secrets Documentation](https://docs.python.org/3/library/secrets.html)

---

## 🔗 Related Tools

- [[AES-Encryption]] - Use strong passwords to encrypt sensitive files
- [[File-Integrity-Checker]] - Verify password database hasn't been tampered with
- [[Data-Deletion-Utility]] - Securely delete old password files

---

**Developer**: Sai Srujan Murthy | **Contact**: saisrujanmurthy@gmail.com
