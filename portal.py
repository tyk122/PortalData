__author__ = 'Troy'

import csv
import urllib2
import openpyxl, pprint
import dateutil.parser

def get_portal_data():
    url = 'http://portal.its.pdx.edu/Portal//index.php/api/highways/simplerange/id/1/start/01-16-2016/stop/01-16-2016/starttime/00:00/endtime/23:59/corridor/1/qty1/speed/qty2/volume/res/1hr/group/no/days/0-1-2-3-4-5-6/format/csv/name/traffic_data.csv'
    response = urllib2.urlopen(url)
    cr = csv.reader(response)

    for row in cr:
        print row

def get_portal_data2():
    url = 'http://portal.its.pdx.edu/Portal//index.php/api/highways/simplerange/id/1/start/01-16-2016/stop/01-16-2016/starttime/00:00/endtime/23:59/corridor/1/qty1/speed/qty2/volume/res/1hr/group/no/days/0-1-2-3-4-5-6/format/csv/name/traffic_data.csv'
    response = urllib2.urlopen(url)
    cr = csv.reader(response)
    #print cr
    header = cr.next()
    print header
    for row in cr:
        print row

DEFAULT_QUERY_DATA = {
    'api':'highways',
    'unknown':'simplerange',
    'id':'1',
    'start':'01-16-2016',
    'stop':'01-16-2016',
    'starttime':'00:00',
    'endtime':'23:59',
    'corridor':'1',
    'qty1':'speed',
    'qty2':'volume',
    'res':'1hr',
    'group':'no',
    'days':'0-1-2-3-4-5-6',
    'format':'csv',
    'name':'traffic_data.csv'
}

DEFAULT_OPTIONS = {
    'api':'highways',
    'unknown':'simplerange',
    'id':'1',
    'start':'01-16-2016',
    'stop':'01-16-2016',
    'starttime':'00:00',
    'endtime':'23:59',
    'corridor':'1',
    'qty1':'speed',
    'qty2':'volume',
    'res':'1hr',
    'group':'no',
    'days':'0-1-2-3-4-5-6',
    'format':'csv',
    'name':'traffic_data.csv'
}

QTY1_OPTIONS = {
    'speed': 'speed',
    'volume': 'volume'
}

DATA_TYPE_RELATIONS = {
    "vol": int,
    "occ": float,
    "speed": float,
    "vmt": int,
    "delay": float,
    "vht": float,
    "traveltime": float,
    "starttime": dateutil.parser.parse
}

DATA_TYPES = ["vol", "occ", "speed", "vmt", "delay", "vht", "traveltime", "starttime"]

TEST_URL = 'http://portal.its.pdx.edu/Portal//index.php/api/stations/chibutton/id/1630/start/01-17-2016/stop/01-17-2016/starttime/00:00/endtime/23:59/corridor/0/qty1/speed/qty2/volume/res/1hr/group/no/days/0-1-2-3-4-5-6/lane/all/format/csv/name/station_1630_01-17-2016_data.csv'

class PortalDataSet():

    def __init__(self):
        self.query_data = {}

class StationData:

    def __init__(self, ):
        pass

# WORKING FUNCTIONS

def csv_url_to_2d_array(urlAsString):
    '''
    :param url:
    :return:
    '''

    response = urllib2.urlopen(urlAsString)
    reader = csv.reader(response)
    return list(reader)

def csv_url_to_2d_array2(urlAsString):
    '''
    :param url:
    :return:
    '''

    response = urllib2.urlopen(urlAsString)
    reader = csv.reader(response)

    tmpArr = list(reader)

    headerArr = tmpArr[0]

    data_types = []
    for head in headerArr:
        for type in DATA_TYPES:
            if type in head:
                data_types.append(type)
                break




