import hashlib
import bcrypt
import time

password = b"Summer2024!"
RUNS = 3  # repeat each benchmark and average, to smooth out noise


def benchmark(label, hash_fn, iterations):
    """Run hash_fn `iterations` times, RUNS times over, and return the average rate."""
    rates = []
    for _ in range(RUNS):
        start = time.perf_counter()  # high-resolution timer, better than time.time()
        for _ in range(iterations):
            hash_fn()
        elapsed = time.perf_counter() - start
        rates.append(iterations / elapsed)
    avg = sum(rates) / len(rates)
    print(f"{label:<18} {iterations:>9,} hashes x {RUNS} runs -> "
          f"avg {avg:>14,.1f} hashes/sec (min {min(rates):,.1f}, max {max(rates):,.1f})")
    return avg


md5_rate = benchmark("MD5", lambda: hashlib.md5(password).hexdigest(), 100_000)
sha_rate = benchmark("SHA-256", lambda: hashlib.sha256(password).hexdigest(), 100_000)
# Far fewer bcrypt iterations, because it is deliberately MUCH slower
bcrypt_rate = benchmark("bcrypt (cost 12)", lambda: bcrypt.hashpw(password, bcrypt.gensalt()), 20)

print(f"\nSHA-256 is ~{sha_rate / bcrypt_rate:,.0f}x faster than bcrypt")
print(f"MD5 is ~{md5_rate / bcrypt_rate:,.0f}x faster than bcrypt")
