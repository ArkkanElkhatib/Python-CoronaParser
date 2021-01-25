import requests
from bs4 import BeautifulSoup

def getSoupFromURL(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    print(soup.prettify())
    return soup

def makeApiRequestToURL(url):
    try:
        res = requests.get(url)
        return res.json()
    except:
        print("Unable to make API request, either data was not in JSON format or API url does not exist")

def mapCountries():
    map100 = makeApiRequestToURL('https://www.who.int/api/multimedias/countries?$expand=WHORegion,Flag($select=Title,UrlName,Url,ThumbnailUrl,Extension)&$orderBy=Title%20asc&sf_culture=en&$top=100&$skip=0&$count=true')
    map200 = makeApiRequestToURL('https://www.who.int/api/multimedias/countries?$expand=WHORegion,Flag($select=Title,UrlName,Url,ThumbnailUrl,Extension)&$orderBy=Title%20asc&sf_culture=en&$top=100&$skip=100&$count=true')
    map300 = makeApiRequestToURL('https://www.who.int/api/multimedias/countries?$expand=WHORegion,Flag($select=Title,UrlName,Url,ThumbnailUrl,Extension)&$orderBy=Title%20asc&sf_culture=en&$top=100&$skip=200&$count=true')

    countryMappings = {}

    for i in map100['value']:
        countryMappings[i['Title'].lower()] = i

    for i in map200['value']:
        countryMappings[i['Title'].lower()] = i

    for i in map300['value']:
        countryMappings[i['Title'].lower()] = i

    return countryMappings

def getCountryCodeByName(countryName):
    global countryMapping
    if (countryName.lower() == 'vietnam'):
        countryName = 'viet nam'
    elif (countryName.lower() == 'usa'):
        countryName = 'united states of america'

    try:
        return countryMapping[countryName.lower()]['Code']
    except:
        print(f'No data for "{countryName}" was found')
        return None

def displayData(data):
    print('##################################################')
    print('### Corona Data For: {name:24}  ###'.format(name=data["ADM0_NAME"]))
    print('##################################################')
    print('#########     New Corona Cases Data     ##########')
    print('## New Cases: {newCases:33} ##'.format(newCases=data["NewCase"]))
    print('## New Deaths: {newDeath:32} ##'.format(newDeath=data["NewDeath"]))
    print('## Cases in last 7 Days: {case7:22} ##'.format(case7=data["CaseLast7Days"]))
    print('## Deaths in last 7 Days: {death7:21} ##'.format(death7=data["DeathLast7Days"]))
    print('##################################################')
    print('#########     Cumulative Corona Data     #########')
    print('## Total Confirmed Cases: {cumCase:21} ##'.format(cumCase=data["CumCase"]))
    print('## Total Confirmed Deaths: {cumDeath:20} ##'.format(cumDeath=data["CumDeath"]))
    print('##################################################')

def getCoronaDataFromCountryCode(countryCode):
    return makeApiRequestToURL(f"https://services.arcgis.com/5T5nSi527N4F7luB/arcgis/rest/services/COVID_19_Historic_cases_by_country_pt_v7_view/FeatureServer/0/query?where=ISO_3_CODE%3D%27{countryCode}%27&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&resultType=none&distance=0.0&units=esriSRUnit_Meter&returnGeodetic=false&outFields=date_epicrv%2CADM0_NAME%2CShort_Name_AR%2CShort_Name_ZH%2CShort_Name_RU%2CShort_Name_ES%2CShort_Name_FR%2CISO_3_CODE%2CNewCase%2CCaseLast7Days%2CCaseLast7DaysChange%2CCumCase%2CCumCasePop%2CNewDeath%2CDeathLast7Days%2CDeathLast7DaysChange%2CCumDeath%2CCumDeathPop%2CISO_2_CODE%2CWHO_REGION&returnGeometry=false&featureEncoding=esriDefault&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=4326&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnQueryGeometry=false&returnDistinctValues=false&cacheHint=true&orderByFields=date_epicrv+desc&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=none&f=pjson&token=")['features'][0]['attributes']


def requestCountryName():
        print('####### Enter a Country Name For Data     ########')
        countryName = input("|Input| Enter Country Name  >>>  ")
        print(f"### You entered: '{countryName}'.  Correct? ")
        choice = input('|Check| (y/n) >>>  ')
        print('##################################################')
        if (choice == 'n' or choice == 'N'):
            return requestCountryName()
        else:
            return countryName


def main():
    global countryMapping;
    countryMapping = mapCountries();
    while 1:
        try:
            print('##################################################')
            print('###        Welcome To Corona Scrapper          ###')
            print('##################################################')
            countryName = requestCountryName()
            countryCode = getCountryCodeByName(countryName)
            countryData = getCoronaDataFromCountryCode(countryCode)
            displayData(countryData)
            input("|Input| Click enter to continue...")
        except:
            print("|ERROR| An error occurred, restarting")
            continue

if __name__ == '__main__':
    main()
