"""File Type Identifier - Magic bytes analysis"""

import os
import magic
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


class FileTypeIdentifier:
    """Identifies file types using magic bytes"""
    
    def __init__(self):
        self.name = "File Type Identifier"
        # Common extension to MIME type mappings
        self.extension_mapping = {
            '.txt': 'text/plain',
            '.pdf': 'application/pdf',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.zip': 'application/zip',
            '.exe': 'application/x-dosexec',
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            '.mp3': 'audio/mpeg',
            '.mp4': 'video/mp4',
            '.avi': 'video/x-msvideo',
            '.html': 'text/html',
            '.css': 'text/css',
            '.js': 'text/javascript',
            '.json': 'application/json',
            '.xml': 'application/xml',
            '.py': 'text/x-python',
            '.sh': 'text/x-shellscript'
        }
    
    def analyze_file(self, file_path):
        """Analyze file type using magic bytes
        
        Args:
            file_path: Path to the file to analyze
            
        Returns:
            dict: Analysis results with mime type, description, and warnings
        """
        try:
            if not os.path.exists(file_path):
                return {
                    'error': 'File not found',
                    'path': file_path
                }
            
            # Get actual MIME type using magic bytes
            mime = magic.Magic(mime=True)
            actual_mime = mime.from_file(file_path)
            
            # Get file description
            mime_desc = magic.Magic()
            description = mime_desc.from_file(file_path)
            
            # Get file extension
            file_ext = Path(file_path).suffix.lower()
            
            # Check for extension mismatch
            expected_mime = self.extension_mapping.get(file_ext, 'unknown')
            mismatch = False
            
            if expected_mime != 'unknown' and actual_mime != expected_mime:
                # Some mime types have variations, check for partial matches
                if not (expected_mime in actual_mime or actual_mime in expected_mime):
                    mismatch = True
            
            return {
                'filename': os.path.basename(file_path),
                'path': file_path,
                'extension': file_ext if file_ext else 'No extension',
                'actual_mime': actual_mime,
                'expected_mime': expected_mime,
                'description': description,
                'mismatch': mismatch,
                'size': os.path.getsize(file_path)
            }
        except Exception as e:
            return {
                'error': str(e),
                'path': file_path
            }
    
    def display_analysis(self, analysis):
        """Display file analysis results
        
        Args:
            analysis: Dictionary containing analysis results
        """
        if 'error' in analysis:
            console.print(Panel(
                f"[red]✗ Error analyzing file[/red]\n\n"
                f"Path: {analysis['path']}\n"
                f"Error: {analysis['error']}",
                title="[bold red]Error[/bold red]",
                border_style="red"
            ))
            return
        
        # Create info table
        table = Table(show_header=False, border_style="cyan", padding=(0, 2))
        table.add_column("Property", style="cyan bold")
        table.add_column("Value", style="white")
        
        table.add_row("Filename", analysis['filename'])
        table.add_row("Extension", analysis['extension'])
        table.add_row("Actual MIME Type", analysis['actual_mime'])
        table.add_row("Expected MIME Type", analysis['expected_mime'])
        table.add_row("Description", analysis['description'])
        table.add_row("Size", f"{analysis['size']:,} bytes")
        
        # Determine panel color and message
        if analysis['mismatch']:
            border_color = "red"
            title = "[bold red]⚠ WARNING: Extension Mismatch Detected![/bold red]"
            warning_msg = (
                "\n[bold red]SECURITY WARNING:[/bold red]\n"
                f"The file extension '{analysis['extension']}' does not match "
                f"the actual file type!\n\n"
                f"[yellow]This could indicate:[/yellow]\n"
                "  • File has been renamed to hide its true nature\n"
                "  • Potential malware disguised with a fake extension\n"
                "  • Social engineering attempt\n"
                "  • Accidental file renaming\n\n"
                "[bold]Exercise caution before opening this file![/bold]"
            )
        else:
            border_color = "green"
            title = "[bold green]✓ File Type Analysis[/bold green]"
            warning_msg = "\n[green]File extension matches the actual file type.[/green]"
        
        console.print("\n")
        console.print(Panel(
            table,
            title=title,
            border_style=border_color,
            padding=(1, 2)
        ))
        
        if analysis['mismatch']:
            console.print(Panel(
                warning_msg,
                title="[bold red]Security Alert[/bold red]",
                border_style="red",
                padding=(1, 2)
            ))
    
    def run(self):
        """Execute the file type identifier"""
        try:
            console.print("\n[bold cyan]File Type Identifier (Magic Bytes Analysis)[/bold cyan]")
            console.print("\nThis tool analyzes files based on their actual content,")
            console.print("not just their file extension, to detect potential threats.")
            
            file_path = console.input("\n[yellow]Enter file path to analyze: [/yellow]").strip()
            
            if not file_path:
                console.print("[red]No file path provided.[/red]")
                input("\nPress Enter to return to menu...")
                return
            
            console.print("\n[cyan]Analyzing file...[/cyan]")
            analysis = self.analyze_file(file_path)
            self.display_analysis(analysis)
            
            input("\nPress Enter to return to menu...")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            input("\nPress Enter to return to menu...")
