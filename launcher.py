import os
import subprocess
from pathlib import Path

# User values
usr_name = "user00"
usr_pwd = "user00"
fish_host = "dfts-0.pigazzini.it"
install_cwd = Path.cwd()
worker_dir = install_cwd / "worker"

env = os.environ.copy()
local_bin = Path.home() / ".local" / "bin"
env["PATH"] = f"{local_bin}{os.pathsep}" + env.get("PATH", "")

try:
    os.chdir(worker_dir)
    # Quote the path to uv.exe/uv to handle spaces in the directory path.
    uv_command = f"uv run worker.py {usr_name} {usr_pwd} --host {fish_host} --compiler g++ --concurrency MAX"
    subprocess.run(uv_command, shell=True, check=True, env=env)
except KeyboardInterrupt:
    print("Operation cancelled by user.")
finally:
    os.chdir(install_cwd)
