# Truffle App Template

**Press 'Use this Template' up in the corner to get started!**

## An early draft of our core documentation will be released shortly

This template is designed to help you get up and running quickly with Truffle
App development. 

## Set up your project's virtual environment

The Truffle SDK currently is supports CPython 3.10+, but is mainly tested with
3.12+. This template repo supports [uv](https://docs.astral.sh/uv/), but you
can build Truffle Apps on any Python dependency stack you'd like.

## Install the Truffle SDK in the CLI

```sh
$ uv add "https://github.com/deepshard/truffle-sdk-public/releases/download/v0.6.3/truffle_sdk-0.6.3-py3-none-any.whl" # or replace uv with poetry
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
### Publishing your Truffle App

To upload your Truffle App to our platform, simply bundle the app into a `.truffle` file:

```sh
(truffle-app-template) $ truffle build MyTruffleApp # where MyTruffleApp is the name of the created project folder
(truffle-app-template) $ truffle upload MyTruffleApp.truffle
```

## Pro Tips & Pointers

* Don't be shy about throwing exceptions - they'll automatically get passed to the model. We've got your back on error handling.

* Remember: you're the magical bridge between code (where stuff actually happens) and language (that parameter ball bouncing around on the GPU). The best patterns are like a good sandwich: simple input, complex magic in the middle, simple output.

* Get creative! Our SDK APIs are your playground. Want to use fuzzy LLM logic to wrangle those finicky JSON APIs? Go for it. We love seeing clever solutions.

* Feel free to push the container to its limits - it's ephemeral anyway. If it breaks, it breaks. That's what containers are for. Just remember: while breaking things is cool, being a container resource hog isn't. Don't be that person.

* If you build something awesome (which we know you will), show it off! We're always stoked to see what creative ways people are using the SDK. Share those wins with the community.

  
## FAQ

### How are uncaught exceptions handled by the App Executor?

The Truffle App Executor forwards the stacktrace and exception message
to the Agent in the case of an uncaught exception. We encourage developers
to lean on this behavior, as we our Agent is capable of self-correcting tool
use in response to these exceptions.
