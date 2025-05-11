"""
A BibTeX parser module that reads .bib files and extracts bibliographic entries.

This module provides the ability to parse BibTeX files and
convert their contents into a structured format.
It supports parsing various entry types (like articles, books, etc.) and
their attached fields (author, title, year, etc.).
"""
import os.path
import re
from pathlib import Path

FIELD_PATTERN = re.compile(r'''
    (\w+)\s*=\s*              # Field name and equal sign
    (                        # Start of value capture
      \{                     #   If value starts with {
        (                    #     Capture group for inside-braces
          (?:[^{}]           #       Any char except braces
            | \{[^{}]*}      #       OR nested one level
          )*
        )
      }                      #   Closing }
      |                      # OR
      "([^"]*)"              #   Value in double quotes
    )
    \s*,?                    # Optional trailing comma
''', re.VERBOSE | re.DOTALL)

ENTRY_START_PATTERN = re.compile(r'@(\w+)\s*\{\s*([^,]+),', re.DOTALL)


def parse_bibtex_file(file_name: str) -> list[dict[str, str]]:
    assert os.path.exists(file_name), f"File {file_name} does not exist"
    bib_file_text = Path(file_name).read_text(encoding="utf-8")
    return parse_bibtex_text(bib_file_text)


def parse_bibtex_text(bib_text: str) -> list:
    entries = []
    pos = 0
    while pos < len(bib_text):
        match = ENTRY_START_PATTERN.search(bib_text, pos)
        if not match:
            break
        entry_type, citation_key = match.groups()
        start = match.end()
        # Now parse the balanced braces starting from `start`
        # todo this only supports the {} style bib
        #  need to add support for "" and ()
        #  write a minimal example bib and test that compiles it.
        brace_level = 1
        i = start
        while i < len(bib_text):
            if bib_text[i] == '{':
                brace_level += 1
            elif bib_text[i] == '}':
                brace_level -= 1
                if brace_level == 0:
                    break
            elif bib_text[i] == '@':
                # early exit: invalid nested entry start
                # found @ while brace_level > 0
                raise ValueError("Unexpected '@' inside BibTeX entry")
            i += 1
        if brace_level != 0:
            raise ValueError("Unbalanced braces in BibTeX entry")
        raw_field_block = bib_text[start:i].strip()
        fields = parse_field_block(raw_field_block)
        entries.append({
            "type": entry_type.lower(),
            "key": citation_key.strip(),
            "fields": fields
        })
        pos = i + 1  # Move to next entry
    return entries


def parse_field_block(raw_field_block):
    fields = {}
    for match in FIELD_PATTERN.finditer(raw_field_block):
        key = match.group(1).strip()
        value = match.group(2) if match.group(2) else match.group(3)
        if ((value.startswith('{') and value.endswith('}'))
                or (value.startswith('"') and value.endswith('"'))):
            # Removing outer {} or ""
            value = value[1:-1].strip()
        fields[key] = value
    return fields
