import databases
import ormar
import sqlalchemy
from config.settings import DB_URL

# Создаем базовые объекты
database = databases.Database(DB_URL)
metadata = sqlalchemy.MetaData()

# Конфигурация ORMAR использует созданные объекты
ormar_base_config = ormar.OrmarConfig(
    database=database,  # Используем существующий объект
    metadata=metadata,  # Используем существующий объект
)
