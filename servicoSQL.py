
import mysql.connector
import pandas as pd
from mysql.connector import Error
from datetime import datetime
import os   

def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

pw ="V&M25sql"

connection = create_server_connection("localhost", "root", pw)
