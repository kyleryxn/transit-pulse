import os
import time
import requests
from dotenv import load_dotenv
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output

load_dotenv()
API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000")

app = dash.Dash(__name__)
app.title = "NYC Transit Pulse"

app.layout = html.Div([
    html.H2("NYC Transit Pulse — Live Status"),
    html.Div(id="status-last-updated", style={"marginBottom":"8px"}),
    dash_table.DataTable(
        id="status-table",
        columns=[{"name":c, "id":c} for c in ["line","status","message","updated_at"]],
        style_cell={"textAlign":"left", "fontFamily":"sans-serif"},
        style_header={"fontWeight":"bold"},
        page_size=25
    ),
    html.Hr(),
    html.Div([
        html.Label("Line:"),
        dcc.Input(id="line-input", value="L", type="text", maxLength=2, style={"width":"60px", "marginRight":"10px"}),
        html.Button("Get Forecast", id="forecast-btn"),
        html.Span(id="forecast-output", style={"marginLeft":"12px", "fontWeight":"bold"})
    ]),
    dcc.Interval(id="poll", interval=15_000, n_intervals=0)
], style={"padding":"16px 24px"})

@app.callback(
    Output("status-table", "data"),
    Output("status-last-updated", "children"),
    Input("poll", "n_intervals")
)
def refresh_status(_):
    try:
        r = requests.get(f"{API_BASE}/status", timeout=4)
        data = r.json()
        ts = time.strftime("%Y-%m-%d %H:%M:%S")
        return data, f"Last refresh: {ts}"
    except Exception as e:
        return [], f"Failed to load: {e}"

@app.callback(
    Output("forecast-output", "children"),
    Input("forecast-btn", "n_clicks"),
    Input("line-input", "value")
)
def do_forecast(n, line):
    if not n:
        return ""
    try:
        r = requests.get(f"{API_BASE}/forecast", params={"line": line, "horizon_minutes": 15}, timeout=4)
        res = r.json()
        return f"{res['line']} — 15m delay risk: {res['risk']} ({res['prob_delay']:.0%})"
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=False)
