from sqlalchemy import *

connection_string = 'mysql://cs441_admin:frieze_indoors_glacier@db-inventory-instance1.celqsluscson.us-west-2.rds.amazonaws.com/dbInv'

db = create_engine(connection_string)

connection = db.connect()
result = connection.execute(test_query)

metadata = MetaData()

user = Table('user', metadata,
    Column('user_id', Integer, primary_key=True),
    Column('user_name', String(16), nullable=False),
    Column('password', String(20), nullable=False)
)

# db.begin()
# conn = db.connect()
# try:
#     conn.execute(log_table.insert(), message="Operation started")
#     db.commit()
#     conn.execute(log_table.insert(), message="Operation succeeded")
# except:
#     db.rollback()
#     conn.execute(log_table.insert(), message="Operation failed")
# finally:
#     conn.close()
