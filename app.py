import asyncio
import json

from flask import Flask, abort, request, render_template
from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError

from database import db
from marker_parser import get_info
from models import Shop, SellOrder


def complete_shops_info(shops):
    with open("items.json", "r") as input_file:
        items = json.load(input_file)
    shops_with_item_names = list()
    for shop in shops:
        orders = list()
        for sell_order in shop.sell_orders:
            sell_item = ''
            currency = ''
            for item in items:
                if item['item_id'] == sell_order.item_id:
                    sell_item = item['name']
                if item['item_id'] == sell_order.currency_id:
                    currency = item['name']
                if sell_item and currency:
                    orders.append({
                        'item_name': sell_item,
                        'currency_name': currency,
                        'quantity': sell_order.quantity,
                        'cost_per_item': sell_order.cost_per_item,
                        'item_is_blueprint': sell_order.item_is_blueprint,
                        'currency_is_blueprint': sell_order.currency_is_blueprint,
                        'shop_id': shop.id})
                    break
        shops_with_item_names.append({'id': shop.id, 'name': shop.name, 'sell_orders': orders})

    return shops_with_item_names


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    db.init_app(app)
    with app.app_context():
        db.create_all()

    @app.route('/update_shops')
    def update_shops():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        rust_markers = loop.run_until_complete(get_info.get_markers())
        shops = [marker for marker in rust_markers if marker.type == 3]
        shops = complete_shops_info([shop for shop in shops if shop.sell_orders])
        db.session.query(SellOrder).delete()
        db.session.commit()
        for s in shops:
            shop = Shop(id=s['id'], name=s['name'])
            try:
                db.session.merge(shop)
                db.session.commit()
            except SQLAlchemyError:
                abort(500, message="An error occurred while inserting the shop.")

            new_orders = [SellOrder(**order) for order in s['sell_orders']]
            try:
                db.session.bulk_save_objects(new_orders)
                db.session.commit()
            except SQLAlchemyError:
                abort(500, message="An error occurred while inserting orders.")
        return 'Updated'

    @app.route('/')
    def index():
        return render_template('orders.html')

    @app.route('/search')
    def search():

        item_name = request.args.get('item_name')
        currency_name = request.args.get('currency_name')
        query = db.session.query(SellOrder)
        if item_name:
            query = query.filter(SellOrder.item_name.contains(item_name))
        if currency_name:
            query = query.filter(SellOrder.currency_name.contains(currency_name))
        query = query.order_by(desc(SellOrder.quantity / SellOrder.cost_per_item))
        results = query.all()
        results = [SellOrder.query.filter_by(id=r.id).first() for r in results]
        return render_template('search_result.html', sell_orders=results, count=len(results))

    return app
