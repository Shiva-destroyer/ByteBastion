"""AES Encryption/Decryption"""

import os
import secrets
from pathlib import Path
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn

console = Console()


class AESCrypto:
    """AES encryption and decryption for files using PBKDF2 key derivation"""
    
    def __init__(self):
        self.name = "AES Encryption/Decryption"
        self.salt_size = 16  # 16 bytes for salt
        self.iv_size = 16    # 16 bytes for IV (AES block size)
        self.key_size = 32   # 32 bytes = 256 bits for AES-256
        self.iterations = 100000  # PBKDF2 iterations
    
    def derive_key(self, password, salt):
        """Derive encryption key from password using PBKDF2
        
        Args:
            password: User password (string)
            salt: Random salt bytes
            
        Returns:
            bytes: Derived key
        """
        try:
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=self.key_size,
                salt=salt,
                iterations=self.iterations,
                backend=default_backend()
            )
            return kdf.derive(password.encode())
        except Exception as e:
            console.print(f"[red]Error deriving key: {e}[/red]")
            return None
    
    def encrypt_file(self, input_path, password):
        """Encrypt a file using AES-256-CBC
        
        Args:
            input_path: Path to file to encrypt
            password: Encryption password
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not os.path.exists(input_path):
                console.print(f"[red]Error: File not found: {input_path}[/red]")
                return False
            
            # Generate random salt and IV
            salt = secrets.token_bytes(self.salt_size)
            iv = secrets.token_bytes(self.iv_size)
            
            # Derive key from password
            console.print("\n[cyan]Deriving encryption key...[/cyan]")
            key = self.derive_key(password, salt)
            if not key:
                return False
            
            # Read input file
            with open(input_path, 'rb') as f:
                plaintext = f.read()
            
            file_size = len(plaintext)
            console.print(f"[cyan]File size: {file_size:,} bytes[/cyan]")
            
            # Add PKCS7 padding
            padding_length = 16 - (len(plaintext) % 16)
            plaintext += bytes([padding_length] * padding_length)
            
            # Create cipher and encrypt
            console.print("[cyan]Encrypting...[/cyan]")
            cipher = Cipher(
                algorithms.AES(key),
                modes.CBC(iv),
                backend=default_backend()
            )
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(plaintext) + encryptor.finalize()
            
            # Write encrypted file with .enc extension
            output_path = input_path + '.enc'
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                console=console
            ) as progress:
                task = progress.add_task("[green]Writing encrypted file...", total=1)
                
                with open(output_path, 'wb') as f:
                    # Write file format: SALT (16) + IV (16) + CIPHERTEXT
                    f.write(salt)
                    f.write(iv)
                    f.write(ciphertext)
                
                progress.update(task, advance=1)
            
            console.print("\n")
            console.print(Panel(
                f"[green]✓ File encrypted successfully![/green]\n\n"
                f"Original: {os.path.basename(input_path)}\n"
                f"Encrypted: {os.path.basename(output_path)}\n"
                f"Algorithm: AES-256-CBC\n"
                f"Key Derivation: PBKDF2-HMAC-SHA256\n"
                f"Iterations: {self.iterations:,}\n\n"
                f"[yellow]Keep your password safe - it cannot be recovered![/yellow]",
                title="[bold green]Encryption Complete[/bold green]",
                border_style="green"
            ))
            
            return True
        except Exception as e:
            console.print(f"[red]Error during encryption: {e}[/red]")
            return False
    
    def decrypt_file(self, input_path, password):
        """Decrypt an AES-encrypted file
        
        Args:
            input_path: Path to encrypted file
            password: Decryption password
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not os.path.exists(input_path):
                console.print(f"[red]Error: File not found: {input_path}[/red]")
                return False
            
            if not input_path.endswith('.enc'):
                console.print("[yellow]Warning: File doesn't have .enc extension[/yellow]")
            
            # Read encrypted file
            with open(input_path, 'rb') as f:
                # Read salt, IV, and ciphertext
                salt = f.read(self.salt_size)
                iv = f.read(self.iv_size)
                ciphertext = f.read()
            
            if len(salt) != self.salt_size or len(iv) != self.iv_size:
                console.print("[red]Error: Invalid encrypted file format[/red]")
                return False
            
            # Derive key from password
            console.print("\n[cyan]Deriving decryption key...[/cyan]")
            key = self.derive_key(password, salt)
            if not key:
                return False
            
            # Decrypt
            console.print("[cyan]Decrypting...[/cyan]")
            cipher = Cipher(
                algorithms.AES(key),
                modes.CBC(iv),
                backend=default_backend()
            )
            decryptor = cipher.decryptor()
            
            try:
                padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
            except Exception as e:
                console.print(Panel(
                    f"[red]✗ Decryption failed![/red]\n\n"
                    f"This could mean:\n"
                    f"  • Wrong password\n"
                    f"  • Corrupted file\n"
                    f"  • Invalid encrypted file format\n\n"
                    f"Error: {str(e)}",
                    title="[bold red]Decryption Error[/bold red]",
                    border_style="red"
                ))
                return False
            
            # Remove PKCS7 padding
            padding_length = padded_plaintext[-1]
            plaintext = padded_plaintext[:-padding_length]
            
            # Write decrypted file (remove .enc extension)
            if input_path.endswith('.enc'):
                output_path = input_path[:-4]
            else:
                output_path = input_path + '.dec'
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                console=console
            ) as progress:
                task = progress.add_task("[green]Writing decrypted file...", total=1)
                
                with open(output_path, 'wb') as f:
                    f.write(plaintext)
                
                progress.update(task, advance=1)
            
            console.print("\n")
            console.print(Panel(
                f"[green]✓ File decrypted successfully![/green]\n\n"
                f"Encrypted: {os.path.basename(input_path)}\n"
                f"Decrypted: {os.path.basename(output_path)}\n"
                f"Size: {len(plaintext):,} bytes",
                title="[bold green]Decryption Complete[/bold green]",
                border_style="green"
            ))
            
            return True
        except Exception as e:
            console.print(f"[red]Error during decryption: {e}[/red]")
            return False
    
    def run(self):
        """Execute the AES crypto tool"""
        try:
            console.print("\n[bold cyan]AES Encryption/Decryption[/bold cyan]")
            console.print("\n[white]Encrypt or decrypt files using AES-256-CBC.[/white]")
            console.print("[dim]Uses PBKDF2-HMAC-SHA256 for key derivation.[/dim]")
            
            console.print("\n1. Encrypt a file")
            console.print("2. Decrypt a file")
            console.print("3. Return to main menu")
            
            choice = console.input("\n[bold green]Select option (1-3): [/bold green]").strip()
            
            if choice == "1":
                file_path = console.input("\n[yellow]Enter file path to encrypt: [/yellow]").strip()
                if not file_path:
                    console.print("[red]No file path provided.[/red]")
                    input("\nPress Enter to return to menu...")
                    return
                
                password = console.input("[yellow]Enter encryption password: [/yellow]", password=True).strip()
                if not password:
                    console.print("[red]Password cannot be empty.[/red]")
                    input("\nPress Enter to return to menu...")
                    return
                
                confirm_password = console.input("[yellow]Confirm password: [/yellow]", password=True).strip()
                if password != confirm_password:
                    console.print("[red]Passwords do not match![/red]")
                    input("\nPress Enter to return to menu...")
                    return
                
                if len(password) < 8:
                    console.print("[yellow]Warning: Password is weak. Use at least 8 characters.[/yellow]")
                
                self.encrypt_file(file_path, password)
            
            elif choice == "2":
                file_path = console.input("\n[yellow]Enter encrypted file path: [/yellow]").strip()
                if not file_path:
                    console.print("[red]No file path provided.[/red]")
                    input("\nPress Enter to return to menu...")
                    return
                
                password = console.input("[yellow]Enter decryption password: [/yellow]", password=True).strip()
                if not password:
                    console.print("[red]Password cannot be empty.[/red]")
                    input("\nPress Enter to return to menu...")
                    return
                
                self.decrypt_file(file_path, password)
            
            elif choice == "3":
                return
            else:
                console.print("[red]Invalid option![/red]")
            
            input("\nPress Enter to return to menu...")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            input("\nPress Enter to return to menu...")
