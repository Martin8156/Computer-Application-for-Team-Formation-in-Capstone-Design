from flask import Flask
from export_excel import output_groups
from grouping import group_sort

api = Flask(__name__)
algo_run = False

@api.route('/groups', methods=['GET'])
def my_profile():
    global algo_run
    if not algo_run:
        print("Calling algorithm")
        group_sort()
        print("ALgorithm run")
        algo_run = True
    df = output_groups()
    df_json = df.to_json(orient='records')
    print(df)
    return df_json

@api.route('/project/<projectID>', methods=['GET'])
def project(projectID):
    df = output_groups()
    df.set_index('ID', inplace=True)
    df = df.loc[projectID]
    print(df)
    df_json = df.to_json()
    return df_json

@api.route('/get_excel', methods=['GET'])
def get_excel():
    global algo_run
    if not algo_run:
        print("Calling algorithm")
        group_sort()
        print("ALgorithm run")
        algo_run = True
    output_groups(export=True)
    return {'result': 'success'}
