import requests

# Variable to store json response from api
output = "string"

# Boolean to check years
isIYearOk = False
isFYearOk = False

# Variables to store year ranges
intialyear = 1900
finalyear = 2024

# Ask user for tmdb bearer token
bearer_token = input("Enter your bearer token to start using the app:")
print("Token accepted.")

# Function to send a request to the api
def ping():
    if option == "1":
        url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&sort_by=popularity.desc"
    elif option == "2":
        url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=2&primary_release_date.gte="+intialyear+"&primary_release_date.lte="+finalyear+"&sort_by=popularity.desc"
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

# Function to format the input years from user
def formatYear():
    global intialyear
    global finalyear

    intialyear = str(intialyear)+"-01-01"
    finalyear = str(finalyear)+"-12-31"

# Provide user options
option = input("\nWhat would you like to do ? \n\n1.Discover recently popular movies.\n2.Search for movies in a particular year range.\nSelect from options: 1, 2\n")

# Check user input
if option == "1":
    ping()
    parse()

elif option == "2":
# Ask for year range
    while isIYearOk == False:
        intialyear = int(input("\nInput initial year for searching movies: \nE.g. 2004\n"))
        if 1900 > intialyear or intialyear > 2024:
            print("\nInvalid value, select a year between 1900 and 2024.\n")
        else:
            isIYearOk = True

    while isFYearOk == False:
        finalyear = int(input("\nInput final year for searching movies: \nE.g. 2010\n"))
        if 1900 > finalyear or finalyear > 2024:
            print("\nInvalid value, select a year between 1900 and 2024.\n")
        elif finalyear < intialyear:
            print("\nInvalid value, final year can't be smaller than initial year.\n")
        else:
            isFYearOk = True

    formatYear()
    ping()
    parse()

else:
    print("Improper input")