import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv


def get_engine():
    """Creating PostgreSQL Engine to interact"""

        
    # WITH PORT
    # engine_uri = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
    #     os.getenv("POSTGRES_USER"),
    #     os.getenv("POSTGRES_PASSWORD"),
    #     os.getenv("POSTGRES_HOST"),
    #     os.getenv("POSTGRES_PORT"),
    #     os.getenv("POSTGRES_DB"),
    # )

    # WITHOUT PORT
    engine_uri = "postgresql+psycopg2://{}:{}@{}/{}".format(
        os.getenv("POSTGRES_USER"),
        os.getenv("POSTGRES_PASSWORD"),
        os.getenv("POSTGRES_HOST"),
        os.getenv("POSTGRES_DB"),
    )
    
    return create_engine(engine_uri, future=True)

def get_session():
    """ Creating session to access database """
    Session = sessionmaker()

    return Session(bind=get_engine())


def run_query(query, commit: bool = False):
    """Runs a query against the given SQLite database.

    Args:
        commit: if True, commit any data-modification query (INSERT, UPDATE, DELETE)
    """
    engine = get_engine()
    if isinstance(query, str):
        query = text(query)

    with engine.connect() as conn:
        if commit:
            conn.execute(query)
            conn.commit()
        else:
            return [dict(row) for row in conn.execute(query)]
