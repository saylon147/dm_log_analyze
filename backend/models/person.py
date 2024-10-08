import mongoengine as me


class Person(me.Document):
    userid = me.StringField(required=True, unique=True)
    name = me.StringField(required=True)
    head_url = me.StringField(required=True)
    meta = {
        'allow_inheritance': True
    }


class Author(Person):
    is_author = me.BooleanField(default=True)


class Player(Person):
    is_author = me.BooleanField(default=False)
