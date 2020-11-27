
from flask import Flask, escape, request
from flask_cors import CORS

# import bugsnag
# from bugsnag.flask import handle_exceptions

import pandas as pd

import joblib

# get env parameters
# import os
# from os.path import join, dirname
# from dotenv import load_dotenv

# dotenv_path = join(dirname(__file__), '.env')
# load_dotenv(dotenv_path)

# BUGSNAG_API_KEY = os.environ.get('BUGSNAG_API_KEY')

# initialize bugsnap
# bugsnag.configure(
#     api_key='BUGSNAG_API_KEY',
#     project_root='/path/to/your/app',
# )

# create flask app
app = Flask(__name__)
CORS(app)

# handle bugsnag
# handle_exceptions(app)

# bugsnag.notify(Exception('Test error'))


@app.route('/')
def hello():
    # get param from http://127.0.0.1:5000/?name=value
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

# @app.route('/toto')
# def hello():
#     return '''
#     <!DOCTYPE>
#     <html>
#         <head>
#             <title>My super page</title>
#         </head>
#         <body>
#             <div>
#                 This is a Le Wagon API site, please use rather the /predict_fare entry point
#                 <img src="https://dwj199mwkel52.cloudfront.net/assets/core/home/coding-school-that-cares-alumni-025e665def0e2f5a9a539cd2f8762fedbd4c5074a725ebed08570a5bdacc45f7.jpg">
#             </div>
#         </body>
#     </html>
#     '''


@app.route('/predict_fare', methods=['POST'])
def predict_fare_post():

    # get request arguments
    key = "2020-10-10 10:10:10 UTC"
    pickup_datetime = request.form.get('pickup_datetime')
    pickup_longitude = float(request.form.get('pickup_longitude'))
    pickup_latitude = float(request.form.get('pickup_latitude'))
    dropoff_longitude = float(request.form.get('dropoff_longitude'))
    dropoff_latitude = float(request.form.get('dropoff_latitude'))
    passenger_count = int(request.form.get('passenger_count'))

    # build X ⚠️ beware to the order of the parameters ⚠️
    X = pd.DataFrame(dict(
        key=[key],
        pickup_datetime=[pickup_datetime],
        pickup_longitude=[pickup_longitude],
        pickup_latitude=[pickup_latitude],
        dropoff_longitude=[dropoff_longitude],
        dropoff_latitude=[dropoff_latitude],
        passenger_count=[passenger_count]))

    # print(X_test.dtypes)

    # TODO: get model from GCP
    # pipeline = get_model_from_gcp()
    pipeline = joblib.load('model.joblib')

    # make prediction
    results = pipeline.predict(X)

    # convert response from numpy to python type
    pred = float(results[0])

    return dict(
        prediction=pred)


@app.route('/predict_fare', methods=['GET'])
def predict_fare():

    # get request arguments
    key = "2020-10-10 10:10:10 UTC"
    pickup_datetime = request.args.get('pickup_datetime')
    pickup_longitude = float(request.args.get('pickup_longitude'))
    pickup_latitude = float(request.args.get('pickup_latitude'))
    dropoff_longitude = float(request.args.get('dropoff_longitude'))
    dropoff_latitude = float(request.args.get('dropoff_latitude'))
    passenger_count = int(request.args.get('passenger_count'))

    # build X ⚠️ beware to the order of the parameters ⚠️
    X = pd.DataFrame(dict(
        key=[key],
        pickup_datetime=[pickup_datetime],
        pickup_longitude=[pickup_longitude],
        pickup_latitude=[pickup_latitude],
        dropoff_longitude=[dropoff_longitude],
        dropoff_latitude=[dropoff_latitude],
        passenger_count=[passenger_count]))

    # print(X_test.dtypes)

    # TODO: get model from GCP
    # pipeline = get_model_from_gcp()
    pipeline = joblib.load('model.joblib')

    # make prediction
    results = pipeline.predict(X)

    # convert response from numpy to python type
    pred = float(results[0])

    return dict(
        prediction=pred)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
