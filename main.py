import requests
import pandas as pd

# The report type
report_type = ''
# An identification key assigned to a user after subscribing to SEMrush. The key is available on the Profile page
key = ''
# A unique name of a website you’d like to investigate
domain = ''
# A regional database (one value from the list) / Base on your 'report_type' you need to pass the database argument
# database = ''


def req_to_SEMRush_API():
    # You can modify your request options here
    req = f"https://api.semrush.com/?type={report_type}&key={key}&domain={domain}&export_escape=1"

    res = requests.get(req).text

    res_list = [row for row in res.split('\n')]

    column_name = res_list.pop(0).strip().split(';')

    res_list = [row[1:-2] for row in res_list]
    res_list = [row.split('";"') for row in res_list]
    res_list = res_list[:-1]

    df = pd.DataFrame(res_list, columns=column_name)

    return df
