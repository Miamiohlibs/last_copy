#beautiful soup ohiolink scraper

# ideally api or list of bib records would be fed into function below
# def souping(args, kwargs):

#sys.argv accepts url passed along from command line
# import sys
# url = sys.argv[1]

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
    # contents)

    # parse larger table body down to primary table rows
    #table = soup.find_all('table')[2].find_all('tr')[1:]
    table = soup.find_all('table')[2].text #does not exclude location code
    #begin to parse row data into respective pieces
    holdingsFile = [] #holdings empty list
    for row in table: #row does not include attrs
        a = row.find('a').attrs['name'] #gets the location code
        cols=row.find_all('td')
        cols=[x.text.strip() for x in cols]
        cols.insert(0,a) #inserts the location code into
        holdingsFile.append(cols)
    #
    # sort through and find only the 945s with local bib/item number/status
    #locals = [x for x in marc if x.startswith('945    ')]

    return marc, holdingsFile
