from bibtexlint.check_preprint import check_preprint
from bibtexlint.linter import lint_entry
from bibtexlint.parser import parse_bibtex


def process_bib_file(input_file):
    entries = parse_bibtex(input_file)

    for entry in entries:
        checked_entry = check_preprint(entry)
        linted_entry = lint_entry(entry)
    return 0


if __name__ == '__main__':
    process_bib_file("../../data/sources.bib")
