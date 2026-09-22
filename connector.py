import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection():
    return psycopg2.connect(
        dbname="mydb",
        user="postgres",
        password=os.getenv("PASSWORD_DB"),
        host="localhost",
        port="5432"
    )

def create_tables():
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:

                cursor.execute("""
                    create table if not exists users(
                        id serial primary key,
                        username varchar(50) unique not null,
                        password varchar(8) not null
                    );
                    create table if not exists tasks(
                        id serial primary key,
                        title varchar(100) not null,
                        description text,
                        user_id int references users(id) on delete cascade
                    );
                """)
        print("Table created")

    except Exception as e:
        print("Ошибка:", e)