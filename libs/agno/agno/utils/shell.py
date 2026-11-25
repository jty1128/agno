from agno.utils.log import log_debug, log_info, logger


def run_shell_command(args: list[str], tail: int = 100) -> str:
    log_info(f"Running shell command: {args}")

    import subprocess

    try:
        result = subprocess.run(args, capture_output=True, text=True, check=True)
        log_debug(f"Result: {result}")
        log_debug(f"Return code: {result.returncode}")

        # return only the last n lines of the output
        return "\n".join(result.stdout.split("\n")[-tail:])
    except subprocess.CalledProcessError as e:
        logger.warning(f"Failed to run shell command: {e}")
        return f"Error: {e.stderr}"
    except OSError as e:
        logger.warning(f"Failed to run shell command: {e}")
        return f"Error: {e}"
