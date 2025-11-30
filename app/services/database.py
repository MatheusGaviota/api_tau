from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

engine_args = {
    "pool_pre_ping": True,
    "pool_recycle": 300,
    "pool_size": 10,
    "max_overflow": 20,
    "connect_args": {}
}

if DATABASE_URL.startswith("postgresql"):
    engine_args["connect_args"] = {
        "connect_timeout": 10
    }

engine = create_engine(DATABASE_URL, **engine_args)

@event.listens_for(engine, "connect")
def receive_connect(dbapi_conn, connection_record):
    connection_record.info['pid'] = os.getpid()

@event.listens_for(engine, "checkout")
def receive_checkout(dbapi_conn, connection_record, connection_proxy):
    pid = os.getpid()
    if connection_record.info['pid'] != pid:
        connection_record.dbapi_connection = connection_proxy.dbapi_connection = None
        raise Exception("Connection record belongs to pid %s, attempting to check out in pid %s" % (connection_record.info['pid'], pid))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
