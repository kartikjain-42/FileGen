import os
import datetime
import mimetypes
from typing import Any, List, Dict, Optional, Union
from pydantic import BaseModel, Field

class ReadFilesArgs(BaseModel):
    paths: List[str] = Field(..., description="List of file or directory paths to read")
    max_size_mb: float = Field(1.0, description="Maximum file size in MB to read")
    include_binary: bool = Field(False, description="Whether to include binary files")
    recursive: bool = Field(True, description="Whether to recursively read directories")

class FileMetadata(BaseModel):
    path: str
    size: int
    modified: str
    mime_type: str
    is_binary: bool

class FileResult(BaseModel):
    metadata: FileMetadata
    content: Optional[str] = None
    error: Optional[str] = None

def get_file_metadata(path: str) -> FileMetadata:
    """Get metadata for a file."""
    stat = os.stat(path)
    mime_type, _ = mimetypes.guess_type(path)
    
    # Default to text/plain if mime_type is None
    if mime_type is None:
        mime_type = "text/plain"
    
    # Check if file is binary
    is_binary = mime_type and not mime_type.startswith(('text/', 'application/json'))
    
    return FileMetadata(
        path=path,
        size=stat.st_size,
        modified=datetime.datetime.fromtimestamp(stat.st_mtime).isoformat(),
        mime_type=mime_type or "application/octet-stream",
        is_binary=is_binary
    )

def read_file_content(path: str, max_size_bytes: int, include_binary: bool) -> FileResult:
    """Read content from a file with error handling and size limits."""
    try:
        metadata = get_file_metadata(path)
        
        # Check file size
        if metadata.size > max_size_bytes:
            return FileResult(
                metadata=metadata,
                error=f"File exceeds maximum size limit of {max_size_bytes/1024/1024:.2f}MB"
            )
        
        # Skip binary files if not included
        if metadata.is_binary and not include_binary:
            return FileResult(
                metadata=metadata,
                error="Binary file skipped (set include_binary=true to read)"
            )
        
        # Read file content
        try:
            # Try UTF-8 first
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            # If binary file is allowed, read as base64
            if include_binary:
                import base64
                with open(path, "rb") as f:
                    binary_content = f.read()
                content = f"[BASE64 ENCODED BINARY DATA: {base64.b64encode(binary_content).decode('ascii')}]"
            else:
                return FileResult(
                    metadata=metadata,
                    error="File contains non-UTF-8 characters"
                )
                
        return FileResult(metadata=metadata, content=content)
    except Exception as e:
        # Create minimal metadata for error case
        try:
            metadata = get_file_metadata(path)
        except:
            # If we can't even get metadata, create a minimal version
            metadata = FileMetadata(
                path=path,
                size=0,
                modified=datetime.datetime.now().isoformat(),
                mime_type="unknown",
                is_binary=False
            )
        
        return FileResult(
            metadata=metadata,
            error=f"Error reading file: {str(e)}"
        )

def walk_directory(path: str, max_size_bytes: int, include_binary: bool, recursive: bool) -> List[FileResult]:
    """Walk a directory and read all files."""
    result = []
    
    if recursive:
        # Recursive walk
        for root, _, files in os.walk(path):
            for file in files:
                full_path = os.path.join(root, file)
                result.append(read_file_content(full_path, max_size_bytes, include_binary))
    else:
        # Non-recursive - only top level
        for item in os.listdir(path):
            full_path = os.path.join(path, item)
            if os.path.isfile(full_path):
                result.append(read_file_content(full_path, max_size_bytes, include_binary))
    
    return result

async def read_files(args: ReadFilesArgs) -> Dict[str, Any]:
    """Read files from specified paths with robust error handling."""
    paths: List[str] = args.paths
    max_size_bytes = int(args.max_size_mb * 1024 * 1024)  # Convert MB to bytes
    include_binary = args.include_binary
    recursive = args.recursive

    if not paths:
        return {
            "status": "error",
            "message": "No paths provided."
        }

    all_files = []
    errors = []

    for p in paths:
        try:
            # Normalize path
            norm_path = os.path.normpath(os.path.abspath(p))
            
            if os.path.isdir(norm_path):
                dir_files = walk_directory(norm_path, max_size_bytes, include_binary, recursive)
                all_files.extend(dir_files)
            elif os.path.isfile(norm_path):
                all_files.append(read_file_content(norm_path, max_size_bytes, include_binary))
            else:
                errors.append(f"Path not found: {p}")
                all_files.append(FileResult(
                    metadata=FileMetadata(
                        path=p,
                        size=0,
                        modified=datetime.datetime.now().isoformat(),
                        mime_type="unknown",
                        is_binary=False
                    ),
                    error=f"Path not found: {p}"
                ))
        except Exception as e:
            errors.append(f"Error processing path '{p}': {str(e)}")
            all_files.append(FileResult(
                metadata=FileMetadata(
                    path=p,
                    size=0,
                    modified=datetime.datetime.now().isoformat(),
                    mime_type="unknown",
                    is_binary=False
                ),
                error=f"Error processing path: {str(e)}"
            ))

    # Convert to dict for JSON serialization
    serializable_files = [file.model_dump() for file in all_files]
    
    return {
        "status": "success" if not errors else "partial_success",
        "files": serializable_files,
        "errors": errors if errors else None,
        "file_count": len(all_files),
        "success_count": sum(1 for f in all_files if f.error is None)
    }
