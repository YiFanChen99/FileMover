# FileMover

Small scripts for moving files out of many subfolders into one folder, for example to read a comic's chapters as one folder of pages.

## flatten_folders.py

Moves every file in each subfolder of the **current folder** up one level, prefixing it with its subfolder's name, then deletes the subfolders.

```
Chapter/
  24.0/01.jpg        ->   Chapter/24.0_01.jpg
  24.0/02.png        ->   Chapter/24.0_02.png
  24.5/01.jpg        ->   Chapter/24.5_01.jpg
```

### Usage

Copy the script into the folder to flatten and double-click it, or run it from inside that folder:

```
python flatten_folders.py
```

It takes no arguments. It prints every planned move and the folder it works on, and moves nothing until you type `y`. Requires Python 3.9 or later.

### Safety

- Before moving anything, it stops with nothing moved when a subfolder contains a folder, when a new name already exists, or when two files would get the same name (`a_b/c.jpg` and `a/b_c.jpg` both become `a_b_c.jpg`).
- After moving, it deletes the subfolders only if every one of them is empty, already-empty subfolders included. If any still holds a file, it deletes none and lists what is left.
- A move that fails halfway, for example on a locked file, is not rolled back. Fix the cause and run it again: files already moved do not block the rest.

### Limits

- **One level of subfolders only.** Nested folders stop the run.
- **It works on the current folder, not the script's folder.** `python some/path/flatten_folders.py` run from `Downloads` flattens every subfolder of `Downloads`. Check the `Folder:` line before typing `y`. Double-clicking runs it in the script's own folder.
- **Order comes from your names.** The script adds the folder name as is and does not renumber. For the result to sort right as plain text (comic readers, archives), pad folder and page numbers to the same width: `24.0` sorts before `100.0` only if written `024.0`, and page `9.jpg` sorts after `10.jpg` unless written `09.jpg`. Writing the main chapter as `24.0` also keeps it ahead of the side chapter `24.5`.
- **Hidden and system files move too**, so a `Thumbs.db` becomes `24.0_Thumbs.db`.

## main.ps1

Moves (or copies) the files of every folder under `$source` whose name matches `$dir_rex` into `$dest`, keeping file names unchanged. Edit the configuration block at the top before running. Files with the same name in different folders collide, so it suits folders whose file names are already unique.
