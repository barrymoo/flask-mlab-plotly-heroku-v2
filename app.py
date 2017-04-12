from flask import Flask, render_template
import pymongo
import json
import plotly

app = Flask(__name__)
uri = 'mongodb://readonly:36677ee5c75a174cf07b6f88b816a5c4@ds157320.mlab.com:57320/crc-status'
client = pymongo.MongoClient(uri)

@app.route('/')
def home_page():
    db = client.get_default_database()

    smp_x = []
    smp_y = []
    for item in db['smp'].find():
        smp_x.append(item['x'])
        smp_y.append(item['y'])

    graph = dict(
            data = [
                dict(
                    x=smp_x,
                    y=smp_y,
                    type = 'scatter',
                    name = 'SMP'
                    )
                ]
            )


    graphJSON = json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder)

    #return render_template("items.html", items=db['status'].find())
    return render_template("items.html", graphJSON=graphJSON)

if __name__ == "__main__":
    app.run()
