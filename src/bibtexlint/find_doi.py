import warnings

from habanero import Crossref
from rapidfuzz import fuzz


def find_doi(entry):
    """
    This function will try to find the DOI, using crossref first result.
    """
    title = entry['fields']['title']
    cr = Crossref()
    results = cr.works(query=title)
    if not results["status"] == "ok":
        warnings.warn("Crossref search was not ok...")
        return None
    first_result = results["message"]["items"][0]
    # checking similarity of titles:
    t1 = title.strip().lower()
    t2 = first_result["title"][0].strip().lower()
    if not t1 == t2:
        if not is_similar(t1, t2):
            warnings.warn(f"Found new publication on crossref but titles "
                          f"don't match OLD:{t1} -- NEW:{t2}")
            return None
    author_string = entry['fields']['author']
    for a in first_result['author']:
        family_name = a.get("family", "")
        if family_name not in author_string:
            warnings.warn(
                f"Author family name '{family_name}' not found in "
                f"previous author list!. Because titles are similar "
                f"enough, this will be ignored...")
    return first_result["DOI"]


def is_similar(title1, title2, threshold=85):
    score = fuzz.ratio(title1.lower(), title2.lower())
    return score >= threshold
