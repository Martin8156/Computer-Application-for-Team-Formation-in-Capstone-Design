from flask import Flask
from export_excel import output_groups

api = Flask(__name__)

@api.route('/groups', methods=['GET'])
def my_profile():
    df = output_groups()
    df_json = df.to_json(orient='records')
    print(df)
    print(df_json)
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
    output_groups(export=True)
    return {'result': 'success'}