def save_as_csv(dataArr,outputFileName):
    '''
    :param dataArr:
    :param outputFileName:
    :return:
    '''

    with open(outputFileName, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(dataArr)

def build_dict_from_url(urlAsStr):

    # STRIP URL OF BASIC INFORMATION
    urlInfo = urlAsStr.partition(".php/")
    base, middle, info = str(urlInfo[2]).partition("id/")
    urlList = str('id/' + info).split('/')

    # GENERATE CATEGORIES AND ENTRIES
    categories = urlList[::2]
    categoryEntries = urlList[1::2]

    # BUILD DICTIONARY
    urlDict = {}
    for cat, ent in zip(categories, categoryEntries):
        urlDict[cat] = ent

    return urlDict

def save_as_excel(dataArr,filename='portal_data.xlsx'):
    '''
    :param dataArr:
    :param filename:
    :return:
    '''
    print('Opening workbook...')
    wb = openpyxl.Workbook()
    sheet = wb.get_active_sheet()

    for rowNum in range(0, len(dataArr)):
        for colNum in range(0, len(dataArr[0])):
            colLet = openpyxl.cell.get_column_letter(colNum+1)
            sheet[colLet + str(rowNum+1)].value = dataArr[rowNum][colNum]

    wb.save(filename)

# DEVELOPING FUNCTIONS

def build_url():
    pass

# ASSIGNMENT FUNCTIONS

def calc_vmt(arr2d):

    # FIND INDEX FOR VOLUME COLUMNS FOR DATA SET
    volColIndex = []
    for colNum in range(0,len(arr2d[0])):
        if '_vol' in arr2d[0][colNum]:
            volColIndex.append(colNum)

    # CREATE
    vmtArr = []
    for colIndex in volColIndex:
        currentColArr = [arr2d[i][colIndex] for i in range(0, len(arr2d))]

def get_data_by_param(arr2d, paramType="vol", customDataType=str):

    DATA_TYPE = {
        "vol": int,
        "occ": float,
        "speed": float,
        "other": customDataType
    }

    # FIND INDEX FOR VOLUME COLUMNS FOR DATA SET
    volColIndex = []
    for colNum in range(0,len(arr2d[0])):
        if paramType in arr2d[0][colNum]:
            volColIndex.append(colNum)

    # GET DATA FROM ARR
    paramArr = []
    for colIndex in volColIndex:
        header = [arr2d[0][colIndex]]
        data = [DATA_TYPE[paramType](arr2d[i][colIndex]) for i in range(1, len(arr2d))]
        paramArr.append(header+data)

    return paramArr

def get_data_by_lane(arr2d, lane=1, customDataType=str):

    DATA_TYPE = {
        "vol": int,
        "occ": float,
        "speed": float,
        "other": customDataType
    }

    # FIND INDEX FOR VOLUME COLUMNS FOR DATA SET
    volColIndex = []
    for colNum in range(0,len(arr2d[0])):
        if paramType in arr2d[0][colNum]:
            volColIndex.append(colNum)

    # GET DATA FROM ARR
    paramArr = []
    for colIndex in volColIndex:
        header = [arr2d[0][colIndex]]
        data = [DATA_TYPE[paramType](arr2d[i][colIndex]) for i in range(1, len(arr2d))]
        paramArr.append(header+data)

    return paramArr

STATION_ATTRS = {
    "stationid": int,
    "agencyid": int,
    "highwayid": int,
    "highwayname": str,
    "milepost": float,
    "description": str,
    "upstream": int,
    "downstream": int,
    "oppositestation": int,
    "lon": float,
    "lat": float
}

def get_station_data():
    arr = csv_url_to_2d_array("http://portal.its.pdx.edu/Portal/index.php/api/downloads/get_stations/")

    stations_by_id = {}
    headers = arr[0][:]
    for i in range(1, len(arr)):
        station_info = {}
        j = 0
        for head in headers:
            try:
                station_info[head] = STATION_ATTRS[head](arr[i][j])
            except:
                station_info[head] = None
            j += 1

        stations_by_id[int(arr[i][0])] = station_info

    return stations_by_id

# SCRIPT MAIN

def main():
    # define the variable 'current_time' as a tuple of time.localtime()
    arr = csv_url_to_2d_array(TEST_URL)
    #save_as_excel(arr)
    print arr

    get_portal_data2()

    arrCol = get_data_by_param(arr)
    print arrCol
    #print get_station_data()

if __name__ == '__main__':     # if the function is the main function ...
    main() # ...call it