from pathlib import Path

from .file_path_utils import is_file_outside_workdir


def write_file(working_directory: str, file_path: str, content: str) -> str:
    """Write contents to a file.

    The should be in the specified file_path in the given working directory.

    Parameters
    ----------
    working_directory: str
        The path to the working directory
    file_path: str
        Path to a file inside the working directory
    content: str
        Text to be written to the specified file

    Returns
    -------
    str
        The following strings will be returned depending on whether any errors were
        encountered:

        - An error message indicating that the file is outside of the working directory
        - An error message indicating that a problem occurred when writing to the file
        - On success, a message indicating a successful write as well as the number of
          characters written to the file
    """
    final_path = Path(working_directory).joinpath(file_path.strip("/"))

    # Check if file path is outside of working directory
    if is_file_outside_workdir(working_directory, file_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    # Create file if it doesn't exist
    final_path.touch()

    # Write to file
    try:
        with open(final_path, "w") as fp:
            fp.write(content)
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except Exception as e:
        return f'Error: Could not write to "{file_path}": {e}'
