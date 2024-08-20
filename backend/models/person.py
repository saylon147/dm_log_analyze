import mongoengine as me


class Person(me.Document):
    id = me.StringField(required=True, unique=True)
    name = me.StringField(required=True)
    head_url = me.StringField(required=True)


class Author(Person):
    is_author = me.BooleanField(default=True)


class Player(Person):
    is_author = me.BooleanField(default=False)
