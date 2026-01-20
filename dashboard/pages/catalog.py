import dash
from dash import html, dcc, callback, Input, Output, State, ALL, ctx
import dash_bootstrap_components as dbc
import pandas as pd
from backend.services import catalog_service

dash.register_page(__name__)

def layout(category=None, mode=None, **kwargs):
    # Setup Stores
    initial_category = category
    initial_mode = mode
    
    return dbc.Container([
        html.H1("Catálogo de Produtos", className="my-4"),
        
        # State Stores
        dcc.Store(id="initial-category-store", data=initial_category),
        dcc.Store(id="catalog-mode-store", data=initial_mode),
        dcc.Store(id="catalog-products-store", data=[]), # Stores the current list of products for lookup
        dcc.Location(id="redirect-url", refresh=True),

        # Filters
        dbc.Row([
            dbc.Col([
                dbc.Input(id="catalog-search", placeholder="Buscar por nome...", type="text"),
            ], width=5),
            dbc.Col([
                dbc.Select(
                    id="category-filter",
                    options=[
                        {"label": "Todas as Categorias", "value": "ALL"},
                        {"label": "Processador", "value": "CPU"},
                        {"label": "Cooler", "value": "CPU Cooler"},
                        {"label": "Placa Mãe", "value": "Motherboard"},
                        {"label": "Memória", "value": "Memory"},
                        {"label": "Armazenamento", "value": "Storage"},
                        {"label": "Placa de Vídeo", "value": "Video Card"},
                        {"label": "Gabinete", "value": "Case"},
                        {"label": "Fonte", "value": "Power Supply"},
                        {"label": "Monitor", "value": "Monitor"},
                    ],
                    value=category if category else "ALL" 
                ),
            ], width=4),
            dbc.Col([
                 dbc.Select(
                    id="store-filter",
                    options=[
                        {"label": "Todas as Lojas", "value": "ALL"},
                        {"label": "Amazon", "value": "Amazon"},
                        {"label": "Kabum", "value": "Kabum"},
                        {"label": "Pichau", "value": "Pichau"},
                        {"label": "Terabyte", "value": "Terabyte"},
                    ],
                    value="ALL"
                ),
            ], width=3),
        ], className="mb-4"),

        # Table
        dbc.Spinner(html.Div(id="catalog-table-container"), color="primary")
    ])

def render_table_manually(df, mode):
    # Custom rendering to support Buttons
    header = html.Thead(html.Tr([
        html.Th("Img"),
        html.Th("Nome"),
        html.Th("Loja"),
        html.Th("Preço"),
        html.Th("Ação")
    ]))
    
    rows = []
    for idx, row in df.iterrows():
        product_id = row.get('id', idx) # Fallback to idx if id missing
        
        # Action Column
        if mode == 'select':
            action_btn = dbc.Button(
                "Selecionar", 
                id={'type': 'select-product-btn', 'index': idx}, 
                color="success", 
                size="sm"
            )
        else:
            action_btn =  dbc.Button(
                "Ver Loja", 
                href=row['url'], 
                target="_blank", 
                color="primary", 
                size="sm", 
                outline=True
            )

        rows.append(html.Tr([
            html.Td(html.Img(src=row.get('image_url', ''), height="40px")),
            html.Td(row['name']),
            html.Td(row['store']),
            html.Td(f"R$ {row['current_price']:,.2f}"),
            html.Td(action_btn),
        ]))
        
    return dbc.Table([header, html.Tbody(rows)], striped=True, bordered=True, hover=True, responsive=True)


@callback(
    [Output("catalog-table-container", "children"),
     Output("catalog-products-store", "data")],
    [Input("catalog-search", "value"),
     Input("store-filter", "value"),
     Input("category-filter", "value"),
     Input("catalog-mode-store", "data")]
)
def update_table(search_term, store, category, mode):
    store_val = None if store == "ALL" else store
    category_val = None if category == "ALL" else category
    
    results = catalog_service.search_catalog(query=search_term, store=store_val, category=category_val, limit=50)
    
    if not results:
        return dbc.Alert("Nenhum produto encontrado.", color="info"), []

    # Normalize data
    data = [r.dict() if hasattr(r, 'dict') else r for r in results]
    df = pd.DataFrame(data)
    
    table_component = render_table_manually(df, mode)
    
    return table_component, data

@callback(
    [Output("build-state", "data"),
     Output("redirect-url", "href")],
    Input({'type': 'select-product-btn', 'index': ALL}, 'n_clicks'),
    [State('build-state', 'data'),
     State('catalog-products-store', 'data')]
)
def handle_selection(n_clicks, current_build, products_data):
    if not any(n_clicks):
        return dash.no_update, dash.no_update
        
    triggered_id = ctx.triggered_id
    if not triggered_id:
        return dash.no_update, dash.no_update
        
    # Index in the products_data list
    selected_index = triggered_id['index']
    if selected_index >= len(products_data):
         return dash.no_update, dash.no_update
         
    selected_product = products_data[selected_index]
    category = selected_product.get('category')
    
    if not current_build:
        current_build = {}
        
    # Save selection
    # Structure: {'CPU': {product_data}, 'GPU': ...}
    current_build[category] = selected_product
    
    return current_build, "/builds"
