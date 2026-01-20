import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import sys
import os

# Add root directory to sys.path to allow importing backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Create the Dash app
app = dash.Dash(
    __name__, 
    external_stylesheets=[dbc.themes.CYBORG], # Premium Dark Theme
    use_pages=True, 
    pages_folder="pages"
)
app.title = "PCBBR - Price Tracker"

# Navbar
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/", active="exact")),
        dbc.NavItem(dbc.NavLink("Catálogo", href="/catalog", active="exact")),
        dbc.NavItem(dbc.NavLink("Builds", href="/builds", active="exact")),
    ],
    brand="PCBBR 🇧🇷",
    brand_href="/",
    color="primary",
    dark=True,
)

# App Layout
app.layout = html.Div([
    navbar,
    dbc.Container([
        dcc.Store(id='build-state', storage_type='session', data={}), # Store for current build (Category -> Product Data)
    dash.page_container
    ], fluid=True, className="mt-4")
])

if __name__ == "__main__":
    app.run(debug=True, port=8050)
