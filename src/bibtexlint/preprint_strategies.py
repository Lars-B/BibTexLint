import warnings

import requests

from bibtexlint.find_doi import find_doi


def handle_published(published_doi):
    doi_request = {
        "url": f"https://doi.org/{published_doi}",
        "headers": {
            "Accept": "application/x-bibtex; charset=utf-8"
        }
    }
    response = requests.get(doi_request["url"],
                            headers=doi_request["headers"])
    if response.status_code != 200:
        warnings.warn(f"Something went wrong with the doi-API-request of:"
                      f"{published_doi}")
        raise ValueError(f"API request failed with status code "
                         f"{response.status_code}...")
    return response.text


class PreprintHandler:

    def __init__(self, name: str, config: dict):
        self.name = name
        self.api_url = config.get("api_url")
        self.published_key = config.get("published_key")

    def make_api_request(self, doi):
        """Common logic to make an API request."""
        # Perform the API call
        if self.name == "arXiv":
            # Should not be called...
            return None
        try:
            response = requests.get(f"{self.api_url}/{doi}")
        except requests.exceptions.MissingSchema:
            warnings.warn(f"API request failed ({doi}), will be ignored.")
            return None
        if response.status_code != 200:
            warnings.warn(f"API request for doi:{doi} failed with status code "
                          f"{response.status_code}...")
            return None
        return response.json()

    def update_preprint(self, entry):
        print(f"Checking a preprint: {entry['fields']['title']}")
        if "doi" not in entry["fields"]:
            raise NotImplementedError("Will need to find DOI somehow....")

        if self.name == "arXiv":
            if 'title' not in entry['fields']:
                raise KeyError("Missing required field: 'title'")
            new_doi = find_doi(entry)
            if new_doi is None:
                # failed crossref result... returning original entry
                # tag for later sorting
                entry['incomplete_entry'] = True
                return entry
            if new_doi == entry["fields"]["doi"]:
                warnings.warn(f"Crossref first result was the same article."
                              f"Returning original entry for "
                              f"{entry['key']}")
                return entry
            published_entry = handle_published(new_doi)
            return published_entry
        response = self.make_api_request(entry["fields"]["doi"])
        if not response or not response.get('collection'):
            # Print any warning or error messages from the API response
            messages = response.get('messages') if response else None
            if messages:
                print("API response messages:")
                for msg in messages:
                    print(f"  - {msg}")
            else:
                print("Warning: API request failed or returned no collection.")
            # Tag for later sorting to top
            entry['incomplete_entry'] = True
            return entry

        # the preprint is now published, we need to update the entry
        published_entry = (
            handle_published(
                response['collection'][0][self.published_key]
            )
        )
        return published_entry


# these are all supported preprint servers
# add lowercase key and class here, class implementation above
# insert links without last slash to make code above more readable
preprint_strategies = {
    "biorxiv":
        PreprintHandler(
            name="bioRxiv",
            config={"api_url":
                        "https://api.biorxiv.org/pubs/biorxiv",
                    "published_key": "published_doi"
                    }),
    "medrxiv":
        PreprintHandler(name="medrxiv",
                        config={"api_url":
                                    "https://api.biorxiv.org/pubs/medrxiv",
                                "published_key": "published_doi"
                                }),
    "arxiv":
        PreprintHandler("arXiv",
                        {
                            "api_url": "TheArxivAPIisNotAsNiceAsTheAbove...",
                            "published_key": "Sad"
                        })
}
