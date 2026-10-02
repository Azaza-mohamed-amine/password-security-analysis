import hashlib
import bcrypt
import time

password = b"Summer2024!"

# Time 100,000 SHA-256 hashes
start = time.time()
for _ in range(100_000):
    hashlib.sha256(password).hexdigest()
sha_time = time.time() - start

# Time 100 bcrypt hashes (fewer, because it's MUCH slower)
start = time.time()
for _ in range(100):
    bcrypt.hashpw(password, bcrypt.gensalt())
bcrypt_time = time.time() - start

print(f"SHA-256: 100,000 hashes in {sha_time:.3f} seconds")
print(f"bcrypt:  100 hashes in {bcrypt_time:.3f} seconds")
print(f"\nSHA-256 hashes/sec: {100_000/sha_time:,.0f}")
print(f"bcrypt hashes/sec:  {100/bcrypt_time:,.0f}")