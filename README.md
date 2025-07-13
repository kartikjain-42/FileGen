# 🚀 FileGen MCP Server

A **Model Context Protocol (MCP)** server designed to read, write, delete files, create project structures, and run system commands — perfect for automating backend workflows or agent integrations.

---

## ✨ Features

* 📂 **Read Files**: Read individual files or recursively read entire directories.
* 🏗️ **Initialize Projects**: Generate custom project structures from template definitions.
* 📝 **Write Files**: Create new files or append content to existing ones.
* ❌ **Delete Files**: Remove unwanted files or folders.
* 💻 **Execute Commands**: Run terminal commands using Python subprocess.

---

## 🛠️ Available Tools

### 🔹 `read_files`

Reads one or more files/directories from the local filesystem.

**Parameters:**

* `paths` (List\[str]): List of file/directory paths to read.

**Returns:**
Status with file contents or error messages.

---

### 🔹 `init_project`

Generates a directory structure with streaming progress updates.

**Parameters:**

* `name` (str): Project name.
* `path` (str, optional): Base path (defaults to current working directory).
* `structure` (Dict\[str, Any]): Nested dictionary defining folders/files.

---

### 🔹 `write_file`

Creates or appends content to a file.

**Parameters:**

* `path` (str): Target file path.
* `content` (str): Content to write.
* `mode` (str, optional): `"w"` for overwrite or `"a"` for append (default: `"w"`).

---

### 🔹 `delete_path`

Deletes a file or directory.

**Parameters:**

* `path` (str): Target path to delete.

---

### 🔹 `execute_command`

Executes a shell command using Python subprocess.

**Parameters:**

* `params` (Dict\[str, Any]): Command and arguments to execute.

---

## ⚙️ Installation

1. Install dependencies:

   ```bash
   uv sync
   ```

2. Run the MCP server:

   ```bash
   uv run python src/main.py
   ```

---

## 📜 Bash Script Setup

For convenience, use the `setup_and_run.sh` script to configure and launch the MCP server:

### ✅ Steps:

1. Ensure Python 3 is installed.

2. Make the script executable:

   ```bash
   chmod +x setup_and_run.sh
   ```

3. Run the script:

   ```bash
   ./setup_and_run.sh
   ```

### 🧰 What It Does:

* Checks for Python and `uv`, installs `uv` if missing.
* Sets up a virtual environment via `uv`.
* Installs dependencies from `pyproject.toml`.
* Generates a default `config.json` via `setup_config.py`.
* Launches the MCP server.

---

## 🧩 Configuration

A `config.json` file will be automatically generated when you run the script.

To manually integrate with your agent system, ensure the `cwd` field points to the correct project path.

💡 Tip: Include the project path in your prompt to the LLM so it knows where to create files.

Example:

```json
{
  "mcpServers": {
    "project": {
      "command": "uv",
      "args": ["run", "python", "src/main.py"],
      "cwd": "/your/absolute/path/project",
      "env": {
        "PYTHONPATH": "/your/absolute/path/project/src"
      }
    }
  }
}
```

---

## 📁 Project Structure

```
project/
├── src/
│   ├── main.py               # MCP server entry point
│   ├── actions/
│   │   ├── read_files.py     # Reads files/directories
│   │   ├── init_project.py   # Project structure creation
│   │   ├── delete_file.py    # File deletion tool
│   │   └── execute_command.py# System command execution
│   └── schemas/
│       └── project_structure.py  # Pydantic models for structure definitions
└── setup_and_run.sh          # Bootstrap script
```

