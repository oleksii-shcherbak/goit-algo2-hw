import hashlib
import json
import math
import struct
import sys
import time


class HyperLogLog:
    def __init__(self, error_rate=0.01):
        b = max(4, math.ceil(math.log2((1.044 / error_rate) ** 2)))
        self.b = b
        self.m = 1 << b
        self.registers = bytearray(self.m)
        self.alpha = {16: 0.673, 32: 0.697, 64: 0.709}.get(
            self.m, 0.7213 / (1 + 1.079 / self.m)
        )

    def add(self, item: str):
        h = struct.unpack(">I", hashlib.md5(item.encode()).digest()[:4])[0]
        bucket = h >> (32 - self.b)
        w = h & ((1 << (32 - self.b)) - 1)
        max_bits = 32 - self.b
        rho = max_bits - w.bit_length() + 1 if w else max_bits + 1
        if rho > self.registers[bucket]:
            self.registers[bucket] = rho

    def count(self) -> int:
        Z = sum(2.0 ** -r for r in self.registers)
        E = self.alpha * self.m * self.m / Z
        if E <= 2.5 * self.m:
            V = self.registers.count(0)
            if V:
                E = self.m * math.log(self.m / V)
        return int(E)


def load_ips(filepath: str) -> list:
    ips = []
    with open(filepath, "r", errors="ignore") as f:
        for line in f:
            try:
                ip = json.loads(line).get("remote_addr", "")
                if ip:
                    ips.append(ip)
            except (json.JSONDecodeError, AttributeError):
                pass
    return ips


def main(log_file="lms-stage-access.log"):
    try:
        ips = load_ips(log_file)
    except FileNotFoundError:
        print(f"Log file '{log_file}' not found.")
        print("Place lms-stage-access.log in the same directory, or pass the path as an argument.")
        sys.exit(1)

    t0 = time.perf_counter()
    exact = len(set(ips))
    t_exact = time.perf_counter() - t0

    t0 = time.perf_counter()
    hll = HyperLogLog(error_rate=0.01)
    for ip in ips:
        hll.add(ip)
    approx = hll.count()
    t_hll = time.perf_counter() - t0

    print("Comparison results:")
    print(f"{'':25} {'Exact count':>15} {'HyperLogLog':>14}")
    print(f"{'Unique elements':25} {float(exact):>15.1f} {float(approx):>14.1f}")
    print(f"{'Time (sec.)':25} {t_exact:>15.4f} {t_hll:>14.4f}")


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "lms-stage-access.log"
    main(path)
