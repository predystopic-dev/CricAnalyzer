# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from urllib.request import urlopen
import requests
import datetime
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
    scheme, netloc, path, query_string, fragment = urlsplit(url_wrapper[0])
    query_params = parse_qsl(query_string, separator=';')
    query_params = dict(query_params)
    #print(f"argument: {arg} - key: {key}")
    query_params[arg] = key
    #print(f"\n{query_params}\n\n")
    new_query = urlencode(query_params, safe=';')
    url_wrapper[0] = urlunsplit((scheme, netloc, path, new_query, fragment))

def team_select(host):
    if host == 'Bangladesh':
        add_params(url_wrapper[0], 'team', 25)
    elif host == 'Ireland':
        add_params(url_wrapper[0], 'team', 29)
    elif host == 'Any team':
        pass
    else:
        add_params(url_wrapper[0], 'team', teams.index(host))

def opposition_select(opp):
    if opp == 'Bangladesh':
        add_params(url_wrapper[0], 'opposition', 25)
    elif opp == 'Ireland':
        add_params(url_wrapper[0], 'opposition', 29)
    elif opp == 'Any team':
        pass
    else:
        add_params(url_wrapper[0], 'opposition', teams.index(opp))


def add_all_params(team, opposition, format, type, condition, from_date, to_date):
    team_select(team)
    opposition_select(opposition)
    add_params(url_wrapper[0], 'template', 'results')
    add_params(url_wrapper[0], 'filter', 'advanced')
    add_params(url_wrapper[0], 'class', formats.index(format))
    add_params(url_wrapper[0], 'type', type)
    add_params(url_wrapper[0], 'home_or_away', conditions.index(condition))
    add_params(url_wrapper[0], 'spanval1', 'span')
    add_params(url_wrapper[0], 'spanmin1', from_date)
    add_params(url_wrapper[0], 'spanmax1', to_date)
    write(f"\n{url_wrapper[0]}\n\n")

def date_convertor(date):
    month = date.strftime('%b')
    date = str(date)
    #months = ['Jan', 'Feb', 'Mar', '']
    return date[8:10] + '+' + month + '+' + date[:4]

formats = ['', 'Test', 'ODI', 'T20']
conditions = ['', 'home', 'away', 'neutral']
teams = ['Any team', 'England', 'Australia', 'South Africa', 'West indies', 'New Zealand', 'India', 'Pakistan', 'Sri Lanka', 'Zimbabwe', 'Bangladesh', 'Ireland']

url = "https://stats.espncricinfo.com/ci/engine/stats/index.html?"
url_wrapper = [url]

with form("form", clear_on_submit=False):
    write('Form start')
    team = selectbox("Select team", teams)
    opposition = selectbox("Select Opposition", teams)
    format = radio("Choose matches format", ('Test', 'ODI', 'T20'), horizontal=True)
    type = radio("Choose type of stat", ('Batting', 'Bowling'), horizontal=True).lower()
    condition = radio("Choose game conditions", ('Home', 'Away', 'Neutral'), horizontal=True).lower()

    col1, col2 = columns(2)
    with col1:
        from_date = date_convertor(date_input("From: ", value=datetime.date(1877, 3, 15), min_value=datetime.date(1877, 3, 15), max_value=datetime.date.today()))
    with col2:
        to_date = date_convertor(date_input("To: ", value=datetime.date.today(), min_value=datetime.date(1877, 3, 15), max_value=datetime.date.today())) #if from > to, reverse. note


    form_submit_button("Submit", on_click=add_all_params(team, opposition, format, type, condition, from_date, to_date))

print("end")
