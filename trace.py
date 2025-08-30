import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
from rich.progress import track
import argparse
import os

console = Console()

# CLI Arguments
parser = argparse.ArgumentParser(description="Live Tracker Info Scraper")
parser.add_argument("-num", help="Phone number to search")
parser.add_argument("-l", help="File path to a list of numbers")
args = parser.parse_args()

# Request Details
url = "https://live-tracker.site/"
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:138.0) Gecko/20100101 Firefox/138.0",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://live-tracker.site",
    "Referer": "https://live-tracker.site/",
}

def fetch_info(number):
    data = {"searchinfo": number}
    try:
        response = requests.post(url, headers=headers, data=data, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        containers = soup.find_all("div", class_="resultcontainer")
        return containers
    except Exception as e:
        return []

def print_result(number, containers):
    if not containers:
        console.print(f"❌ [bold red]No records found for {number}[/bold red]")
    else:
        console.print(f"\n📱 [bold green]Results for:[/bold green] [bold cyan]{number}[/bold cyan]")
        for i, container in enumerate(containers, start=1):
            table = Table(title=f"📄 Entry #{i} | Just Hacked On 👽", show_lines=True, border_style="green")
            table.add_column("🔖 Field", style="bold yellow", width=12)
            table.add_column("📝 Value", style="white")

            rows = container.find_all("div", class_="row")
            for row in rows:
                key = row.find("span", class_="detailshead").text.strip(" :")
                val = row.find("span", class_="details").text.strip()
                table.add_row(key, val)

            console.print(table)

def save_to_file(number, containers, filename):
    with open(filename, "a", encoding="utf-8") as f:
        if not containers:
            f.write(f"No records found for {number}\n\n")
        else:
            f.write(f"\nResults for {number}\n")
            for i, container in enumerate(containers, start=1):
                f.write(f"--- Entry #{i} ---\n")
                rows = container.find_all("div", class_="row")
                for row in rows:
                    key = row.find("span", class_="detailshead").text.strip(" :")
                    val = row.find("span", class_="details").text.strip()
                    f.write(f"{key}: {val}\n")
                f.write("\n")

# === Mode 1: Single Number ===
if args.num:
    containers = fetch_info(args.num)
    print_result(args.num, containers)

# === Mode 2: List of Numbers ===
elif args.l:
    if not os.path.isfile(args.l):
        console.print(f"❌ [bold red]File not found: {args.l}[/bold red]")
    else:
        output_file = "results.txt"
        if os.path.exists(output_file):
            os.remove(output_file)  # remove old output file

        with open(args.l, "r") as f:
            numbers = [line.strip() for line in f if line.strip()]

        for number in track(numbers, description="📡 Scanning..."):
            containers = fetch_info(number)
            save_to_file(number, containers, output_file)

        console.print(f"\n✅ [bold green]Saved all results to {output_file}[/bold green]")

else:
    console.print("[bold red]❗ Please provide -num OR -l argument[/bold red]")
