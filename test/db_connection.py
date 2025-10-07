from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

import os
from dotenv import load_dotenv

load_dotenv()

# Create the database connection URL
DATABASE_URL = os.getenv("DB_URL")

def test_connection():
    try:
        # Create an engine
        engine = create_engine(DATABASE_URL, echo=True)

        # Try connecting
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ Successfully connected! Test query returned:", result.scalar())

    except SQLAlchemyError as e:
        print("❌ Failed to connect to the database.")
        print("Error:", e)

if __name__ == "__main__":
    test_connection()
