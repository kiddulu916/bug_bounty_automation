
import os

def get_amass_command(target, output_dir):
    """
    Returns the amass command as a list for subprocess execution.
    """
    output_file = os.path.join(output_dir, "amass", "amass_output.txt")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    cmd = ["amass", "enum", "-d", target, "-o", output_file]
    return cmd