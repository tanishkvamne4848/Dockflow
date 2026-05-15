import subprocess
import logging

def run_cmd(cmd, msg, timeout=600, log_file=None):
    """
    Safe subprocess wrapper for external bioinformatics tools.
    Supports saving stdout to a file (needed for Vina logs).
    """
    try:
        logging.info(f"Running: {' '.join(cmd)}")

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        if result.returncode != 0:
            logging.error(f"{msg}\nSTDERR:\n{result.stderr}")
            raise RuntimeError(msg)

        # ✅ NEW: save stdout if log_file provided
        if log_file:
            with open(log_file, "w") as f:
                f.write(result.stdout)

        return result.stdout

    except subprocess.TimeoutExpired:
        logging.error(f"{msg}: TIMEOUT after {timeout}s")
        raise RuntimeError(f"Timeout: {msg}")

    except Exception as e:
        logging.error(f"{msg}: {str(e)}")
        raise