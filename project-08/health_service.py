import random

HEALTHY_RATE = 0.6
SLOW_RATE = 0.2
WORK_TIME = 0.5


def check():
    """Simulate a health check that may succeed, be slow, or fail.

    Returns:
        dict with 'status', 'response_time', and 'message'.

    Raises:
        ConnectionError: When the service is unreachable.
    """
    roll = random.random()

    if roll < HEALTHY_RATE:
        return {
            "status": "healthy",
            "response_time": round(random.uniform(0.01, 0.1), 3),
            "message": "Service is healthy",
        }
    elif roll < HEALTHY_RATE + SLOW_RATE:
        return {
            "status": "degraded",
            "response_time": round(random.uniform(1.0, 3.0), 3),
            "message": "Service is slow",
        }
    else:
        raise ConnectionError("Service unreachable")


def recover():
    """Simulate a recovery action (restart the service).

    Returns:
        dict with 'status' and 'message'.
    """
    success = random.random() < 0.7
    if success:
        return {"status": "recovered", "message": "Service restarted successfully"}
    else:
        return {"status": "failed", "message": "Recovery attempt failed"}
