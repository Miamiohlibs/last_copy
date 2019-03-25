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
    #remove first and last <pre> tags
    marc.pop(0),marc.pop(-1)
    # messy;needs to account for multiple \n within single marc field (table of
    # contents)
    #remove marc[0][0] & marc[0][-1]

    # parse larger table body down to primary table rows
    # after column headers, table holdings rows start

    table = soup.find_all('table')[2].find_all('tr')[1:]
    #begin to parse row data into respective pieces
    holdingsFile = [] #holdings empty list
    for row in table:
        cols=row.find_all('td')
        cols=[x.text.strip() for x in cols]
        #store columns in postgres or pandas dataframe
        holdingsFile.append(cols)
    return marc, holdingsFile




# <tr class="holdingscc2tg"><td><a name="cc2tg"></a>Cuyahoga CC</td>
# <td>WEST Library</td>
# <td>&nbsp; </td>
# <td>813.0108 O113p 2003 </td>
# <td>AVAILABLE</td>
# </tr>
#
#
# #scrapy fails and successes
#
# #generate response with url?
#
# a = response.xpath('//table//tr//tr')  #don't use .getall(); it converts to array and excludes continued use of .xpath()
# ## need to include additional info about each row in a
#
# table = a[6:-17]
#
# #parse rows using table
# row = table.xpath
#
#
#     https://olc1.ohiolink.edu/search/z?mu3ug+b3294810
#
# ## use scrapy to parse looking for marc display button; import pymarc and parse marc record from url.response.marc
# marcUrl = response.xpath('//*[@onclick="setRequestEventCookie()"]//@href').getall()[0]
