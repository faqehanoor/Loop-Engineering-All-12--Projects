# Loop Engineering Rules

These rules govern how projects in the Loop Engineering course are built and tested.

## Rule 1: Test Isolation
Every project must have its own test file. Tests must not depend on other projects.

## Rule 2: Mock Time Sleep
Always mock time.sleep in tests to keep them fast.

## Rule 3: Ctrl+C Handling
Every main block must handle KeyboardInterrupt gracefully.

## Rule 4: Dict Returns
Loop functions must return a dict with summary counts and history.

## Rule 5: Module Constants
Configuration must use ALL_CAPS module-level constants.

## Rule 6: Single Exception Type
Each project should use exactly one exception type for simulated failures.

## Rule 7: No Classes Unless Required
Prefer functions over classes unless the project requires internal state management.
