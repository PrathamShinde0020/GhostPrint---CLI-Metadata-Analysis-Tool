# ghostprint.py (Main Script)

import subprocess
import json
import csv
import os
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich import box

# --- Import your custom modules ---
from utils.image_parser import extract_image_metadata_human_friendly
from utils.pdf_parser import extract_pdf_metadata_human_friendly

console = Console()

# ------------------- BANNER -------------------
def display_banner():
    console.print(r"""
                        .--.
                      .-'   `-.
                     /  \   /  \\
                    |    O O    |
                    :=)       (=:
                     \   \-/   /
                      '.___.'
    """, style="cyan")
    
    console.print(r"""
  ██████╗ ██╗  ██╗ ██████╗ ███████╗████████╗██████╗ ██████╗ ██╗███╗   ██╗████████╗
 ██╔════╝ ██║  ██║██╔═══██╗██╔════╝╚══██╔══╝██╔══██╗██╔══██╗██║████╗  ██║╚══██╔══╝
 ██║  ███╗███████║██║   ██║███████╗   ██║   ██████╔╝██████╔╝██║██╔██╗ ██║   ██║   
 ██║   ██║██╔══██║██║   ██║╚════██║   ██║   ██╔═══╝ ██╔══██╗██║██║╚██╗██║   ██║   
 ╚██████╔╝██║  ██║╚██████╔╝███████║   ██║   ██║     ██║  ██║██║██║ ╚████║   ██║   
  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝   ╚═╝     ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝   ╚═╝   
    """, style="cyan bold")
    
    console.print("👻 [cyan]Reveal the invisible. Extract the undeniable.[/]", highlight=False)
    console.print()
    console.print("🔍 [cyan]GhostPrint[/] is a powerful open-source metadata extraction tool designed for", highlight=False)
    console.print("cybersecurity analysts, digital forensic investigators, and OSINT enthusiasts.")
    console.print("It uncovers hidden traces from images, documents, and media files — giving you")
    console.print("the silent digital footprints left behind.")
    console.print()
    console.print("💀 [cyan]Use it. Trace it. Prove it.[/]", highlight=False)
    console.print()
    console.print("-" * 70, style="dim")

# ------------------- EXIFTOOL FUNCTION -------------------
def extract_metadata_exiftool(filepath):
    try:
        result = subprocess.run(["exiftool", "-json", filepath], capture_output=True, text=True)
        if result.returncode != 0:
            console.print(f"[bold red]❌ ExifTool error: {result.stderr}[/bold red]")
            return {}
        metadata = json.loads(result.stdout)[0]
        return metadata
    except FileNotFoundError:
        console.print("[bold red]❌ ExifTool not installed or not in PATH. Please install ExifTool.[/bold red]")
        return {}
    except Exception as e:
        console.print(f"[bold red]❌ Error extracting metadata with exiftool: {e}[/bold red]")
        return {}

