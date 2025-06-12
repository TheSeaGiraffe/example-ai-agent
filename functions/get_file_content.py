from pathlib import Path

MAX_CONTENT_LENGTH = 10000


def get_file_content(working_directory: str, file_path: str) -> str:
    """Return the contents of the specified file.

    Assumes that `file_path` is within the `working_directory`. Any returned file
    content is limited to 10000 characters in order to avoid running into API usage
    limits.

    Parameters
    ----------
    working_directory: str
        The path to the working directory
    file_path: str
        Path to a file inside the working directory

    Returns
    -------
    """
    final_path = Path(working_directory).joinpath(file_path.strip("/"))

    # Check if file_path is outside of working_directory
    if not (final_path.exists() and ".." not in str(final_path)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    # Check if file path is not a file
    if not final_path.is_file():
        return f'Error: File not found or is not a regular file: "{file_path}"'

    # Read file and return contents as string
    try:
        with open(final_path) as fp:
            file_content = fp.read()
        if len(file_content) > MAX_CONTENT_LENGTH:
            file_content = f'{file_content[:MAX_CONTENT_LENGTH]}...File "{file_path}" truncated at {MAX_CONTENT_LENGTH} characters'
        return file_content
    except Exception as e:
        return f'Error: Could not read file "{file_path}": {e}'
