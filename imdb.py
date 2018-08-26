#Python3
'''
provided a title, fetches results from IMDb, can be narrowed down by 'Movie','TV','TV Episode', or 'Video Game'
'''
from urllib.request import urlopen

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
        

test_movie="the shawshank redemption"

print (build_results_query(test_movie,'movie'))