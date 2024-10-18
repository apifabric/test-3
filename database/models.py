# coding: utf-8
from sqlalchemy import DECIMAL, DateTime  # API Logic Server GenAI assist
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  October 18, 2024 13:40:11
# Database: sqlite:////tmp/tmp.5gFDyqLafO/test/database/db.sqlite
# Dialect:  sqlite
#
# mypy: ignore-errors
########################################################################################################################
 
from database.system.SAFRSBaseX import SAFRSBaseX
from flask_login import UserMixin
import safrs, flask_sqlalchemy
from safrs import jsonapi_attr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NullType
from typing import List

db = SQLAlchemy() 
Base = declarative_base()  # type: flask_sqlalchemy.model.DefaultMeta
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.sqlite import *



class ApiConfiguration(SAFRSBaseX, Base):
    """
    description: Stores configurations for accessing different APIs.
    """
    __tablename__ = 'api_configuration'
    _s_collection_name = 'ApiConfiguration'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    base_url = Column(String(255), nullable=False)
    endpoint = Column(String(255))
    method = Column(String(10), nullable=False)
    headers = Column(Text)

    # parent relationships (access parent)

    # child relationships (access children)
    ApiErrorLogList : Mapped[List["ApiErrorLog"]] = relationship(back_populates="config")
    ApiLogList : Mapped[List["ApiLog"]] = relationship(back_populates="config")
    ApiParameterList : Mapped[List["ApiParameter"]] = relationship(back_populates="config")
    ApiResponseList : Mapped[List["ApiResponse"]] = relationship(back_populates="config")
    ApiResponseCacheList : Mapped[List["ApiResponseCache"]] = relationship(back_populates="config")
    ApiUsageStatisticList : Mapped[List["ApiUsageStatistic"]] = relationship(back_populates="config")
    DataTransformationRuleList : Mapped[List["DataTransformationRule"]] = relationship(back_populates="config")
    UserApiConfigurationList : Mapped[List["UserApiConfiguration"]] = relationship(back_populates="config")



class TransformationTemplate(SAFRSBaseX, Base):
    """
    description: Predefined templates for common data transformations.
    """
    __tablename__ = 'transformation_template'
    _s_collection_name = 'TransformationTemplate'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    template_content = Column(Text, nullable=False)

    # parent relationships (access parent)

    # child relationships (access children)



class User(SAFRSBaseX, Base):
    """
    description: Stores user information for tracking and permissions.
    """
    __tablename__ = 'user'
    _s_collection_name = 'User'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    is_active = Column(Boolean, nullable=False)

    # parent relationships (access parent)

    # child relationships (access children)
    ApiUsageStatisticList : Mapped[List["ApiUsageStatistic"]] = relationship(back_populates="user")
    UserApiConfigurationList : Mapped[List["UserApiConfiguration"]] = relationship(back_populates="user")



class ApiErrorLog(SAFRSBaseX, Base):
    """
    description: Logs errors during API requests or data transformations.
    """
    __tablename__ = 'api_error_log'
    _s_collection_name = 'ApiErrorLog'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False)
    config_id = Column(ForeignKey('api_configuration.id'), nullable=False)
    error_message = Column(Text, nullable=False)

    # parent relationships (access parent)
    config : Mapped["ApiConfiguration"] = relationship(back_populates=("ApiErrorLogList"))

    # child relationships (access children)



class ApiLog(SAFRSBaseX, Base):
    """
    description: Keeps a log of all API interactions and their statuses.
    """
    __tablename__ = 'api_log'
    _s_collection_name = 'ApiLog'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False)
    config_id = Column(ForeignKey('api_configuration.id'))
    request_info = Column(Text)
    response_info = Column(Text)
    status = Column(String(50), nullable=False)

    # parent relationships (access parent)
    config : Mapped["ApiConfiguration"] = relationship(back_populates=("ApiLogList"))

    # child relationships (access children)



