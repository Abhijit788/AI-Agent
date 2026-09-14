#!/usr/bin/env python3
"""
Example script demonstrating how to import the built‑in json module,
read a JSON file, and write JSON data back to disk.

This file contains:
  * import json
  * read_json(path) – read a JSON file and return the Python object
  * write_json(path, data) – write a Python object to a JSON file
  * a small demo that reads `sample.json` (if it exists) and prints
    its content, then writes a copy back to `sample_copy.json`.
"""

import json
import os
from pathlib import Path


def read_json(path: str | Path):
    """Read a JSON file and return its content.

    Parameters
    ----------
    path: str | Path
        Path to the JSON file.

    Returns
    -------
    Any
        The Python object decoded from the JSON file.
    """
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"JSON file '{p}' not found")
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: str | Path, data):
    """Write a Python object to a JSON file.

    Parameters
    ----------
    path: str | Path
        Destination file path.
    data: Any
        Python object to encode as JSON.
    """
    p = Path(path)
    with p.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    # Demo usage
    sample = Path("sample.json")
    if sample.is_file():
        try:
            content = read_json(sample)
            print("Read JSON from sample.json:\n", content)
        except Exception as e:
            print("Failed to read sample.json:", e)

        # Write a copy
        copy_path = Path("sample_copy.json")
        try:
            write_json(copy_path, content)
            print(f"Copied JSON to {copy_path}")
        except Exception as e:
            print("Failed to write copy:", e)
    else:
        print("No sample.json found – create one to test the script.")
