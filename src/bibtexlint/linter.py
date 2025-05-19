"""
Module that handles linting of a given bib entry.
"""
import warnings

REQUIRED_FIELDS = {
    'article': {'author', 'title', 'journal', 'year'},
    'book': {'author', 'title', 'publisher', 'year'},
    'inbook': {'author', 'title', 'chapter', 'publisher', 'year'},
    'incollection': {'author', 'title', 'booktitle', 'publisher', 'year'},
    'inproceedings': {'author', 'title', 'booktitle', 'year'},
    'proceedings': {'title', 'year'},
    'phdthesis': {'author', 'title', 'school', 'year'},
    'mastersthesis': {'author', 'title', 'school', 'year'},
    'techreport': {'author', 'title', 'institution', 'year'},
    'manual': {'title'},
    'misc': set(),  # very flexible
    'booklet': {'title'},
    'unpublished': {'author', 'title', 'note'},
}


def lint_entry(entry: dict, author_format='last_first') -> dict:
    entry_type = entry.get('type', '').lower()
    required = REQUIRED_FIELDS.get(entry_type, set())
    missing = [field for field in required if field not in entry['fields']]
    if missing:
        warnings.warn(f'Incomplete entry found: {entry['fields']['title']} '
                      f'is missing the following required entries: {missing}')
        # Tag for later sorting to top
        entry['incomplete_entry'] = True
    entry['fields']['author'] = normalize_author_names(
        entry['fields']['author'],
        to_format=author_format
    )
    return entry  # returns empty list if all required fields are present


def normalize_author_names(author_field, to_format='last_first'):
    """
    Normalize a BibTeX author string.
    - `author_field`: the raw author string
    - `to_format`: either 'last_first' ("Doe, John") or 'first_last' ("John Doe")
    """
    authors = [a.strip() for a in author_field.split(' and ')]

    def normalize(name):
        # Detect if already in "Last, First"
        if ',' in name:
            last, first = map(str.strip, name.split(',', 1))
        else:
            parts = name.split()
            first, last = ' '.join(parts[:-1]), parts[-1]
        return f"{last}, {first}" if to_format == 'last_first' else f"{first} {last}"

    normalized = [normalize(a) for a in authors]
    return ' and '.join(normalized)
