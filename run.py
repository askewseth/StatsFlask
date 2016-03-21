"Plot a PNG using matplotlib in a web request, using Flask."

# Install dependencies, preferably in a virtualenv:
#
#     pip install flask matplotlib
#
# Run the development server:
#
#     python app.py
#
# Go to http://localhost:5000/plot.png and see a plot of random data.

import random
import StringIO

from flask import Flask, make_response, render_template, request
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import sys
sys.path.insert(0, "/home/extra/Desktop/tsite/scripts/")
import scripts.script as sc


app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def stats():
    if request.method == 'GET':
        val = 'NO INPUT'
        avginp = [2,3,4,2,3,2,3,2]
        otherval = str(avginp)
        avg = sc.avg(avginp)
        std, stderror = sc.std(avginp)
        count, med, std, minn, q1, q2, q3, maxx = sc.getDescription(avginp)
        # med = sc.median(avginp)
    else:
        val = 'INPUT'
        otherval = request.form['inputtxt']
        avginp = sc.stripinputlist(otherval)
        avg = sc.avg(avginp)
        std, stderror = sc.std(avginp)
        count, med, std, minn, q1, q2, q3, maxx = sc.getDescription(avginp)
        # med = sc.median(avginp)
    # time = scripts.script.time()
    return render_template('stats.html',
                           val=val,
                           ov=otherval,
                           avg=avg,
                           std=std,
                           q1=q1,
                           q2=q2,
                           q3=q3,
                           minn=minn,
                           maxx=maxx,
                           med=med,
                           count=count,
                           stderr=stderror
                           )


@app.route('/home/')
def home():
    return render_template('home.html')


@app.route('/plot.png')
def plot():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)

    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]

    axis.plot(xs, ys)
    canvas = FigureCanvas(fig)
    output = StringIO.StringIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response



if __name__ == '__main__':
    app.run(debug=True)
