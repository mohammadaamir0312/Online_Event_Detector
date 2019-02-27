# twitter related tokens
ACCESS_TOKEN = "1070722503243223041-l8ub5d1bSZ5gyggJ6J5FIdy4JojcPu"
ACCESS_TOKEN_SECRET = "Vmw7Dr8Lt4ySQJ5rcK6WT1lNwf3bYtMonp60Pk1xsjBER"
CONSUMER_KEY = "S3oQ0jcXS8hHC0HFiAOtAt0pR"
CONSUMER_SECRET = "L2emTSIcus3K1MalJjz6fszhdMcycOYTBZmeN1nu5ZnGi3XkQk"

SF_AREA = [-123.1512, 37.0771, -121.3165, 38.5396]  # san fransisco geographical co-ordinates
NY_AREA = [-74.255735, 40.496044, -73.700272, 40.915256]  # New York geographical co-ordinates
LA_AREA = [-118.6682, 33.7037, -118.1553, 34.3373]  # Loss Angels geographical co-ordinates
CHICAGO = [-87.940267, 41.644335, -87.524044, 42.023131]  # chicago geographical co-ordinates
JAIPUR = [74.0, 25.0, 76.0, 27.0]  # jaipur geographical co-ordinates

stop_word_file = open("docs/stop-word-list.txt")  # file contains the stop words
stop_word_list = []  # stores the stop words
for each_word in stop_word_file:
    stop_word_list.append(each_word)
