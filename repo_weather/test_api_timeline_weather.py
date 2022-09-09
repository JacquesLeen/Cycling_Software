import csv
import codecs
import urllib.request
import urllib.error
import sys


BaseURL = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/'

ApiKey='5DKM32326GJWXTEAASSUPZZGX'

UnitGroup= 'metric'

Location = '53.99,-1.537' # can be specified as a set of lat and lon coordinates, address, partial address

#JSON or CSV 
#JSON format supports daily, hourly, current conditions, weather alerts and events in a single JSON package
#CSV format requires an 'include' parameter below to indicate which table section is required
ContentType="csv"

#if not specified start and end date, then a random day in the past or future gets returned, format is YYYY-MM-DD
StartDate = '2019-09-29'
EndDate=''

#include sections
#values include days,hours,current,alerts
Include="days"

ApiQuery = BaseURL+ Location
if(len(StartDate)):
    ApiQuery+= "/"+StartDate
    if (len(EndDate)):
        ApiQuery+= "/"+EndDate

ApiQuery+="?" #from here on we add the query parameters
if(len(UnitGroup)):
    ApiQuery+="&unitGroup="+UnitGroup

if(len(ContentType)):
    ApiQuery+="&contentType="+ContentType

if(len(Include)):
    ApiQuery+="&include="+Include

ApiQuery+="&key="+ApiKey

print(' - Running query URL: ', ApiQuery)
print()

try: 
    CSVBytes = urllib.request.urlopen(ApiQuery)
except urllib.error.HTTPError  as e:
    ErrorInfo= e.read().decode() 
    print('Error code: ', e.code, ErrorInfo)
    sys.exit()
except  urllib.error.URLError as e:
    ErrorInfo= e.read().decode() 
    print('Error code: ', e.code,ErrorInfo)
    sys.exit()

CSVText = csv.reader(codecs.iterdecode(CSVBytes, 'utf-8'))


RowIndex = 0

# The first row contain the headers and the additional rows each contain the weather metrics for a single day
# To simply our code, we use the knowledge that column 0 contains the location and column 1 contains the date.  The data starts at column 4
for Row in CSVText:
    if RowIndex == 0:
        FirstRow = Row
    else:
        print('Weather in ', Row[0], ' on ', Row[1])

        ColIndex = 0
        for Col in Row:
            if ColIndex >= 4:
                print('   ', FirstRow[ColIndex], ' = ', Row[ColIndex])
            ColIndex += 1
    RowIndex += 1