import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy.orm import sessionmaker
from scraper2 import scrape
from notification import sendEmail
import time

myIt = 1
while True:
    #Print iteration number
    print(f'Running iteration {myIt}')
    #Connect to database

    print('Connecting to database')
    engine = create_engine('sqlite:///test2.db', echo=False)
    con = engine.connect()
    Base = declarative_base()

    class bolig(Base):
        '''
        A table to store data from boligportal
        '''

        __tablename__ = 'bolig'
        id = Column(String, primary_key=True)
        link = Column(String, primary_key = True)
        title = Column(String)
        location = Column(String)
        price = Column(String)
        description = Column(String)

    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()


    #Get apartment list from first page of bolig portal
    print("Getting information from boligportal")
    new_listing = scrape()
    #Extract the entries that are already in the database
    print('Extracting listings')
    sql = "SELECT * FROM table1"
    old_listing = pd.read_sql(sql, con)[new_listing.columns]
    #Extract the new rows from the new df

    print('Matching listings to database')
    def dataframe_difference(df1, df2, which=None):
        """Find differences between two dataframes"""
        a = df1.loc[:, df1.columns != 'id']
        b = df2.loc[:, df2.columns != 'id']
        df = pd.merge(a, b, how='outer', indicator=True)
        new = df[df['_merge']=='right_only'][a.columns]
        return df2[df2['link'].isin(new['link'])]

    new = dataframe_difference(old_listing, new_listing)
    #Append new entries to the database
    print(f'Adding {len(new)} new entries to database')
    new.to_sql(name='table1',con=con, if_exists='append')
    print('Done')


    #Send notification is there are new entries
    sendEmail(new)
    print('..................................')
    myIt += 1
    #time.sleep(60)

