from bibtexlint.check_preprint import check_preprint
from bibtexlint.linter import lint_entry
from bibtexlint.parser import parse_bibtex_file


def process_bib_file(input_file):
    entries = parse_bibtex_file(input_file)
    updated_entries = []

    for entry in entries:
        checked_entry = check_preprint(entry)
        # todo how do we want to handle all the entries?
        #  the updated prerpints are just bib citaitons that need to be
        # linted_entry = lint_entry(entry)
        updated_entries.append(checked_entry)

    print("----")
    for ent in updated_entries:
        print(ent)
        print("----")
    # todo write new bib file, sorted accordingly
    #  parsed... we want to sort the bib file alphabetically
    #  but also with preprints, then artciles, then other stuff?

    return 0


if __name__ == '__main__':
    # todo find test case where arxiv has the updated publication, should
    #  easier?
    process_bib_file("../../data/small_test.bib")
