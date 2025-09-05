from fastapi import FastAPI
from model import Products

myapp=FastAPI()

@myapp.get("/")
def greet():
    return "Hello Mr. Sky."

products = [
    Products(id=1, name='Laptop', description='new laptop',price=42000, qty=10),
    Products(id=2, name='Phone', description='new Phone',price=10002.10, qty=20),
    Products(id=8, name='Note', description='Galaxy Note',price=20890, qty=8),
    Products(id=9, name='Speaker', description='JBL laptop',price=21000, qty=2)
    ]

@myapp.get('/products')
def get_all_products():
    return products

@myapp.get('/product/{id}')
def get_product(id: int):
    for product in products:
        if product.id == id:
            return product
    return 'Product not found'

@myapp.post('/product')
def add_product(product: Products):
    products.append(product)
    return product


@myapp.put('/product')
def update_product(id: int, new_product: Products):
    for index in range(len(products)):
        if products[index].id == id:
            products[index] = new_product
            return new_product
    return 'Product not found'


@myapp.delete('/product')
def delete_product(id: int):
    for index in range(len(products)):
        if products[index].id == id:
            return products.pop(index)
    return 'Product not found'


