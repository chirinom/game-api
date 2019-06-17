from marshmallow import Schema, fields


class GuessSchema(Schema):
    code = fields.List(fields.Str(), required=True)
    black_pegs = fields.Int()
    white_pegs = fields.Int()


class GameSchema(Schema):
    id = fields.Int()
    reference = fields.Str()
    num_colors = fields.Int(required=True)
    num_slots = fields.Int(required=True)
    max_guesses = fields.Int(missing=10)
    colors = fields.List(fields.Str())
    status = fields.Str()
    secret_code = fields.List(fields.Str())
    guesses = fields.List(fields.Nested(GuessSchema))
