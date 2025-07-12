import subprocess
from typing import Dict, Any

def execute_command(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Expected input structure for execute_command:
    {
        'params': {
            'command': 'cmd command to execute'
            }
    }
    """
    command = params.get("command")
    if not command:
        return {"error": "No command provided"}

    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        return {"output": result.stdout, "error": result.stderr}
    except subprocess.CalledProcessError as e:
        return {"error": str(e), "output": e.output}