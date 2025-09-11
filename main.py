from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
import db_model
from model import Product
from dbcon import LocalSession, engine
from sqlalchemy.orm import Session

myapp = FastAPI()
myapp.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
db_model.Base.metadata.create_all(bind=engine)


products = [
    Product(id=1, name="Laptop", description="new laptop", price=42000, quantity=10),
    Product(id=2, name="Phone", description="new Phone", price=10002.10, quantity=20),
    Product(id=8, name="Note", description="Galaxy Note", price=20890, quantity=8),
    Product(id=9, name="Speaker", description="JBL laptop", price=21000, quantity=2),
]


def db_init():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()


def db_create_schema(db: Session):
    count = db.query(db_model.Product).count()
    print("Count of table: ", count)
    if count == 0:
        for product in products:
            db.add(db_model.Product(**product.model_dump()))
        db.commit()
        print("New table created")


@myapp.get("/")
def greet(db: Session = Depends(db_init)):
    db_create_schema(db)
    return "Hello Mr. Sky, I have nothing here for you!"


# @myapp.get("/products/{id}")
# def get_product(id: int, db: Session = Depends(db_init)):
#     db_product = db.query(db_model.Product).filter(db_model.Product.id == id).first()
#     if db_product:
#         return db_product
#     return "Product not found"


from fastapi import Query


@myapp.get("/products")
def get_products(ids: str = Query(None), db: Session = Depends(db_init)):
    if ids:
        id_list = [int(id_str) for id_str in ids.split(",")]
        products = (
            db.query(db_model.Product).filter(db_model.Product.id.in_(id_list)).all()
        )
        if products:
            return products
        else:
            return {"message": "No products found for the given IDs"}
    else:
        return get_all_products(db)


# @myapp.get("/products") // single endlpoints handles All products or procducts with provided ids
def get_all_products(db: Session):
    all_products = db.query(db_model.Product).all()
    return all_products


@myapp.post("/products")
def add_product(product: Product, db: Session = Depends(db_init)):
    new_product = db.add(db_model.Product(**product.model_dump()))
    db.commit()
    return {"message": "Product added", "product": new_product}


@myapp.put("/products/{id}")
def update_product(id: int, new_product: Product, db: Session = Depends(db_init)):
    product_toUpdate = (
        db.query(db_model.Product).filter(db_model.Product.id == id).first()
    )
    if product_toUpdate:
        product_toUpdate.name = new_product.name
        product_toUpdate.description = new_product.description
        product_toUpdate.price = new_product.price
        product_toUpdate.quantity = new_product.quantity
        db.commit()
        return {"message": f"Product with id {id} updated"}
    else:
        return {"message": f"Product with id {id} NOT found"}


@myapp.delete("/products")
def delete_product(id: int, db: Session = Depends(db_init)):
    product_to_delete = db.query(db_model.Product).filter(db_model.Product.id == id)
    if product_to_delete:
        product_to_delete.delete()
        db.commit()
        return {"message": f"Product with id {id} deleted Successfully"}
    else:
        return {"message": f"Product with id {id} NOT found"}
