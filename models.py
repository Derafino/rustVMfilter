from database import db


class SellOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    currency_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer)
    cost_per_item = db.Column(db.Integer)
    item_is_blueprint = db.Column(db.Boolean)
    currency_is_blueprint = db.Column(db.Boolean)
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'))


class Shop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    sell_orders = db.relationship('SellOrder', backref='shop', lazy='dynamic')
