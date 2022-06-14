from dash import Dash, html, dcc, Input, Output, State
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import matplotlib.pyplot as plt             # pip install matplotlib
import mpld3                                # pip install mpld3
from sqlalchemy import create_engine


SERVER='DESKTOP-J8OCEUG\SQLEXPRESS'
DATABASE= 'Sales'
DRIVER= 'SQL server Native client 11.0'
USERNAME= 'mildred'
PASSWORD= 'Mildred*7'
DATABASE_CONNECTION= f'mssql://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}?driver={DRIVER}'


engine = create_engine(DATABASE_CONNECTION)
connection=engine.connect()

df=pd.read_sql_query('select * from salestb', engine)
print(df)
print(df.columns)

#df = pd.read_csv("Sales3.csv")
#print(df)
df['year'] = pd.DatetimeIndex(df['order_date']).year
df = df.drop('order_date', axis=1)
print(df.shape)
print(df.columns)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dbc.Container([
    html.H1("Interactive sales dashboard",  style={'textAlign':'center'}),

    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='yeardropdown',
                value=2012,

                clearable=False,
                options=[{'label': x, 'value': x} for x in df.year.unique()])
        ], width=12),

    ]),
    dbc.Row([
        dbc.Col(
            dcc.Graph(
                id='line-plot',
                figure={},  # here is where we will put the graph we make
                ),

         width=6),
        dbc.Col(
            dcc.Graph(
                id='bar-plot',
                figure={},  # here is where we will put the graph we make
                ),

         width=6)
    ]),
    dbc.Row([
        dbc.Col(
            dcc.Graph(
                id='line-graph',
                figure={},  # here is where we will put the graph we make

            ),

         width=6),
        dbc.Col(
            dcc.Graph(
                id='pie-chart',
                figure={},  # here is where we will put the graph we make

            ),

         width=6)
    ]),

])


# Create interactivity between components and graph
@app.callback(
    Output(component_id='line-plot', component_property='figure'),
    Output(component_id='bar-plot', component_property='figure'),
    Output(component_id='line-graph', component_property='figure'),
    Output(component_id='pie-chart', component_property='figure'),
    Input(component_id='yeardropdown', component_property='value'),

)
def plot_data(selected_year):

    # filter data based on user selection
    dff = df[df.year == selected_year]
    dff['total_revenue'] = dff['total_revenue'].astype('float')
    dff['total_profit'] = dff['total_profit'].astype('float')
    print(df.dtypes)
    print(dff)
    print(dff.info())
    print(dff.columns)

    # build line plot
    import plotly.express as px
    # line_df = dff.groupby(['item_type'])[['total_revenue', 'total_profit']].sum
    # print(line_df)
    # fig_line = px.line(line_df, title="Item Type Vs Total Profit & Revenue")
    # fig_line.update_layout(title_font_color="#6D30FF")

    fig_line = px.line(dff, x="item_type", y='total_revenue', title='Life expectancy in Canada')


    #build bar plot
    # bar_df = dff.groupby(['item_type'])['total_revenue'].sum()
    # fig_bar = px.bar(bar_df, title="Item Type Vs Revenue")
    # fig_bar.update_layout(title_font_color="#6D30FF")
    fig_bar = px.bar(dff, x="item_type", y="total_revenue", title="Item Type Vs Revenue")

    # #build line graph
    # line2_df=dff.groupby(['region'])[['total_profit', 'total_revenue']].sum()
    # fig_line2 = px.line(line2_df, title="Region Vs Total Profit & Revenue", markers=True)
    # fig_line2.update_layout(title_font_color="#6D30FF")
    fig_line2 = px.line(dff, x="region", y="total_revenue")


    #build pie chart
    import plotly.graph_objects as go
    fig = px.pie(dff, title="Sales Channel",  values=dff.sales_channel.value_counts().values, names=dff.sales_channel.value_counts().index)
    fig.update_traces(hoverinfo='label+percent',  textinfo='value')
    fig.update_layout(title_font_color="#6D30FF")






    return fig_line,fig_bar, fig_line2, fig


if __name__ == '__main__':
    app.run_server(debug=True, port=8002)