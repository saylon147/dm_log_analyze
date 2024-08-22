import hashlib
import json
import re

from flask import Blueprint, request, jsonify

from backend.models.msg import MsgSend, MsgReceive, Msg11001Payload, MsgCommentPayload, MsgLikesPayload, \
    MsgFansClubPayload, MsgGiftPayload
from backend.models.person import Author, Player

api = Blueprint('api', __name__)

rec_pattern = re.compile(r'Receive.*? --> (\d+) <-- ({.*})')
send_pattern = re.compile(r'Send.*? --> (\d+) <-- ({.*})')


@api.route('/upload_log', methods=['POST'])
def upload_log():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        contents = file.read().decode('utf-8')
        analyze_string_data(contents)
        return jsonify({"message": "Log uploaded and processed"}), 200


def generate_hash_for_log(log_line):
    return hashlib.sha256(log_line.encode('utf-8')).hexdigest()


def get_author(author_id):
    return Author.objects(userid=author_id).first()


def get_player(player_id):
    return Player.objects(userid=player_id).first()


def msg_rec_existed(log_hash):
    return MsgReceive.objects(hash=log_hash).first()


def msg_send_existed(log_hash):
    return MsgSend.objects(hash=log_hash).first()


def analyze_string_data(data):
    # 将解码后的内容按行分割
    lines = data.splitlines()

    for idx, line in enumerate(lines[:], start=1):
        if line.strip() != "":
            # print(f'processing line: {idx}')
            match = rec_pattern.search(line)
            if match:
                timestamp = match.group(1)
                json_str = match.group(2)
                json_data = json.loads(json_str)
                cmd_type = json_data.get("cmdType", -1)
                result = json_data.get("result", 9999)
                err_msg = json_data.get("errorMsg", "")
                payload = json_data.get("payload", {})
                if cmd_type == 0:
                    msg_id = payload.get("id", 0)
                    if msg_id == 11001:
                        log_hash = generate_hash_for_log(line)
                        if not msg_rec_existed(log_hash):
                            author_id = payload.get("authorInfo", {}).get("authorId", "")
                            author = get_author(author_id)
                            if not author:
                                author_name = payload.get("authorInfo", {}).get("authorName", "")
                                head_url = payload.get("authorInfo", {}).get("authorAvatar", "")
                                author = Author(
                                    userid=author_id, name=author_name, head_url=head_url
                                )
                                author.save()
                            msg_receive = MsgReceive(
                                hash=log_hash,
                                result=result,
                                cmdtype=cmd_type,
                                errormsg=err_msg,
                                payload=Msg11001Payload(
                                    author=author
                                ),
                                real_timestamp=int(timestamp)
                            )
                            msg_receive.save()
                elif cmd_type == 1:
                    if len(payload) > 1:
                        print(f"Multi items in payload:{len(payload)}")
                        continue
                    log_hash = generate_hash_for_log(line)
                    if not msg_rec_existed(log_hash):
                        for item in payload:
                            msg_type = item.get("msgType", "")
                            author_id = item.get("authorId", "")
                            msg_id = item.get("msgId", "")
                            player_id = item.get("userId", "")
                            player = get_player(player_id)
                            if not player:
                                player = Player(
                                    userid=player_id,
                                    name=item.get("userNick", ""),
                                    head_url=item.get("userAvatar", ""),
                                )
                                player.save()
                            ts = item.get("timestamp", 0)
                            if msg_type == "comment":
                                msg_receive = MsgReceive(
                                    hash=log_hash,
                                    result=result,
                                    cmdtype=cmd_type,
                                    errormsg=err_msg,
                                    payload=MsgCommentPayload(
                                        comment=item.get("comment", ""),
                                        author_id=author_id,
                                        type=msg_type,
                                        msg_id=msg_id,
                                        player=player,
                                        timestamp=ts
                                    ),
                                    real_timestamp=int(timestamp)
                                )
                                msg_receive.save()
                            elif msg_type == "like":
                                msg_receive = MsgReceive(
                                    hash=log_hash,
                                    result=result,
                                    cmdtype=cmd_type,
                                    errormsg=err_msg,
                                    payload=MsgLikesPayload(
                                        like_num=item.get("likeNum", 0),
                                        author_id=author_id,
                                        type=msg_type,
                                        msg_id=msg_id,
                                        player=player,
                                        timestamp=ts
                                    ),
                                    real_timestamp=int(timestamp)
                                )
                                msg_receive.save()
                            elif msg_type == "fansclub":
                                msg_receive = MsgReceive(
                                    hash=log_hash,
                                    result=result,
                                    cmdtype=cmd_type,
                                    errormsg=err_msg,
                                    payload=MsgFansClubPayload(
                                        fc_type=item.get("fansclubReasonType", 0),
                                        fc_level=item.get("fansclubLevel", 0),
                                        author_id=author_id,
                                        type=msg_type,
                                        msg_id=msg_id,
                                        player=player,
                                        timestamp=ts
                                    ),
                                    real_timestamp=int(timestamp)
                                )
                                msg_receive.save()
                            elif msg_type == "gift":
                                msg_receive = MsgReceive(
                                    hash=log_hash,
                                    result=result,
                                    cmdtype=cmd_type,
                                    errormsg=err_msg,
                                    payload=MsgGiftPayload(
                                        gift_no=item.get("giftNo", ""),
                                        gift_id=item.get("giftId", ""),
                                        gift_num=item.get("giftNum", 0),
                                        gift_price=item.get("giftUnitPrice", 0),
                                        gift_total_price=item.get("giftTotalPrice", 0),
                                        author_id=author_id,
                                        type=msg_type,
                                        msg_id=msg_id,
                                        player=player,
                                        timestamp=ts
                                    ),
                                    real_timestamp=int(timestamp)
                                )
                                msg_receive.save()
                continue

            match = send_pattern.search(line)
            if match:
                timestamp = match.group(1)
                json_str = match.group(2)
                json_data = json.loads(json_str)
                msg_id = json_data.get("id", 0)
                if msg_id == 12020 or msg_id == 12021:
                    log_hash = generate_hash_for_log(line)
                    if not msg_send_existed(log_hash):
                        msg_send = MsgSend(
                            hash=log_hash,
                            msg_id=msg_id,
                            game=json_data.get("game", ""),
                            platform=json_data.get("platform", 0),
                            roomcode=json_data.get("roomCode", ""),
                            timestamp=json_data.get("timestamp", 0),
                            version=json_data.get("version", ""),
                            real_timestamp=int(timestamp)
                        )
                        msg_send.save()
                continue

            # print(idx, "no match", line)
