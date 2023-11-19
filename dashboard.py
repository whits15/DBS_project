# data set from https://datacatalog.urban.org/dataset/estimated-low-income-jobs-lost-covid-19/resource/cd4ef086-7401-4b63-9424-7881aa2be22d
import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  





app = Dash(__name__)
server = app.server


fips_to_abbreviation = {
    '01': 'AL', '02': 'AK', '04': 'AZ', '05': 'AR', '06': 'CA',
    '08': 'CO', '09': 'CT', '10': 'DE', '11': 'DC', '12': 'FL',
    '13': 'GA', '15': 'HI', '16': 'ID', '17': 'IL', '18': 'IN',
    '19': 'IA', '20': 'KS', '21': 'KY', '22': 'LA', '23': 'ME',
    '24': 'MD', '25': 'MA', '26': 'MI', '27': 'MN', '28': 'MS',
    '29': 'MO', '30': 'MT', '31': 'NE', '32': 'NV', '33': 'NH',
    '34': 'NJ', '35': 'NM', '36': 'NY', '37': 'NC', '38': 'ND',
    '39': 'OH', '40': 'OK', '41': 'OR', '42': 'PA', '44': 'RI',
    '45': 'SC', '46': 'SD', '47': 'TN', '48': 'TX', '49': 'UT',
    '50': 'VT', '51': 'VA', '53': 'WA', '54': 'WV', '55': 'WI',
    '56': 'WY'
}

code_to_sector = {
    "X01": "Agriculture, Forestry, Fishing, and Hunting",
    "X02": "Mining, Quarrying, and Oil and Gas Extraction",
    "X03": "Utilities",
    "X04": "Construction",
    "X05": "Manufacturing",
    "X06": "Wholesale Trade",
    "X07": "Retail Trade",
    "X08": "Transportation and Warehousing",
    "X09": "Information",
    "X10": "Finance and Insurance",
    "X11": "Real Estate and Rental and Leasing",
    "X12": "Professional, Scientific, and Technical Services",
    "X13": "Management of Companies and Enterprises",
    "X14": "Administrative and Support and Waste Management and Remediation Services",
    "X15": "Educational Services",
    "X16": "Health Care and Social Assistance",
    "X17": "Arts, Entertainment, and Recreation",
    "X18": "Accommodation and Food Services",
    "X19": "Other Services (except Public Administration)",
    "X20": "Public Administration",
    "worker_job_loss_rate": "Total Job Loss Index"
}



stats = pd.read_csv('job_stats.csv')
stats = stats.groupby(['state_fips','state_name','state_abbr','X01','X02','X03','X04','X05','X06','X07','X08','X09','X10','X11','X12','X13','X14','X15','X16','X17','X18','X19','X20','X000'])[['worker_job_loss_rate']].mean()
stats.reset_index(inplace=True)
print(stats[:5])

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Job Loss Due to AI by Industry in USA", className='header', style={'text-align': 'center'}),
    html.H2("By: Keegan Whitney and Jessica Conrod", className='header', style={'text-align': 'center'}),
    dcc.Dropdown(id="slct_sector",
                 options=[
                     {"label": "Agriculture, Forestry, Fishing, and Hunting", "value": "X01"},
                     {"label": "Mining, Quarrying, and Oil and Gas Extraction", "value": "X02"},
                     {"label": "Utilities", "value": "X03"},
                     {"label": "Construction", "value": "X04"},
                     {"label": "Manufacturing", "value": "X05"},
                     {"label": "Wholesale Trade", "value": "X06"},
                     {"label": "Retail Trade", "value": "X07"},
                     {"label": "Transportation and Warehousing", "value": "X08"},
                     {"label": "Information", "value": "X09"},
                     {"label": "Finance and Insurance", "value": "X10"},
                     {"label": "Real Estate and Rental and Leasing", "value": "X11"},
                     {"label": "Professional, Scientific, and Technical Services", "value": "X12"},
                     {"label": "Management of Companies and Enterprises", "value": "X13"},
                     {"label": "Administrative and Support and Waste Management and Remediation Services", "value": "X14"},
                     {"label": "Educational Services", "value": "X15"},
                     {"label": "Health Care and Social Assistance", "value": "X16"},
                     {"label": "Arts, Entertainment, and Recreation", "value": "X17"},
                     {"label": "Accommodation and Food Services", "value": "X18"},
                     {"label": "Other Services (except Public Administration)", "value": "X19"},
                     {"label": "Public Administration", "value": "X20"},
                     {"label": "Total Job Loss Index", "value": "worker_job_loss_rate"}],
                 multi=False,
                 value="X01",
                 className='dropdown',
                 style={'width': "60%; color: #000000"}
                 ),
    
    html.Div(id='output_container',className='output-container', children=[] ),
    html.Hr(),

    dcc.Graph(id='job_loss_map',className='graph-container', figure={} ),
    html.Hr()
])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='job_loss_map', component_property='figure')],
    [Input(component_id='slct_sector', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = ""
    print("the option selected is: ")
    print(option_slctd)
    dff = stats.copy()
    dff['custom_hover'] = dff['state_name'] + ': ' + dff[option_slctd].astype(str) + '%'

    print(dff[:5])
    # Plotly Express Choropleth
    fig = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='state_abbr',
        color=option_slctd,
        hover_name='custom_hover',
        hover_data= {'state_name':False, 'state_abbr':False, 'custom_hover':False, option_slctd:False},
        color_continuous_scale=px.colors.sequential.YlOrRd,
        scope="usa",
        labels={'worker_job_loss_rate': '% of jobs lost'},
        template='none'
    )

    fig.update_layout(
    paper_bgcolor='#FFF',  
    plot_bgcolor='#FFF',   
    title_text="Heat Map of Job Gain or Lost in: {} Sector(s) ".format(code_to_sector[option_slctd]),
    title_xanchor="center",
    title_font=dict(size=24),
    title_x=0.5,
    geo=dict(scope='usa'),
)

    return container, fig



# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
