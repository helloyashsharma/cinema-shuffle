import requests
import json
import random
import customtkinter as ctk

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

# Boolean to check if config file is being used
configUsed = False

# Variable for selected popularity
selectedPop = int

# Variable for selected adult rating
isAdult = "true"

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
    
    global configUsed
    configUsed = True

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
    global selectedPop
    global isAdult
    
    initialyear = config['initialyear']
    finalyear = config['finalyear']
    selectedGenre = config['selectedGenre']
    minRating = config['minRating']
    maxRating = config['maxRating']
    selectedLng = config['selectedLng']
    selectedPop = config['popularity']
    isAdult = config['adult']

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

    # Ask for popularity
    try:
        selectedPop = int(input("\nFilter movies based on Popularity\n1. Very Popular\n2. Somewhat Popular\n3. Least Popular\nSelect from options: 1, 2, 3\n"))
        configData['popularity'] = selectedPop
    except ValueError:
        print("\nEntered value must be a number.\n")

    # Ask if adult or not
    try:
        isItAdult = int(input("\nFilter movies based on adult rating\n1. Is Adult\n2. Not Adult\nSelect from options: 1, 2\n"))
        if isItAdult == 1:
            configData['adult'] = "true"
        elif isItAdult == 2:
            configData['adult'] = "false"
    except ValueError:
        print("\nEntered value must be a number.\n")

    print("\nThis is the final config:\n"+str(configData))

    with open('config.json', 'w') as file:
        json.dump(configData, file, indent=4)

# Tesing tkinter
def GUI():
    
    # Window
    window = ctk.CTk()
    window.title('CinemaShuffle')
    window.geometry('800x500')

    # Label
    mainLabel = ctk.CTkLabel(master=window, text='Welcome to CinemaShuffle')
    mainLabel.pack()

    window.mainloop()

# Test window
GUI()

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
        url = "https://api.themoviedb.org/3/movie/upcoming?language=en-US&page=1"
    elif option == "2" or option == "3" or option == "4" or option == "6":
        url = "https://api.themoviedb.org/3/discover/movie?include_adult="+isAdult+"&include_video=false&language=en-US&primary_release_date.gte="+initialyear+"&primary_release_date.lte="+finalyear+"&sort_by=popularity.desc&with_genres="+selectedGenre+"&vote_average.gte="+minRating+"&vote_average.lte="+maxRating+"&with_original_language="+selectedLng
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
    selectedSn = input("\nSelect one or more genres from the above list using its serial number separated with commas.\nFor e.g. 3,21\n").replace(" ", "").replace(",", " ")
    selectedSn = selectedSn.split() # Convert to list for interating below

    # Parse the input to send to ping function's url
    selectedGenre = ""
    for i in selectedSn: # Going through all the selected genres
        selectedG = str(gList["genres"][int(i)-1]['id']) # "int(i)-1" to adjust for dict starting from 0
        selectedGenre += selectedG+"%2C" # Adding the "%2C" between the selected genres to act as AND
        
    selectedGenre = selectedGenre[:-3] # Removing any trailing "%2C"

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
    try:
        selectedLng = int(input("\nSelect one language from the above list using its serial number.\n"))
    except ValueError:
        print("\nEntered value must be a number.\n")

    # Parse the input to send to ping function's url
    selectedLng = str(lList[selectedLng-1]['iso_639_1']) # "selectedLng-1" to adjust for dict starting from 0 

# Function to display results based on popularity
def popMenu():

    global output
    global configUsed
    global selectedPop

    # Sorting the results key based on popularity
    sortedRes = sorted(output['results'], key=lambda x: x['popularity'], reverse=True)

    # Adding the sorted values back to the original json
    output['results'] = sortedRes
    
    # Take input from user
    if configUsed == False: # Only taking input if the config file is not being used
        try:
            selectedPop = int(input("\nFilter movies based on Popularity\n1. Very Popular\n2. Somewhat Popular\n3. Least Popular\nSelect from options: 1, 2, 3\n"))
        except ValueError:
            print("\nEntered value must be a number.\n")
    
    lengthOfResults = len(output['results'])
    splice = int(lengthOfResults/3) # Split by 3 based on popularity after being sorted
    
    # If user selects one then they want the first 1/3rd movies since it has been sorted based on desc popularity 
    if selectedPop == 1:
        spliced = output['results'][:splice] # Using list splicing to only keep the first 1/3 rd splice elements
        output['results'] = spliced
    elif selectedPop == 2:
        spliced = output['results'][splice:splice*2] # Using list splicing to only keep the middle 1/3rd splice elements
        output['results'] = spliced
    elif selectedPop == 3:
        spliced = output['results'][splice*2:lengthOfResults] # Using list splicing to only keep the last 1/3rd splice elements
        output['results'] = spliced


# Provide user options
option = input("\nWhat would you like to do ? \n\n1.Discover upcoming movies.\n2.Search for movies in a particular year range.\n3.Search for movies in a single year.\n4.Use default config.\n5.Edit config file.\n6.Pick a random movie.\nSelect from options: 1, 2, 3, 4, 5, 6\n")

# Check user input
if option == "1":
    # Ping API
    ping()

    # Parse response
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

    # Ping API
    ping()

    # Filter based on popularity
    popMenu()

    # Parse response
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

    # Ping API
    ping()

    # Filter based on popularity
    popMenu()

    # Parse response
    parse()

elif option == "4":
    # Use config file
    useConfig()
    formatYear()

    # Ping API
    ping()

    # Filter based on popularity
    popMenu()

    # Parse response
    parse()

elif option == "5":
    # Edit config file
    editConfig()

elif option == "6":
    # Use config file
    useConfig()
    formatYear()

    # Ping API
    ping()

    # Randomly choose one movie
    output['results'] = [random.choice(output['results'])]
    
    # Parse response
    parse()

else:
    print("Improper input")
