import os

from strands import tool
from pathlib import Path


ROOT = Path("workspace").resolve()
def _safe(path: str) -> Path:
    p = (ROOT / path).resolve()
    if not str(p).startswith(str(ROOT)):
        raise ValueError("path escapes sandbox")
    return p

@tool
def list_dir(path: str=".") -> str:
    """List files in a sub-directory under the sandbox"""
    try: 
        target = _safe(path)
        if not target.exists():
            return f"Directory not found: {path}"
        if not target.is_dir():
            return f"Not a directory: {path}"
        entries = sorted(target.iterdir(), key=lambda p: p.name.lower())

        if not entries:
            return f"(empty) {path}"
        lines = []
        for entry in entries:
            kind = "dir" if entry.is_dir() else "file"
            lines.append(f"[{kind} {entry.relative_to(ROOT)}]")

        return "\n".join(lines)

    except Exception as e:
        return f"list_dir error: {e}"

@tool
def create_file(file_name: str, content: str = "", path: str = ".") -> str:
    """Create a new text file under the sandbox. Fails if the file already exists.

    Args:
        file_name: Name of the file to create (e.g. 'notes.txt').
        content: Initial file contents (default: empty string).
        path: Relative directory inside the workspace where the file is created (default: '.').
    """
    try:
        target = _safe(str(Path(path) / file_name))
        if target.exists():
            return f"File already exists: {target.relative_to(ROOT)}"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return f"Created: {target.relative_to(ROOT)}"
    except Exception as e:
        return f"create_file error: {e}"

@tool
def delete_file(file_name: str) -> str:
    """
    Delete a file from workspace directory
    Args: filename/path
    """
    try:
        os.remove(str(ROOT/file_name))
        return f"Deleted: {file_name}"
    except Exception as e:
        return f"File not found"

