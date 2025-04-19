from abc import ABC, abstractmethod


class PreprintStrategy(ABC):

    def _make_api_request(self, doi):
        """Common logic to make an API request."""
        # Perform the API call that is shared between journals
        print("HELLO, WE HAVE TO MAKE THE API REQUEST AND ALL THAT HERE")
        # response = requests.get(f"https://api.somepreprintserver.org/content/{doi}")
        # if response.status_code == 200:
        #     return response.json()
        # else:
        #     print(f"Error fetching preprint with DOI: {doi}")
        #     return None

    @abstractmethod
    def update_preprint(self, entry):
        pass


# strategy_pattern.py
class BioRxivPreprintStrategy(PreprintStrategy):
    def update_preprint(self, entry):
        print(f"Checking bioRxiv preprint: {entry['fields']['title']}")
        return entry
        # result = self._make_api_request(entry['fields']['doi'])
        # if result:
        #     print(f"bioRxiv entry found: {result}")
        # else:
        #     print("bioRxiv entry not found.")


class MedRxivPreprintStrategy(PreprintStrategy):
    def update_preprint(self, entry):
        print(f"Checking medRxiv preprint: {entry['fields']['title']}")
        return entry
        # result = self._make_api_request(entry['fields']['doi'])
        # if result:
        #     print(f"medRxiv entry found: {result}")
        # else:
        #     print("medRxiv entry not found.")


preprint_strategies = {
    "bioRxiv": BioRxivPreprintStrategy(),
    "medRxiv": MedRxivPreprintStrategy(),
    # Here is where we will add different strategies
}
