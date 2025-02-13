# Pseudocode for Dynamic API Client 

class DynamicAPIClient:
    def __init__(self,base_url):

        #save the base API URL
        """
        using "self" to reference the current instance of the class. 
        It's used to access variables that belong to the class and other methods on the same object
        
        This ensures that each instance of the class stores its own "base_url" value for the API
        """
        self.base_url = base_url

        """
        Retrieve the OpenAPI spec

        This piece of code calls the fetch_spec methood on the current instance of the class (i.e., "self")
        Whatever value is returned by the fetch_spec method is stored in the "spec" instance variable of the current instance of the class

        Which means that when an instance of the DynamicAPIClietn is initialized, it retrieves some specificiation
        which in this case os the OpenAPI spec by calling the fetch_spec method and then stores it in the "spec" instance variable for later use.
        """
        self.spec = self.fetch_spec()

        """
        Extract the endpoints that support GET

        The following code calls the extract_get_endpoints method on the current instance of the class (i.e., "self")
        The value returned by the extract_get_endpoints method is stored in the "get_endpoints" instance variable of the current instance of the class
        
        In summary, the code processes the OpenAPI spec to extract the endpoints that support GET requests and stores them in the "get_endpoints" instance variable
        making said endpoints available for later use.
        """

        self.get_endpoints = self.extract_get_endpoints(self.spec)

    def fetch_spec(self):
        #Make an HTTP Get request to fetch the OpenAPI JSON spec
        response = requests.get(f"{self.base_url}/openapi.json") #need to edit this line to make it work with the name of the actual OpenAPI spec file

        #Convert the response to a JSON object and return it
        return response.json()
    
    def extract_get_endpoints(self,spec):
        endpoints = {}

        # Loop through all the the paths in the spec
        for path, methods in spec.get("paths", {}):
            if "get" in methods:
                #Store the parameters for the GET method
                endpoints[path] = methods["get"]
            return endpoints
        
    def call_endpoint(self, endpoint, params = None):
        # Construct the full URL for the endpoint
        url = self.base_url + endpoint

        # Make the GET request, passing any query parameters
        response = requests.get(url, params=params)
        return response.json()
    
    #Usage Example
    if __name__ == "__main__":
        #Instantiate the DynamicAPIClient class with the base URL of the API
        api_client = DynamicAPIClient("https://api.example.com")

        #Print the available GET endpoints from the spec
        print("Available GET endpoints:", api_client.get_endpoints)

        # Call a specific endpoint (e.g., "/users") with a optional query parameters 
        result = api_client.call_endpoint("/users", params={"limit": "10"})
        print("Result from calling endpoint:", result)
