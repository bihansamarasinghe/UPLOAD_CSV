from flask import Flask, request, render_template, jsonify
import pandas as pd
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    # get the uploaded file
    file = request.files['file']

    # read the file using pandas
    df = pd.read_csv(file, skiprows=7, usecols=['Occurred On (NT)', 'Cleared On (NT)', 'MO Name', 'Name'])
    df.loc[df['MO Name'].str.startswith('NodeB Name='), 'MO Name'] = \
    df.loc[df['MO Name'].str.startswith('NodeB Name='), 'MO Name'].str.split(',', n=1).str[0].str.replace('NodeB Name=', '')

    # extract first 2 characters of MO Name column and add to Region ID column
    df['Region ID'] = df['MO Name'].apply(lambda x: x[-2:])

    # extract first 6 characters of MO Name column and add to Site ID column
    df['Site ID'] = df['MO Name'].apply(lambda x: x[:6])

    # check if 'NOA' is in MO Name, then set Region ID to 'NOA'
    df.loc[df['MO Name'].str.contains('NOA'), 'Region ID'] = 'NOA'

    # move Site ID column to before MO Name column
    cols = list(df.columns)
    cols = cols[:2] + ['Site ID'] + cols[2:4] + ['Region ID'] + cols[4:-2]
    df = df[cols]

    # add 'Site Type' column to df
    def get_site_type(site_id):
        if site_id[0] == 'Q':
            return 'Small Cell'
        elif site_id[0] == 'L':
            return 'Lamp Pole'
        else:
            return 'Macro'

    df['Site Type'] = df['Site ID'].apply(get_site_type)

    # Add Duration column
    occurred = pd.to_datetime(df['Occurred On (NT)'], format='%Y-%m-%d %H:%M:%S')
    cleared = pd.to_datetime(df['Cleared On (NT)'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
    df['Duration'] = (cleared - occurred).dt.total_seconds().div(60).fillna('')

    # Round up Duration values
    df.loc[df['Duration'] != '', 'Duration'] = df.loc[df['Duration'] != '', 'Duration'].astype(float).round(decimals=0)

     # count the occurrences by site ID
    site_counts = df['Site Type'].value_counts().reset_index()
    site_counts.columns = ['Site Type', 'Counts']

    # create a dictionary containing the data for the chart
    chart_data = {
        'labels': site_counts['Site Type'].tolist(),
        'data': site_counts['Counts'].tolist()
    }

    # print the JSON string to the console in debug mode
    if app.debug:
        print(json.dumps(chart_data, indent=4))

    # convert the dataframe to an html table
    table = df.to_html(classes='table table-striped table-bordered table-hover')

    # render the table in the table.html template
    return render_template('table.html', table=table,chart_data=chart_data)

if __name__ == '__main__':
    app.run(debug=True)
