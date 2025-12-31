"""Disk Space Analyzer with Alerts"""

import os
import psutil
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, track

console = Console()


class DiskSpaceAnalyzer:
    """Analyzes disk space usage and provides alerts"""
    
    def __init__(self):
        self.name = "Disk Space Analyzer"
        self.warning_threshold = 80  # Warning at 80%
        self.critical_threshold = 90  # Critical at 90%
    
    def get_partition_usage(self):
        """Get disk usage for all mounted partitions
        
        Returns:
            list: List of partition info dictionaries
        """
        partitions = []
        
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                
                # Calculate percentage
                percent = usage.percent
                
                # Determine status
                if percent >= self.critical_threshold:
                    status = "critical"
                    status_color = "red"
                elif percent >= self.warning_threshold:
                    status = "warning"
                    status_color = "yellow"
                else:
                    status = "ok"
                    status_color = "green"
                
                partitions.append({
                    'device': partition.device,
                    'mountpoint': partition.mountpoint,
                    'fstype': partition.fstype,
                    'total': usage.total,
                    'used': usage.used,
                    'free': usage.free,
                    'percent': percent,
                    'status': status,
                    'status_color': status_color
                })
            except (PermissionError, OSError):
                # Skip partitions we can't access
                continue
        
        return partitions
    
    def format_bytes(self, bytes_value):
        """Format bytes to human-readable format
        
        Args:
            bytes_value: Size in bytes
            
        Returns:
            str: Formatted size string
        """
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.1f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.1f} PB"
    
    def create_usage_bar(self, percent, width=30):
        """Create a visual usage bar
        
        Args:
            percent: Usage percentage
            width: Width of the bar
            
        Returns:
            str: Formatted usage bar
        """
        filled = int(width * percent / 100)
        empty = width - filled
        
        if percent >= self.critical_threshold:
            color = "red"
        elif percent >= self.warning_threshold:
            color = "yellow"
        else:
            color = "green"
        
        bar = f"[{color}]{'█' * filled}[/]{' ' * empty}"
        return bar
    
    def display_partition_usage(self):
        """Display disk partition usage with visual bars"""
        console.print("\n[bold cyan]Disk Partition Analysis[/bold cyan]\n")
        
        partitions = self.get_partition_usage()
        
        if not partitions:
            console.print("[yellow]No accessible partitions found.[/yellow]")
            return
        
        # Check for critical alerts
        critical_parts = [p for p in partitions if p['status'] == 'critical']
        warning_parts = [p for p in partitions if p['status'] == 'warning']
        
        if critical_parts:
            console.print(Panel(
                f"[bold red]⚠️  CRITICAL: {len(critical_parts)} partition(s) over {self.critical_threshold}% full![/bold red]\n\n"
                f"Immediate action required to free up space.",
                title="[bold red]Disk Space Alert[/bold red]",
                border_style="red"
            ))
            console.print()
        elif warning_parts:
            console.print(Panel(
                f"[bold yellow]⚠️  WARNING: {len(warning_parts)} partition(s) over {self.warning_threshold}% full[/bold yellow]\n\n"
                f"Consider freeing up space soon.",
                title="[bold yellow]Disk Space Warning[/bold yellow]",
                border_style="yellow"
            ))
            console.print()
        
        # Create detailed table
        table = Table(
            title="[bold cyan]Partition Usage Details[/bold cyan]",
            show_header=True,
            header_style="bold magenta",
            border_style="cyan"
        )
        
        table.add_column("Mount Point", style="cyan", width=20)
        table.add_column("Filesystem", style="white", width=10)
        table.add_column("Total", justify="right", style="blue", width=12)
        table.add_column("Used", justify="right", style="yellow", width=12)
        table.add_column("Free", justify="right", style="green", width=12)
        table.add_column("Usage", style="white", width=35)
        
        for partition in partitions:
            usage_bar = self.create_usage_bar(partition['percent'])
            percent_str = f"{partition['percent']:.1f}%"
            
            table.add_row(
                partition['mountpoint'],
                partition['fstype'],
                self.format_bytes(partition['total']),
                self.format_bytes(partition['used']),
                self.format_bytes(partition['free']),
                f"{usage_bar} {percent_str}",
                style=partition['status_color'] if partition['status'] != 'ok' else None
            )
        
        console.print(table)
    
    def find_large_files(self, directory, top_n=10):
        """Find the largest files in a directory
        
        Args:
            directory: Directory to scan
            top_n: Number of top files to return
            
        Returns:
            list: List of (path, size) tuples
        """
        files = []
        
        try:
            for root, dirs, filenames in os.walk(directory):
                for filename in filenames:
                    try:
                        filepath = os.path.join(root, filename)
                        size = os.path.getsize(filepath)
                        files.append((filepath, size))
                    except (OSError, PermissionError):
                        continue
        except (OSError, PermissionError):
            pass
        
        # Sort by size (descending) and return top N
        files.sort(key=lambda x: x[1], reverse=True)
        return files[:top_n]
    
    def large_file_hunter(self):
        """Interactive large file finder"""
        try:
            console.print("\n[bold cyan]Large File Hunter[/bold cyan]")
            console.print("\n[white]Find the largest files to free up space.[/white]")
            
            # Get directory to scan
            console.print("\n[yellow]Enter directory to scan:[/yellow]")
            console.print("[dim]Examples: /home/user, ~/Downloads, .[/dim]")
            
            dir_path = console.input("\n[bold green]Path: [/bold green]").strip()
            
            if not dir_path:
                console.print("[red]No path provided.[/red]")
                return
            
            # Expand ~ to home directory
            dir_path = os.path.expanduser(dir_path)
            
            if not os.path.exists(dir_path):
                console.print(f"[red]Error: Directory not found: {dir_path}[/red]")
                return
            
            if not os.path.isdir(dir_path):
                console.print(f"[red]Error: Path is not a directory: {dir_path}[/red]")
                return
            
            # Scan for large files
            console.print(f"\n[cyan]Scanning: {dir_path}[/cyan]")
            console.print("[yellow]This may take a moment...[/yellow]\n")
            
            large_files = []
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("[cyan]Finding large files...", total=None)
                large_files = self.find_large_files(dir_path, top_n=10)
                progress.update(task, completed=True)
            
            # Display results
            if not large_files:
                console.print("\n[yellow]No files found or insufficient permissions.[/yellow]")
                return
            
            console.print("\n")
            table = Table(
                title=f"[bold cyan]Top 10 Largest Files in {dir_path}[/bold cyan]",
                show_header=True,
                header_style="bold magenta",
                border_style="cyan"
            )
            
            table.add_column("#", justify="right", style="cyan", width=5)
            table.add_column("Size", justify="right", style="yellow", width=12)
            table.add_column("Filename", style="green", width=30)
            table.add_column("Path", style="white")
            
            for idx, (filepath, size) in enumerate(large_files, 1):
                size_str = self.format_bytes(size)
                filename = os.path.basename(filepath)
                
                # Color code by size
                if size > 1024 * 1024 * 1024:  # > 1 GB
                    style = "bold red"
                elif size > 100 * 1024 * 1024:  # > 100 MB
                    style = "bold yellow"
                else:
                    style = "white"
                
                table.add_row(
                    str(idx),
                    size_str,
                    filename[:30] + "..." if len(filename) > 30 else filename,
                    filepath,
                    style=style
                )
            
            console.print(table)
            
            # Calculate total
            total_size = sum(size for _, size in large_files)
            console.print("\n")
            console.print(Panel(
                f"[cyan]Total size of top 10 files: {self.format_bytes(total_size)}[/cyan]\n\n"
                f"[dim]Consider removing or archiving these files to free space.[/dim]",
                title="[bold cyan]Summary[/bold cyan]",
                border_style="cyan"
            ))
        except KeyboardInterrupt:
            console.print("\n[yellow]Scan cancelled.[/yellow]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
    
    def run(self):
        """Execute the disk space analyzer"""
        try:
            console.print("\n[bold cyan]Disk Space Analyzer with Alerts[/bold cyan]")
            console.print("\n[white]Analyze disk usage and find space hogs.[/white]")
            
            console.print("\n[bold cyan]Select analysis mode:[/bold cyan]")
            console.print("1. Show all partition usage")
            console.print("2. Find large files (Large File Hunter)")
            console.print("3. Both")
            console.print("4. Return to main menu")
            
            choice = console.input("\n[bold green]Select option (1-4): [/bold green]").strip()
            
            if choice == "1":
                self.display_partition_usage()
            elif choice == "2":
                self.large_file_hunter()
            elif choice == "3":
                self.display_partition_usage()
                self.large_file_hunter()
            elif choice == "4":
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
