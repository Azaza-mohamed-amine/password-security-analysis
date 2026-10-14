# Password Hashing & Security Analysis

**Author:** Mohamed Amine Azaza
**Date:** October 2026
**Domain:** Cryptography / Password Security (CompTIA Security+ aligned)

## 1. Objective

Password storage is one of the most common and most frequently mismanaged areas of application security. Many real-world breaches trace back to weak hashing choices rather than exotic attacks. This project investigates, empirically, why general-purpose hashing algorithms (MD5, SHA-256) are unsuitable for password storage, and why purpose-built algorithms like bcrypt are the correct choice — using hands-on benchmarks rather than theory alone.

## 2. Methodology

All tests were run locally in Python 3, using the standard `hashlib` library (MD5, SHA-256) and the `bcrypt` library (bcrypt, cost factor 12 — the library default). Timings use `time.perf_counter()`, Python's high-resolution timer. Four experiments were conducted:

1. Comparing raw hash output across three algorithms for the same input
2. Benchmarking hashing throughput (hashes per second) for MD5, SHA-256 and bcrypt, with each benchmark repeated 3 times and averaged
3. Simulating a dictionary attack against a weak password hashed with each algorithm
4. Testing whether password strength alone (independent of hashing algorithm) affects resistance to a dictionary attack

## 3. Finding 1 — Hash Output Comparison

Hashing the password `Summer2024!` with three algorithms produced:

| Algorithm | Output | Length |
|---|---|---|
| MD5 | `f065d609e55983bc6087c073c91c9bc7` | 128-bit |
| SHA-256 | `323725e8eff4df0a4974d6ea8c73017aa6467d94e09382745b7a988cec0fba0a` | 256-bit |
| bcrypt | `$2b$12$S5iDqNlJmx1jmQdxUCTgau.Y8NA4zN9cSh42cfUX.AnfSpOncyPoq` | includes embedded salt + cost factor |

The bcrypt string is self-describing: `$2b$` is the algorithm version, `12` is the cost factor (2¹² = 4,096 rounds), the next 22 characters are the 128-bit salt, and the remaining 31 characters are the hash itself.

**Key observation:** unsalted MD5 and SHA-256 are deterministic — the same input always produces the identical output, on any machine. This is what makes them exploitable via precomputed lookup tables (rainbow tables), and it means every user with the same password gets the same hash. bcrypt generates a random salt and embeds it in the hash string, so re-hashing the identical password gives a different result on every run.

Note that it is the **salt**, not bcrypt itself, that defeats precomputation: a salted SHA-256 would also make rainbow tables useless. What bcrypt adds on top of salting is deliberate **slowness** (the cost factor), which is examined in Finding 2.

## 4. Finding 2 — Throughput Benchmark

`speed_test.py` hashes the same password repeatedly with each algorithm, repeats each benchmark 3 times, and reports the average rate (with min and max to show the run-to-run variation):

| Algorithm | Hashes per run | Average rate (3 runs) | Min – max |
|---|---|---|---|
| MD5 | 100,000 | ~1,672,539 hashes/sec | 1,499,900 – 1,926,441 |
| SHA-256 | 100,000 | ~1,860,932 hashes/sec | 1,814,780 – 1,914,037 |
| bcrypt (cost 12) | 20 | ~3.4 hashes/sec | 2.9 – 3.7 |

**Key observations:**

- SHA-256 was roughly **547,000× faster** than bcrypt, and MD5 roughly **492,000× faster**. The absolute numbers depend on the machine and vary between runs; the ratio of several hundred thousand times is the stable result.
- MD5 and SHA-256 come out at similar speeds here. In single-threaded Python, the per-call interpreter overhead (function call, `hexdigest()`) dominates the cost of the hash itself. Optimized cracking tools show the real gap: on GPUs, MD5 is several times faster than SHA-256.
- For general-purpose hashing (file integrity, checksums), speed is a feature. For password storage it is a liability: an attacker with GPU hardware and tools like hashcat can attempt billions of MD5/SHA-256 guesses per second against a stolen database.
- bcrypt is deliberately slow and does not speed up well on GPUs, so attacks against it are **orders of magnitude slower** — but not impossible. A GPU rig still achieves far more than the ~3.4 guesses/sec measured here on one CPU core, which is why the cost factor must be raised over time.

