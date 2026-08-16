# Loop Engineering

A collection of projects from the Loop Engineering course.

## Projects

| Project | Description | Status |
|---------|-------------|--------|
| [Project 01](project-01/) | In-Session Completion Loop | Completed |
| [Project 02](project-02/) | Retry/Timeout Loop | Completed |
| [Project 03](project-03/) | Periodic Task Loop | Completed |
| [Project 04](project-04/) | Worker Queue Loop | Completed |
| [Project 05](project-05/) | Exponential Backoff Loop | Completed |
| [Project 06](project-06/) | Circuit Breaker Loop | Completed |
| [Project 07](project-07/) | Rate Limiting Loop | Completed |
| [Project 08](project-08/) | Health Check / Watchdog Loop | Completed |
| [Project 09](project-09/) | Routine Success vs Failure Drill | Completed |
| [Project 10](project-10/) | Secrets and Environment Variables Drill | Completed |
| [Project 11](project-11/) | Human Gate and Maker-Checker Pattern Drill | Completed |
| [Project 12](project-12/) | Evidence-Based Improvement Loop Capstone | Completed |

## Project 01 — In-Session Completion Loop

**Location:** `project-01/`

**What it does:**
- Simulates a long-running task that waits 2 minutes
- Monitors task completion using a polling loop
- Detects when the task finishes and exits cleanly

**Files:**
- `long_task.py` - Waits 2 minutes, then creates `done.txt`
- `loop.py` - Monitors for `done.txt` every 60 seconds
- `README.md` - Detailed project documentation

**How to run:**
```bash
# Terminal 1: Start the long-running task
cd project-01
python long_task.py

# Terminal 2: Start the monitoring loop
cd project-01
python loop.py
```

**Success criteria:**
- ✅ Task creates `done.txt` after 2 minutes
- ✅ Loop checks every minute
- ✅ Loop detects completion and prints success
- ✅ Loop exits cleanly
- ✅ Ctrl+C handled gracefully

## Project 02 — Retry/Timeout Loop

**Location:** `project-02/`

**What it does:**
- Simulates an unreliable operation that fails randomly
- Retries the operation up to N times with a delay between attempts
- Enforces a total timeout to prevent infinite retries
- Reports success/failure with clear status messages

**Files:**
- `flaky_task.py` - Simulates an unreliable operation (~50% failure rate)
- `retry_loop.py` - Retry loop with max attempts and timeout
- `test_retry.py` - Unit tests for success, failure, and timeout conditions
- `README.md` - Detailed project documentation

**How to run:**
```bash
cd project-02
python retry_loop.py
```

**Success criteria:**
- ✅ Retries on failure up to max attempts
- ✅ Enforces total timeout
- ✅ Reports success when task eventually succeeds
- ✅ Reports failure when all attempts exhausted
- ✅ Reports timeout when limit reached
- ✅ Ctrl+C handled gracefully
- ✅ All tests pass

## Project 03 — Periodic Task Loop

**Location:** `project-03/`

**What it does:**
- Runs a simulated task at fixed intervals (every 5 seconds)
- Tracks execution history (success/failure per run)
- Handles errors gracefully without stopping the loop
- Reports summary when all runs complete

**Files:**
- `scheduled_task.py` - Simulates a periodic task (~30% failure rate)
- `periodic_loop.py` - Scheduling loop with fixed interval and max runs
- `test_periodic.py` - Unit tests for success, failure, and mixed scenarios
- `README.md` - Detailed project documentation

**How to run:**
```bash
cd project-03
python periodic_loop.py
```

**Success criteria:**
- ✅ Runs task at fixed intervals
- ✅ Tracks success/failure history
- ✅ Handles errors without stopping the loop
- ✅ Reports summary after all runs
- ✅ Ctrl+C handled gracefully
- ✅ All tests pass

## Project 04 — Worker Queue Loop

**Location:** `project-04/`

**What it does:**
- Produces work items into a thread-safe queue
- Dispatches items to multiple worker threads for processing
- Tracks success/failure per item
- Shuts down workers gracefully with sentinel value

**Files:**
- `work_item.py` - Simulates processing a work item (~20% failure rate)
- `worker.py` - Worker function that pulls from queue and processes items
- `queue_loop.py` - Main loop: produces items, starts workers, collects results
- `test_queue.py` - Unit tests for task processing, worker, and queue loop
- `README.md` - Detailed project documentation

**How to run:**
```bash
cd project-04
python queue_loop.py
```

