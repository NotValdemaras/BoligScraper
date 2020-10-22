import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy.orm import sessionmaker
from scraper2 import scrape


engine = create_engine('sqlite:///test2.db', echo=False)
con = engine.connect()
Base = declarative_base()

#Get apartment list from first page of bolig portal
listing = scrape()
print(listing['id'])
class bolig(Base):
    '''
    A table to store data from boligportal
    '''

    __tablename__ = 'bolig'
    id = Column(String, primary_key=True)
    link = Column(String, unique = True)
    title = Column(String)
    location = Column(String)
    price = Column(String)
    description = Column(String)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

#Extract the entries that are already in the database


listing.to_sql(name='table1',con=con, if_exists='replace')

sql = "SELECT * FROM table1"
old_listing = pd.read_sql(sql, con)
print(old_listing['id'])

def dataframe_difference(df1, df2, which=None):
    """Find differences between two dataframes"""
    df = pd.merge(df1, df2, how='outer', indicator=True)
    new = df[df['_merge']=='right_only'][df2.columns]
    return new

