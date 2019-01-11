import plotly.graph_objs as go
import pandas as pd
import plotly.offline
import Cloud.uploadDrive as drive

class Interface2:
    # To be defined by the Controller how to be connected
    # cloud.download_file_from_cloud()
    @staticmethod
    def show_values():
        #for linux
        filepath="Files/values.csv"
        htmlpath="Files/Plot.html"

        #for windows
        #filepath="../Files/values.csv"
        #htmlpath="../Files/Plot.html"
        with open(filepath) as f:
            first_line = f.readline()
            lines = f.read().splitlines()
            last_line = lines[-1]
        last = last_line.split(",")
        argList = first_line.split(",")
        df = pd.read_csv(filepath)
        trace = []
        legend = []
        visible = []
        i = 0
        color = ["RED", "BLUE", "DARKGREEN", "ORANGE", "BLACK", "CYAN", "PURPLE"]
        for arg in argList:
            if i != 0 and i < len(argList)-2:
                trace.append(
                    go.Scatter(
                        x=df['datetime'],
                        y=df[arg],
                        name=arg,
                        line=dict(color=color[i % len(color)]),
                        opacity=0.8))
                legend.append('legendonly')
                visible.append(True)
            i += 1
        print(i)
        data = trace
        layout = dict(
            title='SMARTES 1 DATE: ' + str(last[0]),

            plot_bgcolor='rgb(245,245,240)',
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

        updatemenus = list([
            dict(
                buttons=list([
                    dict(
                        args=['visible', visible],
                        label='Select All',
                        method='restyle',
                    ),
                    dict(
                        args=['visible', legend],
                        label='Select None',
                        method='restyle',

                    )
                ]),
                direction='down',
                pad={'r': 1, 't': 1},
                showactive=True,
                x=1.1,
                xanchor='left',
                y=1.1,
                yanchor='bottom',
            ),

        ])
        layout['updatemenus'] = updatemenus
        fig = dict(data=data, layout=layout)
        plotly.offline.plot(fig, filename=htmlpath)
        drive.UploadDrive.write_file_on_cloud(drive, htmlpath, "Plot.html")
