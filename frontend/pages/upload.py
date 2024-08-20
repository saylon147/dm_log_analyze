import base64
import requests
from dash import html, dcc, Input, Output, State, no_update

API_URL = "http://localhost:5000/api"


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
        State('upload-file', 'filename'),
        prevent_init_call=True,
    )
    def upload_log(contents, filename):
        if contents:
            # content是一个以 "data:text/plain;base64," 开头的字符串
            content_type, content_string = contents.split(',')
            # print(content_type)     # >> data:text/plain;base64

            # 解码 base64
            decoded = base64.b64decode(content_string).decode('utf-8')
            # print(type(decoded))    # >> <class 'str'>

            # 将文件内容通过POST请求发送到服务器
            try:
                response = requests.post(
                    API_URL + '/upload_log',
                    files={'file': (filename, decoded)}
                )
                if response.status_code == 200:
                    return "Log uploaded successfully."
                else:
                    return f"Failed to upload log: {response.text}"
            except Exception as e:
                return f"An error occurred: {str(e)}"
        return no_update





