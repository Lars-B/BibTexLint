"""
A BibTeX parser module that reads .bib files and extracts bibliographic entries.

This module provides functionality to parse BibTeX files and convert their contents
into a structured format. It supports parsing various entry types (like articles,
books, etc.) and their associated fields (author, title, year, etc.).
"""
import os.path
import re
from pathlib import Path


def parse_bibtex(file_name: str) -> list[dict[str, str]]:
    """
    Parse a bibtex file and return a list of entries.

    :param file_name: Input file name.
    :type file_name: str
    :return: list of entries in the bibtex file.
    :rtype: list[dict[str, str]]
    """
    assert os.path.exists(file_name), f"File {file_name} does not exist"
    entries = []
    bib_file_text = Path(file_name).read_text(encoding="utf-8")

    raw_entries = re.findall(r'@(\w+)\s*\{\s*([^,]+),(.*?)\n}',
                             bib_file_text,
                             re.DOTALL)
    for entry_type, entry_key, fields_block in raw_entries:
        # Match each key = {value} or key = "value", with nested {} and ,
        field_pattern = re.compile(r'''
                (\w+)\s*=\s*        # Field name and equal sign
                (                   # Start of value capture
                  \{                # If value starts with {
                    (               # Capture group for inside-braces
                      (?:           # Non-capturing group
                        [^{}]       # Any char except braces
                        |           # OR
                        \{[^{}]*}   # Nested one level
                      )*
                    )
                  }                 # Closing }
                  |                 # OR
                  "([^"]*)"         #   Value in double quotes
                )
                \s*,?               # Optional trailing comma
            ''', re.VERBOSE | re.DOTALL)

        fields = {}
        for match in field_pattern.finditer(fields_block):
            key = match.group(1)
            value = match.group(2) if match.group(2) else match.group(3)
            fields[key.strip()] = value.strip()[1:-1]

        entries.append({
            "type": entry_type.lower(),
            "key": entry_key.strip(),
            "fields": fields
        })
    return entries
