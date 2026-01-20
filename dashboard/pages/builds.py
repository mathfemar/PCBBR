import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd

dash.register_page(__name__)

# Categories to display (Ordered as in PCPartPicker)
BUILD_CATEGORIES = [
    {"id": "CPU", "label": "Processador"},
    {"id": "CPU Cooler", "label": "Cooler do Processador"},
    {"id": "Motherboard", "label": "Placa Mãe"},
    {"id": "Memory", "label": "Memória"},
    {"id": "Storage", "label": "Armazenamento"},
    {"id": "Video Card", "label": "Placa de Vídeo"},
    {"id": "Case", "label": "Gabinete"},
    {"id": "Power Supply", "label": "Fonte"},
    {"id": "Monitor", "label": "Monitor"},
]

def render_build_row(category, selected_product=None):
    """
    Renders a single row for the build table.
    """
    if selected_product:
        # Show selected product details
        selection_content = html.Div([
            html.Img(src=selected_product.get('image', ''), height="50px", className="me-2") if selected_product.get('image') else None,
            html.A(selected_product['name'], href=selected_product['url'], target="_blank", className="text-decoration-none fw-bold"),
            # Remove button could go here
        ], className="d-flex align-items-center")
        
        price = f"R$ {selected_product['current_price']:,.2f}"
        store = selected_product['store']
    else:
        # Show "Choose" button
        selection_content = dbc.Button(
            [html.I(className="bi bi-plus-lg me-2"), f"Escolher {category['label']}"],
            color="primary",
            size="sm",
            href=f"/catalog?category={category['id']}&mode=select", # Pre-filter link with Select Mode
            className="text-nowrap"
        )
        price = "-"
        store = "-"

    return html.Tr([
        # Component Label
        html.Td(html.B(category["label"]), className="align-middle"),
        
        # Selection Area
        html.Td(selection_content, className="align-middle"),
        
        # Placeholders / Details
        html.Td("-", className="text-center align-middle text-muted"), # Base
        html.Td("-", className="text-center align-middle text-muted"), # Promo
        html.Td("-", className="text-center align-middle text-muted"), # Shipping
        html.Td("-", className="text-center align-middle text-muted"), # Tax
        html.Td("-", className="text-center align-middle text-muted"), # Availability
        html.Td(price, className="text-center align-middle"), # Price
        html.Td(store, className="text-center align-middle"), # Where
    ])

layout = dbc.Container([
    html.H2("Montagem de PC", className="my-4 display-5"),
    
    # Header Info
    dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.H5("Estimativa de Consumo", className="text-muted"),
                    html.H3("0W", className="text-primary") # Placeholder
                ], width=6),
                dbc.Col([
                    html.H5("Preço Total", className="text-muted"),
                    html.H3(id="build-total-price", children="R$ 0,00", className="text-success")
                ], width=6, className="text-end"),
            ])
        ])
    ], className="mb-4 bg-light bg-opacity-10 border-0"),

    # Main Build Table
    dbc.Table([
        html.Thead([
            html.Tr([
                html.Th("Componente"),
                html.Th("Seleção"),
                html.Th("Base", className="text-center"),
                html.Th("Promo", className="text-center"),
                html.Th("Frete", className="text-center"),
                html.Th("Taxa", className="text-center"),
                html.Th("Disp.", className="text-center"),
                html.Th("Preço", className="text-center"),
                html.Th("Loja", className="text-center"),
            ])
        ]),
        html.Tbody(id="build-table-body")
    ], bordered=True, hover=True, responsive=True, striped=True, className="align-middle"),

    html.Div(className="mb-5")
])

@callback(
    [Output("build-table-body", "children"),
     Output("build-total-price", "children")],
    Input("build-state", "data")
)
def update_build_table(build_data):
    if build_data is None:
        build_data = {}
        
    rows = []
    total_price = 0.0
    
    for category in BUILD_CATEGORIES:
        cat_id = category["id"]
        selected_product = build_data.get(cat_id)
        
        rows.append(render_build_row(category, selected_product))
        
        if selected_product:
            total_price += selected_product.get('current_price', 0)
            
    return rows, f"R$ {total_price:,.2f}"
