import json
import pathlib as pl
from sys import argv

ESC="\033["
RED=f"{ESC}31m"
GREEN=f"{ESC}32m"
YELLOW=f"{ESC}33m"
RESET=f"{ESC}0m"

def inp(msg: str, title: str, default, path=False):
    name = input(msg)
    if path:
        while '/' in name or '\\' in name:
            print(f"{title} cannot contain '/'or '\\'")
            name = input(msg)
    if name == "" or name.isspace():
        name = default
    return name
def sw(msg: str, title: str, default="n"):
    data = inp(msg, title, default)
    if data.upper() != "Y":
        return False
    return True
def CreateProject() -> int:
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

version = "1.0b1"

def GetHelp():
    print("""
                init - Create Project.
                info - Get information about OpenDBI.
                help - Get help.
            """)

if __name__ == "__main__":
    try:
        if argv[1] == "init":
            CreateProject()
        elif argv[1] == "info":
            print("OpenDBI")
            print(version)
        elif argv[1] == "help":
            GetHelp()
        else:
            GetHelp()
    except IndexError:
        GetHelp()