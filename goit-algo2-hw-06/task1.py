import hashlib


class BloomFilter:
    def __init__(self, size=1000, num_hashes=3):
        self.size = size
        self.num_hashes = num_hashes
        self.bits = bytearray(size)

    def _positions(self, item):
        s = str(item).encode()
        for i in range(self.num_hashes):
            h = hashlib.md5(bytes([i]) + s).digest()
            yield int.from_bytes(h, "big") % self.size

    def add(self, item):
        for pos in self._positions(item):
            self.bits[pos] = 1

    def __contains__(self, item):
        return all(self.bits[pos] for pos in self._positions(item))


def check_password_uniqueness(bloom: BloomFilter, passwords: list) -> dict:
    results = {}
    for pwd in passwords:
        if not isinstance(pwd, str) or not pwd:
            results[repr(pwd)] = "invalid"
        elif pwd in bloom:
            results[pwd] = "already used"
        else:
            results[pwd] = "unique"
    return results


if __name__ == "__main__":
    bloom = BloomFilter(size=1000, num_hashes=3)

    existing_passwords = ["password123", "admin123", "qwerty123"]
    for password in existing_passwords:
        bloom.add(password)

    new_passwords_to_check = ["password123", "newpassword", "admin123", "guest"]
    results = check_password_uniqueness(bloom, new_passwords_to_check)

    for password, status in results.items():
        print(f"Password '{password}' — {status}.")
