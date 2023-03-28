import asyncio
import json

from flask import Flask, abort, request, render_template, redirect
from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import aliased

from database import db
from get_items import retrieve_rust_items
from marker_parser import get_info
from models import Shop, SellOrder, RustItem
from flask_migrate import Migrate


def update_items_db():
    items_json_file = retrieve_rust_items()
    with open(items_json_file) as f:
        try:
            items = json.load(f)

        except json.JSONDecodeError as e:
            print(f'Error loading {items_json_file}: {e}')

    update_mappings = []
    for record in items:
        if RustItem.query.filter_by(itemid=record['itemid']).first():
            update_mappings.append(record)
    db.session.bulk_update_mappings(RustItem, update_mappings)

    insert_mappings = []
    for record in items:
        if not RustItem.query.filter_by(itemid=record['itemid']).first():
            insert_mappings.append(record)
    try:
        db.session.bulk_insert_mappings(RustItem, insert_mappings)
        db.session.commit()
    except SQLAlchemyError:
        abort(500, message="An error occurred while inserting the shop.")


def update_shops_db():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    rust_markers = loop.run_until_complete(get_info.get_markers())
    shops = [marker for marker in rust_markers if marker.type == 3]

    db.session.query(Shop).delete()
    db.session.query(SellOrder).delete()
    db.session.commit()
    for s in shops:
        shop = Shop(id=s.id, name=s.name)
        try:
            db.session.merge(shop)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the shop.")

        new_orders = [SellOrder(
            item_id=order.item_id,
            quantity=order.quantity,
            currency_id=order.currency_id,

            cost_per_item=order.cost_per_item,
            item_is_blueprint=order.item_is_blueprint,
            currency_is_blueprint=order.currency_is_blueprint,
            amount_in_stock=order.amount_in_stock,
            shop_id=s.id
        ) for order in s.sell_orders]
        try:
            db.session.bulk_save_objects(new_orders)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting orders.")


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    db.init_app(app)
    migrate = Migrate(app, db)
    with app.app_context():
        db.create_all()

    @app.route('/update_shops')
    def update_shops():
        update_shops_db()
        return redirect('/')

    @app.route('/update_items')
    def update_items():
        update_items_db()
        return redirect('/')

    @app.route('/')
    def index():

        rust_items = db.session.query(RustItem).all()
        shops = db.session.query(Shop).all()
        sell_orders = db.session.query(SellOrder).all()
        rust_items_count = len(rust_items)
        shops_count = len(shops)
        sell_orders_count = len(sell_orders)
        return render_template('orders.html', rust_items_count=rust_items_count, shops_count=shops_count,
                               sell_orders_count=sell_orders_count)

    @app.route('/search')
    def search():

        item_name = request.args.get('item_name')
        currency_name = request.args.get('currency_name')
        query = db.session.query(SellOrder)
        if item_name:
            item_alias = aliased(RustItem)
            query = query.join(item_alias, SellOrder.item).filter(item_alias.name.contains(item_name))
        if currency_name:
            currency_alias = aliased(RustItem)
            query = query.join(currency_alias, SellOrder.currency).filter(currency_alias.name.contains(currency_name))
        query = query.order_by(desc(SellOrder.quantity / SellOrder.cost_per_item))
        results = query.all()
        return render_template('search_result.html', sell_orders=results, count=len(results))

    return app
