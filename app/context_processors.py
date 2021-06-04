from app.blueprints.shop.models import Cart, Product
from flask_login import current_user, login_required
from flask import current_app as app, session
from functools import reduce

@app.context_processor
def build_cart():
    cart_dict = {}
    if current_user.is_authenticated:
        cart = Cart.query.filter_by(user_id=current_user.id).all()
        if len(cart) > 0:
            for i in cart:
                p = Product.query.get(i.product_id)
                if str(i.product_id) not in cart_dict:
                    cart_dict[str(p.id)] = {
                        'id': i.id,
                        'product_id': p.id,
                        'image': p.image,
                        'quantity': 1,
                        'name': p.name,
                        'description': p.description,
                        'price': f"{p.price:.2f}",
                        'tax': p.tax
                    }
                else:
                    cart_dict[str(p.id)]['quantity'] += 1
    
        return {
            'cart_dict': cart_dict, 
            'cart_size': len(cart), 
            'cart_subtotal': reduce(lambda x,y: x+y, [c.to_dict()['product']['price'] for c in cart]) if cart else 0, 
            'cart_tax': reduce(lambda x,y: x+y, [c.to_dict()['product']['tax'] for c in cart]) if cart else 0, 
            'cart_grandtotal': reduce(lambda x,y: x+y, [c.to_dict()['product']['price'] + c.to_dict()['product']['tax'] for c in cart]) if cart else 0
            }
    else:
        return {
        'cart_dict': cart_dict, 
        'cart_size': 0, 
        'cart_subtotal': 0, 
        'cart_tax': 0, 
        'cart_grandtotal': 0
        }


@app.context_processor
def get_stripe_keys():
    return {
        'STRIPE_PUBLISHABLE_KEY': app.config.get('STRIPE_PUBLISHABLE_KEY')
    }