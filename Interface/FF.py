from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import os
import plotly.graph_objs as go


def __init__(self, path="Files/values.csv", title="Smartes\n"):
    self.path = path
    if os.path.isfile(self.path) and os.path.getsize(self.path) > 0:
        self.file = open(self.path, "r")
        self.file.close()
        self.header = False
        plot([go.Scatter(x=[0, 2, 3], y=[3, 1, 6])])
