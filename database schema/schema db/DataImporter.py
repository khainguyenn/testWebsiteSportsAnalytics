import mysql.connector
import glob
import pandas as pd
import csv
import mysql.connector
import os
import datetime
import urllib
import urllib.request

"""
This program populates the TennisSchema schema by inserting informations
on Jeff Sackmann’s ATP Tennis dataset.

"""

# Converts the date obtained from the csv files into a formatted date.
def convertDate(date):
    year = date[0:4]
    month = date[4:6]
    day = date[6:8]
    formatted_date = f"{year}-{month}-{day}"
    return formatted_date

# Define a method to insert player data
def insert_player(cursor, player_id, player_name, player_hand, player_height, player_ioc):
    insert_query = "INSERT INTO player (player_id, player_name, player_hand, player_height, player_ioc) VALUES (%s, %s, %s, %s, %s)"
    data_to_insert = (player_id, player_name, player_hand, player_height, player_ioc)
    data_to_insert = tuple(None if data is None or data == '' else data for data in data_to_insert)  # Replace missing data with None

    try:
        cursor.execute(insert_query, data_to_insert)
    except mysql.connector.Error as error_descriptor:
        print("Failed inserting player data: {}".format(error_descriptor))


# Define a method to insert tournament data
def insert_tournament(cursor, tourney_id, tourney_name, surface, draw_size, tourney_level, tourney_date):
    insert_query = "INSERT INTO tournament (tourney_id, tourney_name, surface, draw_size, tourney_level, tourney_date) VALUES (%s, %s, %s, %s, %s, %s)"
    data_to_insert = (tourney_id, tourney_name, surface, draw_size, tourney_level, tourney_date)
    data_to_insert = tuple(None if data is None or data == '' else data for data in data_to_insert)  # Replace missing data with None

    try:
        cursor.execute(insert_query, data_to_insert)
    except mysql.connector.Error as error_descriptor:
        print("Failed inserting tournament data: {}".format(error_descriptor))

# Define a method to insert match data
def insert_match(cursor, match_num, tourney_id, round, minutes, best_of, score):
    insert_query = "INSERT INTO matchL (match_num, tourney_id, round, minutes, best_of, score) VALUES (%s, %s, %s, %s, %s, %s)"
    data_to_insert = (match_num, tourney_id, round, minutes, best_of, score)
    data_to_insert = tuple(None if data is None or data == '' else data for data in data_to_insert)  # Replace missing data with None

    try:
        cursor.execute(insert_query, data_to_insert)
    except mysql.connector.Error as error_descriptor:
        print("Failed inserting match data: {}".format(error_descriptor))

