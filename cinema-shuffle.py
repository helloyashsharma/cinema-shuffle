import requests

# Variable to store list of genres
gList = "string"

selectedGenre = "string"

lengthOfGlist = 0

# Variable to store json response from api
output = "string"

# Boolean to check years
isIYearOk = False
isFYearOk = False

# Variables to store year ranges
intialyear = 1900
finalyear = 2024

# Function to fetch list of available genres
def reqGenre():
    url = "https://api.themoviedb.org/3/genre/movie/list?language=en"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + bearer_token
    }

    global gList
    gList = requests.get(url, headers=headers)
    gList = gList.json()

    # adding serial number to the genres
    global lengthOfGlist
    lengthOfGlist = len(gList['genres'])
    i=0
    while i < lengthOfGlist:
        gList['genres'][i]['sn'] = i+1 # Adding 1 to first entry instead of 0
        i+=1


# Ask user for tmdb bearer token
bearer_token = input("Enter your bearer token to start using the app:")
print("Token accepted.")
reqGenre()

# Function to send a request to the api
def ping():
    if option == "1":
        url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&sort_by=popularity.desc"
    elif option == "2":
        url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&primary_release_date.gte="+intialyear+"&primary_release_date.lte="+finalyear+"&sort_by=popularity.desc&with_genres="+selectedGenre
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
        print("Name: "+output['results'][i]['title'])
        print("Released on: "+output['results'][i]['release_date'])
        print("Rating: {:.2f}".format(output['results'][i]['vote_average'])) # Truncating rating up to 2 decimal places
        print("Synopsis: "+output['results'][i]['overview']+"\n")
        i+=1

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
        try:
            intialyear = int(input("\nInput initial year for searching movies: \nE.g. 2004\n"))
            if 1900 > intialyear or intialyear > 2024:
                print("\nInvalid value, select a year between 1900 and 2024.\n")
            else:
                isIYearOk = True
        except ValueError:
            print("\nYear should be a number.\n")

    while isFYearOk == False:
        try:
            finalyear = int(input("\nInput final year for searching movies: \nE.g. 2010\n"))
            if 1900 > finalyear or finalyear > 2024:
                print("\nInvalid value, select a year between 1900 and 2024.\n")
            elif finalyear < intialyear:
                print("\nInvalid value, final year can't be smaller than initial year.\n")
            else:
                isFYearOk = True
        except ValueError:
            print("\nYear should be a number.\n")

    formatYear()

    # Print list of genres to select from
    i = 0
    while i < lengthOfGlist:
        print(str(gList['genres'][i]['sn'])+" "+gList['genres'][i]['name'])
        i+=1

    # Select Genre
    selectedSn = int(input("\nSelect one genre from the above list using its serial number.\n"))

    # Parse the input to send to ping function's url
    selectedGenre = str(gList["genres"][selectedSn-1]['id']) # "selectedSn-1" to adjust for dict starting from 0

    ping()
    parse()

else:
    print("Improper input")