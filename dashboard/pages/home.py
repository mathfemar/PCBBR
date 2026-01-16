import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from datetime import datetime

# Import Backend Services
from backend.services.scrapers import amazon, kabum, pichau, terabyte
from backend.services.product_service import save_product_history
from backend.database import engine
from backend.models import PriceHistory
from sqlmodel import Session, select

dash.register_page(__name__, path='/')

layout = dbc.Container([
    # Hero Section
    dbc.Row([
        dbc.Col([
            html.H1("Verificador de Preços 🔎", className="display-3"),
            html.P("Monitore o histórico de preços da Kabum, Pichau, Terabyte e Amazon.", className="lead"),
        ], width=12, className="text-center my-5")
    ]),

    # Search Bar
    dbc.Row([
        dbc.Col([
            dbc.InputGroup([
                dbc.Input(id="url-input", placeholder="Cole a URL do produto aqui...", type="text"),
                dbc.Button("Verificar Agora", id="search-btn", color="primary", n_clicks=0),
            ], size="lg"),
        ], width=8, className="mx-auto")
    ]),

    html.Hr(className="my-5"),

    # Results Section
    dbc.Spinner(
        html.Div(id="result-container"),
        color="primary",
        type="grow",
    )
])

@callback(
    Output("result-container", "children"),
    Input("search-btn", "n_clicks"),
    State("url-input", "value"),
    prevent_initial_call=True
)
def search_product(n_clicks, url):
    if not url:
        return dbc.Alert("Por favor, insira uma URL válida.", color="warning")

    # 1. Identify Store & Scrape
    try:
        if "amazon.com.br" in url:
            result = amazon.fetch_product(url)
        elif "kabum.com.br" in url:
            result = kabum.fetch_product(url)
        elif "pichau.com.br" in url:
            result = pichau.fetch_product(url)
        elif "terabyteshop.com.br" in url:
            result = terabyte.fetch_product(url)
        else:
            return dbc.Alert("Loja não suportada ou URL inválida.", color="danger")
        
        if result.get("error"):
            return dbc.Alert(f"Erro ao buscar produto: {result['error']}", color="danger")

        # 2. Save to DB
        product = save_product_history(result)
        
        if not product:
             return dbc.Alert("Erro crítico ao salvar no banco de dados.", color="danger")

        # 3. Create Chart
        # Fetch history
        with Session(engine) as session:
            histories = session.exec(select(PriceHistory).where(PriceHistory.product_id == product.id).order_by(PriceHistory.timestamp)).all()
            
            data = [{
                "Data": h.timestamp, 
                "Preço (R$)": h.price
            } for h in histories]
            
            df = pd.DataFrame(data)
            
            fig = px.line(df, x="Data", y="Preço (R$)", title=f"Histórico de Preços: {product.name}", markers=True)
            fig.update_layout(template="plotly_dark")

        # 4. Return Layout
        return dbc.Card([
            dbc.CardHeader(product.store),
            dbc.CardBody([
                html.H4(product.name, className="card-title"),
                html.H2(f"R$ {product.current_price:,.2f}", className="text-success"),
                html.P(f"Última atualização: {product.last_updated.strftime('%d/%m/%Y %H:%M')}", className="card-text"),
                dcc.Graph(figure=fig),
                dbc.Button("Ir para a Loja", href=product.url, external_link=True, color="secondary")
            ])
        ])

    except Exception as e:
        return dbc.Alert(f"Erro desconhecido: {str(e)}", color="danger")
