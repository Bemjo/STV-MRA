#!/usr/bin/python

import json
import sys
import requests

def getGoogleSeet(spreadsheet_id):
    url = f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=tsv'
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.content

    print(f'Error downloading Google Sheet: {response.status_code}')
    return ''

def parseSheet(sheet_text, ignore_first_row=True, ignore_first_col=True):
    obj = {}
    lines = sheet_text.splitlines()[1 if ignore_first_row else 0:]
    for line in lines:
        tokens = line.split('\t')[1 if ignore_first_col else 0:]
        if tokens[0]:
            btns = []
            for btn in tokens[1:]:
                if btn:
                    btns.append(btn)
            obj[tokens[0]] = btns
    return obj

sheet_id = sys.argv[1]
sheet = getGoogleSeet(sheet_id).decode()
json_dict = parseSheet(sheet)

outfile = sys.argv[2] if len(sys.argv) > 2 else 'button_overrides.json'
with open(outfile, 'wt', newline='\n') as file:
    json.dump(json_dict, file)
