import typer
from rich.console import Console
from crypto.encryptor import encrypt_file
from crypto.decryptor import decrypt_file
from crypto.utils import wipe_file
import sys
import os

app = typer.Typer()
console = Console()

@app.command()
def encrypt(
    file: str = typer.Option(..., '--file', '-f', help='File to encrypt'),
    password: str = typer.Option(None, '--password', '-p', help='Password for encryption'),
    auto_wipe: int = typer.Option(None, '--auto-wipe', help='Auto-wipe decrypted file after X seconds'),
    hint: str = typer.Option(None, '--hint', help='Optional password hint'),
    overwrite: bool = typer.Option(False, '--overwrite', help='Overwrite output file if exists'),
):
    """Encrypt a file with a password."""
    if not password:
        password = typer.prompt('Enter password', hide_input=True, confirmation_prompt=True)
    try:
        out_file = encrypt_file(file, password, hint=hint, overwrite=overwrite)
        console.print(f'[green]File encrypted:[/] {out_file}')
        if auto_wipe:
            console.print(f'[yellow]Auto-wipe enabled. Decrypted file will be deleted after {auto_wipe} seconds.[/]')
    except Exception as e:
        console.print(f'[red]Encryption failed:[/] {e}')
        sys.exit(1)

@app.command()
def decrypt(
    file: str = typer.Option(..., '--file', '-f', help='File to decrypt'),
    password: str = typer.Option(None, '--password', '-p', help='Password for decryption'),
    auto_wipe: int = typer.Option(None, '--auto-wipe', help='Auto-wipe decrypted file after X seconds'),
    overwrite: bool = typer.Option(False, '--overwrite', help='Overwrite output file if exists'),
):
    """Decrypt a file with a password."""
    if not password:
        password = typer.prompt('Enter password', hide_input=True)
    try:
        out_file = decrypt_file(file, password, overwrite=overwrite)
        console.print(f'[green]File decrypted:[/] {out_file}')
        if auto_wipe:
            import threading, time
            def auto_delete():
                time.sleep(auto_wipe)
                wipe_file(out_file)
                console.print(f'[yellow]Decrypted file auto-wiped: {out_file}[/]')
            threading.Thread(target=auto_delete, daemon=True).start()
    except Exception as e:
        console.print(f'[red]Decryption failed:[/] {e}')
        sys.exit(1)

@app.command()
def test():
    """Test encryption and decryption correctness."""
    from tests.test_encrypt import run_encrypt_test
    from tests.test_decrypt import run_decrypt_test
    encrypt_ok = run_encrypt_test()
    decrypt_ok = run_decrypt_test()
    if encrypt_ok and decrypt_ok:
        console.print('[green]All tests passed![/]')
    else:
        console.print('[red]Some tests failed.[/]')
        sys.exit(1)

if __name__ == '__main__':
    app() 