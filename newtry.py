import os,time, csv, json
from werkzeug.utils import secure_filename
from flask import Flask, request, render_template
import plotly
from sklearn.cluster import KMeans
import numpy as np

app = Flask(__name__)
global ufile

@app.route('/show',methods=['GET','POST'])
def show():
    stime=time.time()
    clst_num = request.form['clsnum']
    datalist = []
    f = open("/home/ubuntu/flaskapp/"+ufile.filename, "rb")
    cf = csv.reader(f)
    for line in cf:
        #print '1st loop'
        try:
            var = [float(line[0]),float(line[1])]
            datalist.append(var)
        except:
            continue
    finaldata = np.array(datalist)
    #print datalist
    km=KMeans(n_clusters=int(clst_num))
    km.fit(finaldata)

    centroids = km.cluster_centers_
    labels = km.labels_
    f.close()
    data1=[]
    yset=[]
    xset=[]
    lset= set(labels)
    print "lset is................................."
    for r in lset:
        print r
    print "labels are................................."
    print labels
    for label in lset:
        x1 = []
        y1 = []
        yn = 0
        i = 0
        print "label is................................................................................\n\n\n\n"
        print label
        print "\n\n\n\n"
        for line in finaldata:

            try:
                if labels[i] == label:

                    x1.append(float(line[0]))
                    y1.append(float(line[1]))
                    yn+=1
                i += 1
            except:
                continue
        yset.append(yn)
        xset.append(label)
        data1.append(dict(x=x1,y=y1,
                    type='scatter',
                    mode='markers'))

        print "new data is..............................................................................................\n\n\n"
        print data1
        print "\n\n\n\n"

    for row in centroids:
        xc=[]
        yc=[]
        xc.append(row[0])
        yc.append(row[1])
        data1.append(dict(x=xc, y=yc,
                          type='scatter',
                          mode='markers'))
        print "new data is..............................................................................................\n\n\n"
        print data1


    graphs = [
        dict(
            data=data1,
            layout=dict(
                title='first graph'
            )
        ),

        dict(
            data=[
                dict(
                    x=xset,
                    y=yset,
                    type='bar'
                ),
            ],
            layout=dict(
                title='second graph'
            )
        )
    ]

    # Add "ids" to each of the graphs to pass up to the client
    # for templating
    ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]

    # Convert the figures to JSON
    # PlotlyJSONEncoder appropriately converts pandas, datetime, etc
    # objects to their JSON equivalents
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
    print graphJSON
    delay=time.time()-stime
    return render_template('index.html', ids=ids, graphJSON=graphJSON, delay=delay)
@app.route('/')
def hello_world():
    return render_template("hello.html")
@app.route('/upload',methods=['GET','POST'])
def upload():
    global ufile
    ufile = request.files['file']
    contents = ufile.read()
    f=open(ufile.filename,'wb')
    f.truncate()
    f.write(contents)
    f.close()
    return render_template("hello.html")

if __name__ == '__main__':
    app.run(host='ec2-50-112-203-124.us-west-2.compute.amazonaws.com',port=5026,debug=True)
