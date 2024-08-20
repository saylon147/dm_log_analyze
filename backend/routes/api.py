import re

from flask import Blueprint, request, jsonify

api = Blueprint('api', __name__)


@api.route('/upload_log', methods=['POST'])
def upload_log():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        contents = file.read().decode('utf-8')
        lines = contents.splitlines()

        print(len(lines))
        print(lines[0])

        return jsonify({"message": "Log uploaded and processed"}), 200


def analyze_string_data(data):
    rec_pattern = re.compile(r'Receive.*? --> (\d+) <-- ({.*})')
    send_pattern = re.compile(r'Send.*? --> (\d+) <-- ({.*})')

    # 将解码后的内容按行分割
    lines = data.splitlines()

    for idx, line in enumerate(lines[:30], start=1):
        if line.strip() != "":
            match = rec_pattern.search(line)
            if match:
                timestamp = match.group(1)
                json_str = match.group(2)
                print(idx, "Receive", timestamp, json_str)
                continue
            match = send_pattern.search(line)
            if match:
                timestamp = match.group(1)
                json_str = match.group(2)
                print(idx, "Send", timestamp, json_str)
                continue
            print(idx, "no match", line)
