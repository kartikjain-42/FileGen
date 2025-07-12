import os
import shutil

def delete_path(path: str) -> None:
    """
    Delete the specified file or directory.
    """
    if os.path.isfile(path):
        os.remove(path)
    elif os.path.isdir(path):
        shutil.rmtree(path)
    else:
        raise FileNotFoundError(f"The path {path} does not exist.")