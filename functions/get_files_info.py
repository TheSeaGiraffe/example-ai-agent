from pathlib import Path


def get_files_info(working_directory: str, directory: str = None) -> str:
    """Return a list of the objects contained in the specified directory as well as some
    associated info.

    Any directory specified by `directory` must be within the current
    `working_directory`. The information about the objects in the specified directory
    include the size of the object in bytes and whether it is a directory.

    Parameters
    ----------
    working_directory: str
        The path to the working directory
    directory: str
        The name of a directory in the working directory. If None, will just use
        working_directory. Default: None

    Returns
    -------
    str
        A string containing all of the files and directories in 'directory'. The string
        is formatted as a list with the following form:

        - file_or_directory: file_size=int bytes, is_dir=bool
        - ...
    """
    wd_path = Path(working_directory)
    final_dir = wd_path if directory is None else wd_path.joinpath(directory.strip("/"))

    # Check that directory is actually a directory
    if not final_dir.is_dir():
        return f'Error: "{directory}" is not a directory'

    # Check that directory is in working_directory
    # Consider using DeMorgan's Law here
    if not (final_dir.exists() and ".." not in str(final_dir)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    # Get the contents of the specified directory
    try:
        files_str: list[str] = []
        for f in final_dir.iterdir():
            files_str.append(
                f"- {f.name}: file_size={f.stat().st_size} bytes, is_dir={f.is_dir()}"
            )
        return "\n".join(files_str)
    except Exception as e:
        return f"Error: {e}"
