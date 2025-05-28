# Install first: pip install dash-ag-grid

from dash import Dash
import dash_ag_grid as dag
import pandas as pd

# Sample data
df = pd.DataFrame({
    "size_mb": [71.2, 54.0, 503.3],
    "age_days": [730, 60, 365]
})

# Format display values while keeping raw data
grid_columns = [
    {
        "field": "size_mb",
        "headerName": "Size",
        "valueFormatter": {"function": "d3.format('.1f')(params.value) + ' MB'"},
        "sortable": True  # Sorts using raw numeric value
    },
    {
        "field": "age_days",
        "headerName": "Age",
        "valueFormatter": {"function": "Math.floor(params.value/365) + ' yrs'"},
        "sortable": True  # Sorts using raw days
    }
]

app = Dash()
app.layout = dag.AgGrid(
    rowData=df.to_dict("records"),
    columnDefs=grid_columns,
    dashGridOptions={"pagination": True}
)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
