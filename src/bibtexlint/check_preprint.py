"""
Module that checks all preprints and updates them if required.
"""
import re

from bibtexlint._preprint_strategies import preprint_strategies
from bibtexlint.parser import parse_field_block


def check_preprint(entry):
    """
    Check if the entry is a preprint and use the correct strategy.
    """
    # the following will likely need to be extended in the future...
    journal = "None"
    if "journal" in entry["fields"]:
        # This is for bioRxiv/medRxiv
        journal = entry["fields"]["journal"]
    elif "archivePrefix" in entry["fields"]:
        # This is for arxiv
        journal = entry["fields"]["archivePrefix"]
        if ("eprint" in entry["fields"] and
                "doi" not in entry["fields"]):
            # arxiv doi: 10.48550/arXiv.[arXiv-id]
            entry["fields"]["doi"] = (f"10.48550/arXiv."
                                      f"{entry["fields"]["eprint"]}")

    if journal.lower() in preprint_strategies:
        # Get the appropriate strategy based on the journal
        strategy = preprint_strategies[journal.lower()]
        entry = strategy.update_preprint(entry)
        if not isinstance(entry, dict):
            doi_bib_entry_pattern = r'@(\w+)\{\s*([^,]+)\s*,(.*)}'
            entry_type, citation_key, raw_fields = re.findall(
                doi_bib_entry_pattern, entry)[0]
            fields = parse_field_block(raw_fields)
            return {
                "type": entry_type.lower(),
                "key": citation_key.strip(),
                "fields": fields
            }

    # return an updated or unchanged entry.
    return entry
