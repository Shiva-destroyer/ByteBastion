"""Data Deletion Utility - Secure file wiping"""

import os
import secrets
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn

console = Console()


class DataDeletionUtility:
    """Securely wipes files beyond recovery using DoD 5220.22-M standard"""
    
    def __init__(self):
        self.name = "Data Deletion Utility"
    
    def secure_wipe_file(self, file_path):
        """Securely wipe a file using DoD 5220.22-M (3-pass) method
        
        Pass 1: Write zeros
        Pass 2: Write ones
        Pass 3: Write random data
        
        Args:
            file_path: Path to file to wipe
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not os.path.exists(file_path):
                console.print(f"[red]Error: File not found: {file_path}[/red]")
                return False
            
            # Get file size
            file_size = os.path.getsize(file_path)
            
            if file_size == 0:
                console.print("[yellow]Warning: File is empty (0 bytes)[/yellow]")
                os.remove(file_path)
                return True
            
            console.print(f"\n[cyan]File size: {file_size:,} bytes[/cyan]")
            console.print("[yellow]Performing DoD 5220.22-M secure wipe (3 passes)...[/yellow]\n")
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                console=console
            ) as progress:
                
                # Pass 1: Write zeros
                task1 = progress.add_task("[red]Pass 1/3: Writing zeros...", total=file_size)
                with open(file_path, "r+b") as f:
                    chunk_size = 4096
                    bytes_written = 0
                    while bytes_written < file_size:
                        chunk = min(chunk_size, file_size - bytes_written)
                        f.write(b'\x00' * chunk)
                        bytes_written += chunk
                        progress.update(task1, advance=chunk)
                    f.flush()
                    os.fsync(f.fileno())
                
                # Pass 2: Write ones
                task2 = progress.add_task("[yellow]Pass 2/3: Writing ones...", total=file_size)
                with open(file_path, "r+b") as f:
                    bytes_written = 0
                    while bytes_written < file_size:
                        chunk = min(chunk_size, file_size - bytes_written)
                        f.write(b'\xFF' * chunk)
                        bytes_written += chunk
                        progress.update(task2, advance=chunk)
                    f.flush()
                    os.fsync(f.fileno())
                
                # Pass 3: Write random data
                task3 = progress.add_task("[green]Pass 3/3: Writing random data...", total=file_size)
                with open(file_path, "r+b") as f:
                    bytes_written = 0
                    while bytes_written < file_size:
                        chunk = min(chunk_size, file_size - bytes_written)
                        f.write(secrets.token_bytes(chunk))
                        bytes_written += chunk
                        progress.update(task3, advance=chunk)
                    f.flush()
                    os.fsync(f.fileno())
            
            # Finally, delete the file
            os.remove(file_path)
            
            console.print("\n")
            console.print(Panel(
                f"[green]✓ File securely wiped and deleted![/green]\n\n"
                f"File: {os.path.basename(file_path)}\n"
                f"Method: DoD 5220.22-M (3-pass)\n"
                f"Data overwritten: {file_size * 3:,} bytes total\n\n"
                f"[dim]The file cannot be recovered by standard recovery tools.[/dim]",
                title="[bold green]Secure Deletion Complete[/bold green]",
                border_style="green"
            ))
            
            return True
        except PermissionError:
            console.print(f"[red]Error: Permission denied. Cannot delete {file_path}[/red]")
            return False
        except Exception as e:
            console.print(f"[red]Error during secure wipe: {e}[/red]")
            return False
    
    def confirm_deletion(self, file_path):
        """Get explicit user confirmation before deletion
        
        Args:
            file_path: Path to file to delete
            
        Returns:
            bool: True if user confirmed, False otherwise
        """
        try:
            filename = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            
            console.print("\n")
            console.print(Panel(
                f"[bold red]⚠ WARNING: PERMANENT DATA DESTRUCTION ⚠[/bold red]\n\n"
                f"File: [yellow]{filename}[/yellow]\n"
                f"Path: {file_path}\n"
                f"Size: {file_size:,} bytes\n\n"
                f"[bold]This operation will:[/bold]\n"
                f"  • Overwrite the file 3 times with different patterns\n"
                f"  • Make data recovery virtually impossible\n"
                f"  • Permanently delete the file\n\n"
                f"[bold red]THIS CANNOT BE UNDONE![/bold red]",
                title="[bold red]Confirm Secure Deletion[/bold red]",
                border_style="red",
                padding=(1, 2)
            ))
            
            console.print("\n[bold yellow]Type 'YES' (all caps) to confirm deletion, or anything else to cancel:[/bold yellow]")
            confirmation = console.input("[bold red]> [/bold red]").strip()
            
            return confirmation == "YES"
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            return False
    
    def run(self):
        """Execute the data deletion utility"""
        try:
            console.print("\n[bold cyan]Data Deletion Utility (Secure Wipe)[/bold cyan]")
            console.print("\n[white]Securely wipe files using DoD 5220.22-M standard (3-pass).[/white]")
            console.print("[dim]This method makes file recovery extremely difficult.[/dim]")
            
            file_path = console.input("\n[yellow]Enter file path to securely delete: [/yellow]").strip()
            
            if not file_path:
                console.print("[red]No file path provided.[/red]")
                input("\nPress Enter to return to menu...")
                return
            
            if not os.path.exists(file_path):
                console.print(f"[red]Error: File not found: {file_path}[/red]")
                input("\nPress Enter to return to menu...")
                return
            
            if not os.path.isfile(file_path):
                console.print(f"[red]Error: Path is not a file: {file_path}[/red]")
                console.print("[yellow]Note: This tool only works with individual files, not directories.[/yellow]")
                input("\nPress Enter to return to menu...")
                return
            
            # Get explicit confirmation
            if self.confirm_deletion(file_path):
                console.print("\n[cyan]Starting secure deletion process...[/cyan]")
                self.secure_wipe_file(file_path)
            else:
                console.print("\n[yellow]Deletion cancelled by user.[/yellow]")
            
            input("\nPress Enter to return to menu...")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            input("\nPress Enter to return to menu...")
