from unittest import mock
from sqlalchemy import create_engine 
import pandas as pd 

#cursor = connection.cursor()

  



class mock_dbconn_csv:
    def __init__(self) -> None:
        self.engine = create_engine('sqlite:///:memory:') 
        self.connection = self.engine.raw_connection()
        self.cursor = self.connection.cursor()
        # self.cursor.execute("select * from table1")
        # record = cursor.fetchone()

    def add_csv(self,table_name,csv_file):
        df=pd.read_csv(csv_file)
        df.to_sql(table_name, self.connection, schema=None, if_exists='fail')
        # print("You're connected to database: ", record)
    def head_table(self,table_name):
        self.cursor.execute(f"select * from {table_name}")
        record = self.cursor.fetchone()
        print(record)
    def __del__(self):
        print("closing connection")

mock_obj=mock_dbconn_csv()
mock_obj.add_csv("table1","/workspaces/session_mock/tests/sample_data/test_table.csv")
mock_obj.add_csv("table2","/workspaces/session_mock/tests/sample_data/test_table.csv")
mock_obj.head_table("table1")
mock_obj.head_table("table2") 

 