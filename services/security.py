from collections import defaultdict
import time

class RateLimiter:
    def __init__(self, max_requests: int, time_window: int):
        self.max_requests = max_requests  # Maximum requests allowed
        self.time_window = time_window    # Time window in seconds
        self.requests = defaultdict(list) # Stores timestamps of requests per user

    def allow_request(self, user_id: str) -> bool:
        current_time = time.time()
        # Remove old requests outside the time window
        self.requests[user_id] = [t for t in self.requests[user_id] if current_time - t < self.time_window]

        if len(self.requests[user_id]) < self.max_requests:
            self.requests[user_id].append(current_time)
            return True
        else:
            return False

class AntiSpamService:
    def __init__(self, max_messages_per_minute=10):
        self.rate_limiter = RateLimiter(max_messages_per_minute, 60) # 10 messages per minute

    def is_spam(self, user_id: str) -> bool:
        return not self.rate_limiter.allow_request(user_id)
