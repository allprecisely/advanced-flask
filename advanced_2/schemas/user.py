from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    password = fields.Str()

    class Meta:
        load_only = ('password',)
        dump_only = ('id',)
