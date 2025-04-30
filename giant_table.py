from dash import Dash, dcc, html, dash_table, Input, Output
import pandas as pd

app = Dash(__name__)

# Simulate a DataFrame with column groups
df = pd.DataFrame({
    **{f"User_{i}": range(10) for i in range(5)},
    **{f"Usage_{i}": range(10) for i in range(5)},
    **{f"Perf_{i}": range(10) for i in range(5)},
})

column_groups = {
    'User Info': [col for col in df.columns if col.startswith("User_")],
    'Usage Metrics': [col for col in df.columns if col.startswith("Usage_")],
    'Performance Stats': [col for col in df.columns if col.startswith("Perf_")],
}

app.layout = html.Div([
    dcc.Tabs(
        id="column-group-tabs",
        value='User Info',
        children=[dcc.Tab(label=group, value=group) for group in column_groups]
    ),
    dash_table.DataTable(
        id='wide-table',
        data=[],
        columns=[],
        page_size=10,
        style_table={'overflowX': 'auto'},
        fixed_rows={'headers': True},
    )
])

@app.callback(
    Output('wide-table', 'columns'),
    Output('wide-table', 'data'),
    Input('column-group-tabs', 'value')
)
def update_columns(tab_name):
    cols = column_groups[tab_name]
    return [{"name": c, "id": c} for c in cols], df[cols].to_dict("records")

if __name__ == '__main__':
    app.run(debug=True)