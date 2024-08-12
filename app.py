import json

from flask import Flask, request

from service.coverage_service import CoverageService

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/coverage')
def coverage_details():
    member_id = request.args.get('member_id')
    coalesce_strategy = request.args.get('coalesce_strategy')
    if member_id is None:
        return 'Member ID is required'
    try:
        coverage_service: CoverageService = CoverageService()
        return json.dumps(coverage_service.calculate_coverage(member_id, coalesce_strategy))
    except Exception as e:
        print(e)
        return 'Exception occurred '+str(e)


if __name__ == '__main__':
    app.run()
