# Project 07 — Rate Limiting Loop

## What it does

Implements the Token Bucket algorithm to control request throughput. A bucket holds a fixed number of tokens that refill at a steady rate. Each API call consumes one token; if no token is available, the call is throttled immediately.

## Files

- `api_service.py` - Simulated API service (~55% success, ~20% rate-limited, ~25% server error)
- `rate_limiter.py` - `TokenBucket` class with token management and `rate_limit_loop()`
- `test_rate_limit.py` - Unit tests for the API service, token bucket, and rate limiting loop

## How to run

```bash
cd project-07
python rate_limiter.py
```

## How to test

```bash
cd project-07
python -m pytest test_rate_limit.py -v
```

## Key concepts

- **Token Bucket**: Tokens refill at a fixed rate (tokens/sec) up to a maximum capacity
- **Consumption**: Each request removes one token; if empty, the request is throttled
- **Refill**: Time-based token replenishment on each consume() call
- **Throttling**: Requests are rejected when no tokens are available
