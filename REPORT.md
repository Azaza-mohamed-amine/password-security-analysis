# Password Hashing & Security Analysis

**Author:** Mohamed Amine Azaza
**Date:** October 2026
**Domain:** Cryptography / Password Security (CompTIA Security+ aligned)

## 1. Objective

Password storage is one of the most common and most frequently mismanaged areas of application security. Many real-world breaches trace back to weak hashing choices rather than exotic attacks. This project investigates, empirically, why general-purpose hashing algorithms (MD5, SHA-256) are unsuitable for password storage, and why purpose-built algorithms like bcrypt are the correct choice — using hands-on benchmarks rather than theory alone.

## 2. Methodology

All tests were run locally in Python 3, using the standard `hashlib` library (MD5, SHA-256) and the `bcrypt` library (bcrypt, cost factor 12 — the library default). Four experiments were conducted:

1. Comparing raw hash output across three algorithms for the same input
2. Benchmarking hashing throughput (hashes per second) for SHA-256 vs. bcrypt
3. Simulating a dictionary attack against a weak password hashed with each algorithm
4. Testing whether password strength alone (independent of hashing algorithm) affects resistance to a dictionary attack

## 3. Finding 1 — Hash Output Comparison

Hashing the password `Summer2024!` with three algorithms produced:

| Algorithm | Output | Length |
|---|---|---|
| MD5 | `f065d609e55983bc6087c073c91c9bc7` | 128-bit |
| SHA-256 | `323725e8eff4df0a4974d6ea8c73017aa6467d94e09382745b7a988cec0fba0a` | 256-bit |
| bcrypt | `$2b$12$S5iDqNlJmx1jmQdxUCTgau.Y8NA4zN9cSh42cfUX.AnfSpOncyPoq` | includes embedded salt + cost factor |

**Key observation:** MD5 and SHA-256 are deterministic — the same input always produces the identical output, every time, on any machine. This is precisely what makes them exploitable via precomputed lookup tables (rainbow tables). bcrypt's output embeds a randomly generated salt directly into the hash string, so re-hashing the identical password produces a different result on every run, defeating precomputation attacks entirely.

## 4. Finding 2 — Throughput Benchmark

| Algorithm | Hashes computed | Time | Rate |
|---|---|---|---|
| SHA-256 | 100,000 | 0.067s | ~1,482,149 hashes/sec |
| bcrypt (cost 12) | 100 | 28.501s | ~4 hashes/sec |

**Key observation:** SHA-256 is approximately **370,000 times faster** than bcrypt. For general-purpose hashing (file integrity, checksums) this speed is a feature. For password storage, it is a liability: an attacker with modern GPU hardware can attempt billions of SHA-256 guesses per second against a stolen password database, but is limited to a handful of guesses per second against bcrypt-hashed passwords, regardless of hardware investment — because bcrypt's cost factor is specifically designed to resist hardware acceleration.

## 5. Finding 3 — Dictionary Attack Simulation

Using a small 10-entry sample wordlist of common passwords, the password `password123` was hashed with SHA-256 and bcrypt, then an attack script attempted to match each against the wordlist.

| Algorithm | Result | Time to crack |
|---|---|---|
| SHA-256 | Cracked | 0.000029s |
| bcrypt | Cracked | 1.491225s |

**Key observation:** Even against a trivially small 10-word list, bcrypt took roughly **51,000 times longer** to crack the same password. Real-world attacks use wordlists with millions of entries (e.g. leaked password corpora such as `rockyou.txt`, ~14 million entries). Extrapolating, a SHA-256-hashed weak password would still fall in well under a second at that scale, while the same password hashed with bcrypt could take hours — a difference that, for a real organization, is often the gap between a breach going unnoticed and being caught and contained in time.

## 6. Finding 4 — Password Strength as an Independent Variable

To isolate the effect of password strength from hashing algorithm, two passwords were hashed with SHA-256 (the weaker, faster algorithm) and tested against the same 10-word list:

| Password | Result |
|---|---|
| `123456` (weak, common) | Cracked in 0.000045s |
| `Xk9#mP2$vL7qR4!wZ` (strong, random, 17 chars) | Not found |

**Key observation:** The dictionary attack succeeds or fails based on whether the password exists in the attacker's wordlist — not purely on hashing speed. A sufficiently strong, unpredictable password resists this attack vector even when hashed with an algorithm unsuitable for password storage. This demonstrates that **password strength and hashing algorithm strength are two independent, complementary layers of defense** — neither compensates fully for a failure in the other.

## 7. Conclusions & Recommendations

1. **Never use MD5 or raw SHA-256 for password storage.** Both are fast, deterministic, and vulnerable to precomputed and brute-force attacks at scale.
2. **Use a purpose-built, slow, salted algorithm** such as bcrypt, scrypt, or Argon2 for any password storage system. These are intentionally resistant to hardware-accelerated brute-forcing.
3. **Enforce password strength requirements independently of hashing choice.** Strong hashing does not excuse weak user passwords, and strong passwords do not excuse weak hashing — both layers are necessary.
4. **Adjust bcrypt's cost factor over time** as hardware improves, to maintain its intended resistance against brute-force attacks.

## 8. Tools & Environment

- Python 3.x
- `hashlib` (standard library)
- `bcrypt` (PyPI package)
- Tested on Windows 10/11, local machine, no network exposure

## Repository Structure

```
password-security-analysis/
├── hash_demo.py                  # Finding 1: hash output comparison
├── speed_test.py                 # Finding 2: throughput benchmark
├── dictionary_attack.py          # Finding 3: dictionary attack simulation
├── password_strength_test.py     # Finding 4: password strength independence
└── REPORT.md                     # This report
```
