
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from db import getStockPriceFromDB
from authenticator import validToken

app = Flask(__name__)
api = Api(app)

CONFIG_DAYS_REQUIRED_AUTHENTICATION = 90


class CheckStockPrice(Resource):
    def get(self, ticker, startdate, timeWindowsInDays):
        try:
            if timeWindowsInDays > CONFIG_DAYS_REQUIRED_AUTHENTICATION:
                if ('x-access-tokens' in request.headers) and (request.headers['x-access-tokens']):
                    apikey = request.headers['x-access-tokens']
                    if (not validToken(apikey)):
                        return {"message": "invalid authentication token"}, 401
                else:
                    return {"message": "authentication token is required"}, 401

            records = getStockPriceFromDB(ticker, startdate, timeWindowsInDays)

            return jsonify({'ticker': ticker, 'stockPrices': records})

        except:
            return {"message": "Unknown error"}, 400


api.add_resource(
    CheckStockPrice, "/api/getStockPrice/<string:ticker>/<string:startdate>/<int:timeWindowsInDays>")


if __name__ == "__main__":
    app.run(debug=True)
