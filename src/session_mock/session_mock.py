
from __future__ import annotations
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from mock_alchemy.mocking import UnifiedAlchemyMagicMock
from unittest import mock
import pandas as pd

Base = declarative_base()

class SomeTable(Base):
    """SQLAlchemy object representing some table."""
    __tablename__ = "some_table"
    pkey = Column(String, primary_key=True)
    # col1 = Column(String(50))
    def __init__(self,**kwargs):
        self.__dict__.update( kwargs )
    # this below should be the same as above
    # def __init__(self, **kwargs):
    #     for k, v in kwargs.iteritems():
    #         setattr(self, k, v)

    def __eq__(self, other: Model) -> bool:
        """Object equality checker."""
        if isinstance(other, SomeTable):
            return self.pkey == other.pkey and self.col1 == other.col1
        return NotImplemented

col1_val = "abc"
row1 = SomeTable(pkey=1, col1=col1_val,col2='abcd')
print("--------",mock.call.query(SomeTable),mock.call.query(SomeTable.col1),mock.call.filter(SomeTable.pkey == 2))
mock_session = UnifiedAlchemyMagicMock(
    data=[
        (
            [
                mock.call.query(SomeTable.col1),
                mock.call.filter(SomeTable.pkey == 1),
            ],
            [(col1_val,)],
        )
        ,
        (
            [
                mock.call.query(SomeTable),
                mock.call.filter(SomeTable.pkey == 1),
            ],
            [row1],
        ) 

    ]
)

#### Selecting on a column and using scalar()

found_col1 = mock_session.query(SomeTable.col1).filter(SomeTable.pkey == 1).scalar()
assert col1_val == found_col1

#### Selecting on a table and using scalar()

found_row = mock_session.query(SomeTable).filter(SomeTable.pkey == 1).scalar()
assert row1 == found_row

print("read sample data")
df=pd.read_csv("/workspaces/session_mock/tests/sample_data/test_table.csv")
print(df)
# for col in df:
#     print(col)
#     for row in df[col]:
#         print(row)


rows=(df.to_dict(orient='records'))
data =[]
print("---data",type(data))
for row in rows:
    print(row)
    x=SomeTable(pkey=1, **row)
    print(x) 
  