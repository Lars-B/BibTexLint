"""
Module that checks all preprints and updates them if required.
"""
from bibtexlint._preprint_strategies import preprint_strategies


def check_preprint(entry):
    """Check if the entry is a preprint and use the correct strategy."""
    # the following will likely need to be extended in the future...
    journal = "None"
    if "journal" in entry["fields"]:
        # This is for biorxiv
        journal = entry["fields"]["journal"]
    elif "archivePrefix" in entry["fields"]:
        # This is for arxiv
        journal = entry["fields"]["archivePrefix"]

    if journal.lower() in preprint_strategies:
        # Get the appropriate strategy based on the journal
        strategy = preprint_strategies[journal.lower()]
        entry = strategy.update_preprint(entry)

    # No matter what happens above, we return the entrys
    return entry
