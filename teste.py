import os, sqlalchemy as sa
from dotenv import load_dotenv
load_dotenv()
engine = sa.create_engine(os.getenv("DATABASE_URL"), pool_pre_ping=True)
with engine.connect() as c:
    print(c.execute(sa.text("select version()")).scalar())
