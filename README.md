# 🚀 FileGen MCP Server

**FileGen MCP Server** is a lightweight Model Context Protocol (MCP) server built to automate file handling, project initialization, and command execution — enabling seamless integration with LLM-based coding workflows.

## 🧠 Why FileGen?

When LLMs generate code and project structures, the developer often has to manually create folders, files, and paste code — a repetitive and time-consuming process.

**FileGen MCP Server** eliminates this friction by letting agents or tools directly:

* Create files/folders
* Write and delete content
* Generate project structures
* Execute terminal commands

It’s the perfect backend utility for building smarter, faster, AI-assisted development pipelines.

---

## ✨ Features

* 📂 **Read Files**: Read individual files or recursively scan directories.
* 🏗️ **Initialize Projects**: Generate complete directory structures from templates.
* 📝 **Write Files**: Create or append content to files.
* ❌ **Delete Files**: Remove unnecessary files or folders.
* 💻 **Execute Commands**: Run system commands via Python subprocess.

---

## 🛠️ Available Tools

### 🔹 `read_files`

Reads one or more files/directories from the local filesystem.

**Parameters:**

* `paths` (List\[str]): List of file/directory paths to read.

---

### 🔹 `init_project`

Generates a folder/file structure.

**Parameters:**

* `name` (str): Project name.
* `path` (str, optional): Base path (default: system root directory).
* `structure` (Dict\[str, Any]): Nested dictionary defining folders/files.

---

### 🔹 `write_file`

Creates or appends content to a file.

**Parameters:**

* `path` (str): Target file path.
* `content` (str): Content to write.
* `mode` (str, optional): `"w"` (overwrite) or `"a"` (append). Default: `"w"`.

---

### 🔹 `delete_path`

Deletes a file or directory.

**Parameters:**

* `path` (str): Target path to delete.

---

### 🔹 `execute_command`

Executes a shell command.

**Parameters:**

* `params` (Dict\[str, Any]): Command and arguments to execute.

---

## ⚙️ Installation

1. Install dependencies:

   ```bash
   uv sync
   ```

2. Start the server:

   ```bash
   uv run python src/main.py
   ```

---

## 📜 Bash Script Setup

Use the `setup_and_run.sh` script to configure and launch the MCP server in one go.

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

* Verifies Python and `uv` availability.
* Installs `uv` if missing.
* Sets up a virtual environment using `uv`.
* Installs dependencies from `pyproject.toml`.
* Generates a default `config.json`.
* Launches the server.

---

## 🧩 Configuration

A `config.json` file is auto-generated when you run the setup script.

To manually integrate with your agent system, ensure the `cwd` field points to the correct project directory.

💡 **Tip:** Include the project path in your LLM prompt so it knows where to write files.

### Example:

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
│   ├── main.py                 # MCP server entry point
│   ├── actions/
│   │   ├── read_files.py       # Read files/directories
│   │   ├── init_project.py     # Project structure creation
│   │   ├── delete_file.py      # File/folder deletion
│   │   └── execute_command.py  # System command execution
│   └── schemas/
│       └── project_structure.py # Pydantic models for project 
└── setup_and_run.sh            # Bootstrap script
```

