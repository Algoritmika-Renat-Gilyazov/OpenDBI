import json
import pathlib as pl
import platform
from sys import argv, executable
from subprocess import run

ESC="\033["
RED=f"{ESC}31m"
GREEN=f"{ESC}32m"
YELLOW=f"{ESC}33m"
RESET=f"{ESC}0m"

def inp(msg: str, title: str, default=None, path=False):
    """Extended input.<br><b>Args</b>:<br> msg: str - input message.<br>title: str - name in code.<br> default: Any - default value(<b>default</b>: None).<br>path: bool - Is path?(<b>default</b>: None)
    """
    name = input(msg)
    if path:
        while '/' in name or '\\' in name:
            print(f"{title} cannot contain '/'or '\\'")
            name = input(msg)
    if name == "" or name.isspace():
        name = default
    return name
def sw(msg: str, title: str):
    """Boolean input.<br><b>Args</b>:<br> msg: str - input message.<br>title: str - name in code.
    """
    data = inp(msg, title)
    if data.upper() != "Y":
        return False
    return True
def CreateProject() -> int:
    """Create Project. Returns int
    """
    name = inp("Enter name of project(Default \"Example Project\"): ", "Name", "Example Project", True)
    id = name.lower().replace(" ", "_")
    root = pl.Path(pl.Path.joinpath(pl.Path.cwd(), id))
    try:
        root.mkdir(exist_ok=True)
    except PermissionError as e:
        print(f"{RED}Cannot access path: '{str(root)}'!{RESET}")
        return 1
    cont = True
    if pl.Path(root / "dbi.json").exists():
        cont = sw("Are you sure to replace existing files?(Y/<any>, default: n): ", "Permission")
    if not cont:
        return 2
    with open(root / "dbi.json", "w") as f:
        json.dump(
            {
                "project": {
                    "name": name,
                    "id": id,
                    "version": "1.0.0"
                }
            },
            f
        )
    root.joinpath("src").mkdir(exist_ok=True)
    if pl.Path(root / "src" / "main.py").exists():
        cont = sw("Are you sure to replace existing files?(Y/<any>, default: n): ", "Permission")
    if not cont:
        return 2
    with open(root / "src" / "main.py", 'w') as f:
        f.write("print('Hi!')")
    print(f"{GREEN}The project '{id}'('{name}') was created successfully!{RESET}")
    return 0

version = "1.0"

def RunProject():
    """Runs the project.
    """
    import shutil
    python_path = shutil.which("python") or shutil.which("python3")
    
    if not python_path:
        print(f"{YELLOW}Python not found in PATH! Please install Python.{RESET}")
        return 1
        
    try:
        run(
            [python_path, "src/main.py"],
            shell=(platform.system() == "Windows")
        )
    except FileNotFoundError:
        print(f"{RED}Python environment at PYTHON_HOME({python_path}) is incorrect!{RESET}")
        return 1
def BuildProject(args: list):
    """Builds the project with PyInstaller.<br><b>Args</b>:<br> args: list - PyInstaller args(<b>default</b>: [])
    """
    from PyInstaller.__main__ import run as build
    
    work_dir = pl.Path.cwd()
    script_path = pl.Path("src").joinpath("main.py")
    data: dict = {}
    with open(work_dir / "dbi.json") as f:
        data = json.load(f)
    args = [
        str(script_path),
        "--onefile",
        f"--name={data.get("project").get("name")}",
        "--clean"
    ] + args
    build(args)
def AddRuntime():
    """Builds the project with adding portative Python.
    """
    import venv

    import os
    
    venv_dir = pl.Path(pl.Path.cwd()).joinpath(".runtime")
    builder = venv.EnvBuilder(with_pip=True)
    builder.create(venv_dir)
    executable = pl.Path(venv_dir).joinpath("Scripts", "python.exe") if os.name == "nt" \
        else pl.Path(venv_dir).joinpath("bin", "python")
    with open("launch.bat", "w") as f:
        f.write("@echo off\n")
        f.write(f"{executable} src\\main.py")
    with open("launch.sh", "w") as f:
            f.write(f"{executable} src/main.py")
    return executable