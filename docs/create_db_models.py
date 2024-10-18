# created from response - used to create database and project
#  should run without error
#  if not, check for decimal, indent, or import issues

import decimal

import logging



logging.getLogger('sqlalchemy.engine.Engine').disabled = True  # remove for additional logging

import sqlalchemy



from sqlalchemy.sql import func  # end imports from system/genai/create_db_models_inserts/create_db_models_prefix.py

from logic_bank.logic_bank import Rule

from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Define SQLite database
engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite', echo=False)
Base = declarative_base()

class APIConfiguration(Base):
    """description: Stores configurations for accessing different APIs."""
    __tablename__ = 'api_configuration'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    base_url = Column(String(255), nullable=False)
    endpoint = Column(String(255), nullable=True)
    method = Column(String(10), nullable=False)  # e.g. GET, POST
    headers = Column(Text, nullable=True)

class APIResponse(Base):
    """description: Stores raw JSON responses from API requests."""
    __tablename__ = 'api_response'

    id = Column(Integer, primary_key=True, autoincrement=True)
    config_id = Column(Integer, ForeignKey('api_configuration.id'), nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    raw_response = Column(Text, nullable=False)

class DataTransformationRule(Base):
    """description: Defines rules for transforming API responses."""
    __tablename__ = 'data_transformation_rule'

    id = Column(Integer, primary_key=True, autoincrement=True)
    config_id = Column(Integer, ForeignKey('api_configuration.id'), nullable=False)
    rule_description = Column(Text, nullable=False)
    transformation_logic = Column(Text, nullable=False)

class ProcessedData(Base):
    """description: Stores data processed and transformed from raw API responses."""
    __tablename__ = 'processed_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    response_id = Column(Integer, ForeignKey('api_response.id'), nullable=False)
    transformed_data = Column(Text, nullable=False)
    processed_timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)

class APILog(Base):
    """description: Keeps a log of all API interactions and their statuses."""
    __tablename__ = 'api_log'

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    config_id = Column(Integer, ForeignKey('api_configuration.id'), nullable=True)
    request_info = Column(Text, nullable=True)
    response_info = Column(Text, nullable=True)
    status = Column(String(50), nullable=False)

class APIParameter(Base):
    """description: Stores parameters for making API requests."""
    __tablename__ = 'api_parameter'

    id = Column(Integer, primary_key=True, autoincrement=True)
    config_id = Column(Integer, ForeignKey('api_configuration.id'), nullable=False)
    param_key = Column(String(100), nullable=False)
    param_value = Column(String(255), nullable=True)

class User(Base):
    """description: Stores user information for tracking and permissions."""
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

class UserAPIConfiguration(Base):
    """description: Links users to specific API configurations they have access to."""
    __tablename__ = 'user_api_configuration'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    config_id = Column(Integer, ForeignKey('api_configuration.id'), nullable=False)

class TransformationTemplate(Base):
    """description: Predefined templates for common data transformations."""
    __tablename__ = 'transformation_template'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    template_content = Column(Text, nullable=False)

class APIResponseCache(Base):
    """description: Cache for storing previously seen API responses to improve performance."""
    __tablename__ = 'api_response_cache'

    id = Column(Integer, primary_key=True, autoincrement=True)
    config_id = Column(Integer, ForeignKey('api_configuration.id'), nullable=False)
    hashed_response = Column(String(255), nullable=False, unique=True)
    cached_data = Column(Text, nullable=False)

class APIErrorLog(Base):
    """description: Logs errors during API requests or data transformations."""
    __tablename__ = 'api_error_log'

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    config_id = Column(Integer, ForeignKey('api_configuration.id'), nullable=False)
    error_message = Column(Text, nullable=False)

class APIUsageStatistics(Base):
    """description: Maintains statistics about API usage for analytics."""
    __tablename__ = 'api_usage_statistics'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    config_id = Column(Integer, ForeignKey('api_configuration.id'), nullable=False)
    api_calls_made = Column(Integer, nullable=False, default=0)
    data_transformed = Column(Integer, nullable=False, default=0)

# Create all tables
Base.metadata.create_all(engine)

# Initialize session
Session = sessionmaker(bind=engine)
session = Session()

# Add sample data for each table
api_config1 = APIConfiguration(name="WeatherAPI", base_url="http://weatherapi.com", endpoint="/current", method="GET")
api_config2 = APIConfiguration(name="CurrencyExchangeAPI", base_url="http://currencyapi.com", endpoint="/rate", method="GET")
session.add(api_config1)
session.add(api_config2)

api_response1 = APIResponse(config_id=1, raw_response='{"temp": "20C", "condition": "Clear"}')
api_response2 = APIResponse(config_id=2, raw_response='{"rate": "1.20", "currency": "USD/EUR"}')
session.add(api_response1)
session.add(api_response2)

transformation_rule1 = DataTransformationRule(config_id=1, rule_description="Extract temperature", transformation_logic="response['temp']")
transformation_rule2 = DataTransformationRule(config_id=2, rule_description="Extract rate", transformation_logic="response['rate']")
session.add(transformation_rule1)
session.add(transformation_rule2)

processed_data1 = ProcessedData(response_id=1, transformed_data='{"temperature": "20C"}')
processed_data2 = ProcessedData(response_id=2, transformed_data='{"exchange_rate": "1.20"}')
session.add(processed_data1)
session.add(processed_data2)

api_log1 = APILog(config_id=1, request_info="GET /current", response_info="200 OK", status="Success")
api_log2 = APILog(config_id=2, request_info="GET /rate", response_info="200 OK", status="Success")
session.add(api_log1)
session.add(api_log2)

api_param1 = APIParameter(config_id=1, param_key="location", param_value="London")
api_param2 = APIParameter(config_id=2, param_key="base_currency", param_value="USD")
session.add(api_param1)
session.add(api_param2)

user1 = User(username="john_doe", email="john@example.com")
user2 = User(username="jane_doe", email="jane@example.com")
session.add(user1)
session.add(user2)

user_api_config1 = UserAPIConfiguration(user_id=1, config_id=1)
user_api_config2 = UserAPIConfiguration(user_id=2, config_id=2)
session.add(user_api_config1)
session.add(user_api_config2)

transformation_template1 = TransformationTemplate(name="TemperatureConversion", template_content="Celsius to Fahrenheit")
transformation_template2 = TransformationTemplate(name="RateFormatting", template_content="Standard Formatting")
session.add(transformation_template1)
session.add(transformation_template2)

api_response_cache1 = APIResponseCache(config_id=1, hashed_response="hashed_response1", cached_data='{"temp": "20C", "condition": "Clear"}')
api_response_cache2 = APIResponseCache(config_id=2, hashed_response="hashed_response2", cached_data='{"rate": "1.20", "currency": "USD/EUR"}')
session.add(api_response_cache1)
session.add(api_response_cache2)

api_error_log1 = APIErrorLog(config_id=1, error_message="Timeout error")
api_error_log2 = APIErrorLog(config_id=2, error_message="Invalid response format")
session.add(api_error_log1)
session.add(api_error_log2)

api_usage_stats1 = APIUsageStatistics(user_id=1, config_id=1, api_calls_made=5, data_transformed=5)
api_usage_stats2 = APIUsageStatistics(user_id=2, config_id=2, api_calls_made=3, data_transformed=2)
session.add(api_usage_stats1)
session.add(api_usage_stats2)

# Commit session
session.commit()
