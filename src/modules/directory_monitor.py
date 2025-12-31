"""Directory Sync Monitor"""

import os
import time
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.layout import Layout

console = Console()


class DirectorySyncMonitor:
    """Monitors directories for changes in real-time"""
    
    def __init__(self):
        self.name = "Directory Sync Monitor"
        self.events = []
        self.max_events = 50  # Keep last 50 events
    
    class EventHandler(FileSystemEventHandler):
        """Handler for file system events"""
        
        def __init__(self, monitor):
            self.monitor = monitor
            super().__init__()
        
        def format_event(self, event_type, src_path, dest_path=None):
            """Format an event for display
            
            Args:
                event_type: Type of event (created, modified, deleted, moved)
                src_path: Source path
                dest_path: Destination path (for moved events)
                
            Returns:
                dict: Formatted event data
            """
            return {
                'timestamp': datetime.now().strftime("%H:%M:%S"),
                'type': event_type,
                'path': src_path,
                'dest_path': dest_path,
                'is_directory': os.path.isdir(src_path) if os.path.exists(src_path) else False
            }
        
        def on_created(self, event):
            """Called when a file or directory is created"""
            if not event.is_directory:
                self.monitor.add_event(self.format_event('Created', event.src_path))
        
        def on_modified(self, event):
            """Called when a file or directory is modified"""
            if not event.is_directory:
                self.monitor.add_event(self.format_event('Modified', event.src_path))
        
        def on_deleted(self, event):
            """Called when a file or directory is deleted"""
            if not event.is_directory:
                self.monitor.add_event(self.format_event('Deleted', event.src_path))
        
        def on_moved(self, event):
            """Called when a file or directory is moved"""
            if not event.is_directory:
                self.monitor.add_event(self.format_event('Moved', event.src_path, event.dest_path))
    
    def add_event(self, event):
        """Add an event to the list
        
        Args:
            event: Event dictionary to add
        """
        self.events.append(event)
        # Keep only the last max_events
        if len(self.events) > self.max_events:
            self.events.pop(0)
    
    def create_events_table(self):
        """Create a rich table with recent events
        
        Returns:
            Table: Rich table with events
        """
        table = Table(
            title=f"[bold cyan]Recent File System Events[/bold cyan] (Last {len(self.events)})",
            show_header=True,
            header_style="bold magenta",
            border_style="cyan"
        )
        
        table.add_column("Time", style="yellow", width=10)
        table.add_column("Event", style="cyan", width=12)
        table.add_column("Path", style="white")
        
        if not self.events:
            table.add_row("--:--:--", "No events", "Waiting for file system activity...")
        else:
            # Show most recent events first
            for event in reversed(self.events[-20:]):  # Show last 20
                event_type = event['type']
                
                # Color code event types
                if event_type == 'Created':
                    event_style = "[green]Created[/green]"
                elif event_type == 'Modified':
                    event_style = "[yellow]Modified[/yellow]"
                elif event_type == 'Deleted':
                    event_style = "[red]Deleted[/red]"
                elif event_type == 'Moved':
                    event_style = "[blue]Moved[/blue]"
                else:
                    event_style = event_type
                
                # Format path
                if event['dest_path']:
                    path_str = f"{os.path.basename(event['path'])} → {os.path.basename(event['dest_path'])}"
                else:
                    path_str = event['path']
                
                table.add_row(
                    event['timestamp'],
                    event_style,
                    path_str
                )
        
        return table
    
    def monitor_directory(self, path):
        """Monitor a directory for changes
        
        Args:
            path: Path to directory to monitor
        """
        try:
            if not os.path.exists(path):
                console.print(f"[red]Error: Directory not found: {path}[/red]")
                return
            
            if not os.path.isdir(path):
                console.print(f"[red]Error: Path is not a directory: {path}[/red]")
                return
            
            console.print(f"\n[cyan]Starting monitoring of: {path}[/cyan]")
            console.print("[yellow]Press Ctrl+C to stop monitoring[/yellow]\n")
            
            # Create observer and event handler
            event_handler = self.EventHandler(self)
            observer = Observer()
            observer.schedule(event_handler, path, recursive=True)
            observer.start()
            
            # Create initial info panel
            info_panel = Panel(
                f"[green]✓ Monitoring active[/green]\n\n"
                f"Directory: [cyan]{path}[/cyan]\n"
                f"Mode: Recursive (includes subdirectories)\n"
                f"Events tracked: Created, Modified, Deleted, Moved\n\n"
                f"[yellow]Press Ctrl+C to stop[/yellow]",
                title="[bold green]Directory Monitor Status[/bold green]",
                border_style="green"
            )
            
            console.print(info_panel)
            console.print()
            
            # Live update loop
            try:
                with Live(self.create_events_table(), refresh_per_second=2, console=console) as live:
                    while True:
                        time.sleep(0.5)
                        live.update(self.create_events_table())
            except KeyboardInterrupt:
                console.print("\n\n[yellow]Stopping monitor...[/yellow]")
                observer.stop()
                observer.join()
                
                console.print("\n")
                console.print(Panel(
                    f"[green]✓ Monitoring stopped successfully![/green]\n\n"
                    f"Total events captured: {len(self.events)}\n"
                    f"Directory: {path}",
                    title="[bold green]Monitor Stopped[/bold green]",
                    border_style="green"
                ))
        except Exception as e:
            console.print(f"[red]Error during monitoring: {e}[/red]")
    
    def run(self):
        """Execute the directory monitor"""
        try:
            console.print("\n[bold cyan]Directory Sync Monitor[/bold cyan]")
            console.print("\n[white]Real-time monitoring of file system changes.[/white]")
            
            # Get directory to monitor
            console.print("\n[yellow]Enter directory path to monitor:[/yellow]")
            console.print("[dim]Examples: /home/user/Documents, ~/Downloads, .[/dim]")
            
            dir_path = console.input("\n[bold green]Path: [/bold green]").strip()
            
            if not dir_path:
                console.print("[red]No path provided.[/red]")
                input("\nPress Enter to return to menu...")
                return
            
            # Expand ~ to home directory
            dir_path = os.path.expanduser(dir_path)
            
            # Start monitoring
            self.monitor_directory(dir_path)
            
            input("\nPress Enter to return to menu...")
        except KeyboardInterrupt:
            console.print("\n[yellow]Operation cancelled.[/yellow]")
            input("\nPress Enter to return to menu...")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            input("\nPress Enter to return to menu...")
