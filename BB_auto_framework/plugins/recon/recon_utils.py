import os
import re
from core.logger import setup_logger

logger = setup_logger()

def ensure_dirs(output_dir, tools):
    os.makedirs(output_dir, exist_ok=True)
    for tool in tools:
        os.makedirs(os.path.join(output_dir, tool), exist_ok=True)

def parse_output(output_dir, output_file):
    """
    Parse the output file and return sets of subdomains, ASNs, IPv4s, and IPv6s.
    
    Args:
        output_dir (str): Directory containing the output file
        output_file (str): Path to the output file
    
    Returns:
        tuple: (subdomains, asns, ipv4s, ipv6s)
    """
    subdomains, asns, ipv4s, ipv6s = set(), set(), set(), set()
    try:
        # Use absolute path to avoid double joining
        abs_output_file = os.path.abspath(output_file)
        with open(abs_output_file, "r") as f:
            for line in f:
                line = line.strip()

                if re.match(r"^\d+\.\d+\.\d+\.\d+$", line):
                    ipv4s.add(line)
                elif re.match(r"^[0-9a-fA-F:]+:+[0-9a-fA-F]+$", line):
                    ipv6s.add(line)
                elif re.match(r"^AS\d+", line):
                    asns.add(line)
                elif "." in line and not any(x in line for x in [" ", ":", "AS"]):
                    subdomains.add(line)
    except FileNotFoundError:
        logger.error(f"[ReconUtils] File not found: {abs_output_file}")
        return set(), set(), set(), set()
    except Exception as e:
        logger.error(f"[ReconUtils] Error parsing output: {e}")
        return set(), set(), set(), set()

    return subdomains, asns, ipv4s, ipv6s

def prompt_user_on_interrupt():
    print("\n[!] Recon paused. Options:")
    print("[C]ontinue")
    print("[S]kip current tool")
    print("[E]nd recon process")
    while True:
        choice = input("Enter choice (C/S/E): ").strip().upper()
        if choice in ("C", "S", "E"):
            return choice
        print("Invalid choice.")

def save_list(items, output_dir, filename, logger=None):
    path = os.path.join(output_dir, f"{filename}.txt")
    with open(path, "w") as f:
        for item in sorted(items):
            f.write(item + "\n")
    if logger:
        logger.info(f"[ReconUtils] Saved {filename} to {path}")
