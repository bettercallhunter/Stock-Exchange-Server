from sqlalchemy import create_engine, text
import sys
engine = create_engine("postgresql://postgres:0000@localhost:5432/stock")

# create a Statement object using a SQL query string
stmt = text("SELECT * FROM "+sys.argv[1])

# get a connection from the engine and execute the statement
with engine.connect() as conn:
    result = conn.execute(stmt)

# process the result
for row in result:
    print(row)

