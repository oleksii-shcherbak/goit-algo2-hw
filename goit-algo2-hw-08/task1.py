import random
import time
from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self._cache = OrderedDict()

    def get(self, key):
        if key not in self._cache:
            return -1
        self._cache.move_to_end(key)
        return self._cache[key]

    def put(self, key, value):
        if key in self._cache:
            self._cache.move_to_end(key)
        self._cache[key] = value
        if len(self._cache) > self.capacity:
            self._cache.popitem(last=False)


_cache = LRUCache(1000)


def range_sum_no_cache(array, left, right):
    return sum(array[left : right + 1])


def update_no_cache(array, index, value):
    array[index] = value


def range_sum_with_cache(array, left, right):
    key = (left, right)
    result = _cache.get(key)
    if result == -1:
        result = sum(array[left : right + 1])
        _cache.put(key, result)
    return result


def update_with_cache(array, index, value):
    array[index] = value
    stale = [k for k in _cache._cache if k[0] <= index <= k[1]]
    for k in stale:
        del _cache._cache[k]


def make_queries(n, q, hot_pool=30, p_hot=0.95, p_update=0.03):
    hot = [
        (random.randint(0, n // 2), random.randint(n // 2, n - 1))
        for _ in range(hot_pool)
    ]
    queries = []
    for _ in range(q):
        if random.random() < p_update:
            idx = random.randint(0, n - 1)
            val = random.randint(1, 100)
            queries.append(("Update", idx, val))
        else:
            if random.random() < p_hot:
                left, right = random.choice(hot)
            else:
                left = random.randint(0, n - 1)
                right = random.randint(left, n - 1)
            queries.append(("Range", left, right))
    return queries


if __name__ == "__main__":
    N, Q = 100_000, 50_000
    random.seed(42)
    array = [random.randint(1, 1000) for _ in range(N)]
    queries = make_queries(N, Q)

    # Without cache
    arr_no = array[:]
    t0 = time.perf_counter()
    for q in queries:
        if q[0] == "Range":
            range_sum_no_cache(arr_no, q[1], q[2])
        else:
            update_no_cache(arr_no, q[1], q[2])
    t_no = time.perf_counter() - t0

    # With cache (fresh array copy, clear cache state)
    _cache._cache.clear()
    arr_cached = array[:]
    t0 = time.perf_counter()
    for q in queries:
        if q[0] == "Range":
            range_sum_with_cache(arr_cached, q[1], q[2])
        else:
            update_with_cache(arr_cached, q[1], q[2])
    t_cached = time.perf_counter() - t0

    speedup = t_no / t_cached if t_cached > 0 else float("inf")
    print(f"No cache :  {t_no:.2f} s")
    print(f"LRU cache:  {t_cached:.2f} s  (speedup x{speedup:.1f})")
