# Truffle App Template

## [Check out the docs for a full explanation of the Truffle SDK too](https://itsalltruffles.com)

This template is designed to help you get up and running quickly with Truffle
App development. 

## Set up your project's virtual environment

The Truffle SDK currently is supports CPython 3.10+, but is mainly tested with
3.12+. This template repo supports both [uv](https://docs.astral.sh/uv/) and
[poetry](https://python-poetry.org/docs/), but we really recommend you give uv
a try.

## Install the Truffle SDK in the CLI and populate the template

```sh
$ uv add truffle-sdk # or replace uv with poetry
```

enter your venv, then use the SDK CLI to populate the template
```sh
$ source .venv/bin/activate
(truffle-app-template) $ truffle setup
App Name: YourAppName
Description: What the app does
Example Prompt 1 of 5: ...
``` 

Now you're ready to start hacking at your first Truffle App!

## A Quickstart to Truffle Apps

The general structure of a Truffle App is to have a Python class, where state
is stored in member fields, and methods are decorated to expose them when the
app is running on the Truffle App Executor.

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
        self.metadata = truffle.AppMetadata(
            name="pythonsoftwareengineer",
            description="Writes and executes Python code to accomplish tasks"
        )
        # Client provides access to LLM capabilities
        self.client = truffle.TruffleClient()

    @truffle.tool(
        description="writes python code to a file",
        icon="pencil.line",
    )
    @truffle.args(
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
```
