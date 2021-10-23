from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
import csv
from sqlalchemy.orm import sessionmaker
from datetime import datetime

engine = create_engine('sqlite:///inventory.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    quantity = Column(Integer)
    updated = Column(Date)

def __repr__(self):
    return f'<User(name={self.name}, quantity={self.quantity}, price={self.price}, updated={self.updated}'

def csv_reader():
    with open('inventory.csv', newline='') as inventory_csv:
        inventory_reader = csv.reader(inventory_csv, delimiter=',')
        next(inventory_reader)
        rows = list(inventory_reader)
        for row in rows:
            add_to_db = Product(name=row[0], price=price_cleaner_db_initializer(row), quantity=quantity_db_initializer(row), updated=date_cleaner_db_initializer(row))
            session.add(add_to_db)
            session.commit()

def price_cleaner_db_initializer(row):
    price_to_clean = row[1]
    without_sign = price_to_clean.replace("$", "")
    try:
        without_sign_float = float(without_sign)
    except ValueError:
        pass
    else:
        return int(without_sign_float * 100)

def quantity_db_initializer(row):
    quantity_start = row[2]
    try:
        quantity_int = int(quantity_start)
    except ValueError:
        pass
    else:
        return quantity_int    

def date_cleaner_db_initializer(row):
        date_time_string = row[3]
        try:
            date_time_obj = datetime.strptime(date_time_string, '%m/%d/%Y')
            return date_time_obj
        except ValueError:
            pass




