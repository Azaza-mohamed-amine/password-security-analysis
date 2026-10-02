import hashlib
import time

# Our tiny demonstration wordlist from before
common_passwords = [
    "123456", "password", "123456789", "qwerty", "abc123",
    "password1", "password123", "admin", "letmein", "welcome"
]

def try_crack(target_hash, wordlist, label):
    print(f"\n=== Attempting to crack: {label} ===")
    start = time.time()
    for guess in wordlist:
        if hashlib.sha256(guess.encode()).hexdigest() == target_hash:
            print(f"CRACKED: '{guess}' in {time.time()-start:.6f} seconds")
            return
    elapsed = time.time() - start
    print(f"NOT FOUND after checking {len(wordlist)} candidates ({elapsed:.6f} seconds)")

# Test 1: a weak, common password
weak_password = "123456"
weak_hash = hashlib.sha256(weak_password.encode()).hexdigest()
try_crack(weak_hash, common_passwords, "weak password ('123456')")

# Test 2: a long, random, unique password
strong_password = "Xk9#mP2$vL7qR4!wZ"
strong_hash = hashlib.sha256(strong_password.encode()).hexdigest()
try_crack(strong_hash, common_passwords, "strong password (random, 17 chars)")