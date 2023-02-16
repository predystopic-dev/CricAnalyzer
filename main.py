# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from urllib.request import urlopen
import requests
import base64
from streamlit import *
from urllib.parse import urlencode, parse_qsl, urlsplit, urlunsplit

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    [data-testid="stAppViewContainer"]    {
    background-image: url("data:image/jpg   ;base64,%s");
    background-size: cover;
    }
    
    [data-testid="stHeader"] {
        background-color: rgba(0,0,0,0);
    }
    </style>
    ''' % bin_str
    markdown(page_bg_img, unsafe_allow_html=True)

set_background('./pitch.png')

def add_params(url, arg, key):
    scheme, netloc, path, query_string, fragment = urlsplit(url)
    query_params = parse_qsl(query_string, separator=';')
    query_params = dict(query_params)
    query_params[arg] = key
    new_query = urlencode(query_params, safe=';')
    url_wrapper[0] = urlunsplit((scheme, netloc, path, new_query, fragment))

formats = ['', 'Test', 'ODI', 'T20']
conditions = ['', 'home', 'away', 'neutral']
teams = ['Any team', 'England', 'Australia', 'South Africa', 'West indies', 'New Zealand', 'India', 'Pakistan', 'Sri Lanka', 'Zimbabwe', 'Bangladesh', 'Ireland']
url = "https://stats.espncricinfo.com/ci/engine/stats/index.html?class=1;filter=advanced;template=results"

url_wrapper = [url]

with form("form", clear_on_submit=False):
    write('Form start')
    format = radio("Choose matches format", ('Test', 'ODI', 'T20'))
    type = radio("Choose type of stat", ('Batting', 'Bowling')).lower()
    team = selectbox("Select team", teams)
    condition = radio("Choose game conditions", ('Home', 'Away', 'Neutral')).lower()

    add_params(url_wrapper[0], 'class', formats.index(format))
    add_params(url_wrapper[0], 'type', type)

    if team == 'Bangladesh':
        add_params(url_wrapper[0], 'team', 25)
    elif team == 'Ireland':
        add_params(url_wrapper[0], 'team', 29)
    elif team == 'Any team':
        pass
    else:
        add_params(url_wrapper[0], 'team', teams.index(team))
    add_params(url_wrapper[0], 'home_or_away', conditions.index(condition))

    form_submit_button("Submit", on_click=write(url_wrapper[0]))

