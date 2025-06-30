import subprocess
from pathlib import Path

from .file_path_utils import is_file_outside_workdir


def run_python_file(working_directory: str, file_path: str) -> str:
    """Execute a python file.

    Parameters
    ----------
    working_directory: str
    file_path: str

    Returns
    -------
    str
        On a successful execution, returns a string containing information about the
        process, specifically:

        - Any output from `stdout`, prefixed by `STDOUT:`
        - Any output from `stderr`, prefixed by `STDERR:`

        On error, returns an appropriate error message.
    """

    final_path = Path(working_directory).joinpath(file_path)

    # Check if file exists
    if not final_path.exists():
        return f'Error: File "{file_path}" not found.'

    # Check if file is in working directory
    if is_file_outside_workdir(working_directory, file_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    # Check if file ends in `.py`
    if final_path.suffix != ".py":
        return f'Error: "{file_path}" is not a Python file.'

    # Run file
    try:
        proc_results = subprocess.run(
            ["python", str(final_path)], capture_output=True, timeout=30, check=True
        )

        results_str = ""
        if proc_results.stderr or proc_results.stdout:
            if proc_results.stdout:
                results_str += f"STDOUT: {proc_results.stdout.decode()}"
            if proc_results.stderr:
                results_str += f"STDERR: {proc_results.stderr.decode()}"
        else:
            results_str = "No output produced"

        if proc_results.returncode != 0:
            results_str += f"Process exited with code {proc_results.returncode} "

        return results_str
    except Exception as e:
        return f"Error: executing Python file: {e}"
