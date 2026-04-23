from app.database import engine
from sqlalchemy import text

with engine.connect() as connection:
    connection.execute(text("DROP SCHEMA public CASCADE;"))
    connection.execute(text("CREATE SCHEMA public;"))
    connection.execute(text("GRANT ALL ON SCHEMA public TO postgres;"))
    connection.execute(text("GRANT ALL ON SCHEMA public TO public;"))
    connection.commit()
    print("База данных очищена")