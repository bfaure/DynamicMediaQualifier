#Python3
'''
provided a title, fetches results from IMDb, can be narrowed down by 'Movie','TV','TV Episode', or 'Video Game'
'''
from urllib.request import urlopen # for downloading HTML
from bs4 import BeautifulSoup # for more easily parsing HTML


# returns the url for searching imdb results for the provided title.
# if a filter is provided it must be one of ['movie','tv','tv episode','video game']
# any other provided filter type will throw an error
def build_results_query(title,filter=None):
    # prepares provided title so it fits with encoding used on IMDb site
    def prep_title(title):
        encodings={'+':'%2B',' ':'%20'}
        for key,val in encodings.items():
            title=title.replace(key,val)
        return title
    filter_mapping={'movie':      "https://www.imdb.com/find?q=[INSERT_HERE]&s=tt&ttype=ft&ref_=fn_ft",
                    'tv':         "https://www.imdb.com/find?q=[INSERT_HERE]&s=tt&ttype=tv&ref_=fn_tv",
                    'tv episode': "https://www.imdb.com/find?q=[INSERT_HERE]&s=tt&ttype=ep&ref_=fn_ep",
                    'video game': "https://www.imdb.com/find?q=[INSERT_HERE]&s=tt&ttype=vg&ref_=fn_vg"}
    if filter!=None:
        if filter.lower() not in filter_mapping:
            errstr=list(filter_mapping.keys())
            raise ValueError("build_results_query was passed an invalid filter, valid filters include ",errstr)
        return filter_mapping[filter].replace("[INSERT_HERE]",prep_title(title))
    url="https://www.imdb.com/find?ref_=nv_sr_fn&q=[INSERT_HERE]&s=all"
    return url.replace("[INSERT_HERE]",prep_title(title))
        

# provided a url from build_results_query, returns a list of dictionaries containing
# {title, [url to exact imdb listing, YYYY the movie was released] for all results of the IMDB search
def fetch_search_results(query):
    html=urlopen(query).read()
    soup=BeautifulSoup(html,'lxml')
    items=soup.find_all('td',{'class':'result_text'})
    results=[]
    for item in items: 
        results.append({item.find('a').text:["https://www.imdb.com"+item.find('a').get('href'),item.text.split("(")[1].split(")")[0]]})
    return results

# provided a dictionary result (an element of the list returned by fetch_search_results)
# will download the HTML for the result page and parse out attributes such as
# user ratings, number of ratings, runtime, genre, and release date
def fetch_result_data(search_result):
    url=list(search_result.values())[0][0]
    html=urlopen(url).read()
    soup=BeautifulSoup(html,'lxml')
    data={'rating':soup.find('div',{'class':'ratingValue'}).find('strong').text}
    data['volume']=soup.find('div',{'class':'imdbRating'}).find('span',{'class':'small'}).text
    metadata=[e.strip("\n").strip() for e in soup.find('div',{'class':'subtext'}).text.split("|")]
    data['mpaa'],data['runtime'],data['genre'],data['release date']=metadata
    data['title']=list(search_result.keys())[0]
    return data
        

# provided a movie title will return all information pertaining to it
def search_for_movie(title):
    search_query=build_results_query(title,'movie')
    search_results=fetch_search_results(search_query)
    data=fetch_result_data(search_results[0])
    print(data)

search_for_movie('the shawshank redemption')

