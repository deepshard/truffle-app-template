from pathlib import Path
import truffle

# PythonSoftwareEngineer acts as a Truffle App that can write, read, and execute code
class ${name}:

    def __init__(self) -> None:
        self.metadata = truffle.AppMetadata(
            name="${name}",
            description="${description}"
            icon="icon.png",
        )
        # Client provides access to LLM capabilities
        self.client = truffle.TruffleClient()

    @truffle.tool(
        description="Replace this with what the tool does!",
        icon="circle.circle", # Probably replace this with something better
    )
    @truffle.args(
        the_code="a string containing the valid python code",
        destination_path="the path to the file",
    )
    def ${name}Tool(self, tool_argument: str) -> str:
        """ Replace this with a useful docstring."""
        return f"Return something useful here instead"

if __name__ == "__main__":
    app = truffle.TruffleApp(${name}())
    app.launch()
