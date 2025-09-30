from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from postgres.models import Base
import os

# Настройки подключения (лучше использовать environment variables в k8s)
DB_USER = os.getenv('POSTGRES_USER', 'postgres')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'password')
DB_HOST = os.getenv('POSTGRES_HOST', 'postgres-service')  # Имя сервиса в k8s
DB_PORT = os.getenv('POSTGRES_PORT', '5432')
DB_NAME = os.getenv('POSTGRES_DB', 'myapp')

# Формируем строку подключения
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Создаем движок SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Проверка соединения перед использованием
    echo=True  # Логирование SQL-запросов (отключить в продакшене)
)

Session = sessionmaker(engine, autoflush=True)


def init_db():
    """Функция для создания таблиц в базе данных"""
    try:
        Base.metadata.create_all(bind=engine)
        print("Таблицы успешно созданы")
    except Exception as e:
        print(f"Ошибка при создании таблиц: {e}")
        raise


def get_session():
    """Зависимость для получения сессии БД"""
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()


if __name__ == "__main__":
    # Инициализация БД при прямом запуске
    init_db()
