# Es necesario importar Product para que SQLAlchemy
# conozca la existencia del modelo.
from retail_order_api.models.product import Product
from retail_order_api.db.database import Base, engine


def create_tables():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_tables()
    print("Tables created successfully")