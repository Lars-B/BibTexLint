"""
Command line interface for bibtool.
"""
import sys
from .process import process_bib_file


def main():
    # todo this is the CLI entry point.... Needs to be properly adapted
    if len(sys.argv) != 2:
        print("Usage: bibtool path/to/file.bib")
        sys.exit(1)
    process_bib_file(sys.argv[1])
