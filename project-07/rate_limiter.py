import time
import sys
from api_service import call

MAX_CALLS = 15
RATE_LIMIT = 3
BUCKET_SIZE = 5


class TokenBucket:
    """Token bucket rate limiter.

    Tokens refill at a fixed rate up to the bucket size.
    Each request consumes one token. If no token is available,
    the request is throttled.
    """

    def __init__(self, rate, capacity):
        self.rate = rate
        self.capacity = capacity
        self.tokens = capacity
        self.last_refill = time.time()
        self.history = []

    def _refill(self):
        now = time.time()
        elapsed = now - self.last_refill
        new_tokens = elapsed * self.rate
        if new_tokens > 0:
            self.tokens = min(self.capacity, self.tokens + new_tokens)
            self.last_refill = now

    def consume(self):
        self._refill()
        if self.tokens >= 1:
            self.tokens -= 1
            self._record("consumed", f"tokens={self.tokens:.1f}")
            return True
        self._record("throttled", f"tokens={self.tokens:.1f}")
        return False

    def _record(self, event, detail=""):
        self.history.append({"event": event, "detail": detail})


def rate_limit_loop():
    """Send requests through the rate limiter.

    Returns:
        dict with success/failure counts and request history.
    """
    bucket = TokenBucket(RATE_LIMIT, BUCKET_SIZE)
    results = []

    print(f"Rate limiting loop started.")
    print(f"  Rate: {RATE_LIMIT} tokens/sec, Bucket: {BUCKET_SIZE} tokens, Max calls: {MAX_CALLS}")

    for i in range(1, MAX_CALLS + 1):
        if bucket.consume():
            try:
                result = call()
                results.append({"attempt": i, "success": True, "message": result["message"]})
                print(f"  Call {i:2d}: OK - {result['message']}")
            except (RuntimeError, ConnectionError) as e:
                results.append({"attempt": i, "success": False, "message": str(e)})
                print(f"  Call {i:2d}: FAIL - {e}")
        else:
            results.append({"attempt": i, "success": False, "message": "Rate limited"})
            print(f"  Call {i:2d}: THROTTLED - no tokens available")

    succeeded = sum(1 for r in results if r["success"])
    failed = sum(1 for r in results if not r["success"])
    throttled = sum(1 for r in results if r["message"] == "Rate limited")

    print(f"\nRate limiting loop finished.")
    print(f"  Results: {succeeded} succeeded, {failed} failed ({throttled} rate-limited)")

    return {
        "succeeded": succeeded,
        "failed": failed,
        "throttled": throttled,
        "results": results,
        "history": bucket.history,
    }


if __name__ == "__main__":
    try:
        summary = rate_limit_loop()
        if summary["throttled"] > 0:
            print(f"  {summary['throttled']} call(s) were rate-limited.")
    except KeyboardInterrupt:
        print("\nRate limiting loop stopped by user.")
        sys.exit(0)
