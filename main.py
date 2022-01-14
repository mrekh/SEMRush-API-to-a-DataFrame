"""The main function that converts your SEMRush API request to a DataFrame."""

import requests
import pandas as pd
import config

# The report type
REPORT_TYPE = ''
# An identification key assigned to a user after subscribing to SEMrush. The key is available on the Profile page
KEY = config.API_KEY
# A unique name of a website you’d like to investigate
DOMAIN = ''
# A regional database (one value from the list) / Base on your 'REPORT_TYPE' you need to pass the database argument
# database = ''""


def req_to_semrush_api():
    """Convert SEMRush API request to a Pandas DataFrame."""
    # You can modify your request options here
    req = f"https://api.semrush.com/?type={REPORT_TYPE}&key={KEY}&domain={DOMAIN}&export_escape=1"

    res = requests.get(req).text

    res_list = [row for row in res.split('\n')]

    column_name = res_list.pop(0).strip().split(';')

    res_list = [row[1:-2] for row in res_list]
    res_list = [row.split('";"') for row in res_list]
    res_list = res_list[:-1]

    df = pd.DataFrame(res_list, columns=column_name)

    return df
