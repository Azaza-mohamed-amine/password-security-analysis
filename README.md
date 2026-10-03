[README.md](https://github.com/user-attachments/files/33000845/README.md)
# Password Hashing & Security Analysis

Hands-on comparison of password hashing algorithms (MD5, SHA-256, bcrypt), demonstrating why algorithm choice matters for password storage security.

## What this project shows

- 🔑 Why deterministic hashes (MD5, SHA-256) are unsafe for password storage
- ⚡ Real throughput benchmarks: SHA-256 (~1.48M hashes/sec) vs bcrypt (~4 hashes/sec)
- 🎯 A working dictionary attack demo against both algorithms
- 🛡️ Why password strength and hashing strength are independent, complementary defenses

## Key result

| Test | SHA-256 | bcrypt |
|---|---|---|
| Hashing speed | ~1,482,149/sec | ~4/sec |
| Time to crack weak password (10-word list) | 0.000029s | 1.49s |

**→ bcrypt was ~370,000x slower to hash and ~51,000x slower to crack — by design.**

## Tech stack

Python 3 · `hashlib` · `bcrypt`

## Files

| File | Purpose |
|---|---|
| `hash_demo.py` | Compares raw hash output across MD5, SHA-256, bcrypt |
| `speed_test.py` | Benchmarks hashing throughput |
| `dictionary_attack.py` | Simulates a dictionary attack on a weak password |
| `password_strength_test.py` | Isolates the effect of password strength from hashing algorithm |
| `REPORT.md` | Full write-up with methodology, findings, and recommendations |

📄 **[Read the full report →](REPORT.md)**

## Run it yourself

```bash
pip install bcrypt
python hash_demo.py
python speed_test.py
python dictionary_attack.py
python password_strength_test.py
```

---

**Author:** Mohamed Amine Azaza — CS Student, Università del Piemonte Orientale
