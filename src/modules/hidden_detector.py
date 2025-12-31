"""Hidden File Detector"""

import os
import stat
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


class HiddenFileDetector:
    """Detects hidden files in directories"""
    
    def __init__(self):
        self.name = "Hidden File Detector"
        self.hidden_files = []
        self.total_size = 0
    
    def is_hidden_unix(self, path):
        """Check if file is hidden on Unix-like systems
        
        Args:
            path: File path to check
            
        Returns:
            bool: True if hidden
        """
        name = os.path.basename(path)
        return name.startswith('.')
    
    def is_suspicious_location(self, path, base_path):
        """Check if file is in a suspicious location
        
        Args:
            path: File path to check
            base_path: Base path of the scan
            
        Returns:
            tuple: (is_suspicious, reason)
        """
        # Calculate nesting depth
        relative_path = os.path.relpath(path, base_path)
        depth = len(Path(relative_path).parts)
        
        # Check for suspicious patterns
        if depth > 10:
            return (True, "Deeply nested (>10 levels)")
        
        # Check for hidden files in unusual locations
        if self.is_hidden_unix(path):
            parent = os.path.dirname(path)
            if not self.is_hidden_unix(parent):
                # Hidden file in non-hidden directory
                file_ext = os.path.splitext(path)[1].lower()
                suspicious_exts = ['.exe', '.dll', '.so', '.dylib', '.sh', '.bat', '.ps1']
                if file_ext in suspicious_exts:
                    return (True, f"Hidden executable ({file_ext})")
        
        return (False, "")
    
    def scan_directory(self, path, recursive=True, max_depth=20, current_depth=0):
        """Scan directory for hidden files
        
        Args:
            path: Directory path to scan
            recursive: Whether to scan subdirectories
            max_depth: Maximum recursion depth
            current_depth: Current recursion depth
        """
        try:
            if current_depth > max_depth:
                return
            
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                
                try:
                    # Check if hidden
                    is_hidden = self.is_hidden_unix(item_path)
                    
                    if os.path.isfile(item_path):
                        if is_hidden:
                            size = os.path.getsize(item_path)
                            is_suspicious, reason = self.is_suspicious_location(item_path, path)
                            
                            self.hidden_files.append({
                                'path': item_path,
                                'name': item,
                                'size': size,
                                'suspicious': is_suspicious,
                                'reason': reason,
                                'depth': current_depth
                            })
                            self.total_size += size
                    
                    elif os.path.isdir(item_path) and recursive:
                        # Recursively scan subdirectories
                        self.scan_directory(item_path, recursive, max_depth, current_depth + 1)
                
                except (PermissionError, OSError) as e:
                    # Skip files/directories we can't access
                    continue
        
        except (PermissionError, OSError):
            # Skip directories we can't access
            pass
    
    def display_results(self):
        """Display scan results in a table"""
        if not self.hidden_files:
            console.print(Panel(
                "[green]No hidden files found![/green]\n\n"
                "The scanned directory contains no hidden files.",
                title="[bold green]Scan Complete[/bold green]",
                border_style="green"
            ))
            return
        
        # Separate suspicious and normal hidden files
        suspicious_files = [f for f in self.hidden_files if f['suspicious']]
        normal_files = [f for f in self.hidden_files if not f['suspicious']]
        
        # Display suspicious files first if any
        if suspicious_files:
            console.print("\n")
            console.print(Panel(
                f"[bold red]⚠️  Found {len(suspicious_files)} suspicious hidden file(s)![/bold red]\n\n"
                f"These files may warrant investigation.",
                title="[bold red]Security Alert[/bold red]",
                border_style="red"
            ))
            
            sus_table = Table(
                title="[bold red]Suspicious Hidden Files[/bold red]",
                show_header=True,
                header_style="bold red",
                border_style="red"
            )
            
            sus_table.add_column("Filename", style="yellow")
            sus_table.add_column("Path", style="white")
            sus_table.add_column("Size", justify="right", style="cyan")
            sus_table.add_column("Reason", style="red")
            
            for file_info in suspicious_files:
                size_str = self._format_size(file_info['size'])
                sus_table.add_row(
                    file_info['name'],
                    file_info['path'],
                    size_str,
                    file_info['reason']
                )
            
            console.print("\n")
            console.print(sus_table)
        
        # Display all hidden files
        console.print("\n")
        table = Table(
            title=f"[bold cyan]All Hidden Files Found ({len(self.hidden_files)} total)[/bold cyan]",
            show_header=True,
            header_style="bold magenta",
            border_style="cyan"
        )
        
        table.add_column("Filename", style="yellow", width=30)
        table.add_column("Path", style="white", width=50)
        table.add_column("Size", justify="right", style="green", width=12)
        table.add_column("Depth", justify="right", style="cyan", width=8)
        
        # Sort by path
        sorted_files = sorted(self.hidden_files, key=lambda x: x['path'])
        
        # Show up to 50 files
        display_count = min(50, len(sorted_files))
        for file_info in sorted_files[:display_count]:
            size_str = self._format_size(file_info['size'])
            style = "red" if file_info['suspicious'] else "white"
            
            table.add_row(
                file_info['name'],
                file_info['path'][:50] + "..." if len(file_info['path']) > 50 else file_info['path'],
                size_str,
                str(file_info['depth']),
                style=style
            )
        
        if len(sorted_files) > display_count:
            table.add_row(
                f"... and {len(sorted_files) - display_count} more",
                "",
                "",
                "",
                style="dim"
            )
        
        console.print("\n")
        console.print(table)
        
        # Display summary
        total_size_str = self._format_size(self.total_size)
        console.print("\n")
        console.print(Panel(
            f"[cyan]Total hidden files: {len(self.hidden_files)}[/cyan]\n"
            f"[cyan]Total size: {total_size_str}[/cyan]\n"
            f"[yellow]Suspicious files: {len(suspicious_files)}[/yellow]\n"
            f"[green]Normal hidden files: {len(normal_files)}[/green]",
            title="[bold cyan]Summary[/bold cyan]",
            border_style="cyan"
        ))
    
    def _format_size(self, size):
        """Format file size in human-readable format
        
        Args:
            size: Size in bytes
            
        Returns:
            str: Formatted size string
        """
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    
    def run(self):
        """Execute the hidden file detector"""
        try:
            console.print("\n[bold cyan]Hidden File Detector[/bold cyan]")
            console.print("\n[white]Scan directories for hidden files and suspicious patterns.[/white]")
            
            # Get directory to scan
            console.print("\n[yellow]Enter directory path to scan:[/yellow]")
            console.print("[dim]Examples: /home/user, ~/Documents, .[/dim]")
            
            dir_path = console.input("\n[bold green]Path: [/bold green]").strip()
            
            if not dir_path:
                console.print("[red]No path provided.[/red]")
                input("\nPress Enter to return to menu...")
                return
            
            # Expand ~ to home directory
            dir_path = os.path.expanduser(dir_path)
            
            if not os.path.exists(dir_path):
                console.print(f"[red]Error: Directory not found: {dir_path}[/red]")
                input("\nPress Enter to return to menu...")
                return
            
            if not os.path.isdir(dir_path):
                console.print(f"[red]Error: Path is not a directory: {dir_path}[/red]")
                input("\nPress Enter to return to menu...")
                return
            
            # Ask about recursive scan
            recursive_input = console.input("\n[yellow]Scan subdirectories recursively? (Y/n): [/yellow]").strip().lower()
            recursive = recursive_input != 'n'
            
            # Start scanning
            console.print(f"\n[cyan]Scanning: {dir_path}[/cyan]")
            if recursive:
                console.print("[cyan]Mode: Recursive[/cyan]")
            console.print("[yellow]This may take a moment...[/yellow]\n")
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("[cyan]Scanning for hidden files...", total=None)
                self.scan_directory(dir_path, recursive=recursive)
                progress.update(task, completed=True)
            
            # Display results
            self.display_results()
            
            input("\nPress Enter to return to menu...")
        except KeyboardInterrupt:
            console.print("\n[yellow]Scan cancelled.[/yellow]")
            input("\nPress Enter to return to menu...")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            input("\nPress Enter to return to menu...")
