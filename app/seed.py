import stripe
from flask import current_app as app
from app.blueprints.shop.models import Product
from app import db

stripe.api_key = "sk_test_51IxhpTB4Zc5fMFvYks9440tRdZt7AYiaYzLzT5vTo2HiYbO7Rua4NW4045HoZI2pKmCD4AObVP3kFnO2uw4nwFXR00d6LyTuPu"


def seed_data():

    [db.session.delete(p) for p in Product.query.all()]

    try:
        for i in stripe.Product.list():
            data={
                'name': i['name'],
                'description': i['description'],
                'image': i['images'][0],
                'price': round(float(i['metadata']['price']), 2)
            }
            p = Product()
            p.from_dict(data)
            p.save()
    except Exception as err:
        print('There was an error')
        print('=' *40)

