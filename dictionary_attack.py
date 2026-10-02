import hashlib
import bcrypt
import time

# A deliberately weak password, hashed both ways
weak_password = "password123"
target_sha256 = hashlib.sha256(weak_password.encode()).hexdigest()
target_bcrypt = bcrypt.hashpw(weak_password.encode(), bcrypt.gensalt())

# A small sample wordlist (normally this would be millions of entries,
# e.g. the real "rockyou.txt" list used in actual security testing)
common_passwords = [
    "123456", "password", "123456789", "qwerty", "abc123",
    "password1", "password123", "admin", "letmein", "welcome"
]

print("=== Cracking with SHA-256 ===")
start = time.time()
found = False
for guess in common_passwords:
    if hashlib.sha256(guess.encode()).hexdigest() == target_sha256:
        print(f"CRACKED: '{guess}' in {time.time()-start:.6f} seconds")
        found = True
        break
if not found:
    print("Not found in wordlist")

print("\n=== Cracking with bcrypt ===")
start = time.time()
found = False
for guess in common_passwords:
    if bcrypt.checkpw(guess.encode(), target_bcrypt):
        print(f"CRACKED: '{guess}' in {time.time()-start:.6f} seconds")
        found = True
        break
if not found:
    print("Not found in wordlist")