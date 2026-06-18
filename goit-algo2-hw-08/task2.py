import random
import time
from collections import deque
from typing import Dict


class SlidingWindowRateLimiter:
    def __init__(self, window_size: int = 10, max_requests: int = 1):
        self.window_size = window_size
        self.max_requests = max_requests
        self._history: Dict[str, deque] = {}

    def _cleanup_window(self, user_id: str, current_time: float) -> None:
        if user_id not in self._history:
            return
        dq = self._history[user_id]
        while dq and current_time - dq[0] >= self.window_size:
            dq.popleft()
        if not dq:
            del self._history[user_id]

    def can_send_message(self, user_id: str) -> bool:
        self._cleanup_window(user_id, time.time())
        return len(self._history.get(user_id, [])) < self.max_requests

    def record_message(self, user_id: str) -> bool:
        now = time.time()
        self._cleanup_window(user_id, now)
        if len(self._history.get(user_id, [])) < self.max_requests:
            self._history.setdefault(user_id, deque()).append(now)
            return True
        return False

    def time_until_next_allowed(self, user_id: str) -> float:
        now = time.time()
        self._cleanup_window(user_id, now)
        if user_id not in self._history or len(self._history[user_id]) < self.max_requests:
            return 0.0
        return max(0.0, self.window_size - (now - self._history[user_id][0]))


def test_rate_limiter():
    limiter = SlidingWindowRateLimiter(window_size=10, max_requests=1)

    print("\n=== Message stream simulation ===")
    for message_id in range(1, 11):
        user_id = message_id % 5 + 1
        result = limiter.record_message(str(user_id))
        wait_time = limiter.time_until_next_allowed(str(user_id))
        print(
            f"Message {message_id:2d} | User {user_id} | "
            f"{'✓' if result else f'× (wait {wait_time:.1f}s)'}"
        )
        time.sleep(random.uniform(0.1, 1.0))

    print("\nWaiting 4 seconds...")
    time.sleep(4)

    print("\n=== New message series after waiting ===")
    for message_id in range(11, 21):
        user_id = message_id % 5 + 1
        result = limiter.record_message(str(user_id))
        wait_time = limiter.time_until_next_allowed(str(user_id))
        print(
            f"Message {message_id:2d} | User {user_id} | "
            f"{'✓' if result else f'× (wait {wait_time:.1f}s)'}"
        )
        time.sleep(random.uniform(0.1, 1.0))


if __name__ == "__main__":
    test_rate_limiter()
