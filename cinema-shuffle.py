import requests
import json

# Variable to store json response from api
output = str

# Variable to store list of genres
gList = str
selectedGenre = str
lengthOfGlist = 0

# Variable to store list of languages
lList = str
selectedLng = str
lengthOfLlist = 0

# Boolean & variable to validate bearer token
isTokenOk = False
statusCode = int

# Variables to store year ranges
initialyear = 1900
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
    
    

# Function to add serial number to genre list
def addSn(length, list):
    i=0
    while i < length:
        list['genres'][i]['sn'] = i+1 # Adding 1 to first entry instead of 0
        i+=1

# Function to add serial number to languages list
def addSnLng(length, list):
    i=0
    while i < length:
        list[i]['sn'] = i+1 # Adding 1 to first entry instead of 0
        i+=1

# Function to fetch list of available languages
def reqLng():
    try:
        url = "https://api.themoviedb.org/3/configuration/languages"

        headers = {
            "accept": "application/json",
            "Authorization": "Bearer " + bearer_token
        }

        global lList
        lList = requests.get(url, headers=headers)

        global statusCode
        statusCode = lList.status_code
        print("\nStatus Code: "+str(statusCode))
    except requests.exceptions.RequestException as e:
        print(e)
        raise
    
    # Convert json to python dictionary
    lList = lList.json()
    global lengthOfLlist
    lengthOfLlist = len(lList)

    # add serial number to the language list
    addSnLng(lengthOfLlist, lList)

# Function to use the config file
def useConfig():

    with open('config.json', 'r') as file:
        config = open('config.json')
        config = json.load(config)

        print("\nThis is the default config:\n"+str(config))

    global initialyear
    global finalyear
    global selectedGenre
    global minRating
    global maxRating
    global selectedLng
    
    initialyear = config['initialyear']
    finalyear = config['finalyear']
    selectedGenre = config['selectedGenre']
    minRating = config['minRating']
    maxRating = config['maxRating']
    selectedLng = config['selectedLng']

# Function to edit the config file
def editConfig():

    with open('config.json', 'r') as file:
        config = open('config.json')
        configData = json.load(config)

    print("\nThis is the default config:\n"+str(configData))

    checkYears()
    configData['initialyear'] = str(initialyear)
    configData['finalyear'] = str(finalyear)

    # Ask for genre
    genreMenu()
    configData['selectedGenre'] = selectedGenre

    # Ask for rating
    ratingRange()
    configData['minRating'] = minRating
    configData['maxRating'] = maxRating

    # Ask for languague
    reqLng()
    langMenu()
    configData['selectedLng'] = selectedLng

    print("\nThis is the final config:\n"+str(configData))

    with open('config.json', 'w') as file:
        json.dump(configData, file, indent=4)


# Ask user for tmdb bearer token
while isTokenOk == False:
    bearer_token = input("Enter your bearer token to start using the app:\n")
    reqGenre()
    if statusCode == 200:
        isTokenOk = True
        print("\nToken accepted.")

        # Convert json to python dictionary
        gList = gList.json()
        lengthOfGlist = len(gList['genres'])

        # Add serial number to the list
        addSn(lengthOfGlist, gList)
    elif statusCode == 401:
        print("\nUnauthorized, incorrect bearer token.\n")

# Function to send a request to the api
def ping():
    if option == "1":
        url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&sort_by=popularity.desc"
    elif option == "2" or option == "3" or option == "4":
        url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&primary_release_date.gte="+initialyear+"&primary_release_date.lte="+finalyear+"&sort_by=popularity.desc&with_genres="+selectedGenre+"&vote_average.gte="+minRating+"&vote_average.lte="+maxRating+"&with_original_language="+selectedLng
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

    global initialyear
    global finalyear

    # Boolean to check years
    isIYearOk = False
    isFYearOk = False
    
    while isIYearOk == False:
        try:
            initialyear = int(input("\nInput initial year for searching movies: \nE.g. 2004\n"))
            if 1900 > initialyear or initialyear > 2024:
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
            elif finalyear < initialyear:
                print("\nInvalid value, final year can't be smaller than initial year.\n")
            else:
                isFYearOk = True
        except ValueError:
            print("\nYear should be a number.\n")

# Function to format the input years from user
def formatYear():
    global initialyear
    global finalyear

    initialyear = str(initialyear)+"-01-01"
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

# Function to provide language selection
def langMenu():
    global selectedLng

    # Print list of languages to select from
    i = 0
    while i < lengthOfLlist:
        print(str(lList[i]['sn'])+" "+lList[i]['english_name'])
        i+=1

    # Select Genre
    selectedLng = int(input("\nSelect one language from the above list using its serial number.\n"))

    # Parse the input to send to ping function's url
    selectedLng = str(lList[selectedLng-1]['iso_639_1']) # "selectedLng-1" to adjust for dict starting from 0 

# Provide user options
option = input("\nWhat would you like to do ? \n\n1.Discover recently popular movies.\n2.Search for movies in a particular year range.\n3.Search for movies in a single year.\n4.Use default config.\n5.Edit config file.\nSelect from options: 1, 2, 3, 4, 5\n")

# Check user input
if option == "1":
    ping()
    parse()

elif option == "2":
    # Ask for year range
    checkYears()
    formatYear()

    # Ask for genre
    genreMenu()

    # Ask for rating
    ratingRange()

    # Ask for languague
    reqLng()
    langMenu()

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
                initialyear = finalyear = inputyear

        except ValueError:
            print("\nYear should be a number.\n")
            
    formatYear()

    # Ask for genre
    genreMenu()

    # Ask for rating
    ratingRange()

    # Ask for languague
    reqLng()
    langMenu()


    ping()
    parse()

elif option == "4":
    # Use config file
    useConfig()
    formatYear()

    ping()
    parse()

elif option == "5":
    # Edit config file
    editConfig()

else:
    print("Improper input")
