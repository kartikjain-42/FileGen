import os
import datetime
from typing import Any, Dict
from pydantic import BaseModel, Field

from schemas.project_structure import FileNode

class InitProjectArgs(BaseModel):
    name: str
    path: str = "."
    structure: Dict[str, Any]

class WriteFileArgs(BaseModel):
    path: str = Field(..., description="Path to the file to write to")
    content: str = Field(..., description="Content to write to the file")
    mode: str = Field("w", description="File mode: 'w' for write/overwrite, 'a' for append")
    create_dirs: bool = Field(True, description="Create parent directories if they don't exist")
    encoding: str = Field("utf-8", description="File encoding")
    overwrite_protection: bool = Field(False, description="Prevent overwriting existing files when mode is 'w'")
    binary: bool = Field(False, description="Treat content as base64 encoded binary data")

def write_structure(base_path: str, node: FileNode):
    root = node.root
    if isinstance(root, str):
        os.makedirs(os.path.dirname(base_path), exist_ok=True)
        with open(base_path, "w", encoding="utf-8") as f:
            f.write(root)
    else:
        os.makedirs(base_path, exist_ok=True)
        for name, child in root.items():
            write_structure(os.path.join(base_path, name), child)

def validate_path(path: str) -> str:
    abs_path = os.path.abspath(path)

    # Create if it doesn't exist
    if not os.path.exists(abs_path):
        try:
            os.makedirs(abs_path, exist_ok=True)
        except Exception as e:
            raise ValueError(f"Cannot create directory '{abs_path}': {e}")

    # Check if writable
    if not os.access(abs_path, os.W_OK):
        raise PermissionError(f"No write permission for '{abs_path}'")

    return abs_path

async def init_project(args: InitProjectArgs) -> str:
    project_name = args.name
    structure = args.structure
    user_path = args.path

    try:
        base_dir = validate_path(user_path)
        target_path = os.path.join(base_dir, project_name)

        parsed = FileNode.model_validate(structure)
        
        write_structure(target_path, parsed)

        return f"✅ Project created at {target_path}"
    except Exception as e:
        return f"❌ Error: {e}"

async def write_file(args: WriteFileArgs) -> Dict[str, Any]:
    """
    Write or append content to a file with enhanced error handling and options.
    
    Features:
    - Path normalization and validation
    - Directory creation (optional)
    - Overwrite protection (optional)
    - Binary file support via base64
    - Detailed error reporting
    """
    try:
        # Normalize path
        norm_path = os.path.normpath(os.path.abspath(args.path))
        
        # Create parent directories if needed and requested
        if args.create_dirs:
            try:
                dir_path = os.path.dirname(norm_path)
                if dir_path:  # Only create if there's a directory component
                    os.makedirs(dir_path, exist_ok=True)
            except Exception as e:
                return {
                    "status": "error",
                    "message": f"Failed to create directories: {e}",
                    "path": args.path,
                    "error_type": "directory_creation_failed"
                }
        
        # Check for overwrite protection
        if args.overwrite_protection and args.mode == 'w' and os.path.exists(norm_path):
            return {
                "status": "error",
                "message": f"File already exists and overwrite_protection is enabled",
                "path": norm_path,
                "error_type": "overwrite_protection"
            }
        
        # Handle binary content
        if args.binary:
            try:
                import base64
                binary_data = base64.b64decode(args.content)
                
                with open(norm_path, args.mode + 'b') as f:  # Binary mode
                    f.write(binary_data)
            except Exception as e:
                return {
                    "status": "error",
                    "message": f"Failed to decode or write binary data: {e}",
                    "path": norm_path,
                    "error_type": "binary_write_failed"
                }
        else:
            # Text mode
            with open(norm_path, args.mode, encoding=args.encoding) as f:
                f.write(args.content)
        
        # Get file stats for the response
        file_stats = os.stat(norm_path)
        
        return {
            "status": "success",
            "message": f"File {'appended to' if args.mode == 'a' else 'written to'} {norm_path}",
            "path": norm_path,
            "size": file_stats.st_size,
            "modified": datetime.datetime.fromtimestamp(file_stats.st_mtime).isoformat(),
            "operation": "append" if args.mode == 'a' else "write"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to write file: {e}",
            "path": args.path,
            "error_type": "write_failed",
            "error_details": str(e)
        }
