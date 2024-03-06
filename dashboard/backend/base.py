from flask import Flask
from group import group

api = Flask(__name__)

@api.route('/groups', methods=['GET'])
def my_profile():
    df = group()
    df_json = df.to_json(orient='records')
    print(df)
    print(df_json)
    return df_json

@api.route('/project/<projectID>', methods=['GET'])
def project(projectID):
    df = group()
    df.set_index('Project', inplace=True)
    df = df.loc[projectID]
    print(df)
    df_json = df.to_json()
    return df_json
