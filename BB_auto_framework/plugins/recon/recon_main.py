import os
import signal
import subprocess
import argparse
from core.logger import setup_logger, setup_error_logger
import plugins.recon.recon_utils as recon_utils
from plugins.recon import amass_enum

logger = setup_logger()

def run_tool_process(cmd, tool_name, logger, error_logger):
    try:
        logger.info(f"[Recon] Starting tool: {tool_name}")
        process = subprocess.Popen(cmd)

        while True:
            try:
                process.wait()
                logger.info(f"[Recon] {tool_name} completed successfully.")
                break
            except KeyboardInterrupt:
                os.kill(process.pid, signal.SIGSTOP)
                logger.warning(f"[Recon] {tool_name} paused by user.")
                choice = recon_utils.prompt_user_on_interrupt()
                if choice == "S":
                    logger.info(f"[Recon] Skipping {tool_name}")
                    process.terminate()
                    break
                elif choice == "E":
                    logger.warning("[Recon] Aborting recon stage.")
                    process.terminate()
                    exit(0)
                elif choice == "C":
                    logger.info(f"[Recon] Resuming {tool_name}")
                    os.kill(process.pid, signal.SIGCONT)
                    continue
    except Exception as e:
        logger.exception(f"[Recon] {tool_name} failed with error: {e}")
        error_logger.error(f"[{tool_name}] {e}")

def main(target, output_dir=None):
    logger.info(f"[Recon] Starting recon for {target}")
    error_logger = setup_error_logger(target)

    tools = ["amass", "subfinder", "assetfinder", "crtsh", "shodan", "bgp"]
    
    if output_dir is None:
        output_dir = os.path.join("outputs", target)
    
    recon_utils.ensure_dirs(output_dir, tools)

    recon_steps = [
        ("amass", amass_enum.get_amass_command(target, output_dir)),
        # Add more tools as you implement them
        # ("subfinder", subfinder_enum.get_subfinder_command(target, output_dir)),
    ]

    for name, cmd in recon_steps:
        try:
            run_tool_process(cmd, name, logger, error_logger)
            if name == "amass":
                output_file = os.path.join(output_dir, "amass", "amass_output.txt")
                subdomains, asns, ipv4s, ipv6s = recon_utils.parse_output(output_dir, output_file)
                recon_utils.save_list(subdomains, output_dir, "subdomains", logger)
                recon_utils.save_list(asns, output_dir, "asns", logger)
                recon_utils.save_list(ipv4s, output_dir, "ipv4s", logger)
                recon_utils.save_list(ipv6s, output_dir, "ipv6s", logger)
        except Exception as e:
            logger.exception(f"[Recon] {name} failed with error: {e}")
            error_logger.error(f"[{name}] {e}")
            continue

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Recon Stage Runner")
    parser.add_argument("--target", required=True, help="Target domain (e.g., example.com)")
    parser.add_argument("--output-dir", default=None, help="Output directory")
    args = parser.parse_args()
    main(args.target, args.output_dir)