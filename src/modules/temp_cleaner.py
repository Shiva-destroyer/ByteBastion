"""Temporary File Cleaner"""

import os
import shutil
import time
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn

console = Console()


class TempFileCleaner:
    """Cleans temporary files from the system"""
    
    def __init__(self):
        self.name = "Temporary File Cleaner"
        self.files_to_delete = []
        self.total_size = 0
    
    def get_safe_temp_locations(self):
        """Get list of safe temporary file locations
        
        Returns:
            list: List of (path, description, age_filter) tuples
        """
        home = os.path.expanduser("~")
        locations = []
        
        # User cache thumbnails
        thumbnails_path = os.path.join(home, ".cache", "thumbnails")
        if os.path.exists(thumbnails_path):
            locations.append((thumbnails_path, "User thumbnails cache", 0))
        
        # User general cache (be selective)
        cache_path = os.path.join(home, ".cache")
        if os.path.exists(cache_path):
            locations.append((cache_path, "User cache directory", 7))  # 7 days old
        
        # System temp (Linux)
        if os.path.exists("/tmp"):
            locations.append(("/tmp", "System temp directory", 1))  # 1 day old
        
        # User temp directories
        user_tmp = os.path.join(home, ".tmp")
        if os.path.exists(user_tmp):
            locations.append((user_tmp, "User temp directory", 1))
        
        return locations
    
    def is_file_old_enough(self, file_path, days):
        """Check if file is older than specified days
        
        Args:
            file_path: Path to file
            days: Number of days
            
        Returns:
            bool: True if file is old enough to delete
        """
        try:
            if days == 0:
                return True
            
            file_time = os.path.getmtime(file_path)
            current_time = time.time()
            age_days = (current_time - file_time) / (24 * 3600)
            
            return age_days >= days
        except Exception:
            return False
    
    def scan_directory(self, path, age_days, max_depth=3, current_depth=0):
        """Scan directory for temporary files
        
        Args:
            path: Directory path to scan
            age_days: Minimum age in days for files to include
            max_depth: Maximum recursion depth
            current_depth: Current recursion depth
        """
        try:
            if current_depth > max_depth:
                return
            
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                
                try:
                    if os.path.isfile(item_path):
                        if self.is_file_old_enough(item_path, age_days):
                            size = os.path.getsize(item_path)
                            self.files_to_delete.append({
                                'path': item_path,
                                'size': size,
                                'name': item
                            })
                            self.total_size += size
                    elif os.path.isdir(item_path):
                        # Recursively scan subdirectories
                        self.scan_directory(item_path, age_days, max_depth, current_depth + 1)
                except (PermissionError, OSError):
                    # Skip files/directories we can't access
                    continue
        except (PermissionError, OSError):
            # Skip directories we can't access
            pass
    
    def scan_custom_path(self, path):
        """Scan a user-specified path
        
        Args:
            path: Path to scan
        """
        try:
            if not os.path.exists(path):
                console.print(f"[red]Error: Path does not exist: {path}[/red]")
                return False
            
            if not os.path.isdir(path):
                console.print(f"[red]Error: Path is not a directory: {path}[/red]")
                return False
            
            console.print(f"\n[cyan]Scanning: {path}[/cyan]")
            console.print("[yellow]This may take a moment...[/yellow]\n")
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("[cyan]Scanning files...", total=None)
                self.scan_directory(path, age_days=0, max_depth=5)
                progress.update(task, completed=True)
            
            return True
        except Exception as e:
            console.print(f"[red]Error scanning path: {e}[/red]")
            return False
    
    def display_scan_report(self):
        """Display scan results in a table"""
        if not self.files_to_delete:
            console.print(Panel(
                "[green]No temporary files found to clean![/green]\n\n"
                "Your system is clean.",
                title="[bold green]Scan Complete[/bold green]",
                border_style="green"
            ))
            return
        
        # Create summary table
        table = Table(
            title="[bold cyan]Temporary Files Found[/bold cyan]",
            show_header=True,
            header_style="bold magenta",
            border_style="cyan"
        )
        
        table.add_column("Category", style="yellow")
        table.add_column("Count", justify="right", style="cyan")
        table.add_column("Size", justify="right", style="green")
        
        # Group by directory
        dir_stats = {}
        for file_info in self.files_to_delete:
            dir_name = os.path.dirname(file_info['path'])
            if dir_name not in dir_stats:
                dir_stats[dir_name] = {'count': 0, 'size': 0}
            dir_stats[dir_name]['count'] += 1
            dir_stats[dir_name]['size'] += file_info['size']
        
        # Add rows for each directory
        for dir_path, stats in sorted(dir_stats.items()):
            size_mb = stats['size'] / (1024 * 1024)
            table.add_row(
                os.path.basename(dir_path) or dir_path,
                str(stats['count']),
                f"{size_mb:.2f} MB"
            )
        
        # Add total row
        table.add_row("", "", "", style="dim")
        total_mb = self.total_size / (1024 * 1024)
        table.add_row(
            "[bold]TOTAL[/bold]",
            f"[bold]{len(self.files_to_delete)}[/bold]",
            f"[bold]{total_mb:.2f} MB[/bold]",
            style="bold green"
        )
        
        console.print("\n")
        console.print(table)
        console.print("\n")
        
        console.print(Panel(
            f"[yellow]Space to be freed: {total_mb:.2f} MB[/yellow]\n"
            f"Files to delete: {len(self.files_to_delete)}\n\n"
            f"[dim]Note: Files will be permanently deleted.[/dim]",
            title="[bold yellow]Summary[/bold yellow]",
            border_style="yellow"
        ))
    
    def confirm_deletion(self):
        """Get user confirmation for deletion
        
        Returns:
            bool: True if user confirms, False otherwise
        """
        console.print("\n[bold yellow]Type 'YES' (all caps) to proceed with deletion:[/bold yellow]")
        response = console.input("[bold red]> [/bold red]").strip()
        return response == "YES"
    
    def delete_files(self):
        """Delete the scanned temporary files"""
        try:
            deleted_count = 0
            deleted_size = 0
            errors = 0
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                console=console
            ) as progress:
                task = progress.add_task(
                    "[red]Deleting files...",
                    total=len(self.files_to_delete)
                )
                
                for file_info in self.files_to_delete:
                    try:
                        os.remove(file_info['path'])
                        deleted_count += 1
                        deleted_size += file_info['size']
                    except Exception:
                        errors += 1
                    progress.update(task, advance=1)
            
            # Display results
            console.print("\n")
            deleted_mb = deleted_size / (1024 * 1024)
            
            if errors == 0:
                console.print(Panel(
                    f"[green]✓ Cleanup completed successfully![/green]\n\n"
                    f"Files deleted: {deleted_count}\n"
                    f"Space freed: {deleted_mb:.2f} MB",
                    title="[bold green]Success[/bold green]",
                    border_style="green"
                ))
            else:
                console.print(Panel(
                    f"[yellow]Cleanup completed with some errors[/yellow]\n\n"
                    f"Files deleted: {deleted_count}\n"
                    f"Space freed: {deleted_mb:.2f} MB\n"
                    f"Errors: {errors} files could not be deleted\n\n"
                    f"[dim]Some files may be in use or require elevated permissions.[/dim]",
                    title="[bold yellow]Partial Success[/bold yellow]",
                    border_style="yellow"
                ))
        except Exception as e:
            console.print(f"[red]Error during deletion: {e}[/red]")
    
    def run(self):
        """Execute the temp file cleaner"""
        try:
            console.print("\n[bold cyan]Temporary File Cleaner[/bold cyan]")
            console.print("\n[white]Clean up temporary files to free disk space.[/white]")
            
            console.print("\n[bold cyan]Select cleaning mode:[/bold cyan]")
            console.print("1. Scan safe system locations (recommended)")
            console.print("2. Scan custom directory")
            console.print("3. Return to main menu")
            
            choice = console.input("\n[bold green]Select option (1-3): [/bold green]").strip()
            
            if choice == "1":
                # Scan safe locations
                console.print("\n[cyan]Scanning safe temporary file locations...[/cyan]")
                
                locations = self.get_safe_temp_locations()
                
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    console=console
                ) as progress:
                    task = progress.add_task("[cyan]Scanning...", total=len(locations))
                    
                    for path, desc, age_days in locations:
                        self.scan_directory(path, age_days, max_depth=2)
                        progress.update(task, advance=1)
                
                self.display_scan_report()
                
                if self.files_to_delete and self.confirm_deletion():
                    self.delete_files()
                else:
                    console.print("\n[yellow]Deletion cancelled.[/yellow]")
            
            elif choice == "2":
                # Custom path
                path = console.input("\n[yellow]Enter directory path to clean: [/yellow]").strip()
                path = os.path.expanduser(path)
                
                if self.scan_custom_path(path):
                    self.display_scan_report()
                    
                    if self.files_to_delete and self.confirm_deletion():
                        self.delete_files()
                    else:
                        console.print("\n[yellow]Deletion cancelled.[/yellow]")
            
            elif choice == "3":
                return
            else:
                console.print("[red]Invalid option![/red]")
            
            input("\nPress Enter to return to menu...")
        except KeyboardInterrupt:
            console.print("\n[yellow]Operation cancelled.[/yellow]")
            input("\nPress Enter to return to menu...")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            input("\nPress Enter to return to menu...")
