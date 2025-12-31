"""File Integrity Checker - Hash-based verification"""

import hashlib
import json
import os
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


class FileIntegrityChecker:
    """Verifies file integrity using cryptographic hashes"""
    
    def __init__(self):
        self.name = "File Integrity Checker"
        self.db_file = Path("integrity_database.json")
        self.database = self._load_database()
    
    def _load_database(self):
        """Load the hash database from JSON file"""
        try:
            if self.db_file.exists():
                with open(self.db_file, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            console.print(f"[yellow]Warning: Could not load database: {e}[/yellow]")
            return {}
    
    def _save_database(self):
        """Save the hash database to JSON file"""
        try:
            with open(self.db_file, 'w') as f:
                json.dump(self.database, f, indent=4)
            return True
        except Exception as e:
            console.print(f"[red]Error saving database: {e}[/red]")
            return False
    
    def calculate_sha256(self, file_path):
        """Calculate SHA-256 hash of a file
        
        Args:
            file_path: Path to the file to hash
            
        Returns:
            str: Hexadecimal hash string or None on error
        """
        try:
            sha256_hash = hashlib.sha256()
            with open(file_path, "rb") as f:
                # Read file in chunks for memory efficiency
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception as e:
            console.print(f"[red]Error calculating hash: {e}[/red]")
            return None
    
    def add_file_hash(self, file_path):
        """Add file hash to database
        
        Args:
            file_path: Path to the file to add
        """
        try:
            if not os.path.exists(file_path):
                console.print(f"[red]Error: File not found: {file_path}[/red]")
                return
            
            console.print(f"\n[cyan]Calculating hash for: {file_path}[/cyan]")
            file_hash = self.calculate_sha256(file_path)
            
            if file_hash:
                abs_path = os.path.abspath(file_path)
                self.database[abs_path] = {
                    "hash": file_hash,
                    "filename": os.path.basename(file_path),
                    "size": os.path.getsize(file_path)
                }
                
                if self._save_database():
                    console.print(Panel(
                        f"[green]✓ Hash saved successfully![/green]\n\n"
                        f"File: {os.path.basename(file_path)}\n"
                        f"SHA-256: {file_hash}",
                        title="[bold green]Success[/bold green]",
                        border_style="green"
                    ))
        except Exception as e:
            console.print(f"[red]Error adding file: {e}[/red]")
    
    def verify_file(self, file_path):
        """Verify file against stored hash
        
        Args:
            file_path: Path to the file to verify
        """
        try:
            if not os.path.exists(file_path):
                console.print(f"[red]Error: File not found: {file_path}[/red]")
                return
            
            abs_path = os.path.abspath(file_path)
            
            if abs_path not in self.database:
                console.print(Panel(
                    f"[yellow]⚠ No hash found in database for this file![/yellow]\n\n"
                    f"File: {os.path.basename(file_path)}\n"
                    f"Please add the file hash first.",
                    title="[bold yellow]Not Found[/bold yellow]",
                    border_style="yellow"
                ))
                return
            
            console.print(f"\n[cyan]Verifying: {file_path}[/cyan]")
            current_hash = self.calculate_sha256(file_path)
            stored_hash = self.database[abs_path]["hash"]
            
            if current_hash == stored_hash:
                console.print(Panel(
                    f"[green]✓ MATCH - File integrity verified![/green]\n\n"
                    f"File: {os.path.basename(file_path)}\n"
                    f"Current Hash: {current_hash}\n"
                    f"Stored Hash:  {stored_hash}",
                    title="[bold green]Integrity Check: PASSED[/bold green]",
                    border_style="green"
                ))
            else:
                console.print(Panel(
                    f"[red]✗ MISMATCH - File has been modified![/red]\n\n"
                    f"File: {os.path.basename(file_path)}\n"
                    f"Current Hash: {current_hash}\n"
                    f"Stored Hash:  {stored_hash}\n\n"
                    f"[yellow]⚠ Warning: This file may have been tampered with![/yellow]",
                    title="[bold red]Integrity Check: FAILED[/bold red]",
                    border_style="red"
                ))
        except Exception as e:
            console.print(f"[red]Error verifying file: {e}[/red]")
    
    def list_tracked_files(self):
        """List all files in the database"""
        if not self.database:
            console.print("\n[yellow]No files in database yet.[/yellow]")
            return
        
        table = Table(title="[bold cyan]Tracked Files[/bold cyan]", border_style="cyan")
        table.add_column("Filename", style="green")
        table.add_column("Path", style="white")
        table.add_column("Size (bytes)", style="yellow", justify="right")
        
        for path, data in self.database.items():
            table.add_row(
                data["filename"],
                path,
                str(data["size"])
            )
        
        console.print("\n")
        console.print(table)
    
    def run(self):
        """Execute the file integrity checker"""
        try:
            while True:
                console.print("\n[bold cyan]File Integrity Checker[/bold cyan]")
                console.print("\n1. Add file hash to database")
                console.print("2. Verify file integrity")
                console.print("3. List tracked files")
                console.print("4. Return to main menu")
                
                choice = console.input("\n[bold green]Select option (1-4): [/bold green]").strip()
                
                if choice == "1":
                    file_path = console.input("\n[yellow]Enter file path: [/yellow]").strip()
                    self.add_file_hash(file_path)
                elif choice == "2":
                    file_path = console.input("\n[yellow]Enter file path: [/yellow]").strip()
                    self.verify_file(file_path)
                elif choice == "3":
                    self.list_tracked_files()
                elif choice == "4":
                    break
                else:
                    console.print("[red]Invalid option![/red]")
                
                if choice in ["1", "2", "3"]:
                    input("\nPress Enter to continue...")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            input("\nPress Enter to return to menu...")
