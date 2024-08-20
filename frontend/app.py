from dash import Dash, html, dcc
import dash_mantine_components as dmc
from dash_iconify import DashIconify

from callbacks import register_callbacks

app = Dash(__name__)
app.config.suppress_callback_exceptions = True  # 忽略回调异常

app.layout = dmc.MantineProvider(
    html.Div([
        dcc.Location(id="url"),
        dmc.NotificationProvider(),
        html.Div(id="notifications-container"),

        dmc.Flex([
            html.Div([
                dmc.NavLink(label="Query", leftSection=DashIconify(icon="mdi:sql-query"),
                            rightSection=DashIconify(icon="tabler-chevron-right"),
                            href="/", active=True),
                dmc.NavLink(label="Upload", leftSection=DashIconify(icon="ant-design:cloud-upload-outlined"),
                            rightSection=DashIconify(icon="tabler-chevron-right"),
                            href="/upload", active=True),
            ], style={"width": "20%"}),
            html.Div(id='page-content', style={"width": "80%"},),
        ], gap={"base": "lg"}),
    ], style={'margin': '20px'},)
)

register_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True)
