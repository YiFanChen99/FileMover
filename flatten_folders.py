"""Move every file in each subfolder of the current folder up one level, then delete the emptied subfolders.

Each moved file gets its folder name as a prefix: `24.0/01.jpg` -> `24.0_01.jpg`.
File names that are only digits are zero-padded to the longest such name across all subfolders,
so with a `100.jpg` somewhere, `24.0/1.jpg` -> `24.0_001.jpg`.

Run it in the folder to flatten, then answer y to confirm:
    python flatten_folders.py
"""

import re
import sys
from pathlib import Path

SEPARATOR = "_"
DIGITS_ONLY = re.compile(r"[0-9]+")

# Without this, printing a CJK path the console code page lacks (for example Simplified Chinese under cp950) crashes
sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def finish(message: str, exit_code: int = 0) -> None:
    print(message)
    input("\nPress Enter to close.")
    sys.exit(exit_code)


def is_number_name(file: Path) -> bool:
    return DIGITS_ONLY.fullmatch(file.stem) is not None


def build_plan(root: Path, folders: list[Path]) -> list[tuple[Path, Path]]:
    files = []
    for folder in folders:
        nested_folders = [path for path in folder.iterdir() if path.is_dir()]
        if nested_folders:
            finish(f"Stopped, nothing moved: {folder.name} has nested folders {[path.name for path in nested_folders]}", 1)
        files.extend(sorted(folder.iterdir()))

    width = max((len(file.stem) for file in files if is_number_name(file)), default=0)
    plan = []
    for file in files:
        name = file.stem.zfill(width) + file.suffix if is_number_name(file) else file.name
        plan.append((file, root / f"{file.parent.name}{SEPARATOR}{name}"))
    return plan


def find_conflicts(plan: list[tuple[Path, Path]]) -> list[str]:
    conflicts = []
    seen_targets = set()
    for source, target in plan:
        key = target.name.lower()  # Windows file names are case-insensitive
        if key in seen_targets:
            conflicts.append(f"two files map to {target.name}")
        if target.exists():
            conflicts.append(f"{target.name} already exists (from {source})")
        seen_targets.add(key)
    return conflicts


def main() -> None:
    root = Path.cwd()
    folders = sorted(path for path in root.iterdir() if path.is_dir())
    if not folders:
        finish(f"No subfolders in {root}")

    plan = build_plan(root, folders)
    conflicts = find_conflicts(plan)
    if conflicts:
        finish("Stopped, nothing moved. Conflicts:\n" + "\n".join(f"  {conflict}" for conflict in conflicts), 1)

    for source, target in sorted(plan, key=lambda move: move[1].name):
        print(f"{source.relative_to(root)}  ->  {target.name}")
    print(f"\nFolder: {root}")
    print(f"{len(plan)} files from {len(folders)} subfolders; all {len(folders)} subfolders are deleted afterwards.")
    if input("Type y to go ahead: ").strip().lower() != "y":
        finish("Cancelled, nothing moved.")

    for source, target in plan:
        source.rename(target)

    not_empty = [folder for folder in folders if any(folder.iterdir())]
    if not_empty:
        finish(
            "Moved, but these folders are not empty, so none were deleted:\n"
            + "\n".join(f"  {folder.name}: {[path.name for path in folder.iterdir()]}" for folder in not_empty),
            1,
        )

    for folder in folders:
        folder.rmdir()  # rmdir refuses non-empty folders, a second safety net
    finish(f"Moved {len(plan)} files and deleted {len(folders)} empty folders.")


if __name__ == "__main__":
    main()
