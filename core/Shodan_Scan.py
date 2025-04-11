import shodan
import logging

class ShodanScanner:
    def __init__(self, api_key):
        self.api = shodan.Shodan(api_key)

    def scan(self, query):
        try:
            results = self.api.search(query)
            return [
                match.get("ip_str", "No IP") + " - " + (
                    match["hostnames"][0] if match.get("hostnames") else "No Hostname"
                )
                for match in results["matches"]
            ]
        except shodan.APIError as e:
            logging.error(f"Shodan Error: {e}")
            return []
