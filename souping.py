#beautiful soup ohiolink scraper

# ideally api or list of bib records would be fed into function below
# def souping(args, kwargs):

def souping():
    import bs4, requests
    from bs4 import beautifulSoup AS bs

    url = 'https://olc1.ohiolink.edu/search/z?mu3ug+b3294810'
    page = requests.get(url).text
    soup = bs(page, "lxml")

    #get path to the marc file to parse later with pymarc library; add domain later
    marcPath = soup.find_all('a')[15].get('href')

    # parse path; raise exception if path end doesn't start with marc
    if marcPath.split('/')[-1].startswith('marc&FF'):
        #continue loading html data
    else:
        print("Bad marc url. Cannot parse Ohiolink marc url.")
        raise Exception
        #break
    # parse larger table body down to primary table rows
    # after column headers, table holdings rows start
    table = soup.find_all('table')[4].find_all('tr')[1:]
    #begin to parse row data into respective pieces
    holdingsFile = []
    for row in table:
        cols=row.find_all('td')
        cols=[x.text.strip() for x in cols]
        #store columns in postgres or pandas dataframe
        holdingsFile.append(cols)





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
