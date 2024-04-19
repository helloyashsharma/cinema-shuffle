import requests

# Variable to store json response from api
output = "string"

# Ask user for tmdb bearer token
bearer_token = input("Enter your bearer token to start using the app:")
print("Token accepted.")

# Function to send a request to the api
def ping():
    url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + bearer_token
    }
    global output
    output = requests.get(url, headers=headers)
    output = output.json()

# Function to parse response from api
def parse():
    print("\nList of movies:\n")

    global output
    # output = json.loads(output)
    lengthOfResults = len(output['results'])

    i = 0
    while i < lengthOfResults:
        print(output['results'][i]['title'])
        i +=1


# Provide user options
option = input("\nWhat would you like to do ? \n\n1.Discover movies to watch.\n\nSelect from options: 1\n")

# Check user input
if option == "1":
    ping()
    parse()
else:
    print("Improper input")