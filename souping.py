#beautiful soup ohiolink scraper

#class bibliographic:
def souping(location,bibid):
    import bs4, requests
    from bs4 import BeautifulSoup as bs

    url = 'https://olc1.ohiolink.edu/search~S0?/z'+location+'+'+bibid+'/z'+location+'+'+bibid+'/1%2C1%2C1%2CB/marc&FF=z'+location+'+'+bibid+'&1%2C1%2C'
    page = requests.get(url).text
    soup = bs(page, "lxml")

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

    return oclc,locals,isbn

def holdingsParse(holdingsFile):
    #parsing the holdings file into table schema

def awsPush(marc):
    #storing in private bucket for error logging purposes at a later Date
