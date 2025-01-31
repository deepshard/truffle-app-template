<div align="right">
<img src="./arrow.svg" width="500" height="220" alt="Use this template arrow">
</div>

# Truffle App Template

## [Check out the docs for a full explanation of the Truffle SDK too](https://itsalltruffles.com)

This template is designed to help you get up and running quickly with Truffle
App development. 

## Set up your project's virtual environment

The Truffle SDK currently is supports CPython 3.10+, but is mainly tested with
3.12+. This template repo supports both [uv](https://docs.astral.sh/uv/) and
[poetry](https://python-poetry.org/docs/), but uv the officially recommended 
tool.

## Install the Truffle SDK in the CLI

```sh
$ uv add truffle-sdk # or replace uv with poetry
```

## Use the SDK's CLI to populate the template
```sh
$ source .venv/bin/activate
(truffle-app-template) $ truffle setup
App Name: YourAppName
Description: What the app does
Example Prompt 1 of 5: ...
``` 

Now you're ready to start hacking at your first Truffle App!

## Truffle Apps for Devs in a Hurry

The general structure of a Truffle App is to have a Python class, that gets passed
to a `truffle.TruffleApp`, which then gets launched with the `.launch()` method.

State is stored in member fields, and methods are decorated with `truffle.tool()` 
to expose them to the Agent.

### A Worked Example: A simple Truffle App for Python programming
```python
from pathlib import Path
import subprocess
import truffle
from typing import List

# PythonSoftwareEngineer acts as a Truffle App that can write, read, and execute code
class PythonSoftwareEngineer:
    """
    A Truffle App that performs common software engineering tasks:
    - Writing Python code to files
    - Reading file contents
    - Executing shell commands
    """
    def __init__(self) -> None:
        # this is the data that the Agent sees when selecting your app
        self.metadata = truffle.AppMetadata(
            name="pythonsoftwareengineer",
            description="Writes and executes Python code to accomplish tasks"
        )
        # Client provides access to LLM capabilities
        self.client = truffle.TruffleClient()

    @truffle.tool(
        description="writes python code to a file",
        icon="pencil.line", # icons for tools are SF Symbol names
    )
    @truffle.args( # this decorator tells the agent about the tool's arguments
        the_code="a string containing the valid python code",
        destination_path="the path to the file",
    )
    def WritePython(self, the_code: str, destination_path: str) -> str:
        """Writes provided Python code to specified file path."""
        file_path = Path(destination_path)
        file_path.write_text(the_code)
        return f"Code written to {file_path.absolute()}"

    @truffle.tool(
        description="reads the contents of a file",
        icon="pencil.line",
    )
    @truffle.args(
        source_path="the path to the file",
    )
    def ReadFile(self, source_path: str) -> str:
        """Reads and returns the contents of a file at the given path."""
        return Path(source_path).read_text()

    @truffle.tool(
        description="Run a command in a the shell",
        icon="apple.terminal"
    )
    @truffle.args(
        cmd_args="The shell command to execute split up as a list of strings, like an argv array",
    )
    def RunCommand(self, cmd_args: List[str]) -> str:
        """
        Executes a shell command safely by accepting pre-split arguments.
        Returns formatted output including exit code, stdout, and stderr.
        """
        cmd_result = subprocess.run(cmd_args, capture_output=True, encoding="utf-8")
        return "\n---\n".join(
            [
                f"Commmand returned exit code {cmd_result.returncode}",
                f"stdout contents: {cmd_result.stdout}",
                f"stderr contents: {cmd_result.stderr}",
            ]
        )

# launch the app when the script is run
if __name__ == "__main__":
    app = truffle.TruffleApp(PythonSoftwareEngineer())
    app.launch()
```

## FAQ

### How are uncaught exceptions handled by the App Executor?

The Truffle App Executor forwards the stacktrace and exception message
to the Agent in the case of an uncaught exception. We encourage developers
to lean on this behavior, as we our Agent is capable of self-correcting tool
use in response to these exceptions.
