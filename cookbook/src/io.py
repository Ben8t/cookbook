import os

def write_file(filename:str, content:str, path: str="docs"):
    with open(f"{path}/{filename}.md", "w+") as fopen:
        fopen.write(content)

def write_folder(name, path: str="docs"):
    try:
        os.mkdir(f"{path}/{name}")
    except FileExistsError as exeception:
        print(f"Folder {path}/{name} already exists")
        return exeception