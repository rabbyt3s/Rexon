#!/usr/bin/env python3

from rich.console import Console
from itertools import cycle
from rich.theme import Theme
from command_executor import CommandExecutor
import sys
from time import sleep
from rich.live import Live

console = Console(theme=Theme({
    "accent": "#3B82F6",
    "warning": "#FFB000", 
    "error": "#FF6B6B",
    "success": "#00FF00",
    "white": "#FFFFFF" 
}))

def initialize_app():
    from InquirerPy import inquirer
    from InquirerPy.base.control import Choice
    from InquirerPy.separator import Separator
    from command_generator import CommandGenerator
    from command_executor import CommandExecutor
    
    panel_content = f"""[accent]╭─[/accent] Initializing [accent]─[/accent]
[accent]│[/accent]
[accent]│[/accent] {{spinner}}
[accent]│[/accent]
[accent]╰───────────────────[/accent]"""
    
    try:
        generator = CommandGenerator()
        executor = CommandExecutor()
        
        with Live(panel_content.format(spinner='|'), refresh_per_second=10, console=console) as live:
            for _ in range(3):
                for spinner in ['|', '/', '-', '\\']:
                    live.update(panel_content.format(spinner=spinner))
                    sleep(0.1)
            
            return generator, executor, inquirer, Choice, Separator
                    
    except Exception as e:
        console.print(f"[red]Error during initialization: {str(e)}[/red]")
        sys.exit(1)

def print_banner():
    console.print("""[accent]
 __   ___      __
|__) |__  \_/ /  \ |\ |
|  \ |___ / \ \__/ | \|[/accent]""")
    
    console.print("\n[accent]Reconnaissance Assistant[/accent]")
    console.print(f"By: [accent]Rabbytes[/accent] ([accent]@Rabbyt3s[/accent])")
    console.print("\n[accent]> Rexon 1.0.0 <[/accent]\n")

def clear_screen():
    console.clear()
    print_banner()

def get_reconnaissance_details(inquirer, Choice):
    clear_screen()
    target_type = inquirer.select(
        message="Select target type",
        choices=[
            Choice("single", "Single domain (e.g., example.com)"),
            Choice("file", "Multiple domains from file"),
            Separator(),
            Choice("back", "[←] Back to main menu")
        ],
        qmark="[?]",
        pointer="→",
        instruction=None
    ).execute()

    if target_type == "back":
        return None, None, None

    clear_screen()
    if target_type == "single":
        target = inquirer.text(
            message="Enter target domain (e.g., example.com) > ",
            qmark="[?]",
            instruction=None
        ).execute()
        
        if not target:
            return None, None, None
    else:
        target = inquirer.filepath(
            message="Select domains file (File should contain one domain per line) > ",
            qmark="[?]",
            instruction=None,
            only_files=True
        ).execute()
        
        if not target:
            return None, None, None

    clear_screen()
    query = inquirer.text(
        message="What do you want to do with the target(s) > ",
        qmark="[?]",
        instruction=None
    ).execute()

    if not query:
        return None, None, None

    return query, target_type, target

def process_existing_file(inquirer, generator):
    clear_screen()
    file_path = inquirer.filepath(
        message="Select the file to process (e.g., urls.txt, subdomains.txt) > ",
        qmark="[?]",
        instruction=None,
        only_files=True
    ).execute()

    if not file_path:
        return None, None

    clear_screen()
    console.print("\n[accent]Example queries:[/accent]")
    console.print("[warning]  • Keep only subdomains of api.example.com[/warning]")
    console.print("[warning]  • Filter URLs containing 'admin' or 'dashboard'[/warning]")
    console.print("[warning]  • Sort by domain name and remove duplicates[/warning]")
    console.print("[warning]  • Extract all endpoints containing '/api/v2/'[/warning]")
    console.print("[warning]  • Remove all URLs with status code 404[/warning]")
    console.print()

    query = inquirer.text(
        message="Describe how you want to process the file > ",
        qmark="[?]",
        instruction=None
    ).execute()

    if not query:
        return None, None

    return file_path, query

