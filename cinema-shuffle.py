import requests

# Variable to store json response from api
output = "string"

# Variable to store list of genres
gList = "string"

selectedGenre = "string"

lengthOfGlist = 0

# Boolean & variable to validate bearer token
isTokenOk = False
statusCode = int

# Variables to store year ranges
intialyear = 1900
finalyear = 2024

# Variables to store min and max rating
minRating = 0
maxRating = 10

# Function to fetch list of available genres
def reqGenre():
    try:
        url = "https://api.themoviedb.org/3/genre/movie/list?language=en"

        headers = {
            "accept": "application/json",
            "Authorization": "Bearer " + bearer_token
        }

        global gList
        gList = requests.get(url, headers=headers)

        global statusCode
        statusCode = gList.status_code
        print("\nStatus Code: "+str(statusCode))
    except requests.exceptions.RequestException as e:
        print(e)
        raise
    
    # Convert json to python dictionary
    gList = gList.json()

# Function to add serial number to the genre list
def addSn():
    global lengthOfGlist
    lengthOfGlist = len(gList['genres'])
    i=0
    while i < lengthOfGlist:
        gList['genres'][i]['sn'] = i+1 # Adding 1 to first entry instead of 0
        i+=1


# Ask user for tmdb bearer token
while isTokenOk == False:
    bearer_token = input("Enter your bearer token to start using the app:\n")
    reqGenre()
    if statusCode == 200:
        isTokenOk = True
        addSn()
        print("\nToken accepted.")
    elif statusCode == 401:
        print("\nUnauthorized, incorrect bearer token.")

# Function to send a request to the api
def ping():
    if option == "1":
        url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&sort_by=popularity.desc"
    elif option == "2" or option == "3":
        url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&primary_release_date.gte="+intialyear+"&primary_release_date.lte="+finalyear+"&sort_by=popularity.desc&with_genres="+selectedGenre+"&vote_average.gte="+minRating+"&vote_average.lte="+maxRating
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

# Year checker
def checkYears():

    global intialyear
    global finalyear

    # Boolean to check years
    isIYearOk = False
    isFYearOk = False
    
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

# Function to format the input years from user
def formatYear():
    global intialyear
    global finalyear

    intialyear = str(intialyear)+"-01-01"
    finalyear = str(finalyear)+"-12-31"

# Function to provide genre selection
def genreMenu():
    global selectedGenre

    # Print list of genres to select from
    i = 0
    while i < lengthOfGlist:
        print(str(gList['genres'][i]['sn'])+" "+gList['genres'][i]['name'])
        i+=1

    # Select Genre
    selectedSn = int(input("\nSelect one genre from the above list using its serial number.\n"))

    # Parse the input to send to ping function's url
    selectedGenre = str(gList["genres"][selectedSn-1]['id']) # "selectedSn-1" to adjust for dict starting from 0

# Function to provide rating range selection
def ratingRange():
    global minRating
    global maxRating

    # Boolean to check ratings
    isMinOk = False
    isMaxOk = False
    
    while isMinOk == False:
        try:
            minRating = int(input("\nInput minimum rating for searching movies: \nE.g. 3\n"))
            if 0 > minRating or minRating > 10:
                print("\nInvalid value, select a rating between 0 and 10.\n")
            else:
                isMinOk = True
                minRating = str(minRating)
        except ValueError:
            print("\nRating should be a number.\n")

    while isMaxOk == False:
        try:
            maxRating = int(input("\nInput maximum rating for searching movies: \nE.g. 8\n"))
            if 0 > maxRating or maxRating > 10:
                print("\nInvalid value, select a rating between 0 and 10.\n")
            else:
                isMaxOk = True
                maxRating = str(maxRating)
        except ValueError:
            print("\nRating should be a number.\n")


# Provide user options
option = input("\nWhat would you like to do ? \n\n1.Discover recently popular movies.\n2.Search for movies in a particular year range.\n3.Search for movies in a single year.\nSelect from options: 1, 2, 3\n")

# Check user input
if option == "1":
    ping()
    parse()

elif option == "2":
# Ask for year range
    checkYears()
    formatYear()
    genreMenu()
    ratingRange()
    

    ping()
    parse()

elif option == "3":
    # Boolean to check input year
    isYearOk = False
    while isYearOk == False:
        try:
            inputyear = int(input("\nInput the year for searching movies: \nE.g. 2004\n"))
            if 1900 > inputyear or inputyear > 2024:
                print("\nInvalid value, select a year between 1900 and 2024.\n")
            else:
                isYearOk = True
                intialyear = finalyear = inputyear

        except ValueError:
            print("\nYear should be a number.\n")
            
    formatYear()
    genreMenu()
    ratingRange()


    ping()
    parse()

else:
    print("Improper input")