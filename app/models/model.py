from sqlalchemy import Column, String, Integer
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker 

Base = declarative_base()

class User(Base):
	"""docstring for User"""
	__tablename__ = 'user'

	id = Column(Integer, primary_key=True)
	username = Column(String(100), unique=True, nullable=False)
	email = Column(String(100), nullable=False)
	password = Column(String(100), nullable=False)

	def __repr__(Self):
		return (username, email)

# Create an engine that stores data in the local directory's
engine = create_engine('sqlite:///database.db')

# Create all tables in the engine. This is equivalent to "Create Table"
Base.metadata.create_all(engine)

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
Session = sessionmaker(bind=engine)

def insert_user(username, email, password):
	new_user = User(username=username, email=email, password=password)
	session = Session()
	session.add(new_user)
	Session.commit()