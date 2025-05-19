from bibtexlint.check_preprint import check_preprint
from bibtexlint.linter import lint_entry
from bibtexlint.parser import parse_bibtex_file


def process_bib_file(input_file, author_format='last_first'):
    entries = parse_bibtex_file(input_file)
    updated_entries = []

    for entry in entries:
        checked_entry = check_preprint(entry)
        linted_entry = lint_entry(checked_entry, author_format)
        updated_entries.append(linted_entry)

    # todo cleanup and combine these two...
    type_priority = {
        'article': 1,
        'book': 2,
        'inbook': 3,
        'incollection': 4,
        'inproceedings': 5,
        'proceedings': 6,
        'phdthesis': 7,
        'mastersthesis': 8,
        'techreport': 9,
        'manual': 10,
        'misc': 11,
        'booklet': 12,
        'unpublished': 13
    }

    type_labels = {
        'article': 'Journal Articles',
        'book': 'Books',
        'inbook': 'Chapters in Books',
        'incollection': 'Contributions to Collections',
        'inproceedings': 'Conference Papers',
        'proceedings': 'Conference Proceedings',
        'phdthesis': 'PhD Theses',
        'mastersthesis': 'Master’s Theses',
        'techreport': 'Technical Reports',
        'manual': 'Manuals',
        'misc': 'Miscellaneous',
        'booklet': 'Booklets',
        'unpublished': 'Unpublished Works'
    }

    sorted_entries = sorted(
        updated_entries,
        key=lambda entry: (
            not entry.get('incomplete_entry', False),
            type_priority.get(entry['type'].lower(), 99),
            entry['fields'].get('author').lower()
        )
    )

    current_type = None
    printed_lookup_failed_header = False

    for cur_entry in sorted_entries:
        entry_type = cur_entry["type"].lower()

        # Print a special section for entries that failed lookup
        if cur_entry.get("incomplete_entry", False):
            if not printed_lookup_failed_header:
                print(
                    "% --------------------------------\n"
                    "% Incomplete/Unpublished Entries\n"
                    "% Manual cleanup might be required"
                    "% --------------------------------\n"
                )
                printed_lookup_failed_header = True
            # No type-based heading for these
        else:
            # Print type-based header if this is a new type group
            if entry_type != current_type:
                label = type_labels.get(entry_type, entry_type.capitalize())
                print(
                    f"\n"
                    f"% {'-' * len(label)}\n"
                    f"% {label}\n"
                    f"% {'-' * len(label)}\n"
                )
                current_type = entry_type

        # Format fields
        fields = cur_entry["fields"]
        formatted_fields = "\n  ".join(
            f"{k} = {{{v}}}," for k, v in fields.items())
        cit = f"@{cur_entry['type']}{{{cur_entry['key']},\n  {formatted_fields}\n}}"

        print(cit)
    return 0


if __name__ == '__main__':
    # todo set email for the cross ref api stuff should be possible to be nice
    # todo finishe output to file in appropriate format with some rules
    # todo if above update README and publish first release...
    # todo write and upload documentation too...
    process_bib_file("../../data/small_test.bib")
