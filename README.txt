Note: This file looks much nicer as a markdown file, which is included in the zip file

# What option?
##################################################
Option 2

# What does it do?
##################################################
This program uses a list of movies and gathers information about the movies, it then gets tweets about the top paid actors in the movies and stores all of that information into a database. The database is then used to query interesting intersections of information about the movie and tweets. No input is needed.

# How to run it?
##################################################
Run the command: python 206_final_project.py

# What are the dependencies?
##################################################
* A twitter_info.py file containing your consumer_key, consumer_secret, access_token, and access_token_secret, all gathered from twitter

# Files included?
##################################################
## 206_final_project.py
    - Completed project with all final code
## final_project.db
    - File containing all final database data
## output.txt
    - Final output of 206_final_project.py

## 206_data_access.py
    - The second checkpoint file to this project, just sets up the caching methods and some tests
## 206_final_project_cache.json
    - Dictionary file used for caching API data
## 206_finalproject_plan.txt
    - Outline of my initial project plan
## 206_project_plan.py
    - Initial project plan program with tests

# Function Descriptions
##################################################
## get_twitter_search_data
    -input: a required string variable named search_term
    -return value: a json formatted search term query response from the tweepy api
    -behavior: this function uses caching to speed up search results from tweepy
## get_twitter_user_data
    -input: a required user string variable which can either be a twitter screen name or twitter id string
    -return value: a json formatted user search response from the tweepy api
    -behavior: this function uses caching to speed up search results from tweepy
## get_OMDB_data
    -input: a required string variable named search_term that should be a movie
    -return value: a json formatted response from the OMDB api containing data about the movie searched for
    -behavior: this function uses caching to speed up search results from the OMDB api

# Class Descriptions
##################################################
## Movie
    -One Instance: this respresents a single movie and all of its relevant data
    -Required constructor input: structured data - json formatted dictionary containing the same parameters as are given in a response from the OMDB api
    -Methods
        * __str__
            -Input: No input required
            -Behavior: It concatenates the movie title and director to produce a more unique movie title
            -Return Value: the string formed by the concatenation of movie title, and director
        * get_actors
            -Input: Optional input num_actors detailing the amount of actors the user wants returned
            -Behavior: creates a list of actors from the movie starting with the top paid actor and moving down
            -Return Value: a list of actor name strings

# Database Descriptions
##################################################
## Tweets Table
    -Row Representation: a tweet from Twitter
    -Attributes in each row: 
        *text
            - the main body text of the tweet
        *tweet_id
            - the unique tweet id assigned by twitter
        *user_id
            - the unique user id assigned by twitter and pertaining to a row in the Users Table
        *movie_id
            - the movie id pertaining to a row in the Movie table, uniquely assigned by the OMDB api
        *num_favorites
            - the amount of times this tweet has been favorited
        *num_retweets
            - the amoount of times this tweet has been retweeted
## Movies Table
    -Row Representation: a Movie from the OMDB api
    -Attributes in each row:
        *movie_id
            - the unique id assigned to this movie by the OMDB api
        *title
            - the title of the movie with its director name to make it more unique in case multiple movies exist with the same name but different directors
        *director
            - the name of the director of the movie
        *num_languages
            - the number of languages this movie was produced in
        *imdb_rating
            - the decimal rating of the movie given by imdb
        *top_billed_actor
            - the name of the actor that was top billed in the movie
## Users Table
    -Row Representation: a user from Twitter
    -Attributes in each row:
        *user_id
            - the unique user id assigned by twitter
        *screen_name
            - the screen name of the Twitter user
        *num_favorites
            - the number of tweets the user has favorited
        *description
            - the user given text description of themself

# Data Manipulation Descriptions
##################################################
What else does the code do?
    *The code also uses many different structures throughout to gather the data in meaningful ways, such as using dictionaries to store actor, movie pairs and lists to store instances of movies for future database population.
How is it useful?
    *This code is useful for gathering all of the information into usable structures that allow database insertion to be simpler and more meaningful
What will it show you?
    *This program will show you interesting data about relevant actors (judged by the amount of retweets about them), popular tweets about those actors in good movies. It will show you the users most favorited tweets about these actors, the most common characters used in these tweets and the most active users in the created database (judged by the number of favorites they have made)
What should a user expect?
    *The user should expect an output file containing all of the above information in a nicley formatted, readable output

# Why did I choose this project?
##################################################
I wanted to be able to see data about some of my favorite movies and use that in combination with Twitter to see which actors from those movies are still relevant in the eyes of Twitter users

# SI 206 Specific Information
##################################################
Line(s) on which each of your data gathering functions begin(s):
    *get_twitter_search_data: line 57
    *get_twitter_user_data: line 69
    *get_OMDB_data: line 82
Line(s) on which your class definition(s) begin(s):
    * Movie Definition: line 99
Line(s) where your database is created in the program:
    * Database creation: lines 164-207
Line(s) of code that load data into your database:
    * Database loading: lines 209-254
Line(s) of code (approx) where your data processing code occurs — where in the file can we see all the processing techniques you used?
    *General area: lines 259 - 288
    *Dictionary comprehension: line 259, 265
    *List comprehension: line 270
    *Collections Counter: lines 276 - 281
    *Sorting with a key parameter: line 287
Line(s) of code that generate the output.
    *Output generation: lines 291 - 339
