import motor.motor_asyncio
from constants.external_servers import *
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration
import sentry_sdk
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine



# Connect to MongoDB
mongodb_client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)


# Configure Sentry SDK for error tracking
sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=[
        StarletteIntegration(),
        FastApiIntegration(),
    ],
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=1.0
)

# Configure SQLAlchemy for database access
sqlalchemy_engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args = { 'check_same_thread': False }
)

sqlalchemy_session = sessionmaker(
    autocommit = False,
    autoflush = False,
    bind = sqlalchemy_engine
)