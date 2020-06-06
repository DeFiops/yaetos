from simple_salesforce import Salesforce
import pandas as pd
from configparser import ConfigParser
import os


def connect(creds_section, creds_or_file='conf/connections.cfg'):
    config = ConfigParser()
    if isinstance(creds_or_file, str):
        config.read(creds_or_file)
    else:
        config = creds_or_file

    user = config.get(creds_section, 'user')
    pwd = config.get(creds_section, 'password')
    return Salesforce(username=user, password=pwd, security_token='')

def query(query_str, **connect_args):
    sf = connect(**connect_args)
    resp = sf.query_all(query_str)
    rows = resp['records']
    for row in rows:
        row.__delitem__('attributes')
    df = pd.DataFrame.from_dict(rows)
    return df

if __name__ == "__main__":
    df = query('SELECT Account.Name FROM Account', creds_section='name_of_connection_from_credentials_file')
    print(df)