# ------------------- DISPLAY FUNCTIONS -------------------
def display_rich_table(data, title, summary=None):
    table = Table(title=title, box=box.DOUBLE)
    table.add_column("Field", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")
    table.add_column("OSINT Risk", style="red")

    for row in data:
        table.add_row(*row)

    console.print(table)

    if summary:
        console.print("\n[bold yellow]🛡️ Summary:[/]")
        for k, v in summary.items():
            console.print(f"- {k}: {v}")

def display_full_metadata(full_data, title="Full Metadata Dump"):
    console.print(f"\n[bold blue]📦 {title}:[/]")
    for key, value in full_data.items():
        if isinstance(value, bytes):
            value = f"{len(value)} bytes [binary data]"
        console.print(f"[bold]{key}[/]: {value}")

def check_thumbnail(img):
    if img is None:
        return
        
    try:
        exif = img._getexif()
        if not exif:
            console.print("\n[bold yellow]No EXIF data found for thumbnail check.[/]")
            return
            
        thumb = exif.get(0x501B)
        if thumb:
            console.print("\n[bold green]🖼️ Embedded thumbnail found![/]")
        else:
            console.print("\n[bold yellow]No embedded thumbnail found.[/]")
    except Exception as e:
        console.print(f"\n[bold yellow]Thumbnail extraction failed: {e}[/]")

def check_binary_blocks(full_data):
    console.print("\n[bold blue]🔍 Binary Blocks:[/]")
    binary_fields = ['MakerNote', 'UserComment']
    found = False
    
    for key in binary_fields:
        if key in full_data:
            found = True
            val = full_data[key]
            
            if isinstance(val, bytes):
                console.print(f"[bold]{key}[/]: {len(val)} bytes [binary data]")
            else:
                console.print(f"[bold]{key}[/]: {val}")
    
    if not found:
        console.print("[yellow]No binary blocks found in metadata.[/yellow]")

# ------------------- EXPORT FUNCTION -------------------
def save_metadata(metadata, base_name="metadata_export"):
    if not metadata:
        console.print("[yellow]⚠️ No metadata to export[/yellow]")
        return
        
    choice = Prompt.ask("\n💾 Do you want to export metadata as json / csv / none export?", choices=["j", "c", "n"])
    
    if choice == "n":
        return
        
    try:
        base_path = Path(base_name)
        
        if choice == "j":
            file_path = f"{base_path}.json"
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=4)
            console.print(f"[green]✅ Metadata saved as {file_path}[/green]")
            
        elif choice == "c":
            file_path = f"{base_path}.csv"
            with open(file_path, "w", newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Field", "Value"])
                for k, v in metadata.items():
                    if isinstance(v, bytes):
                        v = f"[Binary data: {len(v)} bytes]"
                    writer.writerow([k, str(v)])
            console.print(f"[green]✅ Metadata saved as {file_path}[/green]")
    except Exception as e:
        console.print(f"[bold red]❌ Error saving metadata: {e}[/bold red]")

# ------------------- MAIN PROCESSING LOGIC -------------------
def process_file(file_path):
    if not os.path.exists(file_path):
        console.print("[bold red]❌ File does not exist. Please check the path and try again.[/]")
        return

    file_ext = os.path.splitext(file_path)[1].lower()
    base_name = os.path.splitext(os.path.basename(file_path))[0] + "_metadata"
    
    # Common pattern: extract metadata, display, then maybe show more details
    exiftool_meta = extract_metadata_exiftool(file_path)

    if file_ext in [".jpg", ".jpeg", ".png", ".tiff", ".tif", ".gif", ".bmp"]:
        # This now calls your imported function
        rich_data, summary, full_data, img = extract_image_metadata_human_friendly(file_path)
        display_rich_table(rich_data, f"📸 Image Metadata: {os.path.basename(file_path)}", summary)
        
        # Only offer exiftool dump if we actually got data
        if exiftool_meta:
            show = Prompt.ask("\n🧩 Show Exiftool Full Dump?", choices=["y", "n"])
            if show == "y":
                console.print("\n📦 [bold blue]Exiftool Full Metadata Dump:[/bold blue]")
                console.print_json(json.dumps(exiftool_meta, indent=4))

        # Advanced analysis options
        choices = ["r", "t", "b", "a", "skip"]
        choice = Prompt.ask("\n🧩 Do you want to see [R]emaining metadata, [T]humbnail, [B]inary data, or [A]ll?", 
                           choices=choices)
                           
        if choice != "skip":
            if 'r' in choice or 'a' in choice:
                display_full_metadata(full_data)
            if 't' in choice or 'a' in choice:
                check_thumbnail(img)
            if 'b' in choice or 'a' in choice:
                check_binary_blocks(full_data)

        # Use exiftool data for export if available, otherwise use PIL data
        save_metadata(exiftool_meta or full_data, base_name)

    elif file_ext == ".pdf":
        # This now calls your imported function
        rich_data, summary, full_meta, page_count = extract_pdf_metadata_human_friendly(file_path)
        display_rich_table(rich_data, f"📄 PDF Metadata: {os.path.basename(file_path)} ({page_count} pages)", summary)

        if exiftool_meta:
            show = Prompt.ask("\n📘 Show Exiftool Full Dump?", choices=["y", "n"])
            if show == "y":
                console.print("\n📦 [bold blue]Exiftool Full Metadata Dump:[/bold blue]")
                console.print_json(json.dumps(exiftool_meta, indent=4))

        show_pdf_raw = Prompt.ask("\n📘 Show PDF Library Metadata Dump?", choices=["y", "n"])
        if show_pdf_raw == "y":
            display_full_metadata(full_meta, "PDF Library Metadata Dump")

        save_metadata(exiftool_meta or full_meta, base_name)

    else:
        if exiftool_meta:  # Try to use exiftool for unsupported file types
            console.print(f"[yellow]⚠️ Using ExifTool for unsupported file type: {file_ext}[/yellow]")
            console.print("\n📦 [bold blue]Exiftool Metadata Dump:[/bold blue]")
            console.print_json(json.dumps(exiftool_meta, indent=4))
            save_metadata(exiftool_meta, base_name)
        else:
            console.print("[bold red]❌ Unsupported file type and ExifTool extraction failed.[/]")
            console.print("Supported types: .pdf, .jpg, .jpeg, .png, .tiff, .tif, .gif, .bmp")

def main():
    # Display the banner at the start of the program
    display_banner()
    
    console.print("\n[bold cyan]🔍 Metadata Extraction Tool[/bold cyan]")
    console.print("[bold yellow]🛡️ OSINT Awareness:[/] Metadata can reveal more than you think.")
    console.print("Use with OSINT tools like [bold green]Maltego, Spiderfoot, or Recon-ng[/] for deeper investigation.\n")
    
    while True:
        file_path = Prompt.ask("📂 Enter the path of the file to analyze (or 'q' to quit)")
        
        if file_path.lower() in ('q', 'quit', 'exit'):
            console.print("[bold green]👋 Thank you for using the Metadata Extraction Tool![/]")
            break
            
        process_file(file_path)
        console.print("\n" + "-" * 50 + "\n")

if __name__ == "__main__":
    main()