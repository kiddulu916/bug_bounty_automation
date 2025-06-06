# bughunt_framework/main.py

import argparse
from core.logger import setup_logger
from core.plugin_loader import load_plugins

def run_stage(stage, target):
    logger = setup_logger()
    logger.info(f"Starting stage: {stage} for {target}")

    plugins = load_plugins(stage)
    for plugin in plugins:
        logger.info(f"Running plugin: {plugin.__name__}")
        plugin.run(target)

def main():
    parser = argparse.ArgumentParser(description="Bug Hunting Automation Framework")
    parser.add_argument("stage", choices=["recon", "scan", "test", "report"], help="Which stage to run")
    parser.add_argument("--target", required=True, help="Target domain or IP")
    args = parser.parse_args()

    run_stage(args.stage, args.target)

if __name__ == "__main__":
    main()
