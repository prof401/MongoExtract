from pymongo import MongoClient
import yaml


def get_database():
    with open('config.yml', 'r') as file:
        config_file = yaml.safe_load(file)

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    connection_string = config_file['mongodb']['uri']

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(connection_string)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client[config_file['mongodb']['client']]


# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":
    # Get the database
    dbname = get_database()
