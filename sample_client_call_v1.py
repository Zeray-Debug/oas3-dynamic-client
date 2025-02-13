"""
Dynamic API client Module for making API calls to an OpenAPI-compliant API

This module fetches the OpenAPI (Swagger) specification from a given API,
extracts the endpoints that support GET request, and allows dynamic GET requests. 

"""

import requests 
import json

class DynamicAPIClient:
    def __init_(self, base_url, spec_path= "path-to-spec-file"):
        """
        Initialize the client with the base URL of the API and the path to the OpenAPI spec file.
        :param base_url: The base URL of the API
        :param spec_path: The path to the OpenAPI spec file

        """

        self.base_url = base_url.rstrip("/") # Remove trailing slash if present
        self.spec_url = f"{self.base_url}{spec_path}"
        self.spec = self.fetch_spec() # Retrieve the OpenAPI spec
        self.get_endpoints = self.extract_get_endpoints(self.spec) # Extract the endpoints that support GET requests

    def fetch_spec(self): 
        """
        Fetch the OpenAPI specification from the API
        """
        try:
            response = requests.get(self.spec_url)
            response.raise_for_status() # Raise an exception for 4XX and 5XX status codes
            print(f"Successfully fetched spec from {self.spec_url}")
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching spec: {e}")
            return {}
        
    def extract_get_endpoints(self, spec):
        """
        Extract the endpoints that support GET requests from the OpenAPI spec
        :param spec: The OpenAPI spec as a dictionary
        :return: Dictionary with endpoint paths as keys, and GEt operation details as values
        """
        endpoints = {}
        paths = spec.get("paths", {})
        for path, methods in paths.items():
            if "get" in methods:
                endpoints[path] = methods["get"]
        return endpoints
    
    #TODO finish implementing the call_endpoint method