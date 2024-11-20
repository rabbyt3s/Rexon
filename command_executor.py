import subprocess
import os
from typing import Tuple
from utils import LoadingAnimation
from rich.console import Console
from rich.theme import Theme

custom_theme = Theme({
    "accent": "#3B82F6",
    "warning": "#FFB000", 
    "error": "#FF6B6B",
    "success": "#00FF00"
})

console = Console(theme=custom_theme)

class CommandExecutor:
    def __init__(self):
        self.output_dir = 'output'
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def execute(self, command: str) -> Tuple[bool, str]:
        try:
            parts = command.split('>')
            if len(parts) > 1:
                input_command = parts[0].strip()
                output_file = parts[1].strip()
                output_path = os.path.join(self.output_dir, output_file)
                command = f"{input_command} > {output_path}"
            
            console.print("\n[accent]╭─[/accent] Executing Command [accent]─[/accent]")
            console.print(f"[accent]│[/accent]")
            console.print(f"[accent]│[/accent] {command}")
            console.print(f"[accent]│[/accent]")
            console.print("[accent]╰───────────────────[/accent]")
            
            loading = LoadingAnimation()
            loading.start()
            
            try:
                process = subprocess.run(
                    command,
                    shell=True,
                    executable='/bin/bash',
                    capture_output=True,
                    text=True
                )
                
            finally:
                loading.stop()

            if process.returncode == 0:
                if len(parts) > 1:
                    console.print(f"\n[green][+][/green] Command completed successfully. Results saved to: {output_path}")
                else:
                    console.print(f"\n[green][+][/green] Command completed successfully.")
                console.print("\n[warning][*][/warning] Press Enter to continue...")
                input()
                return True, ""
            else:
                console.print(f"\n[red][-][/red] Command failed with return code: {process.returncode}")
                console.print("\n[warning][*][/warning] Press Enter to continue...")
                input()
                return False, ""

        except Exception as e:
            console.print(f"\n[red][-][/red] Error executing command: {str(e)}")
            return False, str(e)
