import hashlib
import bcrypt

password = "Summer2024!"

# MD5 - old, fast, broken for security use
md5_hash = hashlib.md5(password.encode()).hexdigest()

# SHA-256 - modern, fast, but still not ideal alone for passwords
sha256_hash = hashlib.sha256(password.encode()).hexdigest()

# bcrypt - slow by design, includes built-in salt
bcrypt_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

print("Original password:", password)
print("MD5:        ", md5_hash)
print("SHA-256:     ", sha256_hash)
print("bcrypt:      ", bcrypt_hash.decode())