from flask import Flask, render_template
import pymongo
import json
import plotly


def fill_x_y_lists(db, cluster, x, y, limit):
    cursor = db['status'].find({'cluster': cluster}).sort('_id', pymongo.DESCENDING).limit(limit)
    counter = 0
    for item in reversed(list(cursor)):
        x[counter] = item['time']
        y[counter] = 100 * item['allocated'] / item['total']
        counter += 1
        if counter == limit:
            return [cluster, item['allocated'], item['total']]


# Ready the app and the database
app = Flask(__name__)
uri = 'mongodb://readonly:36677ee5c75a174cf07b6f88b816a5c4@ds157320.mlab.com:57320/crc-status'
client = pymongo.MongoClient(uri)
db = client.get_default_database()

# The limit of datapoints to return
limit = 24

@app.route('/')
def home_page():
    # A list of lists
    items = []

    # SMP x,y and append to list of lists
    smp_x = [0] * limit
    smp_y = [0] * limit
    items.append(fill_x_y_lists(db, 'smp', smp_x, smp_y, limit))

    # GPU x,y and append to list of lists
    gpu_x = [0] * limit
    gpu_y = [0] * limit
    items.append(fill_x_y_lists(db, 'gpu', gpu_x, gpu_y, limit))

    # MPI x,y and append to list of lists
    mpi_x = [0] * limit
    mpi_y = [0] * limit
    items.append(fill_x_y_lists(db, 'mpi', mpi_x, mpi_y, limit))

    # HTC x,y and append to list of lists
    htc_x = [0] * limit
    htc_y = [0] * limit
    items.append(fill_x_y_lists(db, 'htc', htc_x, htc_y, limit))

    # MPI_IB x,y and append to list of lists
    ib_x = [0] * limit
    ib_y = [0] * limit
    items.append(fill_x_y_lists(db, 'ib', ib_x, ib_y, limit))

    graph = dict(
            data = [
                dict(
                    x=smp_x,
                    y=smp_y,
                    type='scatter',
                    name='SMP',
                    mode='lines+markers'
                    ),
                dict(
                    x=gpu_x,
                    y=gpu_y,
                    type='scatter',
                    name='GPU (Cards)',
                    mode='lines+markers'
                    ),
                dict(
                    x=mpi_x,
                    y=mpi_y,
                    type='scatter',
                    name='MPI',
                    mode='lines+markers'
                    ),
                dict(
                    x=htc_x,
                    y=htc_y,
                    type='scatter',
                    name='HTC',
                    mode='lines+markers'
                    ),
                dict(
                    x=ib_x,
                    y=ib_y,
                    type='scatter',
                    name='MPI (IB below)',
                    mode='lines+markers'
                    )
                ]
            )

    layout = dict(
                #title = 'CRC Status',
                #titlefont = dict(
                #        size = 18
                #    ),
                yaxis = dict(
                        ticksuffix = '%',
                        title = 'Percent Utilization',
                        side = 'top',
                        titlefont = dict(
                                size = 18
                            ),
                        tickfont = dict(
                                size = 18
                            )
                    ),
                xaxis = dict(
                    title = 'Date (MM/DD/YY-HH:MM)',
                    nticks = 4,
                        titlefont = dict(
                                size = 18
                            ),
                        tickfont = dict(
                                size = 18
                            )
                    ),
                legend = dict(
                        font = dict(
                                size = 18
                            )
                        )
             )


    graph_json = json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder)
    layout_json = json.dumps(layout, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("index.html", graph_json=graph_json, layout_json=layout_json, items=items)

if __name__ == "__main__":
    app.run()
