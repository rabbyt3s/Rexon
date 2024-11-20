import shutil
from rich.console import Console

console = Console()

class ToolChecker:
    def __init__(self):
        self.tools = [
            "subfinder",
            "httpx",
            "nuclei",
            "naabu",
            "katana",
            "waybackurls",
            "gau"
        ]
        self.installed = "[green]+[/green]"
        self.not_installed = "[red]?[/red]"

    def check_tool(self, tool_name: str) -> bool:
        """Check if a tool is available in PATH"""
        return shutil.which(tool_name) is not None

    def check_all_tools(self):
        """Check all tools and display results"""
        console.print("\n[accent]╭─[/accent] Tool Status [accent]─[/accent]")
        console.print("[accent]│[/accent]")
        
        for tool in self.tools:
            is_installed = self.check_tool(tool)
            status = self.installed if is_installed else self.not_installed
            console.print(f"[accent]│[/accent] {status} {tool}")

        console.print("[accent]│[/accent]")
        console.print("[accent]╰───────────────────[/accent]")
