# Password Hashing & Security Analysis

Mohamed Amine Azaza, October 2026

## 1. Why I did this

When a company gets breached, the password database is often one of the things stolen. Websites don't keep the passwords themselves, only hashes of them, so how safe users are comes down to how hard those hashes are to crack. I'd read that fast algorithms like MD5 and SHA-256 are a bad idea for passwords and that bcrypt is the right choice, but I wanted to measure it myself instead of taking it on faith. This ties in with what I'm studying for CompTIA Security+.

## 2. How I tested it

Everything runs locally in Python 3. I used the built-in `hashlib` library for MD5 and SHA-256, and the `bcrypt` library with its default cost factor of 12. For timing I used `time.perf_counter()`, which is Python's high-resolution timer.

I ran four small experiments, one script each:

1. Hash the same password with all three algorithms and compare the output
2. Measure how many hashes per second each one can do, repeating each test 3 times and averaging
3. Try to crack a weak password hashed with SHA-256 and with bcrypt, using a short wordlist
4. Keep the algorithm the same and change only the password, to see whether password strength matters on its own

## 3. What the hashes look like

I hashed `Summer2024!` with each algorithm:

| Algorithm | Output | Length |
|---|---|---|
| MD5 | `f065d609e55983bc6087c073c91c9bc7` | 128 bits |
| SHA-256 | `323725e8eff4df0a4974d6ea8c73017aa6467d94e09382745b7a988cec0fba0a` | 256 bits |
| bcrypt | `$2b$12$S5iDqNlJmx1jmQdxUCTgau.Y8NA4zN9cSh42cfUX.AnfSpOncyPoq` | includes the salt and cost |

The bcrypt string carries everything needed to check a password later: `$2b$` is the version, `12` is the cost factor (2¹² = 4,096 rounds), the next 22 characters are a 128-bit salt, and the last 31 are the hash itself.

Running the script twice shows the main difference. MD5 and SHA-256 give exactly the same output every time, on any machine. That's what makes precomputed lookup tables (rainbow tables) work against them, and it means two users with the same password end up with the same hash. bcrypt generates a new random salt each time, so the output changes on every run.

One thing I had to get straight: it's the salt that defeats rainbow tables, not bcrypt as such. A salted SHA-256 would beat them too. What bcrypt adds on top is that it's deliberately slow, which is what the next test measures.

## 4. How fast each one is

`speed_test.py` hashes the same password over and over with each algorithm, three times, and reports the average along with the slowest and fastest run:

| Algorithm | Hashes per run | Average (3 runs) | Range |
|---|---|---|---|
| MD5 | 100,000 | ~1,672,539 per second | 1,499,900 – 1,926,441 |
| SHA-256 | 100,000 | ~1,860,932 per second | 1,814,780 – 1,914,037 |
| bcrypt (cost 12) | 20 | ~3.4 per second | 2.9 – 3.7 |

SHA-256 came out about 547,000 times faster than bcrypt, and MD5 about 492,000 times faster. I only ran 20 bcrypt hashes per round because 100,000 would have taken around 8 hours. Since I compare hashes per second, the different counts don't affect the comparison.

I expected MD5 to be clearly faster than SHA-256, but SHA-256 was slightly ahead, and the MD5 range overlaps it. I think there are two reasons. In single-threaded Python, the overhead of each function call costs about as much as the hash itself. And many modern CPUs have built-in instructions for SHA-256 that the underlying OpenSSL library uses. Proper cracking tools on GPUs show the real gap, where MD5 is several times faster.

For checking file integrity, speed is a good thing. For passwords it's the opposite: with GPUs and a tool like hashcat, an attacker can try billions of MD5 or SHA-256 guesses per second against a stolen database. bcrypt is built to be slow and doesn't speed up well on GPUs, so attacks against it are orders of magnitude slower. They're not impossible, though. A GPU rig gets far more than the ~3.4 guesses per second I measured on one CPU core, which is why the cost factor has to go up as hardware improves.

## 5. Cracking a weak password

I hashed `password123` with SHA-256 and with bcrypt, then tried to crack both with a 10-word list of common passwords (`password123` is the 7th). Cracking never reverses a hash. You guess, hash the guess and compare it with the stolen hash. For bcrypt the script uses `bcrypt.checkpw()`, which reads the salt and cost from the stored hash and reuses them, just like a real login check.

| Algorithm | Result | Time |
|---|---|---|
| SHA-256 | Cracked | 0.000037 s |
| bcrypt | Cracked | 2.258182 s |

Even with only 10 words, bcrypt took about 61,000 times longer. Real attackers use lists with millions of entries, like the leaked `rockyou.txt` with about 14 million passwords. At the speeds I measured on one CPU core, going through that list takes a few seconds against a SHA-256 hash and roughly 48 days against a bcrypt hash. GPUs shorten both, but the gap stays huge.

## 6. Does the password itself matter?

To separate the password from the algorithm, I used SHA-256 (the fast, weak one) for both tests and changed only the password:

| Password | Result |
|---|---|
| `123456` (weak, very common) | Cracked in 0.000011 s |
| `Xk9#mP2$vL7qR4!wZ` (17 random characters) | Not found after all 10 candidates (0.000024 s) |

A dictionary attack only works if the password is on the list, however fast the hash is.

I know "not found in 10 words" doesn't prove much by itself. The real point is the number of possibilities: 17 random characters from the ~94 printable ASCII characters give about 94¹⁷ ≈ 3.5 × 10³³ combinations (~111 bits). A password like that won't be in any leaked list, and brute-forcing it isn't feasible even at billions of guesses per second.

On the other hand, `Summer2024!` looks strong because it has a capital, numbers and a symbol, but it follows a very common pattern: word, year, exclamation mark. Attackers add rules like that to their wordlists, so passwords like this fall much faster than their length suggests.

So password strength and hash strength are two separate layers of defence, and neither one makes up for the other.

## 7. What I'd recommend

1. Don't store passwords with MD5 or plain SHA-256. They're fast, and without a salt they're deterministic.
2. Use an algorithm made for passwords. Argon2id is OWASP's first recommendation today because it's also memory-hard, which makes GPU attacks harder. bcrypt and scrypt are still fine.
3. Enforce strong passwords anyway. A good algorithm doesn't excuse weak passwords, and strong passwords don't excuse a weak algorithm.
4. Raise bcrypt's cost factor over time as hardware gets faster. Each +1 doubles the work.

## 8. Limitations and next steps

- These are single-threaded Python numbers on one laptop CPU. Attackers with GPU tools are much faster, so the ratios matter more than the absolute numbers.
- The 10-word list is only a demonstration.

What I'd like to try next:

- add Argon2 to the benchmark
- test several bcrypt cost factors (10 to 14) to show the doubling
- use a real wordlist like `rockyou.txt` with mutation rules
- measure real attacker speeds with hashcat on a GPU

## 9. Setup

- Python 3.14 on a Windows 10/11 laptop, run locally with no network exposure
- `hashlib` (standard library) and `bcrypt` (from PyPI)

## Files

```
password-security-analysis/
├── hash_demo.py                  # section 3: what the hashes look like
├── speed_test.py                 # section 4: speed benchmark (MD5, SHA-256, bcrypt)
├── dictionary_attack.py          # section 5: dictionary attack
├── password_strength_test.py     # section 6: weak vs strong password
├── README.md                     # short overview
└── REPORT.md                     # this report
```
