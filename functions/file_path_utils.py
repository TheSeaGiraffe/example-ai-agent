import os


def is_file_outside_workdir(working_dir: str, file_path: str) -> bool:
    """Check if the file path is inside of the working directory.

    Parameters
    ----------
    working_dir: str
        Path to the working directory
    file_path: str
        Path to a file in the working directory

    Returns
    -------
    bool
        A boolean that indicates whether file_path is actually in the working directory.
    """
    working_dir_abs = os.path.abspath(working_dir)
    full_path_abs = os.path.abspath(os.path.join(working_dir, file_path))
    common_path = os.path.commonpath([working_dir_abs, full_path_abs])

    return not (
        common_path == working_dir_abs
        and full_path_abs.startswith(working_dir_abs + os.sep)
        or full_path_abs == working_dir_abs
    )
