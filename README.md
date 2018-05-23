# bg-visualization
Python scripts to facilitate the retrieval and visualization of blood glucose data stored in a remote MongoDB.

As a Type 1 Diabetic myself, I value the ability to gain insights from data illustrating my management. Today, existing tools often end up being insufficient or inconvenient to use for accomplishing this goal. Furthermore, many of the available tools are difficult or even impossible to modify to suit an individual's needs or preferneces. This simple project was built with these ideals in mind, providing two interesting and helpful ways to realize trends in a diabetic's data and management.

Following are additional details about each script.

### getData.py
At the heart of this project is the ability to retrieve the necessary data from a remote database. The script is written to specifically pull data from a MongoDB database (and has a read-only connection to my own personal database for example purposes) using the MongoDB driver. The script creates a connection to the database, queries for the relevant BG data, does minor data cleanup, and returns a dictionary of the BG values and their timestamp (in milliseconds sicne epoch). Also included in the script is a function to determine the time-interval over which data should be collected (as downloading the entire database may not be optimal). This "determineTimeInterval" function prompts the user to enter the number of weeks to collect data for and does the necessary math to determine a date which all data after that date should be collected. The collectData function depends on the determineTimeInterval function.

### graph.py
This first script dedicated to creating the graph(s) using Matplotlib imports and calls the collectData function from the getData script. With this data stored locally, the script stores the data in a more useful format (a couple times, actually), determines whether each value is in or out of range, and *then* graphs the data. The graph that is created is a stacked bar graph that shows the time spent in range (by number of entries) for each week worth of data. I anticipate that this graph would provide a more general insight into management over a period of time that falls between daily analysis and monthly overviews.

### graph2.py
The second graphing script shares a significant amoount of similaries and overlap with the other, but is rewritten slightly to graph the time spent in range by each day of the week. In comparison to the previous graph, I created this one in hopes of revealing any potential patterns that reoccur on a particular day of the week (e.g. consistently occuring lows on Tuesdays due to an additonal amount of exercise that wasn't noticed previously).

### Program limitations and issues
These scripts are best summed up as functional prototypes. They will not fail gracefully, possess some scattered (minor yet significant) approximations that may influence the data, and could more generally be improved to provide a clearer insight into the data while being more reselient.

Most notably, graph.py and graph2.py could likely be combined into a single script, but were kept seperate due to issues with Matplotlib creating two figures in one script. Given how similar the two are, being able to combine them would be more efficient. 

### Contribuiting
While this project wasn't built with the expectation of receiving outside contributions, pull requests are welcome, particuarly if they provide meaningful improvements to the script('s) efficiency and functionality. More than anything, I hope this project will serve as an example of how it is possible to visualize one's own data in an effcient manner.

To test these scripts out for yourself, download this repository, ensure that the three scripts stay in the same directory, and run either graph.py or graph2.py depending on which type of graph you would like.
