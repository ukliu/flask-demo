from flask import Flask, render_template, request, redirect



app = Flask(__name__)


app.vars={}

import simplejson as json
import urllib2
import numpy as np
import pandas as pd
from bokeh.charts import TimeSeries
from bokeh.embed import components

quandlkey='8Wy423i2j9KUSTzAoZEA'

@app.route('/')

def main():
  
    return redirect('/index')


@app.route('/index',methods=['GET','POST'])

def index():

    if request.method == 'GET': 
        return render_template('index.html')


    else:
	app.vars['ticker']=request.form['ticker']
	app.vars['selected_features'] = request.form.getlist("features")
	#print app.vars
        url=''.join(['https://www.quandl.com/api/v3/datasets/WIKI/',app.vars['ticker'],'.json?api_key=',quandlkey])
        pydata= json.loads(urllib2.urlopen(url).read())
        colname=pydata['dataset']['column_names']
        data=pydata['dataset']['data']
        df=pd.DataFrame(np.array(data),columns=colname)
    
        col=app.vars['selected_features']
        df[col]=df[col].astype(float)

        df=df.sort_values(by='Date')
	#print df.head()
        tsline=TimeSeries(df,x='Date',y=col)
        script, div = components(tsline)
        return render_template('graph.html', script=script, div=div)	

if __name__ == '__main__':
  
    app.run(port=33507)
