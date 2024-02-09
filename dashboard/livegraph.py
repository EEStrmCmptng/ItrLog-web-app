import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import random
 
app = dash.Dash(__name__)

# Function to read data from file
def read_data_from_file():
    #return random.randint(0, 100)
    return [random.randint(1, 99), random.randint(2, 100)]

# Layout of the application
app.layout = html.Div([
    dcc.Graph(id='live-update-graph'),
    dcc.Interval(
        id='interval-component',
        interval=1*1000,  # in milliseconds
        n_intervals=0
    )
])

# Initial x-axis value
x_values = [0]
y_values = [0]
y_values2 = [0]
# Callback to update the graph every second
@app.callback(
    Output('live-update-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_graph(n):
    # Read data from file
    y = read_data_from_file()
    
    # Update x-axis
    x_values.append(x_values[-1] + 1)
    y_values.append(y[0])
    y_values2.append(y[1])
    
    # Create the line graph
    #data = []
    #for i, yv in enumerate(y_values):
    #data.append({'x': x_values, 'y': yv, 'type': 'line', 'name': f'Data {i+1}'})
    
    #print(data)

    fig = {
        'data': [{'x': x_values, 'y': y_values, 'type': 'line', 'name': 'Data'},
                 {'x': x_values, 'y': y_values2, 'type': 'line', 'name': 'Data'}],
        'layout': {'title': 'Live Update Graph'}
    }
    
    return fig

if __name__ == '__main__':
    app.run_server(port=8888, debug=True, host='128.110.96.4')
