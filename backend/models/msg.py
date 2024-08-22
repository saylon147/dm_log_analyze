import mongoengine as me
from backend.models.person import Author, Player


# Send 消息主要记录主播发送 START_BATTLE = 12020 和 END_BATTLE = 12021
class MsgSend(me.Document):
    hash = me.StringField(required=True, unique=True)
    id = me.IntField(required=True)
    game = me.StringField(required=True)
    platform = me.IntField(required=True)
    roomcode = me.StringField(required=True)
    timestamp = me.LongField(required=True)
    version = me.StringField(required=True)
    # 客户端的时间戳
    real_timestamp = me.LongField(required=True)


# Receive 消息主要记录 START_CONNECT = 11001（获取主播信息） ；直播间互动（点赞 评论 礼物 粉丝俱乐部）
class MsgReceive(me.Document):
    hash = me.StringField(required=True, unique=True)
    result = me.IntField(required=True)
    cmdtype = me.IntField(required=True)
    errormsg = me.StringField(required=True)
    payload = me.GenericReferenceField()
    # 客户端的时间戳
    real_timestamp = me.LongField(required=True)


class Msg11001Payload(me.Document):
    author = me.ReferenceField(Author)


# L: Likes  C: Comment  G:Gift  F:FansClub
class MsgLCGFPayload(me.Document):
    author_id = me.StringField(required=True)
    type = me.StringField(required=True)
    msg_id = me.StringField(required=True)
    player = me.ReferenceField(Player)
    timestamp = me.LongField(required=True)
    meta = {
        'allow_inheritance': True
    }


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






