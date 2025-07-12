from typing import Union, Dict
from pydantic import field_validator, RootModel
import os

FileContent = str

class FileNode(RootModel[Union[FileContent, Dict[str, 'FileNode']]]):
    root: Union[FileContent, Dict[str, 'FileNode']]

    @field_validator('root')
    @classmethod
    def not_empty(cls, v):
        if isinstance(v, str) and not v.strip():
            raise ValueError("File content cannot be empty")
        return v

def get_project_structure(directory: str) -> Dict[str, Union[str, Dict]]:
    """
    Traverse the directory and return a dictionary representing the project structure,
    excluding directories that start with '.'.
    """
    structure = {}
    for root, dirs, files in os.walk(directory):
        # Modify dirs in-place to skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        path = root.split(os.sep)
        parent = structure
        for folder in path:
            parent = parent.setdefault(folder, {})
        for file in files:
            parent[file] = 'file'
    return structure
