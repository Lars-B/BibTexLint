from bibtexlint.parser import parse_bibtex


def process_bib_file(input_file):
    entries = parse_bibtex(input_file)
    for key in entries[4]:
        print(key, " -- ", entries[4][key])
    return 0


if __name__ == '__main__':
    process_bib_file("../../data/sources.bib")
