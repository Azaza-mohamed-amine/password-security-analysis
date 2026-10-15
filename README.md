# Password Hashing & Security Analysis

I wanted to see for myself why the choice of hashing algorithm matters when a website stores passwords. So I compared MD5, SHA-256 and bcrypt in Python: what their hashes look like, how fast they are, and how long a simple dictionary attack takes against each.

## What I found

| | MD5 | SHA-256 | bcrypt (cost 12) |
|---|---|---|---|
| Hashes per second (one CPU core, average of 3 runs) | ~1.67M | ~1.86M | ~3.4 |
| Time to crack `password123` with a 10-word list | — | 0.000037 s | 2.26 s |

bcrypt was about 500,000 times slower to hash and about 61,000 times slower to crack. That's on purpose: a login only needs one hash, but an attacker needs millions.

The exact numbers depend on the machine, and real attackers use GPUs, which are much faster. What matters is the gap between the algorithms. The other thing I learned is that a slow hash doesn't save a weak password: `123456` still falls on the first guess. You need both a good algorithm and a good password.

The full write-up, with the method and the limitations, is in [REPORT.md](REPORT.md).

## The scripts

| File | What it does |
|---|---|
| `hash_demo.py` | Hashes the same password with all three and prints the results |
| `speed_test.py` | Measures hashes per second for each (3 runs, averaged) |
| `dictionary_attack.py` | Tries to crack a weak password hashed with SHA-256 and with bcrypt |
| `password_strength_test.py` | Same algorithm, weak vs strong password, to see if the password alone makes a difference |

## Running it

```bash
pip install bcrypt
python hash_demo.py
python speed_test.py
python dictionary_attack.py
python password_strength_test.py
```

Built with Python 3, `hashlib` and `bcrypt`.

Mohamed Amine Azaza, CS student at Università del Piemonte Orientale
