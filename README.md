# OSINT-PK 🔍

A lightweight OSINT tool to collect **publicly available information** about Pakistani phone numbers.  
Supports **single number lookups** and **bulk scanning from file lists** — perfect for researchers, students, and ethical hackers.  

> **Disclaimer:** This tool is for **educational and research purposes only**.  
> The author does **not** encourage or support illegal use.

---

## Features ✨
- Fetches name, CNIC, and address linked to a number *(if available)*  
- Lookup **single numbers** or **bulk lists**  
- Beautiful terminal output with [rich](https://github.com/Textualize/rich)  
- Automatically saves bulk results to `results.txt`  

---

## Installation ⚙️

git clone https://github.com/JustHackedOn/OSINT-PK.git
cd OSINT-PK
pip install -r requirements.txt

## Usage 🚀

python trace.py -num 03001234567

python trace.py -l numbers.txt
