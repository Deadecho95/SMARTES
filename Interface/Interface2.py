import plotly.graph_objs as go
import pandas as pd
import plotly.offline
import Cloud.uploadDrive as drive


class Interface2:
    # To be defined by the Controller how to be connected
    # cloud.download_file_from_cloud()

    @staticmethod
    def show_values():
        # for Windows
        # filepath="../Files/values.csv"
        # htmlpath="../Files/Plot.html"
        # for Linux

        filepath = "Files/values.csv"
        htmlpath = "Files/Plot.html"
        total = 0
        # Open a csv file and read it
        with open(filepath) as f:
            first_line = f.readline()
            lines = f.read().splitlines()
            last_line = lines[-1]
        last = last_line.split(",")
        arg_list = first_line.split(",")
        df = pd.read_csv(filepath)
        trace = []
        legend = []
        visible = []
        i = 0
        color = ["RED", "BLUE", "DARKGREEN", "ORANGE", "BLACK", "CYAN", "PURPLE"]
        # add trace for each argument and add a trace for the total of 3 phases
        for arg in arg_list:
            isVisible = 'legendonly'
            if i != 0 and i < len(arg_list) - 2:
                if arg.find("Percent_Soc_Battery"):
                    isVisible = True
                trace.append(
                    go.Scatter(
                        x=df['datetime'],
                        y=df[arg],
                        name=arg,
                        line=dict(color=color[i % len(color)]),
                        opacity=0.8,
                        visible=isVisible))
            if (arg.find("1") != -1) or (arg.find("2") != -1):
                total += df[arg]

            if arg.find("3") != -1:
                if arg.find("Power_Consumption_Total"):
                    color1 = "GREEN"
                if arg.find("Power_PvOnGrid"):
                    color1 = "ORANGE"
                    isVisible=True
                if arg.find("Power_Grid"):
                    color1 = "RED"
                    isVisible=True
                if arg.find("Power_Genset"):
                    color1 = "PURPLE"
                else:
                    color1 = "GREY"
                trace.append(
                    go.Scatter(
                        x=df['datetime'],
                        y=total,
                        name=arg.replace("L3", "Total"),
                        line=dict(color=color1),
                        opacity=0.8,
                        visible=isVisible
                    )
                )
                total = 0
            i += 1
        print("Nb of traces : ")
        print(i)
        data = trace
        # add buttons to select some trace
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
        # add of the menus for the selection of the trace
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
        plotly.offline.plot(fig, filename=htmlpath, auto_open=False)