**Success criteria:**
- ✅ Produces items into queue
- ✅ Workers process items concurrently
- ✅ Tracks success/failure per item
- ✅ Graceful shutdown with sentinel
- ✅ Reports summary after all items processed
- ✅ Ctrl+C handled gracefully
- ✅ All tests pass

## Project 05 — Exponential Backoff Loop

**Location:** `project-05/`

**What it does:**
- Simulates an unreliable service call that fails frequently
- Retries with exponential backoff (delay doubles each attempt)
- Adds jitter to prevent thundering herd problems
- Enforces max backoff cap and total timeout

**Files:**
- `flaky_service.py` - Simulates an unreliable service call (~60% failure rate)
- `backoff_loop.py` - Retry loop with exponential backoff, jitter, and timeout
- `test_backoff.py` - Unit tests for success, failure, timeout, and backoff behavior
- `README.md` - Detailed project documentation

**How to run:**
```bash
cd project-05
python backoff_loop.py
```

**Success criteria:**
- ✅ Retries with exponentially increasing delays
- ✅ Jitter prevents synchronized retries
- ✅ Max backoff cap prevents runaway delays
- ✅ Total timeout stops retries
- ✅ Reports success with attempt count and delays
- ✅ Reports failure when all attempts exhausted
- ✅ Reports timeout when limit reached
- ✅ Ctrl+C handled gracefully
- ✅ All tests pass

## Project 06 — Circuit Breaker Loop

**Location:** `project-06/`

**What it does:**
- Implements the Circuit Breaker pattern to protect against cascading failures
- Monitors consecutive failures and trips the circuit open when threshold is reached
- Rejects calls immediately when circuit is open (fail-fast)
- Transitions to HALF_OPEN after cooldown to test if service recovered
- Resets to CLOSED on successful test call, or reopens on failure

**Files:**
- `api_service.py` - Simulates an unreliable API service (~70% failure rate)
- `circuit_breaker.py` - CircuitBreaker class with state management and `circuit_loop()`
- `test_circuit.py` - Unit tests for the API service, circuit breaker states, and transitions
- `README.md` - Detailed project documentation

**How to run:**
```bash
cd project-06
python circuit_breaker.py
```

**Success criteria:**
- ✅ Circuit trips open after failure threshold is reached
- ✅ Calls are rejected when circuit is open (fail-fast)
- ✅ Circuit transitions to HALF_OPEN after cooldown expires
- ✅ Successful test call resets circuit to CLOSED
- ✅ Failed test call reopens circuit to OPEN
- ✅ State history is tracked
- ✅ Ctrl+C handled gracefully
- ✅ All tests pass

## Project 07 — Rate Limiting Loop

**Location:** `project-07/`

**What it does:**
- Implements the Token Bucket algorithm to control request throughput
- Refills tokens at a fixed rate up to a maximum bucket capacity
- Each API call consumes one token; throttles when bucket is empty
- Tracks success, failure, and throttled requests

**Files:**
- `api_service.py` - Simulated API service (~55% success, ~20% rate-limited, ~25% server error)
- `rate_limiter.py` - `TokenBucket` class with token management and `rate_limit_loop()`
- `test_rate_limit.py` - Unit tests for the API service, token bucket, and rate limiting loop
- `README.md` - Detailed project documentation

**How to run:**
```bash
cd project-07
python rate_limiter.py
```

**Success criteria:**
- ✅ Token bucket starts full at capacity
- ✅ Tokens refill at a fixed rate over time
- ✅ Requests consume tokens when available
- ✅ Requests are throttled when tokens are depleted
- ✅ Refill caps at bucket capacity
- ✅ Server errors are tracked separately from throttling
- ✅ History of consumed/throttled events is recorded
- ✅ Ctrl+C handled gracefully
- ✅ All tests pass

## Project 08 — Health Check / Watchdog Loop

**Location:** `project-08/`

**What it does:**
- Monitors a service's health using periodic checks
- Tracks state transitions between HEALTHY, DEGRADED, and UNHEALTHY
- Triggers automatic recovery when the service becomes unhealthy
- Requires consecutive successful checks to recover (prevents flapping)

**Files:**
- `health_service.py` - Simulated health check service (~60% healthy, ~20% degraded, ~20% unreachable) with recovery action
- `health_monitor.py` - `HealthMonitor` class with state management and `watchdog_loop()`
- `test_health.py` - Unit tests for the health service, monitor states, transitions, and recovery
- `README.md` - Detailed project documentation

**How to run:**
```bash
cd project-08
python health_monitor.py
```

