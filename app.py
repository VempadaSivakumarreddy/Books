import pandas,requests
import openpyxl
import json
import numpy
from flask import jsonify,Flask,request

app = Flask(__name__)
data: pandas.DataFrame = pandas.read_excel(r'D:\Temp\env\books-2-Nov-12-2021-09-58-42-74-AM.xlsx',
                                           index_col=False)
print(data)


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.integer):
            return int(obj)
        elif isinstance(obj, numpy.floating):
            return float(obj)
        elif isinstance(obj, numpy.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)

@app.route('/api/rows=<rows>', methods=['GET','POST'])
def GetRow(rows):
    if rows == None:
        raise ValueError('row must not be none')
    rows=int(rows)
    
    rows = rows + 1 if data.shape[0] >= rows + 1 else data.shape[0]
    result = {'Books': [{cname: data.loc[i][cname] for cname in data.columns} for i in range(rows)]}
    return json.dumps(result, cls=NpEncoder)
    

@app.route('/api/get_info', methods=['POST'])
def GetInfo():
    
    filters = request.get_json()
    print('*'*153,request)
    if filters==None:
        return json.dumps({'books':[]})
    fil_cond = None
    for key, val in filters.items():
        if key in data.columns:
            try:
                val = numpy.float64(val) if isinstance(data[key].iloc[0], numpy.number) else val
            except:
                pass
            fil_cond = (data[key] == val) if fil_cond is None else (data[key] == val) & fil_cond
        else:
            return json.dumps({'error': f'no filter type {key} not available'})
    indxs = data[fil_cond].index
    return json.dumps({'books': [{cname: data.loc[i][cname] for cname in data.columns} for i in indxs]}, cls=NpEncoder)


# print(GetInfo(json.dumps({'author': 'Lorraine Anderson'})))


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)