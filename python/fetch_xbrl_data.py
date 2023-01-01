import requests

def fetch_xbrl_zip_file(url):
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