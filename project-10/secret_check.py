import os


EXPECTED_TOKEN = "DUMMY_TOKEN_12345"


def check_from_env_file():
    """Try to read the token from a local .env file.

    Returns:
        dict with 'success', 'source', and 'token' or 'error'.
    """
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    try:
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("DUMMY_TOKEN="):
                    token = line.split("=", 1)[1]
                    return {"success": True, "source": "local .env file", "token": token}
        return {"success": False, "source": "local .env file", "error": "DUMMY_TOKEN not found in .env"}
    except FileNotFoundError:
        return {"success": False, "source": "local .env file", "error": ".env file not found"}


def check_from_environment():
    """Read the token from environment variables.

    Returns:
        dict with 'success', 'source', and 'token' or 'error'.
    """
    token = os.environ.get("DUMMY_TOKEN")
    if token:
        return {"success": True, "source": "environment variable", "token": token}
    return {"success": False, "source": "environment variable", "error": "DUMMY_TOKEN not set in environment"}


def verify_token(token):
    """Verify the token matches the expected value.

    Args:
        token: The token to verify.

    Returns:
        dict with 'success' and 'message'.
    """
    if token == EXPECTED_TOKEN:
        return {"success": True, "message": "Token verified successfully"}
    return {"success": False, "message": f"Token mismatch: got '{token}'"}


def run(use_env_var=False):
    """Execute the secret check routine.

    Args:
        use_env_var: If True, read from environment variables.
                     If False, read from local .env file.

    Returns:
        dict with full result including status and task_succeeded.
    """
    if use_env_var:
        result = check_from_environment()
    else:
        result = check_from_env_file()

    if not result["success"]:
        return {
            "status": "completed",
            "task_succeeded": False,
            "method": "env_var" if use_env_var else "env_file",
            "result": result,
            "verification": None,
        }

    verification = verify_token(result["token"])
    return {
        "status": "completed",
        "task_succeeded": verification["success"],
        "method": "env_var" if use_env_var else "env_file",
        "result": result,
        "verification": verification,
    }
