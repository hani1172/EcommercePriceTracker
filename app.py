from flask import Flask, render_template, request, redirect, url_for
from models import db, Product, PriceHistory
from scraper import scrape_product_data
from data_wrangling import process_scraped_data

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/track', methods=['POST'])
def track_product():
    url = request.form['url']
    product_data = scrape_product_data(url)
    if product_data:
        processed_data = process_scraped_data(product_data)
        product = Product(name=processed_data['name'], url=url)
        db.session.add(product)
        db.session.commit()

        price_history = PriceHistory(price=processed_data['price'], product_id=product.id)
        db.session.add(price_history)
        db.session.commit()

    return redirect(url_for('index'))

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get(product_id)
    price_history = PriceHistory.query.filter_by(product_id=product_id).all()
    return render_template('product.html', product=product, price_history=price_history)

if __name__ == '__main__':
    app.run(debug=True)
