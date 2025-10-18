# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

sites = spacex_df['Launch Site'].unique()
dropdownoptions = [{'label':site,'value':site}for site in sites]
dropdownoptions.insert(0,{'label':'All Site','value':'ALL'})

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                             options = dropdownoptions,
                                              value = 'ALL',
                                              placeholder ='Select a Launch Site here',
                                              searchable =True
                                             ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                            
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payloadslider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',100: '100',500:'500',1000:'1000',5000:'5000',10000:'10000'},
                                                value=[min_payload,max_payload]),


                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback( Output(component_id='success-pie-chart', component_property='figure'),
               Input(component_id='site-dropdown', component_property='value'))
# add callback decorator
def get_pie_chart(entered_site):
    
    if entered_site == 'ALL':
        filtered_df = spacex_df[['Launch Site','class']]
        filtered_df = filtered_df.groupby('Launch Site')['class'].sum().reset_index()
        fig = px.pie(filtered_df,values='class', names='Launch Site', 
        title='Success Launch for All Sites')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        result = filtered_df['class'].value_counts().reset_index()
        result.columns = ['class', 'count']
        fig = px.pie(result,values = 'count',names = 'class',title=f'{entered_site} Launch Outcome' )
        # return the outcomes piechart for a selected site
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'),
    Input(component_id="payloadslider", component_property="value")
    )

def payloadslider (entered_site,enter_payload):
    low,high = enter_payload
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & 
                            (spacex_df['Payload Mass (kg)'] <= high)]
    if entered_site == 'ALL':
        
        fig = px.scatter(filtered_df, y='class', 
        x='Payload Mass (kg)',
        color="Booster Version Category",
        title='relationship between payload and success for All Sites')
        return fig
    else:
        filtered_df = spacex_df[(spacex_df['Launch Site'] == entered_site)]
        fig = px.scatter(filtered_df,y='class', 
        x='Payload Mass (kg)',title=f'{entered_site} relationship between payload and success',color="Booster Version Category")
        # return the outcomes piechart for a selected site
    return fig





# Run the app
if __name__ == '__main__':
    app.run()
