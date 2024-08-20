import mongoengine as me
from person import Author, Player


class MsgSend(me.Document):
    id = me.IntField(required=True)
    game = me.StringField(required=True)
    platform = me.IntField(required=True)
    roomcode = me.StringField(required=True)
    timestamp = me.LongField(required=True)
    sign = me.StringField(required=True)
    version = me.StringField(required=True)


class MsgSendConn(MsgSend):
    mac = me.StringField(required=True)


class MsgSendData(MsgSend):
    payload = me.StringField(required=True)


class MsgReceive(me.Document):
    result = me.IntField(required=True)
    cmdtype = me.IntField(required=True)
    errormsg = me.StringField(required=True)
    payload = me.GenericReferenceField()


class MsgReceivePayload(me.Document):
    rest = me.StringField()


class Msg11001Payload(MsgReceivePayload):
    author = Author()


# L: Likes  C: Comment  G:Gift  F:FansClub
class MsgLCGFPayload(me.Document):
    author_id = me.StringField(required=True)
    type = me.StringField(required=True)
    msg_id = me.StringField(required=True)
    player = Player()
    timestamp = me.LongField(required=True)


class MsgLikesPayload(MsgLCGFPayload):
    like_num = me.IntField(required=True)


class MsgCommentPayload(MsgLCGFPayload):
    comment = me.StringField(required=True)


class MsgGiftPayload(MsgLCGFPayload):
    gift_no = me.StringField(required=True)
    gift_id = me.StringField(required=True)
    gift_num = me.IntField(required=True)
    gift_price = me.IntField(required=True)
    gift_total_price = me.IntField(required=True)


class MsgFansClubPayload(MsgLCGFPayload):
    fc_type = me.IntField(required=True)
    fc_level = me.IntField(required=True)






