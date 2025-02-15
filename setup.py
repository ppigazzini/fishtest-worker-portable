import os
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path

# URLs and user values
fishtest_url = (
    "https://github.com/official-stockfish/fishtest/archive/refs/heads/master.zip"
)
uv_url = "https://astral.sh/uv/install.sh"
usr_name = "user00"
usr_pwd = "user00"
fish_host = "dfts-0.pigazzini.it"


# Helper function to download files using curl or wget
def download_file(url, dest):
    if shutil.which("curl"):
        cmd = f"curl -L -o {dest} {url}"
    elif shutil.which("wget"):
        cmd = f"wget -O {dest} {url}"
    else:
        raise RuntimeError("Neither curl nor wget is available; please install one.")
    subprocess.run(cmd, shell=True, check=True)


# Download and extract fishtest
with tempfile.TemporaryDirectory() as temp_dir:
    temp_path = Path(temp_dir)
    fishtest_zip_path = temp_path / "fishtest.zip"
    download_file(fishtest_url, fishtest_zip_path)
    with zipfile.ZipFile(fishtest_zip_path, "r") as zip_ref:
        zip_ref.extractall(temp_path)
    fishtest_worker_path = temp_path / "fishtest-master" / "worker"
    fishtest_worker_path.rename(Path.cwd() / "worker")

    # Delete the worker/packages subfolder if it exists using shutil
    worker_packages = Path.cwd() / "worker" / "packages"
    if worker_packages.exists():
        shutil.rmtree(worker_packages)

# Install uv if missing
if shutil.which("uv"):
    print("UV is already installed, skipping installation.")
elif os.environ.get("MSYSTEM"):
    msystem = os.environ.get("MSYSTEM").lower()
    msystem_packages = {
        "ucrt64": "mingw-w64-ucrt-x86_64-python-uv",
        "clang64": "mingw-w64-clang-x86_64-python-uv",
        "clangarm64": "mingw-w64-clang-aarch64-python-uv",
        "mingw64": "mingw-w64-x86_64-python-uv",
    }
    pkg_str = msystem_packages.get(msystem)
    if pkg_str:
        print(f"Installing UV via pacman for {msystem}...")
        cmd = "pacman -S --noconfirm --needed " + pkg_str
        subprocess.run(cmd, shell=True, check=True)
    else:
        raise RuntimeError(f"MSYSTEM '{msystem}' is not supported for UV installation")
else:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file_path = Path(tmp_file.name)
    download_file(uv_url, tmp_file_path)
    try:
        subprocess.run(f"bash '{tmp_file_path}'", shell=True, check=True)
    finally:
        tmp_file_path.unlink()
