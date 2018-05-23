# pymongo for DB access, time for determining the current time
import pymongo
from datetime import timedelta, datetime

def determineTimeInterval():
    # Prompt the user to enter the number of weeks that they want to view data for
    userInput = int(input("Please enter the number of weeks that you would like to retrieve data for: "))

    # Retrieve the current date/time
    currentTime = datetime.now()

    # Find the start of the week (approximately) to be the difference between the current time and the time elapsed in
    # the current week
    startOfWeek = currentTime - timedelta(days=currentTime.weekday())

    # Convert currentTIme and startOfWeek to milliseconds...
    currentTimeMs = int(round(currentTime.timestamp() * 1000))
    startOfWeekMs = int(round(startOfWeek.timestamp() * 1000))

    # ...which facilitates the math to find a final date in ms since epoch to collect data after with clean separation
    # of individual weeks
    gatherDataSince = currentTimeMs - (userInput * 604800000) + (currentTimeMs - startOfWeekMs)

    return gatherDataSince


def collectData():
    # Local variable to store the time value to determine how much data to collect
    gatherDataSince = determineTimeInterval()

    # Dictionary for data from DB
    bgData = {}

    # Connection URI to the DB
    uri = 'mongodb://readonly:password@ds062448.mlab.com:62448/chancehdb'

    # Create a client object that uses MongoClient from pymongo provided the URI
    client = pymongo.MongoClient(uri)

    # Get the default database at the URI
    db = client.get_database()

    # Get the entries collections from the DB
    entriesCollection = db.entries

    # find() returns a Cursor instance which allows us to iterate over all matching documents.
    # Get all entries since a certain time and only include the relevant fields (time, date, and no entry ID)
    allCursor = entriesCollection.find({"date": {"$gte": gatherDataSince}},
                                       {"sgv": 1, "date": 1, "_id": 0})

    # Sort the entries in descending order by date
    allCursor.sort("date", pymongo.DESCENDING)

    # Iterate through the cursor
    for entry in allCursor:
        bgData[entry["date"]] = entry["sgv"]

    # At this point it should be safe to close the client object
    client.close()

    return bgData
