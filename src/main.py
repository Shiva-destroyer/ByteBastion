#!/usr/bin/env python3
"""
ByteBastion - Comprehensive Security Suite
Developer: Sai Srujan Murthy
Contact: saisrujanmurthy@gmail.com
"""

import sys
import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
import pyfiglet

from modules.file_checker import FileIntegrityChecker
from modules.keylogger import EducationalKeylogger
from modules.file_type_identifier import FileTypeIdentifier
from modules.password_generator import PasswordGenerator
from modules.data_deletion import DataDeletionUtility
from modules.aes_crypto import AESCrypto
from modules.directory_monitor import DirectorySyncMonitor
from modules.temp_cleaner import TempFileCleaner
from modules.hidden_detector import HiddenFileDetector
from modules.disk_analyzer import DiskSpaceAnalyzer


console = Console()


def display_banner():
    """Display the cybersecurity-styled banner (shown once at startup)"""
    banner_text = pyfiglet.figlet_format("ByteBastion", font="doom")
    
    banner = Text()
    banner.append(banner_text, style="bold red")
    
    console.print(Panel(
        banner,
        title="[bold cyan]Comprehensive Security Suite[/bold cyan]",
        subtitle="[bold yellow]Developer: Sai Srujan Murthy | Contact: saisrujanmurthy@gmail.com[/bold yellow]",
        border_style="green",
        padding=(1, 2)
    ))


def display_menu_header():
    """Display a clean menu header (shown in loop)"""
    console.print("\n")
    console.print(Panel(
        "[bold cyan]ByteBastion Security Menu[/bold cyan]",
        border_style="green",
        padding=(0, 2)
    ))
    console.print("\n")


def display_menu():
    """Display the main menu using rich tables"""
    table = Table(
        title="[bold cyan]Security Tools Menu[/bold cyan]",
        show_header=True,
        header_style="bold magenta",
        border_style="blue",
        title_style="bold cyan"
    )
    
    table.add_column("ID", style="cyan", width=6, justify="center")
    table.add_column("Tool Name", style="green", width=40)
    table.add_column("Category", style="yellow", width=20)
    
    tools = [
        ("1", "File Integrity Checker (Hashes)", "Verification"),
        ("2", "Educational Keylogger", "Monitoring"),
        ("3", "File Type Identifier (Magic Bytes)", "Analysis"),
        ("4", "Secure Password Generator", "Security"),
        ("5", "Data Deletion Utility (Secure Wipe)", "Privacy"),
        ("6", "AES Encryption/Decryption", "Cryptography"),
        ("7", "Directory Sync Monitor", "Monitoring"),
        ("8", "Temporary File Cleaner", "Maintenance"),
        ("9", "Hidden File Detector", "Analysis"),
        ("10", "Disk Space Analyzer with Alerts", "System")
    ]
    
    for tool_id, tool_name, category in tools:
        table.add_row(tool_id, tool_name, category)
    
    table.add_row("", "", "", style="dim")
    table.add_row("0", "Exit", "System", style="bold red")
    
    console.print("\n")
    console.print(table)
    console.print("\n")


def get_tool_instance(choice):
    """Return the appropriate tool instance based on user choice"""
    tools = {
        "1": FileIntegrityChecker(),
        "2": EducationalKeylogger(),
        "3": FileTypeIdentifier(),
        "4": PasswordGenerator(),
        "5": DataDeletionUtility(),
        "6": AESCrypto(),
        "7": DirectorySyncMonitor(),
        "8": TempFileCleaner(),
        "9": HiddenFileDetector(),
        "10": DiskSpaceAnalyzer()
    }
    return tools.get(choice)


def main():
    """Main application loop"""
    # Display banner once at startup
    console.clear()
    display_banner()
    
    first_iteration = True
    
    while True:
        # Clear screen only on subsequent iterations (keeps banner visible on first)
        if not first_iteration:
            os.system('cls' if os.name == 'nt' else 'clear')
            display_menu_header()
        else:
            console.print("\n")
        
        display_menu()
        first_iteration = False
        
        choice = console.input("[bold green]Select a tool (0-10): [/bold green]").strip()
        
        if choice == "0":
            console.print("\n[bold red]Exiting ByteBastion...[/bold red]")
            console.print("[bold yellow]Developer: Sai Srujan Murthy | Contact: saisrujanmurthy@gmail.com[/bold yellow]")
            console.print("[bold yellow]Stay secure! 🔒[/bold yellow]\n")
            sys.exit(0)
        
        tool = get_tool_instance(choice)
        
        if tool:
            os.system('cls' if os.name == 'nt' else 'clear')
            display_menu_header()
            try:
                tool.run()
            except Exception as e:
                console.print(f"\n[bold red]Error:[/bold red] {str(e)}")
                input("\nPress Enter to return to menu...")
        else:
            console.print(
                "\n[bold red]Invalid choice![/bold red] "
                "Please select a number between 0 and 10."
            )
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n\n[bold red]Program interrupted by user.[/bold red]")
        console.print("[bold yellow]Developer: Sai Srujan Murthy | Contact: saisrujanmurthy@gmail.com[/bold yellow]")
        console.print("[bold yellow]Stay secure! 🔒[/bold yellow]\n")
        sys.exit(0)
