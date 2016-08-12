__author__ = 'Troy'

'''
CAN CURRENTLY
    - SAVE AS: csv, excel
    - GET DATA BY:
        - Lane
        - Parameters

    - Obtain csv data from specified url
    - Can save data

DEFINITIONS
- Primary functions:
- Secondary functions: Functions which build upon primary functions for more useful or specific data applications
'''

import csv
import urllib2
import openpyxl, pprint
import dateutil.parser

def get_portal_data():
    url = 'http://portal.its.pdx.edu/api/highways/simplerange/id/1/start/01-16-2016/stop/01-16-2016/starttime/00:00/endtime/23:59/corridor/1/qty1/speed/qty2/volume/res/1hr/group/no/days/0-1-2-3-4-5-6/format/csv/name/traffic_data.csv'
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

DEFAULT_PARAM_DICT = {'lane': 'all',
                      'group': 'no',
                      'corridor': '0',
                      'qty1': 'speed',
                      'res': '1hr',
                      'format': 'csv',
                      'stop': '02-04-2016',
                      'days': '0-1-2-3-4-5-6',
                      'start': '02-04-2016',
                      'qty2': 'volume',
                      'starttime': '00:00',
                      'endtime': '23:59',
                      'id': '3170',
                      'name': 'traffic_data.csv'}

QTY1_OPTIONS = {
    'speed': 'speed',
    'volume': 'volume'
}

QTY_OPTIONS = ['speed','volume','totalvolume','occupancy','vmt','vht','traveltime','delay']

DATA_TYPE_RELATIONS = {
    "vol": int,
    "occ": float,
    "speed": float,
    "spd": float,
    "vmt": int,
    "delay": float,
    "vht": float,
    "traveltime": float,
    "starttime": dateutil.parser.parse
}

DATA_TYPES = ["vol", "occ", "speed", "spd", "vmt", "delay", "vht", "traveltime", "starttime"]
URL_DATA_TYPES = ["vol", "occ", "spd", "vmt", "delay", "vht", "traveltime", "starttime"]

TEST_URL = 'http://portal.its.pdx.edu/api/stations/twoquantityungroupedsimplerange/id/3170/start/02-04-2016/stop/02-04-2016/starttime/00:00/endtime/23:59/corridor/0/qty1/speed/qty2/volume/res/1hr/group/no/days/0-1-2-3-4-5-6/lane/all/format/csv/name/traffic_data.csv'

class PortalDataSet():

    def __init__(self):
        self.query_data = {}

class StationData:

    def __init__(self, ):
        pass

# WORKING FUNCTIONS

# PRIMARY FUNCTIONS

def csv_url_to_2d_array(urlAsString, withHeader=True):
    '''
    :param url:
    :return:
    '''

    # GET DATA AS 2D LIST
    response = urllib2.urlopen(urlAsString)
    reader = csv.reader(response)
    tmpArr = list(reader)

    # DETERMINE PROPER DATA TYPES FOR EACH COLUMN
    headerArr = tmpArr[0]
    data_types = []
    for head in headerArr:
        for dtype in DATA_TYPES:
            if dtype in head:
                data_types.append(dtype)
                break

    # APPLY DATA TYPES AND CREATE CORRECT TYPES
    arr_with_correct_types = []
    for row in tmpArr[1:]:
        rowArr = []
        for i in range(0,len(row)):
            try:
                result = DATA_TYPE_RELATIONS[data_types[i]](row[i])
            except:
                result = None
            rowArr.append(result)
        arr_with_correct_types.append(rowArr)

    if withHeader:
        arr_with_correct_types = [headerArr] + arr_with_correct_types

    return arr_with_correct_types

def get_all_info(urlAsString, withHeader=True):
    '''
    :param url:
    :return:
    '''

    # GET INITIAL DATA AS DICTIONARY
    param_dict = build_param_dict_from_url(urlAsString)
    final_arr = []
    firstRun = True
    print param_dict

    for i in range(0,len(QTY_OPTIONS),2):

        print QTY_OPTIONS[i],QTY_OPTIONS[i+1]

        # ITERATE THROUGH QTY_OPTIONS TO CHANGE QTY1/QTY2
        param_dict['qty1'] = QTY_OPTIONS[i]
        param_dict['qty2'] = QTY_OPTIONS[i+1]

        # GET DATA AS 2D LIST
        response = urllib2.urlopen(urlAsString)
        reader = csv.reader(response)
        tmpArr = list(reader)

        # DETERMINE PROPER DATA TYPES FOR EACH COLUMN
        headerArr = tmpArr[0]
        data_types = []
        for head in headerArr:
            for dtype in DATA_TYPES:
                if dtype in head:
                    data_types.append(dtype)
                    break

        # APPLY DATA TYPES AND CREATE CORRECT TYPES
        arr_with_correct_types = []
        for row in tmpArr[1:]:
            rowArr = []
            for i in range(0,len(row)):
                try:
                    result = DATA_TYPE_RELATIONS[data_types[i]](row[i])
                except:
                    result = None
                rowArr.append(result)
            arr_with_correct_types.append(rowArr)

        if withHeader:
            arr_with_correct_types = [headerArr] + arr_with_correct_types

        print arr_with_correct_types

        if firstRun:
            final_arr = arr_with_correct_types
            firstRun = False
        else:
            for row, new_row in zip(final_arr,arr_with_correct_types):
                row.append(new_row[1])
                row.append(new_row[2])

    return final_arr