**Success criteria:**
- ✅ Starts in HEALTHY state
- ✅ Transitions to DEGRADED on slow responses
- ✅ Transitions to UNHEALTHY after failure threshold reached
- ✅ Triggers automatic recovery on UNHEALTHY
- ✅ Requires consecutive successes to recover (anti-flapping)
- ✅ Failure count resets on successful check
- ✅ Recovery count resets on failure
- ✅ State history is tracked
- ✅ Ctrl+C handled gracefully
- ✅ All tests pass

## Project 09 — Routine Success vs Failure Drill

**Location:** `project-09/`

**What it does:**
- Demonstrates that a green (completed) status does not guarantee task success
- Runs a file summarizer routine against an existing file (success) and a missing file (failure)
- Captures transcripts showing infrastructure status vs task result
- Teaches the key lesson: always verify the transcript, not just the status column

**Files:**
- `routine.py` - File summarizer routine that reads a file and reports stats
- `run_routine.py` - One-off runner that executes the routine and captures a transcript
- `sample_data.txt` - Sample file for the successful run
- `transcript_success.txt` - Transcript from the successful run
- `transcript_failure.txt` - Transcript from the failed run
- `README.md` - Detailed project documentation

**How to run:**
```bash
cd project-09
python run_routine.py sample_data.txt
python run_routine.py missing-file-that-does-not-exist.txt
```

**Success criteria:**
- ✅ Successful run produces transcript with SUCCESS task result
- ✅ Failed run produces transcript with FAILURE task result
- ✅ Both runs show GREEN infrastructure status
- ✅ Transcripts are saved and verifiable
- ✅ Key lesson is demonstrated

## Project 10 — Secrets and Environment Variables Drill

**Location:** `project-10/`

**What it does:**
- Demonstrates why secrets should be supplied via environment variables, not local `.env` files
- Shows that gitignored `.env` files never reach GitHub or cloud clones
- Runs a token verification routine in two modes: local file and environment variable
- Captures transcripts showing the mechanical reason for failure

**Files:**
- `.env` - Dummy token file (gitignored, not committed)
- `.gitignore` - Excludes `.env` from version control
- `secret_check.py` - Token verification routine with two modes
- `run_check.py` - Runner with transcript capture
- `transcript_env_file.txt` - Transcript from the local .env run
- `transcript_cloud_sim.txt` - Transcript from the simulated cloud run (no .env)
- `transcript_env_var.txt` - Transcript from the environment variable run
- `README.md` - Detailed project documentation

**How to run:**
```bash
cd project-10
python run_check.py env_file
python run_check.py env_var
```

**Success criteria:**
- ✅ `.env` file contains dummy token
- ✅ `.gitignore` excludes `.env`
- ✅ Local .env run succeeds (works locally)
- ✅ Cloud simulation run fails (no .env available)
- ✅ Environment variable run succeeds
- ✅ Transcripts capture both outcomes
- ✅ Key lesson is demonstrated

## Project 11 — Human Gate and Maker-Checker Pattern Drill

**Location:** `project-11/`

**What it does:**
- Demonstrates the human gate and maker-checker pattern
- Routine A (Maker) creates a reviewable artifact
- Routine B (Checker) processes it only after explicit human approval
- Routine B is protected by a bearer token API trigger
- State file tracks workflow progress

**Files:**
- `maker.py` - Routine A: creates a draft summary artifact
- `checker.py` - Routine B: processes the artifact after human approval + valid token
- `run_routine.py` - Runner for both routines with transcript capture
- `.gitignore` - Excludes tokens, state, and output files
- `transcripts/` - Saved transcripts from each run
- `README.md` - Detailed project documentation

**How to run:**
```bash
cd project-11
python run_routine.py maker
python run_routine.py approve
python run_routine.py token
python run_routine.py checker <token>
```

**Success criteria:**
- ✅ Routine A creates a reviewable artifact
- ✅ Routine B is blocked without human approval
- ✅ Routine B is denied with invalid token
- ✅ Routine B succeeds only with valid token + approval
- ✅ Transcripts capture all outcomes
- ✅ Bearer token is not committed or exposed
- ✅ Key lesson is demonstrated

## Course Structure

This folder contains projects organized by number:
- `project-01/` - Project 01 files
- `project-02/` - Project 02 files
- `project-03/` - Project 03 files
- `project-04/` - Project 04 files
- `project-05/` - Project 05 files
- `project-06/` - Project 06 files
- `project-07/` - Project 07 files
- `project-08/` - Project 08 files
- `project-09/` - Project 09 files
- `project-10/` - Project 10 files
- `project-11/` - Project 11 files
- `project-12/` - Project 12 files
- etc.

Each project is independently runnable and self-contained within its folder.