class ApiParameter(SAFRSBaseX, Base):
    """
    description: Stores parameters for making API requests.
    """
    __tablename__ = 'api_parameter'
    _s_collection_name = 'ApiParameter'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    config_id = Column(ForeignKey('api_configuration.id'), nullable=False)
    param_key = Column(String(100), nullable=False)
    param_value = Column(String(255))

    # parent relationships (access parent)
    config : Mapped["ApiConfiguration"] = relationship(back_populates=("ApiParameterList"))

    # child relationships (access children)



class ApiResponse(SAFRSBaseX, Base):
    """
    description: Stores raw JSON responses from API requests.
    """
    __tablename__ = 'api_response'
    _s_collection_name = 'ApiResponse'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    config_id = Column(ForeignKey('api_configuration.id'), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    raw_response = Column(Text, nullable=False)

    # parent relationships (access parent)
    config : Mapped["ApiConfiguration"] = relationship(back_populates=("ApiResponseList"))

    # child relationships (access children)
    ProcessedDatumList : Mapped[List["ProcessedDatum"]] = relationship(back_populates="response")



class ApiResponseCache(SAFRSBaseX, Base):
    """
    description: Cache for storing previously seen API responses to improve performance.
    """
    __tablename__ = 'api_response_cache'
    _s_collection_name = 'ApiResponseCache'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    config_id = Column(ForeignKey('api_configuration.id'), nullable=False)
    hashed_response = Column(String(255), nullable=False, unique=True)
    cached_data = Column(Text, nullable=False)

    # parent relationships (access parent)
    config : Mapped["ApiConfiguration"] = relationship(back_populates=("ApiResponseCacheList"))

    # child relationships (access children)



class ApiUsageStatistic(SAFRSBaseX, Base):
    """
    description: Maintains statistics about API usage for analytics.
    """
    __tablename__ = 'api_usage_statistics'
    _s_collection_name = 'ApiUsageStatistic'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.id'), nullable=False)
    config_id = Column(ForeignKey('api_configuration.id'), nullable=False)
    api_calls_made = Column(Integer, nullable=False)
    data_transformed = Column(Integer, nullable=False)

    # parent relationships (access parent)
    config : Mapped["ApiConfiguration"] = relationship(back_populates=("ApiUsageStatisticList"))
    user : Mapped["User"] = relationship(back_populates=("ApiUsageStatisticList"))

    # child relationships (access children)



class DataTransformationRule(SAFRSBaseX, Base):
    """
    description: Defines rules for transforming API responses.
    """
    __tablename__ = 'data_transformation_rule'
    _s_collection_name = 'DataTransformationRule'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    config_id = Column(ForeignKey('api_configuration.id'), nullable=False)
    rule_description = Column(Text, nullable=False)
    transformation_logic = Column(Text, nullable=False)

    # parent relationships (access parent)
    config : Mapped["ApiConfiguration"] = relationship(back_populates=("DataTransformationRuleList"))

    # child relationships (access children)



class UserApiConfiguration(SAFRSBaseX, Base):
    """
    description: Links users to specific API configurations they have access to.
    """
    __tablename__ = 'user_api_configuration'
    _s_collection_name = 'UserApiConfiguration'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.id'), nullable=False)
    config_id = Column(ForeignKey('api_configuration.id'), nullable=False)

    # parent relationships (access parent)
    config : Mapped["ApiConfiguration"] = relationship(back_populates=("UserApiConfigurationList"))
    user : Mapped["User"] = relationship(back_populates=("UserApiConfigurationList"))

    # child relationships (access children)



class ProcessedDatum(SAFRSBaseX, Base):
    """
    description: Stores data processed and transformed from raw API responses.
    """
    __tablename__ = 'processed_data'
    _s_collection_name = 'ProcessedDatum'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    response_id = Column(ForeignKey('api_response.id'), nullable=False)
    transformed_data = Column(Text, nullable=False)
    processed_timestamp = Column(DateTime, nullable=False)

    # parent relationships (access parent)
    response : Mapped["ApiResponse"] = relationship(back_populates=("ProcessedDatumList"))

    # child relationships (access children)
