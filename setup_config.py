import json
import os
import sys

TEMPLATE = {
    "mcpServers": {
        "filegen": {
            "command": "",
            "args": ["run", "python"],
            "cwd": "",
            "env": {
                "PYTHONPATH": ""
            }
        }
    }
}

def main():
    if len(sys.argv) < 3:
        print("Project path and/or uv path not provided by the shell script.")
        return

    project_path = sys.argv[1]
    uv_path = sys.argv[2]

    print(f"📁 Using project path: {project_path}")
    print(f"Using uv at: {uv_path}")

    if not os.path.isdir(project_path):
        print("The provided path is not valid.")
        return

    config = TEMPLATE.copy()
    main_path = os.path.join(project_path, "src/main.py")
    python_path = os.path.join(project_path, "src")

    if not os.path.isfile(main_path):
        print("The provided path does not contain src/main.py.")
        return

    config["mcpServers"]["filegen"]["cwd"] = project_path
    config["mcpServers"]["filegen"]["args"].append(main_path)
    config["mcpServers"]["filegen"]["env"]["PYTHONPATH"] = python_path
    config["mcpServers"]["filegen"]["command"] = uv_path

    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    with open(config_path, "w") as f:
        json.dump(config, f, indent=4)

    print(f"config.json generated successfully at {config_path}")

if __name__ == "__main__":
    main()
