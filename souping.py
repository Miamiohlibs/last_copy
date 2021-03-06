#beautiful soup ohiolink scraper

#class bibliographic:
def souping(location,bibid):
    import bs4, requests
    from bs4 import BeautifulSoup as bs
    from user_agent import generate_user_agent #https://hackernoon.com/web-scraping-tutorial-with-python-tips-and-tricks-db070e70e071
    # dev variables
    #location,bibid = 'mu3ug', 'b4413839'

    url = 'https://olc1.ohiolink.edu/search~S0?/z'+location+'+'+bibid+'/z'+location+'+'+bibid+'/1%2C1%2C1%2CB/marc&FF=z'+location+'+'+bibid+'&1%2C1%2C'
    headers = {'User-Agent': generate_user_agent(device_type="desktop", os=('mac', 'linux'))}
    try:
        page = requests.get(url, timeout=5, headers=headers)
        if page.status_code == 200:
            soup = bs(page.text, "lxml")
        else:
            print(page.status_code)
    except requests.Timeout as e:
        print("It is time to timeout")
        print(str(e))

    #scrapes only the broken marc table; parse with PyMarc library
    marc = str(soup.find_all('pre')).split('\n')
    #trim first and last <pre> tags from list
    marc = marc[1:-1]
    # messy;needs to account for multiple \n within single marc field (table of
    # contents) ; clean up marc() function

    # parse larger table body down to primary table rows
    #table = soup.find_all('table')[2].find_all('tr')[1:]
    table = soup.find_all('table')[2] #does not exclude location code
    rows = table.find_all('tr')[1:]
    #empty vars
    holdingsFile = [] #holdings empty list
    a = []
    # for loop to process holdings rows
    for i in rows:
        if i.find_all('a'):
            a = i.find('a') #highly strucutured;only 'a' should always be here
            #print(a.attrs['name'])
        cols=i.find_all('td')
        cols=[x.text.strip() for x in cols]
        a = a.attrs['name'] #gets the location code
        cols.insert(0,a) #inserts the location code into
        holdingsFile.append(cols)
    return marc, holdingsFile

def marcParse(marc):
    import re
    oclc,locals,isbn= [],[],[]
    # sort through and find only the 945s with local bib/item number/status
    for x in marc:
        if x.startswith('001 '):
            oclc.append(re.findall('[0-9]{8,13}', x))
        if x.startswith('945 '):
            locals.append(x)
        if x.startswith('020 '):
            isbn.append(re.findall('[0-9]{10,13}', x))
        #add 022
        #add 019 previous record merges of oclc numbers

    return oclc,locals,isbn

# sql alchemy fields
# make sure to include the following sql fields using boto3
# last_scraped_time, total_times_scraped


#start to parse the objects into sql
#def sqlParse(oclc,locals,isbn,holdingsFile):
#    import

#def holdingsParse(holdingsFile):
#     #parsing the holdings file into table schema
#
# def awsPush(marc):
#     #storing in private bucket for error logging purposes at a later Date