def show_menu(generator, executor, inquirer, Choice, Separator):
    clear_screen()
    
    menu_choices = [
        Choice("recon", "[+] Launch Reconnaissance"),
        Choice("process", "[*] Process Existing File (NLP)"),
        Separator(),
        Choice("tools", "[~] Check Tools"),
        Separator(),
        Choice("exit", "[x] Exit")
    ]

    while True:
        choice = inquirer.select(
            message="Select an action",
            choices=menu_choices,
            default="recon",
            qmark="[?]",
            pointer="→"
        ).execute()
        clear_screen()

        if choice == "recon":
            query, target_type, target = get_reconnaissance_details(inquirer, Choice)
            if all(v is not None for v in [query, target_type, target]):
                console.print("\n[accent]╭─[/accent] Task Details [accent]─[/accent]")
                console.print(f"[accent]│[/accent] [bold]Task:[/bold]    {query}")
                console.print(f"[accent]│[/accent] [bold]Type:[/bold]    {target_type}")
                console.print(f"[accent]│[/accent] [bold]Target:[/bold]  {target}")
                console.print("[accent]╰───────────────────[/accent]")
                
                console.print(f"\n[warning][*][/warning] Generating command...")

                if target_type == "single":
                    command = generator.generate_command(query, target)
                else:
                    command = generator.process_file(query, target)

                if command:
                    console.print("\n[accent]╭─[/accent] Generated Command [accent]─[/accent]")
                    console.print(f"[accent]│[/accent]")
                    console.print(f"[accent]│[/accent] {command}")
                    console.print(f"[accent]│[/accent]")
                    console.print("[accent]╰──────────────────[/accent]")

                    execute = inquirer.confirm(
                        message="Do you want to execute this command",
                        qmark=">",
                        default=True
                    ).execute()

                    if execute:
                        success, output = executor.execute(command)
                else:
                    console.print("\n[error][-][/error] Failed to generate command")
        
        elif choice == "process":
            file_path, query = process_existing_file(inquirer, generator)
            if all(v is not None for v in [file_path, query]):
                console.print("\n[accent]╭─[/accent] Task Details [accent]─[/accent]")
                console.print(f"[accent]│[/accent] [bold]File:[/bold]    {file_path}")
                console.print(f"[accent]│[/accent] [bold]Task:[/bold]    {query}")
                console.print("[accent]╰───────────────────[/accent]")
                
                console.print(f"\n[warning][*][/warning] Generating command...")

                command = generator.process_file(query, file_path)

                if command:
                    console.print("\n[accent]╭─[/accent] Generated Command [accent]─[/accent]")
                    console.print(f"[accent]│[/accent]")
                    console.print(f"[accent]│[/accent] {command}")
                    console.print(f"[accent]│[/accent]")
                    console.print("[accent]╰─────────────────[/accent]")

                    execute = inquirer.confirm(
                        message="Do you want to execute this command",
                        qmark=">",
                        default=True
                    ).execute()

                    if execute:
                        success, output = executor.execute(command)
                else:
                    console.print("\n[error][-][/error] Failed to generate command")
        
        elif choice == "tools":
            clear_screen()
            from tool_checker import ToolChecker
            checker = ToolChecker()
            checker.check_all_tools()
            console.print("\n[warning][*][/warning] Press Enter to continue...")
            input()
            clear_screen()
        
        elif choice == "exit":
            console.print(f"\n[accent][+][/accent] Goodbye!")
            sys.exit(0)
        
        if choice != "exit":
            clear_screen()

if __name__ == '__main__':
    try:
        generator, executor, inquirer, Choice, Separator = initialize_app()
        clear_screen()
        show_menu(generator, executor, inquirer, Choice, Separator)
    except KeyboardInterrupt:
        console.print("\n[error][-][/error] Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[error][-][/error] Error: {str(e)}")
        sys.exit(1)
