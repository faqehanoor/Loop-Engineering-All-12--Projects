# Project 06 — Circuit Breaker Loop

## What it does

Implements the Circuit Breaker pattern to protect against cascading failures when calling an unreliable service. The circuit breaker monitors failures and transitions between three states:

- **CLOSED**: Normal operation. Calls pass through; failures are counted.
- **OPEN**: Failure threshold reached. Calls are rejected immediately until a cooldown period expires.
- **HALF_OPEN**: Cooldown expired. One test call is allowed. If it succeeds, the circuit closes. If it fails, the circuit reopens.

## Files

- `api_service.py` - Simulates an unreliable API service (~70% failure rate)
- `circuit_breaker.py` - CircuitBreaker class with state management and `circuit_loop()`
- `test_circuit.py` - Unit tests for the API service, circuit breaker states, and transitions

## How to run

```bash
cd project-06
python circuit_breaker.py
```

## How to test

```bash
cd project-06
python -m pytest test_circuit.py -v
```

## Key concepts

- **Failure threshold**: Number of consecutive failures before the circuit trips open
- **Cooldown period**: Time (in seconds) the circuit stays open before allowing a test call
- **State transitions**: CLOSED -> OPEN -> HALF_OPEN -> CLOSED (or back to OPEN)
- **Fail-fast**: When the circuit is open, calls are rejected immediately without hitting the service
