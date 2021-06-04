from flask import render_template, redirect, url_for, current_app as app, flash, request, session, jsonify
from flask_login.utils import login_required
from flask_migrate import current
from . import bp as shop
import stripe
from .models import Product, Cart, Order
from app.seed import seed_data
from flask_login import current_user
import json
from app import db


#print('stripe:', app.config.get('STRIPE_PUBLISHABLE_KEY'))

@shop.context_processor
def get_stripe_data():
    stripe.api_key = app.config.get('STRIPE_SECRET_KEY')
    return { 'stripe': stripe }

stripe.api_key = "sk_test_51IxhpTB4Zc5fMFvYks9440tRdZt7AYiaYzLzT5vTo2HiYbO7Rua4NW4045HoZI2pKmCD4AObVP3kFnO2uw4nwFXR00d6LyTuPu"

@shop.route('/')
def index():
    context = {
        'products': [p.to_dict() for p in Product.query.all()]
    }
    return render_template('shop/index.html', **context)

@shop.route('/seed')
def seed():
    seed_data()
    flash('Your product data has been seeded.', 'primary')
    return redirect(url_for('shop.index'))

@shop.route('/cart/add')
def add_to_cart():
    try:
        p = Product.query.get(request.args.get('product_id'))
        print(current_user.id)
        item = Cart(user_id=current_user.id, product_id=p.id)
        item.save()
        flash(f"{p.name} has been added successfully", 'success')
    except Exception as err:
        flash(f"There was an error adding the {p.name}", 'danger')
        print(err)
    return redirect(url_for('shop.index'))

@shop.route('/cart')
def cart():
    from app.context_processors import build_cart

    display_cart = build_cart()['cart_dict']
    
    session['session_display_cart'] = display_cart
    
    context = {
        'cart': display_cart.values()
    }
    return render_template('shop/cart.html', **context)

@shop.route('/checkout', methods=['POST'])
def checkout():
    dc = session.get('session_display_cart')
    l_items = []
    for product in dc.values():
        product_dict = {
            'price_data': {
                'currency': 'usd',
                'unit_amount': int(float(product['price'])) * 100,
                'product_data': {
                    'name': product['name'],
                    'images': [product['image']],
                },
            },
            'quantity': product['quantity'],
        }
        l_items.append(product_dict)
        
    
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=l_items,
            mode='payment',
            success_url=app.config.get('YOUR_DOMAIN') + '/shop/success',
            cancel_url=app.config.get('YOUR_DOMAIN') + '/shop/cancel',
        )
        
        for i in Cart.query.filter_by(user_id=current_user.id).all():
            db.session.delete(i)
        db.session.commit()
        print(l_items)
        return jsonify({'session_id': checkout_session.id})
    except Exception as e:
        return jsonify(error=str(e)), 403

@shop.route('/success')
def success():
    # [db.session.delete(c) for c in Cart.query.filter_by(user_id=current_user.id).all()]
    # db.session.commit()
    flash('All items remove from the cart successfully', 'info')
    return render_template('shop/checkout/success.html')
