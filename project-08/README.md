# Project 08 — Health Check / Watchdog Loop

## What it does

Monitors a service's health using periodic checks, tracks state transitions (HEALTHY → DEGRADED → UNHEALTHY), and automatically triggers recovery when the service becomes unhealthy. Requires consecutive successful checks to recover, preventing flapping between states.

## Files

- `health_service.py` - Simulated health check service (~60% healthy, ~20% degraded, ~20% unreachable) with recovery action
- `health_monitor.py` - `HealthMonitor` class with state management and `watchdog_loop()`
- `test_health.py` - Unit tests for the health service, monitor states, transitions, and recovery

## How to run

```bash
cd project-08
python health_monitor.py
```

## How to test

```bash
cd project-08
python -m pytest test_health.py -v
```

## Key concepts

- **Three-state health model**: HEALTHY, DEGRADED, UNHEALTHY
- **Failure threshold**: Consecutive failures before marking unhealthy
- **Recovery threshold**: Consecutive successes required to recover (prevents flapping)
- **Automatic recovery**: Recovery action triggered when service becomes unhealthy
- **State history**: Full audit trail of all state transitions and events
