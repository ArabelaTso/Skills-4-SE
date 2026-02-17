# Flask Example Application

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)


# Models
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    active = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'active': self.active
        }


# Routes
@app.route('/items', methods=['GET'])
def get_items():
    """Get all items."""
    items = Item.query.all()
    return jsonify([item.to_dict() for item in items])


@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """Get a specific item."""
    item = Item.query.get_or_404(item_id)
    return jsonify(item.to_dict())


@app.route('/items', methods=['POST'])
def create_item():
    """Create a new item."""
    data = request.json
    item = Item(
        name=data['name'],
        description=data.get('description'),
        price=data.get('price'),
        active=data.get('active', True)
    )
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201


@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    """Update an existing item."""
    item = Item.query.get_or_404(item_id)
    data = request.json

    item.name = data.get('name', item.name)
    item.description = data.get('description', item.description)
    item.price = data.get('price', item.price)
    item.active = data.get('active', item.active)

    db.session.commit()
    return jsonify(item.to_dict())


@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """Delete an item."""
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return '', 204


@app.route('/items/search', methods=['GET'])
def search_items():
    """Search items by name."""
    query = request.args.get('q', '')
    items = Item.query.filter(Item.name.contains(query)).all()
    return jsonify([item.to_dict() for item in items])


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
