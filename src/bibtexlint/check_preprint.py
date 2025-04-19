"""
Module that checks all preprints and updates them if required.
"""
from bibtexlint._preprint_strategies import preprint_strategies


def check_preprint(entry):
    """Check if the entry is a preprint and use the correct strategy."""
    if "journal" in entry["fields"]:
        journal = entry["fields"]["journal"]
        if journal in preprint_strategies:
            # Get the appropriate strategy based on the journal
            strategy = preprint_strategies[journal]
            entry = strategy.update_preprint(entry)  # Call the check_preprint method
    # No matter what happens above, we return entry
    return entry
