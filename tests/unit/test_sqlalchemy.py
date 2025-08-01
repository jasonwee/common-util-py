# -*- coding: utf-8 -*-
import pytest
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# Use in-memory SQLite for testing
engine = create_engine('sqlite:///:memory:')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Define the User model
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    email = Column(String(50), unique=True)

# Create tables for each test session
Base.metadata.create_all(bind=engine)

@pytest.fixture
def session():
    session = SessionLocal()
    yield session
    session.close()

def test_create_user(session):
    user = User(name='John Doe', email='johndoe@example.com')
    session.add(user)
    session.commit()
    
    assert user.id is not None
    assert user.name == 'John Doe'
    assert user.email == 'johndoe@example.com'

def test_read_user(session):
    user = User(name='Jane Doe', email='janedoe@example.com')
    session.add(user)
    session.commit()
    
    queried_user = session.query(User).filter_by(email='janedoe@example.com').first()
    
    assert queried_user is not None
    assert queried_user.name == 'Jane Doe'

def test_update_user(session):
    user = User(name='Alice', email='alice@example.com')
    session.add(user)
    session.commit()
    
    user.name = 'Alice Smith'
    session.commit()
    
    updated_user = session.query(User).filter_by(email='alice@example.com').first()
    
    assert updated_user is not None
    assert updated_user.name == 'Alice Smith'

def test_delete_user(session):
    user = User(name='Bob', email='bob@example.com')
    session.add(user)
    session.commit()
    
    session.delete(user)
    session.commit()
    
    deleted_user = session.query(User).filter_by(email='bob@example.com').first()
    
    assert deleted_user is None
