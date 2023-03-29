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

    def __repr__(self):
        return f'<SellOrder id={self.id}, ' \
               f'item_id={self.item_id},' \
               f'quantity={self.quantity},' \
               f'currency_id={self.currency_id},' \
               f'cost_per_item={self.cost_per_item},' \
               f'item_is_blueprint={self.item_is_blueprint},' \
               f'currency_is_blueprint={self.currency_is_blueprint},' \
               f'amount_in_stock={self.amount_in_stock},' \
               f'shop_id={self.shop_id},' \
               f'item={self.item},' \
               f'currency={self.currency}>'


class RustItem(db.Model):
    itemid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(200), nullable=False)


class Shop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    sell_orders = db.relationship('SellOrder', backref='shop', lazy='dynamic')
