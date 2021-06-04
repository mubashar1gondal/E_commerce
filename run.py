from app import create_app, db, cli
from app.models import Post
from app.blueprints.authentication.models import User, Post
from app.blueprints.shop.models import Cart, Product, Order

app = create_app()
cli.register(app)

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'Post': Post,
        'User': User,
        'Cart': Cart,
        'Product': Product,
        'Order': Order
    }