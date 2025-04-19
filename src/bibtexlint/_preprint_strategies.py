import warnings

import requests


class PreprintHandler():

    def __init__(self, name: str, config: dict):
        self.name = name
        self.api_url = config.get("api_url")
        self.published_key = config.get("published_key")

    def _make_api_request(self, doi):
        """Common logic to make an API request."""
        # Perform the API call
        try:
            response = requests.get(f"{self.api_url}/{doi}")
        except requests.exceptions.MissingSchema:
            warnings.warn(f"API request failed ({doi}), will be ignored.")
            return None
        if response.status_code == 200:
            return response.json()
        else:
            warnings.warn(f"API request for doi:{doi} failed with status code "
                          f"{response.status_code}...")
            return None

    def _find_doi(self):
        """
        This function will try to find the DOI for a preprint.
        :return:
        :rtype:
        """
        doi = ""
        # todo try to find doi for an entry that does not have one...
        return doi

    def handle_published(self, data):
        published_doi = data['collection'][0][self.published_key]
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

    def update_preprint(self, entry):
        print(f"Checking a preprint: {entry['fields']['title']}")
        if "doi" in entry["fields"]:
            response = self._make_api_request(entry["fields"]["doi"])
            if not response:
                # API request failed, warnings were printed and we simply return
                return entry
            if not self.published_key in response['collection'][0]:
                print(f"Publication ({entry["fields"]["doi"]}) is not yet "
                      f"published...")
                return entry
            # the preprint is now published, we need to update the entry
            published_entry = self.handle_published(response)
            return published_entry
        else:
            raise NotImplementedError("Will need to find DOI somehow....")

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
        PreprintHandler(name="arXiv",
                        config={"api_url":
                                    "https://api.biorxiv.org/pubs/medrxiv",
                                "published_key": "published_doi"
                                }),
    "arxiv":
        PreprintHandler("", {
            "api_url": "",
            "published_key": ""
            # todo this seesm to not exist..
            #  in this case I will have to google scholar
            # todo also need to set api_url for arxiv and figure out next steps
        })
}
