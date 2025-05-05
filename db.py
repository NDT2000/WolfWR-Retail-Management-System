import mariadb
from mariadb import Error

from configparser import ConfigParser

def read_db_config(filename='config.ini', section='database'):
    parser = ConfigParser()
    parser.read(filename)

    if not parser.has_section(section):
        raise Exception(f"Section {section} not found in the {filename} file")

    return {key: value for key, value in parser.items(section)}

def connect_to_db():
    connection = None
    try:
        # Establish the connection to MariaDB
        config = read_db_config()
        connection = mariadb.connect(
            host=config['host'],  # Replace with your MariaDB host
            database=config['database'],  # Replace with your database name
            user=config['user'],  # Your username
            password=config['password'],  # Your password
            autocommit=False
        )

        if connection:
            print("\nSuccessfully connected to the database")
            # Now the connection is open, and you can perform operations here

    except Error as e:
        print(f"Error: {e}")

    return connection

def close_connection(connection):
    if connection:
        connection.close()
        print("Connection closed")

# Main execution
if __name__ == "__main__":
    db_connection = connect_to_db()
    # Perform additional operations with the connection here (e.g., queries or updates)
    # Do not close the connection immediately
    # close_connection(db_connection)  # Only call this when you actually want to close the connection
