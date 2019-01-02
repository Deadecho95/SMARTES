import plotly
import plotly.graph_objs as go
import pandas as pd


class Interface2:
    # To be defined by the Controller how to be connected
    # cloud.download_file_from_cloud()
    @staticmethod
    def show_values():
        with open("../Files/example.csv") as f:
            first_line = f.readline()
            lines = f.read().splitlines()
            last_line = lines[-1]
        last = last_line.split(",")
        argList = first_line.split(",")
        df = pd.read_csv("../Files/example.csv")
        trace = []
        i = 0
        color = ["RED", "BLUE", "DARKGREEN", "ORANGE", "BLACK", "CYAN", "PURPLE"]
        for arg in argList:
            if i != 0 and i < 7:
                trace.append(
                    go.Scatter(
                        x=df['Date'],
                        y=df[arg],
                        name=arg,
                        line=dict(color=color[i % len(color)]),
                        opacity=0.8))
            i += 1
        print(i)
        data = trace
        layout = dict(
            title='SMARTES 1 DATE: '+ str(last[0]),
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                             label='1h',
                             step='hour',
                             stepmode='backward'),
                        dict(count=1,
                             label='1d',
                             step='day',
                             stepmode='backward'),
                        dict(count=1,
                             label='1m',
                             step='month',
                             stepmode='backward'),
                        dict(count=6,
                             label='6m',
                             step='month',
                             stepmode='backward'),
                        dict(count=1,
                             label='1y',
                             step='year',
                             stepmode='backward'),
                        dict(step='all')
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type='date'
            )
        )
        fig = dict(data=data, layout=layout)
        plotly.offline.plot(fig, filename="../Files/Plot.html")
