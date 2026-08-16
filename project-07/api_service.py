import random

MAX_CALLS = 15


def call():
    """Simulate an API call that may be rate-limited.

    Returns:
        dict with 'status', 'message', and 'data' on success.

    Raises:
        RuntimeError: When the server returns an error.
        ConnectionError: When the request is rate-limited (429).
    """
    roll = random.random()

    if roll < 0.55:
        return {
            "status": "ok",
            "message": "Request successful",
            "data": {"id": random.randint(1000, 9999)},
        }
    elif roll < 0.75:
        raise ConnectionError("Rate limit exceeded (429 Too Many Requests)")
    else:
        raise RuntimeError("Internal server error (500)")
