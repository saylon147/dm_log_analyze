import base64
import re

from dash import html, dcc, Input, Output, no_update


def upload_page():
    return html.Div([
        html.Div(id="upload-notifications-container"),

        html.H1("Upload Page"),

        dcc.Upload(
            id='upload-file',
            children=html.Div(['Drag and Drop or ', html.A('Select Files')]),
            style={
                'width': '100%', 'height': '60px', 'lineHeight': '60px',
                'borderWidth': '1px', 'borderStyle': 'dashed',
                'borderRadius': '5px', 'textAlign': 'center'
            },
            multiple=False
        ),
    ])


def register_callbacks_upload(app):
    @app.callback(
        Output("upload-notifications-container", "children"),
        Input("upload-file", "contents"),
        prevent_init_call=True,
    )
    def upload_log(contents):
        if contents:
            # content是一个以 "data:text/plain;base64," 开头的字符串
            content_type, content_string = contents.split(',')
            # print(content_type)     # >> data:text/plain;base64

            # 解码 base64
            decoded = base64.b64decode(content_string).decode('utf-8')
            # print(type(decoded))    # >> <class 'str'>

            analyze_string_data(decoded)

            return no_update
        else:
            return no_update


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


