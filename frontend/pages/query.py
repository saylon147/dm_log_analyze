from time import sleep

import requests
from dash import html, Output, Input, no_update, clientside_callback
import dash_mantine_components as dmc


API_URL = "http://localhost:5000/api"


def get_cell(url, name, userid):
    return dmc.Flex([
        dmc.Avatar(src=url, radius=10, size=100, ),
        dmc.Stack([
            dmc.Text(name),
            dmc.Text(userid),
        ], align="flex-start")
    ], direction="row")


def query_page():
    return html.Div([

        html.H1("Query Page"),
        dmc.Button("All Authors", id="query-author-btn"),
        dmc.Grid(
            children=[
                dmc.GridCol(get_cell("https://p11.douyinpic.com/aweme/720x720/aweme-avatar/tos-cn-i"
                                     "-0813c001_oYEgc9ClnJk70e9cRaAnQgAACiAbAH1AvIAeDO.jpeg?from=3067671334",
                                     "NAME", "ID"),
                            span=6),
                dmc.GridCol(get_cell("https://p11.douyinpic.com/aweme/100x100/aweme-avatar/tos-cn-i"
                            "-0813c001_oEEoIAAA9l1qAxDmnFCAfFRPfW8AMEAgNLJYC9.jpeg?from=3067671334",
                                     "NAME", "ID"),
                            span=6),
                dmc.GridCol(get_cell("https://p3.douyinpic.com/aweme/100x100/aweme-avatar/tos-cn-i"
                            "-0813_oQAoAehBGCFaLALDfGIvXSIFjIMQqeMAVe27iA.jpeg?from=3067671334",
                                     "NAME", "ID"),
                            span=6),
            ],
            gutter="xl", id="person-grid-view"
        ),

    ])


clientside_callback(
    """
    function updateLoadingState(n_clicks) {
        return true
    }
    """,
    Output("query-author-btn", "loading", allow_duplicate=True),
    Input("query-author-btn", "n_clicks"),
    prevent_initial_call=True,
)


def register_callbacks_query(app):
    @app.callback(
        Output("person-grid-view", "children"),
        Output("query-author-btn", "loading"),
        Input("query-author-btn", "n_clicks"),
        prevent_init_call=True,
    )
    def query_author(n_clicks):
        if n_clicks:
            # 发送 GET 请求到 /authors 路由
            response = requests.get(f"{API_URL}/authors")

            # 检查响应状态码
            if response.status_code == 200:
                # 成功响应，解析 JSON 数据
                authors = response.json()
                print("Authors:", authors)
            else:
                # 请求失败，打印错误信息
                print(f"Failed to fetch authors. Status code: {response.status_code}")

        return no_update, False
