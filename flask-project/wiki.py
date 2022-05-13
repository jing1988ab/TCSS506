import requests

def replaceEmptyImages(dictList, url):
    for d in dictList:
        if ("thumbnail" not in d or not d["thumbnail"]):
            d["thumbnail"]=url

def findBirths(monthDay,year,size=10):
    #monthDay is in form "mm/dd"
    #year is in form "yyyy"
    #returns a list of names, birth years and thumbnails 
    #sortedbyClosestYear[i]['text'] has name of ith match
    #sortedbyClosestYear[i]['year'] has year of ith match's birthdate
    #sortedbyClosestYear[i]['thumbnail'] has url of ith match's thumbnail picture or localhost if there is none
    size=int(size)
    year=int(year)
    path="https://api.wikimedia.org/feed/v1/wikipedia/en/onthisday"
    response=requests.get(path+"/births/"+monthDay)
    data=response.json()
    sortedbyClosestYear=sorted(data["births"], key=lambda i: abs(int(i['year'])-year))
    if len(sortedbyClosestYear) > size:
        sortedbyClosestYear=sortedbyClosestYear[0:size]
    for item in sortedbyClosestYear:
        # item['thumbnail']="localhost"
        if "thumbnail" in item['pages'][0]:
            item['thumbnail']=item['pages'][0]["thumbnail"]["source"]
    print('This is error output')
    print(sortedbyClosestYear)
    replaceEmptyImages(sortedbyClosestYear,"https://www.diamondpet.com/wp-content/uploads/2016/09/20160927-PlayKitty_1200x630.jpg")
    return sortedbyClosestYear