def insert_played(cursor, tourney_id, match_num, player_id, win_loss, player_seed, player_ace, player_entry, player_df, player_svpt, player_bpSaved, player_rank, player_rank_points):
    insert_query = """
    INSERT INTO played (tourney_id, match_num, player_id, win_loss, player_seed, player_ace, player_entry, player_df, player_svpt, player_bpSaved, player_rank, player_rank_points)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    data_to_insert = (tourney_id, match_num, player_id, win_loss, player_seed, player_ace, player_entry, player_df, player_svpt, player_bpSaved, player_rank, player_rank_points)
    data_to_insert = tuple(None if data is None or data == '' else data for data in data_to_insert)  # Replace missing data with None

    try:
        cursor.execute(insert_query, data_to_insert)
    except mysql.connector.Error as error_descriptor:
        print("Failed inserting played data: {}".format(error_descriptor))


# Read the 'TennisSchema.sql' file into the 'schema_string' variable
schema_string = "TennisSchema.sql"
with open(schema_string, 'r') as f:
    schema_string = f.read()

# Connect to MySQL
connection = mysql.connector.connect(user='root', password='123456', host='localhost')
cursor = connection.cursor()
databaseName = "TennisSchema"


# Drop the database if it already exists
try:
	cursor.execute("DROP DATABASE IF EXISTS {}".format(databaseName))
except mysql.connector.Error as error_descriptor:
	print("Failed dropping database: {}".format(error_descriptor))
	exit(1)
# Create database
try:
	cursor.execute("CREATE DATABASE {}".format(databaseName))
except mysql.connector.Error as error_descriptor:
	print("Failed creating database: {}".format(error_descriptor))
	exit(1)
# Use the created database
try:
	cursor.execute("USE {}".format(databaseName))
except mysql.connector.Error as error_descriptor:
	print("Failed using database: {}".format(error_descriptor))
	exit(1)
# Execute the SQL schema from 'Schema.sql' to create tables
try:
	for result in cursor.execute(schema_string, multi=True):
		pass
except mysql.connector.Error as error_descriptor:
	if error_descriptor.errno == mysql.connector.errorcode.ER_TABLE_EXISTS_ERROR:
		print("Table already exists: {}".format(error_descriptor))
	else:
		print("Failed creating schema: {}".format(error_descriptor))
	exit(1)

# Closing the connection
cursor.close()


cursor = connection.cursor() #Create a new cursor to separate the data definition from the data insertion

# Connect to MySQL
player_dict = {}
tourney_dict = {}
match_dict = {} 
inserted_matches = {}
csv_directory = "/Users/nguyenduckhai/Desktop/hw3 db/tennis_atp-master/*.csv"

for filename in glob.glob(csv_directory):
    if filename.endswith(".csv"):
        csv_path = os.path.join(csv_directory, filename)
        #print("Processing file:", csv_path)
        with open(csv_path, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Extract player data for both winners and losers
                players = [(row['winner_id'], 'winner_'), (row['loser_id'], 'loser_')]
                for player_id, prefix in players:
                    if player_id not in player_dict:
                        player_name = row[prefix + 'name']
                        player_hand = row[prefix + 'hand']
                        player_height = row[prefix + 'ht']
                        player_ioc = row[prefix + 'ioc']
                        insert_player(cursor, player_id, player_name, player_hand, player_height, player_ioc)
                        player_dict[player_id] = True
                

                # Populate the tournament table
                tourney_id = row['tourney_id']
                if tourney_id not in tourney_dict:
                    tourney_name = row['tourney_name']
                    surface = row['surface']
                    draw_size = row['draw_size']
                    tourney_level = row['tourney_level']
                    tourney_date = convertDate(row['tourney_date'])
                    insert_tournament(cursor, tourney_id, tourney_name, surface, draw_size, tourney_level, tourney_date)
                    tourney_dict[tourney_id] = True

                
                # Populate the match table
                match_key = (row['match_num'], tourney_id)
                if match_key not in match_dict:
                    round = row['round']
                    minutes = row['minutes']
                    best_of = row['best_of']
                    score = row['score']
                    insert_match(cursor, row['match_num'], tourney_id, round, minutes, best_of, score)
                    match_dict[match_key] = True
                
                # Populate the played table
                # Extract the relevant data for the winner
                match_key_winner = (row['tourney_id'], row['match_num'], row['winner_id'])
                match_key_loser = (row['tourney_id'], row['match_num'], row['loser_id'])

                if match_key_winner not in inserted_matches:
                    # Extract data and insert for the winner
                    winner_id = row['winner_id']
                    winner_seed = row['winner_seed']
                    winner_entry = row['winner_entry']
                    winner_rank = row['winner_rank']
                    winner_rank_points = row['winner_rank_points']
                    winner_ace = row['w_ace']  
                    winner_df = row['w_df']
                    winner_svpt = row['w_svpt']
                    winner_bpSaved = row['w_bpSaved']
                    win_loss = 'W'

                    insert_played(cursor, row['tourney_id'], row['match_num'], winner_id, win_loss, winner_seed, winner_ace, winner_entry, winner_df, winner_svpt, winner_bpSaved, winner_rank, winner_rank_points)

                    inserted_matches[match_key_winner] = True  # Track the inserted match

                if match_key_loser not in inserted_matches:
                    # Extract data and insert for the loser
                    loser_id = row['loser_id']
                    loser_seed = row['loser_seed']
                    loser_entry = row['loser_entry']
                    loser_rank = row['loser_rank']
                    loser_rank_points = row['loser_rank_points']
                    loser_ace = row['l_ace']
                    loser_df = row['l_df']
                    loser_svpt = row['l_svpt']
                    loser_bpSaved = row['l_bpSaved']
                    win_loss = 'L'

                    insert_played(cursor, row['tourney_id'], row['match_num'], loser_id, win_loss, loser_seed, loser_ace, loser_entry, loser_df, loser_svpt,loser_bpSaved, loser_rank, loser_rank_points)

                    inserted_matches[match_key_loser] = True # Track the inserted match
                

connection.commit()
cursor.close()
