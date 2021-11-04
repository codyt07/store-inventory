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
    date_updated = Column(Date)

def __repr__(self):
    return f'<User(name={self.name}, quantity={self.quantity}, price={self.price}, date_updated={self.date_updated}'

def csv_reader():
    with open('inventory.csv', newline='') as inventory_csv:
        inventory_reader = csv.reader(inventory_csv, delimiter=',')
        next(inventory_reader)
        rows = list(inventory_reader)
        for row in rows:
            add_to_db = Product(name=row[0], price=price_cleaner_db_initializer(
                row), quantity=quantity_db_initializer(row), date_updated=date_cleaner_db_initializer(row))
            check_double = session.query(Product).filter(Product.name==add_to_db.name).one_or_none()
            if check_double == None:
                session.add(add_to_db)
                session.commit()
            else:
                if add_to_db.date_updated.date() > check_double.date_updated:
                    session.delete(check_double)
                    session.add(add_to_db)
                    session.commit()
                else:
                    pass
            
            
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


if __name__ == '__main__':
    print("Please Use App.Py instead!")
    

