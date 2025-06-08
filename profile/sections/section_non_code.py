# profile/sections/section_non_code.py

from dash import html

def render(profile_data, main_language=None, language_type=None):
    return html.Div(
        [
            html.H4("Non-Code Repository", className="text-danger"),
            html.P(f"Language: {main_language or 'N/A'}"),
            html.P(f"Language Type: {language_type or 'N/A'}"),
        ],
        style={"padding": "10px", "border": "1px solid #ccc", "marginBottom": "20px"},
    )
