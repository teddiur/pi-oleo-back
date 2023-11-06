from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_URL = 'sqlite:///oleo-descarte.sqlite3'

engine = create_engine(DB_URL, connect_args={'check_same_thread': False})
sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
metadata = Base.metadata

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    with engine.connect() as connection:
        try:        
            Base.metadata.create_all(bind=engine)
            # seed_data()
        except Exception as e:
            print(f"Error creating tables: {str(e)}")

def drop_tables():
    with engine.connect() as connection:
        try:
            Base.metadata.drop_all(bind=engine)
        except Exception as e:
            print(f"Error dropping tables: {str(e)}")
    
def seed_data():
    db = sessionlocal()
    try:
        # user1 = user.User(email="user1@example.com", name="User 1", hashed_password="password1", city="City 1", district="District 1", oil_quantity=100)
        # user2 = user.User(email="user2@example.com", name="User 2", hashed_password="password2", city="City 2", district="District 2", oil_quantity=200)

        # db.add(user1)
        # db.add(user2)
        db.commit()
    finally:
        db.close()