def save_as_csv(dataArr,outputFileName):
    '''
    :param dataArr:
    :param outputFileName:
    :return:
    '''

    with open(outputFileName, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(dataArr)

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

def filter_data_by(arr2d, filterType):
    '''
    Filters data using the headers to find
    :param arr2d:
    :param paramType:
    :return: array of
    '''

    # FIND INDEX FOR SELECTED PARAMETER COLUMNS FOR DATA SET
    filterColIndex = []
    for colNum in range(0,len(arr2d[0])):
        print colNum, arr2d[0][colNum]
        if filterType in arr2d[0][colNum]:
            filterColIndex.append(colNum)

    # GET DATA FROM ARR
    paramArr = []
    for colIndex in filterColIndex:
        header = [arr2d[0][colIndex]]
        data = [arr2d[i][colIndex] for i in range(1, len(arr2d))]
        paramArr.append(header+data)

    return paramArr

# SECONDARY FUNCTIONS

def build_param_dict_from_url(urlAsStr):

    # STRIP URL OF BASIC INFORMATION
    urlInfo = urlAsStr.partition(".edu/")
    base, middle, info = str(urlInfo[2]).partition("id/")
    urlList = str('id/' + info).split('/')
    print info


    # GENERATE CATEGORIES AND ENTRIES
    categories = urlList[::2]
    categoryEntries = urlList[1::2]

    # BUILD DICTIONARY
    urlDict = {}
    for cat, ent in zip(categories, categoryEntries):
        urlDict[cat] = ent

    return urlDict

def get_data_by_param(arr2d, paramType="vol"):
    '''
    Filters data using the headers to find
    :param arr2d:
    :param paramType:
    :return: array of
    '''

    return filter_data_by(arr2d, paramType)

def get_data_by_lane(arr2d, lane=1):
    return filter_data_by(arr2d, str(lane))

def get_all_data(urlAsString, withHeader=True):
    '''
    :param url:
    :return:
    '''

    url_param_dict = build_param_dict_from_url(urlAsString)

    # GET DATA AS 2D LIST
    response = urllib2.urlopen(urlAsString)
    reader = csv.reader(response)
    tmpArr = list(reader)

    # DETERMINE PROPER DATA TYPES FOR EACH COLUMN
    headerArr = tmpArr[0]
    data_types = []
    for head in headerArr:
        for dtype in DATA_TYPES:
            if dtype in head:
                data_types.append(dtype)
                break

    # APPLY DATA TYPES AND CREATE CORRECT TYPES
    arr_with_correct_types = []
    for row in tmpArr[1:]:
        rowArr = []
        for i in range(0,len(row)):
            try:
                result = DATA_TYPE_RELATIONS[data_types[i]](row[i])
            except:
                result = None
            rowArr.append(result)
        arr_with_correct_types.append(rowArr)

    if withHeader:
        arr_with_correct_types = [headerArr] + arr_with_correct_types

    return arr_with_correct_types

# DEVELOPING FUNCTIONS

URL_ORDER = ['id','start','stop','starttime','endtime','corridor','qty1','qty2','res','group','days','lane','format','name']

def build_url(url_param_dict):
    base_url = 'http://portal.its.pdx.edu/api/stations/twoquantityungroupedsimplerange/'
    end_url = ''

    for category in URL_ORDER[:-2:]:
        end_url += category + "/" + str(url_param_dict[category]) + "/"
    end_url += "name" + "/" + str(url_param_dict["name"])

    return base_url + end_url

# ASSIGNMENT FUNCTIONS

def vmt(segment_vol, influence_area):
    return segment_vol * influence_area

def vht(segment_vol, influence_area, segment_ave_speed):
    return segment_vol * influence_area / segment_ave_speed

def pmt(segment_vol, influence_area, persons):
    return vmt(segment_vol, influence_area) * persons

def pht(segment_vol, influence_area, segment_ave_speed, persons):
    return vht(segment_vol, influence_area, segment_ave_speed) * persons

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
    #arr = csv_url_to_2d_array(TEST_URL)
    #save_as_excel(arr)
    #print arr

    #get_portal_data2()

    ##arrCol = get_data_by_param(arr)
    #print arrCol
    #print get_station_data()
    #url_param_dict = build_param_dict_from_url(TEST_URL)
    #print 'url_param_dict', url_param_dict
    #print build_url(url_param_dict)

    all_arr = get_all_data(TEST_URL)
    print all_arr

if __name__ == '__main__':     # if the function is the main function ...
    main() # ...call it

# OLD FUNCTIONS


def csv_url_to_2d_array_old(urlAsString):
    '''
    #:param url:
    #:return:
    '''

    response = urllib2.urlopen(urlAsString)
    reader = csv.reader(response)
    return list(reader)

def calc_vmt2(arr2d):

    #for colIndex in volColIndex:
    # FIND INDEX FOR VOLUME COLUMNS FOR DATA SET
    volColIndex = []
    for colNum in range(0,len(arr2d[0])):
        if '_vol' in arr2d[0][colNum]:
            volColIndex.append(colNum)

    # CREATE
    vmtArr = []
    currentColArr = [arr2d[i][colIndex] for i in range(0, len(arr2d))]