## 5. Finding 3 — Dictionary Attack Simulation

Using a small 10-entry sample wordlist of common passwords, the password `password123` (7th entry in the list) was hashed with SHA-256 and bcrypt, then an attack script attempted to match each against the wordlist. Hash-and-compare is how real cracking works: a hash is never "reversed", each guess is hashed and compared to the stolen hash. For bcrypt, `bcrypt.checkpw()` re-hashes each guess using the salt and cost stored in the target hash.

| Algorithm | Result | Time to crack |
|---|---|---|
| SHA-256 | Cracked | 0.000029s |
| bcrypt | Cracked | 1.491225s |

**Key observation:** Even against a trivially small 10-word list, bcrypt took roughly **51,000 times longer** to crack the same password. Real-world attacks use wordlists with millions of entries (e.g. the leaked `rockyou.txt` corpus, ~14 million entries). At the measured rates on a single CPU core, running that whole list against one SHA-256 hash takes a few seconds, while against one bcrypt hash it would take roughly 48 days. GPU hardware shortens both, but the gap between them remains several orders of magnitude.

## 6. Finding 4 — Password Strength as an Independent Variable

To isolate the effect of password strength from hashing algorithm, two passwords were hashed with SHA-256 (the weaker, faster algorithm) and tested against the same 10-word list:

| Password | Result |
|---|---|
| `123456` (weak, common) | Cracked in 0.000045s |
| `Xk9#mP2$vL7qR4!wZ` (strong, random, 17 chars) | Not found |

**Key observation:** A dictionary attack succeeds or fails based on whether the password is in the attacker's wordlist, not on hashing speed alone.

Not being found in a 10-word list is only a demonstration; on its own it proves little. The real argument is the size of the search space: a random 17-character password drawn from the ~94 printable ASCII characters has about 94¹⁷ ≈ 3.5 × 10³³ possibilities (~111 bits of entropy). It will not appear in any leaked wordlist, and brute-forcing it is infeasible even at billions of SHA-256 guesses per second.

By contrast, a password like `Summer2024!` *looks* strong (capital, digits, symbol) but follows a predictable "word + year + symbol" pattern. Real attackers apply mutation rules to wordlists (capitalization, appended years, trailing `!`), so passwords like this are cracked far faster than their length suggests.

This demonstrates that **password strength and hashing algorithm strength are two independent, complementary layers of defense** — neither compensates fully for a failure in the other.

## 7. Conclusions & Recommendations

1. **Never use MD5 or raw SHA-256 for password storage.** Both are fast and, unsalted, deterministic — vulnerable to precomputed and brute-force attacks at scale.
2. **Use a purpose-built, slow, salted algorithm.** Argon2id is the current first recommendation (OWASP) because it is also memory-hard, which further limits GPU attacks; bcrypt and scrypt remain acceptable.
3. **Enforce password strength requirements independently of hashing choice.** Strong hashing does not excuse weak user passwords, and strong passwords do not excuse weak hashing — both layers are necessary.
4. **Adjust bcrypt's cost factor over time** as hardware improves. Each +1 doubles the work per hash.

## 8. Limitations & Future Work

- **Single-threaded Python on a CPU.** These speeds are far below what attackers achieve with optimized GPU tools; the ratios are the meaningful result, not the absolute numbers.
- **Toy wordlist.** The 10-word list is for demonstration only.
- **Next steps:**
  - add Argon2 to the benchmark
  - test several bcrypt cost factors (10–14) to show the doubling effect
  - use a real wordlist such as `rockyou.txt` with mutation rules
  - compare with GPU cracking in hashcat to measure realistic attacker speeds

## 9. Tools & Environment

- Python 3.14
- `hashlib` (standard library)
- `bcrypt` (PyPI package)
- Windows 10/11 laptop, local machine, no network exposure

## Repository Structure

```
password-security-analysis/
├── hash_demo.py                  # Finding 1: hash output comparison
├── speed_test.py                 # Finding 2: throughput benchmark (MD5, SHA-256, bcrypt)
├── dictionary_attack.py          # Finding 3: dictionary attack simulation
├── password_strength_test.py     # Finding 4: password strength independence
├── README.md                     # Project overview
└── REPORT.md                     # This report
```
