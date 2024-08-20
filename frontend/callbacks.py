from dash import Output, Input, html
from pages.query import query_page, register_callbacks_query
from pages.upload import upload_page, register_callbacks_upload


def register_callbacks(app):
    @app.callback(
        Output("page-content", "children"),
        [Input("url", "pathname"),
         Input("url", "search"), ]
    )
    def render_page_content(pathname, search):
        if pathname == "/":
            return query_page()
        elif pathname == "/upload":
            return upload_page()
        else:
            return html.Div(
                [
                    html.H1("404: Not found", className="text-danger"),
                ],
                className="p-3 bg-light rounded-3",
            )

    register_callbacks_query(app)
    register_callbacks_upload(app)
