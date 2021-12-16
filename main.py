import requests
import pandas as pd

# The report type
report_type = ''
# An identification key assigned to a user after subscribing to SEMrush. The key is available on the Profile page.
key = ''
# A unique name of a website you’d like to investigate.
domain = ''


def req_to_SEMRush_API():
    # You can modify your request options here
    req = f"https://api.semrush.com/?type={report_type}&key={key}&domain={domain}"

    res = requests.get(req).text

    res_list = [line.split(';') for line in res.split('\n')]
    for list in res_list:
        list[-1] = list[-1].strip()
    res_list = res_list[:-1]

    column_name = res_list.pop(0)
    df = pd.DataFrame(res_list, columns=column_name)

    return df
