import os
import sys
import shutil
import builtins
import pytest
from BB_auto_framework.plugins.recon.recon_utils import ensure_dirs, parse_output, save_list


@pytest.fixture
def tmp_output_dir():
    dir_path = "test_outputs"
    tools = ["amass", "subfinder"]
    ensure_dirs(dir_path, tools)  # This will create the directory structure
    yield dir_path
    shutil.rmtree(dir_path)

def test_ensure_dirs(tmp_output_dir):
    for tool in ["amass", "subfinder"]:
        assert os.path.isdir(os.path.join(tmp_output_dir, tool))

def test_save_and_parse(tmp_output_dir):
    data = ["test.example.com", "AS123", "192.168.1.1", "fe80::1"]
    # Create the file directly in the amass directory
    out_file = os.path.join(tmp_output_dir, "amass", "amass_output.txt")
    with open(out_file, "w") as f:
        for line in data:
            f.write(line + "\n")

    # Parse using just the file path since we're already in the correct directory
    subs, asns, ipv4s, ipv6s = parse_output(tmp_output_dir, out_file)
    assert "test.example.com" in subs
    assert "AS123" in asns
    assert "192.168.1.1" in ipv4s
    assert "fe80::1" in ipv6s
