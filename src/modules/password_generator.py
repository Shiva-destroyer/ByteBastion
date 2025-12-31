"""Secure Password Generator"""

import secrets
import string
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


class PasswordGenerator:
    """Generates secure random passwords using cryptographic methods"""
    
    def __init__(self):
        self.name = "Secure Password Generator"
    
    def generate_password(self, length=16, use_uppercase=True, use_digits=True, 
                         use_symbols=True, use_lowercase=True):
        """Generate a cryptographically secure random password
        
        Args:
            length: Length of the password (minimum 8)
            use_uppercase: Include uppercase letters
            use_digits: Include digits
            use_symbols: Include special symbols
            use_lowercase: Include lowercase letters
            
        Returns:
            str: Generated password or None on error
        """
        try:
            if length < 8:
                console.print("[yellow]Warning: Minimum length is 8. Using 8.[/yellow]")
                length = 8
            
            # Build character set based on options
            characters = ""
            password_chars = []
            
            if use_lowercase:
                characters += string.ascii_lowercase
                # Ensure at least one lowercase character
                password_chars.append(secrets.choice(string.ascii_lowercase))
            
            if use_uppercase:
                characters += string.ascii_uppercase
                # Ensure at least one uppercase character
                password_chars.append(secrets.choice(string.ascii_uppercase))
            
            if use_digits:
                characters += string.digits
                # Ensure at least one digit
                password_chars.append(secrets.choice(string.digits))
            
            if use_symbols:
                symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
                characters += symbols
                # Ensure at least one symbol
                password_chars.append(secrets.choice(symbols))
            
            if not characters:
                console.print("[red]Error: At least one character type must be selected![/red]")
                return None
            
            # Fill the remaining length with random characters
            remaining_length = length - len(password_chars)
            for _ in range(remaining_length):
                password_chars.append(secrets.choice(characters))
            
            # Shuffle the password characters using secrets
            # Convert to list and shuffle by swapping
            for i in range(len(password_chars) - 1, 0, -1):
                j = secrets.randbelow(i + 1)
                password_chars[i], password_chars[j] = password_chars[j], password_chars[i]
            
            return ''.join(password_chars)
        except Exception as e:
            console.print(f"[red]Error generating password: {e}[/red]")
            return None
    
    def calculate_entropy(self, length, charset_size):
        """Calculate password entropy in bits
        
        Args:
            length: Password length
            charset_size: Size of character set used
            
        Returns:
            float: Entropy in bits
        """
        import math
        return length * math.log2(charset_size)
    
    def display_password(self, password, config):
        """Display generated password in a secure panel
        
        Args:
            password: The generated password
            config: Dictionary with password configuration
        """
        # Calculate character set size
        charset_size = 0
        if config['lowercase']:
            charset_size += 26
        if config['uppercase']:
            charset_size += 26
        if config['digits']:
            charset_size += 10
        if config['symbols']:
            charset_size += 22  # Approximate number of symbols
        
        entropy = self.calculate_entropy(len(password), charset_size)
        
        # Determine strength
        if entropy < 50:
            strength = "[red]Weak[/red]"
            strength_color = "red"
        elif entropy < 75:
            strength = "[yellow]Moderate[/yellow]"
            strength_color = "yellow"
        elif entropy < 100:
            strength = "[green]Strong[/green]"
            strength_color = "green"
        else:
            strength = "[bold green]Very Strong[/bold green]"
            strength_color = "green"
        
        # Create configuration table
        config_table = Table(show_header=False, border_style="cyan", padding=(0, 1))
        config_table.add_column("Setting", style="cyan")
        config_table.add_column("Value", style="white")
        
        config_table.add_row("Length", str(len(password)))
        config_table.add_row("Lowercase", "✓" if config['lowercase'] else "✗")
        config_table.add_row("Uppercase", "✓" if config['uppercase'] else "✗")
        config_table.add_row("Digits", "✓" if config['digits'] else "✗")
        config_table.add_row("Symbols", "✓" if config['symbols'] else "✗")
        config_table.add_row("Charset Size", str(charset_size))
        config_table.add_row("Entropy", f"{entropy:.1f} bits")
        config_table.add_row("Strength", strength)
        
        console.print("\n")
        console.print(Panel(
            f"[bold yellow]{password}[/bold yellow]",
            title="[bold cyan]🔐 Generated Password[/bold cyan]",
            border_style=strength_color,
            padding=(1, 2)
        ))
        
        console.print(Panel(
            config_table,
            title="[bold cyan]Password Configuration[/bold cyan]",
            border_style="cyan",
            padding=(1, 2)
        ))
        
        console.print("\n[dim]⚠ Store this password in a secure password manager.[/dim]")
    
    def get_user_preferences(self):
        """Get password generation preferences from user
        
        Returns:
            dict: User preferences or None if cancelled
        """
        try:
            console.print("\n[bold cyan]Password Generation Options[/bold cyan]\n")
            
            # Get length
            length_input = console.input("[yellow]Password length (8-128, default 16): [/yellow]").strip()
            try:
                length = int(length_input) if length_input else 16
                if length < 8:
                    length = 8
                elif length > 128:
                    length = 128
            except ValueError:
                console.print("[yellow]Invalid length, using default (16)[/yellow]")
                length = 16
            
            # Get character type preferences
            console.print("\n[cyan]Include character types:[/cyan]")
            
            lowercase_input = console.input("Include lowercase letters? (Y/n): ").strip().lower()
            use_lowercase = lowercase_input != 'n'
            
            uppercase_input = console.input("Include uppercase letters? (Y/n): ").strip().lower()
            use_uppercase = uppercase_input != 'n'
            
            digits_input = console.input("Include digits? (Y/n): ").strip().lower()
            use_digits = digits_input != 'n'
            
            symbols_input = console.input("Include symbols? (Y/n): ").strip().lower()
            use_symbols = symbols_input != 'n'
            
            if not (use_lowercase or use_uppercase or use_digits or use_symbols):
                console.print("[red]Error: At least one character type must be selected![/red]")
                return None
            
            return {
                'length': length,
                'lowercase': use_lowercase,
                'uppercase': use_uppercase,
                'digits': use_digits,
                'symbols': use_symbols
            }
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            return None
    
    def run(self):
        """Execute the password generator"""
        try:
            console.print("\n[bold cyan]Secure Password Generator[/bold cyan]")
            console.print("\n[white]Generate cryptographically secure random passwords.[/white]")
            
            preferences = self.get_user_preferences()
            
            if preferences:
                console.print("\n[cyan]Generating password...[/cyan]")
                password = self.generate_password(
                    length=preferences['length'],
                    use_lowercase=preferences['lowercase'],
                    use_uppercase=preferences['uppercase'],
                    use_digits=preferences['digits'],
                    use_symbols=preferences['symbols']
                )
                
                if password:
                    self.display_password(password, preferences)
            
            input("\nPress Enter to return to menu...")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            input("\nPress Enter to return to menu...")
