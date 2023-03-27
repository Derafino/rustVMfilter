from database import db


class SellOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('rust_item.itemid'))
    quantity = db.Column(db.Integer)
    currency_id = db.Column(db.Integer, db.ForeignKey('rust_item.itemid'))
    cost_per_item = db.Column(db.Integer)
    item_is_blueprint = db.Column(db.Boolean)
    currency_is_blueprint = db.Column(db.Boolean)
    amount_in_stock = db.Column(db.Integer)
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'))

    item = db.relationship('RustItem', foreign_keys=[item_id])
    currency = db.relationship('RustItem', foreign_keys=[currency_id])


class RustItem(db.Model):
    itemid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(200), nullable=False)


class Shop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    sell_orders = db.relationship('SellOrder', backref='shop', lazy='dynamic')
