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
    bib_file_text = Path(file_name).read_text()

    raw_entries = re.findall(r'@(\w+)\s*\{\s*([^,]+),(.*?)\n}',
                             bib_file_text,
                             re.DOTALL)
    for entry_type, entry_key, fields_block in raw_entries:
        fields = {}
        # Match each key = {value} or key = "value"
        field_matches = re.findall(r'(\w+)\s*=\s*[{"]([^"}]+)[}"]', fields_block)
        for field_name, value in field_matches:
            fields[field_name.strip()] = value.strip()

        entries.append({
            "type": entry_type.lower(),
            "key": entry_key.strip(),
            "fields": fields
        })
    return entries
