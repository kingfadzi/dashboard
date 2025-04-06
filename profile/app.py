from dash import Dash, html
import dash_bootstrap_components as dbc

# Import sample data and helpers
from data_sample import profile_data, dependencies
import helpers

# Import sections
import sections.section_kpis as section_kpis
import sections.section_tech_stack as section_tech_stack
import sections.section_modernization as section_modernization
import sections.section_code_quality as section_code_quality
import sections.section_dependencies as section_dependencies
# (more sections later)
from sections.section_dependencies_category as dependencies_category



# Initialize Dash app

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

# App Layout
app.layout = html.Div([
    html.H2(f"{profile_data['Repo ID']} Repository Profile", style={"marginBottom": "30px"}),

    section_kpis.render(profile_data),
    section_tech_stack.render(profile_data),
    section_modernization.render(profile_data),
    section_code_quality.render(profile_data),
    section_dependencies.render(profile_data),
    dependencies_category.render(profile_data),
    # (later you will add more sections here like dependency health, security, etc.)
], style={"padding": "20px"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)