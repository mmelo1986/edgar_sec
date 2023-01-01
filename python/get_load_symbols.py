from dotenv import dotenv_values
from zipfile import ZipFile as zf
import requests, os, json, datetime as dt, sys
from alphavantage import get_company_details, get_symbol_status
import pandas as pd
import mysql.connector as mc
import sqlalchemy as db
from datetime import date
from sec_cik_mapper import StockMapper

def fetch_zip_file(url):
    # Try to get the ZIP file
    try:
        print('Downloading Edgar data...')
        path = 'temp/edgar_data.zip'
        user_agent = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:108.0) Gecko/20100101 Firefox/108.0'}
        response = requests.get(url, headers=user_agent)
        print('Edgar data downloaded successfully!')
    except OSError:
        print('No connection to the server!')
        return None

    # check if the request is succesful
    if response.status_code == 200:
        # Save dataset to file
        print('Status 200, OK')
        open(path, 'wb').write(response.content)
    else:
        print('ZIP file request not successful!.')
        return None
def error_log_entry(error, logfile):
    message = '[ERROR] : {} : {}\n'.format(error, dt.datetime.now())
    logfile.write(message)

def get_accounting_names_count(cik_files_dir, cik_files):
    key_counts = {}
    for file in cik_files:
        fpath = os.path.join(cik_files_dir, file)
        try:
            data = json.load(open(fpath))
            gaap_keys = data['facts']['us-gaap'].keys()
            for key in gaap_keys:
                if key in key_counts.keys():
                    key_counts[key] += 1
                if key not in key_counts.keys():
                    key_counts[key] = 1
        except Exception as e:
            print('Error in file {}\nRemoving file.'.format(file, e))
            os.unlink(fpath)
            continue
    key_counts =  {k: v for k, v in sorted(key_counts.items(), key=lambda item: item[1])}
    print(key_counts)


def main():
    start_time = dt.datetime.now()
    cik_files_dir = 'temp/cik_data/'
    cik_files =  os.listdir(cik_files_dir)
    get_accounting_names_count(cik_files_dir, cik_files)
    if os.path.exists('python/log/logfile.txt'):
        logfile = open('python/log/logfile.txt', 'a')
        logfile.write('[INFO] : Log file opened successfully. : {}\n'.format(dt.datetime.now()))
    else:
        logfile = open('python/log/logfile.txt', 'w')
        logfile.write('[INFO] : Log file created successfully. : {}\n'.format(dt.datetime.now()))
    try:
        config = dotenv_values('conf/conf.env')
        av_key = config['ALPHAVANTAGE_KEY']
        logfile.write('[INFO] : Configuration file opened successfully. : {}\n'.format(dt.datetime.now()))
    except Exception as e:
        error_log_entry(e, logfile)
    # GETTING SYMBOL DATA FROM DB
    try:
        mysql_engine = db.create_engine("mysql+pymysql://root:password@localhost/edgar_sec_xbrl")
        sql_conn = mysql_engine.connect()
    except Exception as e:
        error_log_entry(e, logfile)
    try:
        cik_data = StockMapper().raw_dataframe
        cik_data['Date'] = date.today()
        cik_data = cik_data.rename(columns={'Ticker':'symbol', 'CIK':'cik', 'Name':'company_name','Exchange':'exchange','Date':'date_updated'})
        # cik_data = cik_data[['Ticker', 'CIK', 'Name', 'Exchange', 'Date']]
        # print(cik_data)
        cik_data[['symbol', 'cik', 'company_name', 'exchange', 'date_updated']].reset_index(drop=True).to_sql(con=sql_conn, name='symbols', if_exists='append', index=False)
    except Exception as e:
        print(e)
        error_log_entry(e, logfile)
    end_time = dt.datetime.now()
    print('Run time: {}'.format(end_time - start_time))


if __name__ == '__main__':
    main()