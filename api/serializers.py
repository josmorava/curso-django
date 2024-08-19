from marshmallow import Schema, fields, validate



class ProductSchema(Schema):
    """Esquema del Producto"""
    id = fields.Integer()
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    price = fields.Integer(required=True)
    available = fields.Boolean(required=True)
    date = fields.Date(required=True)

class UserSchema(Schema):
    """Esquema de inicio de Sesión"""
    username = fields.Str(required=True)
    password = fields.Str(required=True)