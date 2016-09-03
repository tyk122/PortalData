__author__ = 'Troy'

'''
CAN CURRENTLY
    - SAVE AS: csv, excel
    - GET DATA BY:
        - Lane
        - Parameters

    - Obtain csv data from specified url
    - Can save data

CLASSES
- Station
    -

FUNCTIONS
    - csv_url_to_2d_array
    - get_all_info
    - get_array_from_csv
    - save_as_csv
    - save_as_excel
    - build_param_dict_from_url
    - get_data_by_param
    - get_data_by_lane
    - vmt
    - vht
    - pmt
    - csv_url_2_list
    - get_station_data_as_list
    - get_station_data_as_dict
    - get_station_ids
    - station_lookup
    - station_dictionary
    - create_station_data_backup
    - get_station_data_from_file
    - get_col

DEFINITIONS
- Primary functions:
- Secondary functions: Functions which build upon primary functions for more useful or specific data applications

DEFAULT DICTIONARIES
-   DEFAULT_QUERY_DATA :
-   DEFAULT_OPTIONS :
-   DATA_TYPE_RELATIONS :

DEFAULT LISTS
-   QTY_OPTIONS :
-   DATA_TYPES :
-   URL_DATA_TYPES :

MISCELLANEOUS LITERALS
-   TEST_URL
-   STATION_DATA_BACKUP_PATH
'''

import csv
import urllib2
import openpyxl, pprint
import dateutil.parser
import pandas as pd
import os.path

DEFAULT_QUERY_DATA = {
    'api':'highways',       'unknown':'simplerange',    'id':'1',
    'start':'01-16-2016',   'stop':'01-16-2016',        'starttime':'00:00',
    'endtime':'23:59',      'corridor':'1',             'qty1':'speed',
    'qty2':'volume',        'res':'1hr',                'group':'no',
    'days':'0-1-2-3-4-5-6', 'format':'csv',             'name':'traffic_data.csv'
}

DEFAULT_OPTIONS = {
    'api':'highways',       'unknown':'simplerange',    'id':'1',
    'start':'01-16-2016',   'stop':'01-16-2016',        'starttime':'00:00',
    'endtime':'23:59',      'corridor':'1',             'qty1':'speed',
    'qty2':'volume',        'res':'1hr',                'group':'no',
    'days':'0-1-2-3-4-5-6', 'format':'csv',             'name':'traffic_data.csv'
}

DEFAULT_PARAM_DICT = {
    'lane': 'all',          'group': 'no',              'corridor': '0',
    'qty1': 'speed',        'res': '1hr',               'format': 'csv',
    'stop': '02-04-2016',   'days': '0-1-2-3-4-5-6',    'start': '02-04-2016',
    'qty2': 'volume',       'starttime': '00:00',       'endtime': '23:59',
    'id': '3170',           'name': 'traffic_data.csv'
}

DATA_TYPE_RELATIONS = {
    "vol": int,     "occ": float,           "speed": float,
    "spd": float,   "vmt": int,             "delay": float,
    "vht": float,   "traveltime": float,    "starttime": dateutil.parser.parse
}

STATION_ATTRS = {
    "stationid": int,   "agencyid": int,    "highwayid": int,
    "highwayname": str, "milepost": float,  "description": str,
    "upstream": int,    "downstream": int,  "oppositestation": int,
    "lon": float,       "lat": float
}

DATA_TYPES = ["vol", "occ", "speed", "spd", "vmt", "delay", "vht", "traveltime", "starttime"]
URL_DATA_TYPES = ["vol", "occ", "spd", "vmt", "delay", "vht", "traveltime", "starttime"]
QTY_OPTIONS = ['speed','volume','totalvolume','occupancy','vmt','vht','traveltime','delay']
URL_ORDER = ['id','start','stop','starttime','endtime','corridor','qty1','qty2','res','group','days','lane','format','name']

TEST_URL = 'http://portal.its.pdx.edu/api/stations/twoquantityungroupedsimplerange/id/3170/start/02-04-2016/stop/02-04-2016/starttime/00:00/endtime/23:59/corridor/0/qty1/speed/qty2/volume/res/1hr/group/no/days/0-1-2-3-4-5-6/lane/all/format/csv/name/traffic_data.csv'
STATION_DATA_BACKUP_PATH = "station_data_backup.csv"

STATION_ATTRIBUTES = ['stationid','agencyid','highway', 'highwayname', 'milepost','description','upstream','downstream','oppositestation','lon','lat']
STATION_DEFAULT = {'stationid':1001,'agencyid':103,'highway':1,'highwayname':'I-5','milepost':286.1,'description':'EB Elligsen Loop (2R315) to NB I-5 ','upstream':3165,'downstream':1002,'oppositestation':3113,'lon':-122.76774,'lat':45.33496}


class PortalDataSet:

    SETS_ACTIVE = {}
    SET_COUNT = 0

    def __init__(self, **kwargs):
        # CHECK THAT ALL NECESSARY STATION INFORMATION IS IN KWARGS
        for attribute in URL_ORDER:
            kwargs.setdefault(attribute, DEFAULT_PARAM_DICT[attribute])
            #

        # SET
        for key, value in kwargs.items():
            if key in URL_ORDER:
                setattr(self, key, value)

        self.station_data = get_all_info(kwargs)

        PortalDataSet.SET_COUNT += 1
        self.id = PortalDataSet.SET_COUNT
        PortalDataSet.SETS_ACTIVE[self.id] = self

    @classmethod
    def from_url(cls, url_as_str):
        param_dict = build_param_dict_from_url(url_as_str)
        return PortalDataSet(**param_dict)

class Station:

    STATIONS_ACTIVE = {}

    def __init__(self, **kwargs):

        # CHECK THAT ALL NECESSARY STATION INFORMATION IS IN KWARGS
        for attribute in STATION_ATTRIBUTES:
            kwargs.setdefault(attribute, STATION_DEFAULT[attribute])
            #

        # SET
        for key, value in kwargs.items():
            if key in STATION_ATTRIBUTES:
                setattr(self, key, value)

        self.stationdata = {}

        Station.STATIONS_ACTIVE[self.stationid] = self

    def __str__(self):
        return str([getattr(self,attribute) for attribute in STATION_ATTRIBUTES])

    def get_next_station(self):
        pass

    def get_next_station_id(self):
        id_arr = get_station_ids()
        next_id = int(id_arr.index(self.stationid)) + 1
        if next_id > len(id_arr):
            next_id = 0
        return str(id_arr[next_id])

    def get_prev_station_id(self):
        id_arr = get_station_ids()
        prev_id = int(id_arr.index(self.stationid)) - 1
        if prev_id < 0:
            next_id = len(id_arr) - 1
        return str(id_arr[next_id])

    def get_next_station(self):
        next_id = Station.get_next_station_id(self)
        if next_id in Station.STATIONS_ACTIVE.keys():
            return Station.STATIONS_ACTIVE[next_id]
        else:
            return Station.from_station_id(next_id)

    def get_prev_station(self):
        prev_id = Station.get_prev_station_id(self)
        if prev_id in Station.STATIONS_ACTIVE.keys():
            return Station.STATIONS_ACTIVE[prev_id]
        else:
            return Station.from_station_id(prev_id)



    @classmethod
    def from_station_id(cls, stationid):
        d = station_dictionary(stationid)
        return Station(**d)

class StationData:

    PARAMETER_ELEMENTS = ['lane', 'group', 'corridor', 'qty1', 'res', 'format', 'stop', 'days', 'start', 'qty2', 'starttime', 'endtime', 'id', 'name']
    QTY_OPTIONS = ['speed','volume','totalvolume','occupancy','vmt','vht','traveltime','delay']

    def __init__(self, lane='all', group='no', corridor='0', qty1='speed', res='1hr', file_format='csv', stop=None,
                        days='0-1-2-3-4-5-6', start=None, qty2='volume', starttime='00:00', endtime='23:59',
                        station_id='3170', file_name='traffic_data.csv'):

        self.lane = lane
        self.group = group
        self.corridor = corridor
        self.qty1 = qty1
        self.res = res
        self.file_format = file_format
        self.stop = stop
        self.days = days
        self.start = start
        self.qty2 = qty2
        self.starttime = starttime
        self.endtime = endtime
        self.station_id = station_id
        self.file_name = file_name

    def get_data(self):
        pass

class StationDateData():
    pass

# WORKING FUNCTIONS

######################
# PRIMARY FUNCTIONS
######################

# DATA RETRIEVAL FUNCTIONS

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

def get_all_info_from_url(urlAsString, withHeader=True):
    param_dict = build_param_dict_from_url(urlAsString)
    return get_all_info(param_dict, withHeader)

def get_all_info(paramDict, withHeader=True, acceptPartialDataRows=False):
    '''
    :param url:
    :return:
    '''

    # GET INITIAL DATA AS DICTIONARY
    param_dict = paramDict
    final_arr = []
    firstRun = True

    for i in range(0,len(QTY_OPTIONS),2):
        # ITERATE THROUGH QTY_OPTIONS TO CHANGE QTY1/QTY2
        param_dict['qty1'] = QTY_OPTIONS[i]
        param_dict['qty2'] = QTY_OPTIONS[i+1]
        newUrlAsString = build_url(param_dict)

        # GET DATA AS 2D LIST
        response = urllib2.urlopen(newUrlAsString)
        tmpArr = list(csv.reader(response))
        #        ^(1)^^-------(2)--------^
        # (1)
        # (2)

        # DETERMINE PROPER DATA TYPES FOR EACH COLUMN
        headerArr = tmpArr[0]
        data_types = []
        for head in headerArr:                  # Takes data in headerArr and
            for dtype in DATA_TYPES:            #
                if dtype in head:               #
                    data_types.append(dtype)
                    break

        # APPLY DATA TYPES AND CREATE CORRECT TYPES
        arr_with_correct_types = []
        for row in tmpArr[1:]:
            rowArr = []

            # Turn columns into correct data types, row-by-row
            if acceptPartialDataRows:
                for i in range(0,len(row)):
                    try:
                        result = DATA_TYPE_RELATIONS[data_types[i]](row[i])
                        #        ^--------(1)------^^-----(2)-----^^--(3)-^
                        # (1) Dictionary with pairs for the data        | DATA_TYPE_RELATIONS[data_types[i]](row[i])
                        #     columns and their respective data types   | DATA_TYPE_RELATIONS["vol"](row[i])
                        # (2) String to serve as key for (1)            | int(row[i])
                        # (3) Data [i]th element to process             | int('175')
                    except:
                        result = None
                    rowArr.append(result)
                arr_with_correct_types.append(rowArr)
            else: # If one cell in a row fails, the entire row is rejected. This will execute faster because try/except
                  # are only called every row, not every cell
                try:
                    for i in range(0,len(row)):
                        result = DATA_TYPE_RELATIONS[data_types[i]](row[i])
                        #        ^------------As above--------------------^
                        rowArr.append(result)
                    rowArr.append(result)
                except:
                    pass
        # end loop

        if withHeader: # add headerArr to the larger data set
            arr_with_correct_types = [headerArr] + arr_with_correct_types

        if firstRun:
            final_arr = arr_with_correct_types
            firstRun = False
        else:
            for row, new_row in zip(final_arr,arr_with_correct_types):
                row.append(new_row[1])
                row.append(new_row[2])

    return final_arr

# DATA STORAGE FUNCTIONS

def get_array_from_csv():

    with open(STATION_DATA_BACKUP_PATH) as csvfile:
        arr = list(csv.reader(csvfile))

    return arr

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
    
# DATA PROCESSING FUNCTIONS

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

def view_data_table(arr):
    df = pd.DataFrame(arr)
    return df

# PLOTTING FUNCTIONS

#########################
# SECONDARY FUNCTIONS
#########################

def build_param_dict_from_url(urlAsStr):

    # STRIP URL OF BASIC INFORMATION
    urlInfo = urlAsStr.partition(".edu/")
    base, middle, info = str(urlInfo[2]).partition("id/")
    urlList = str('id/' + info).split('/')

    # GENERATE CATEGORIES AND ENTRIES
    categories = urlList[::2]           # Skip every other in category/entry pair to get category
    categoryEntries = urlList[1::2]     # Skip every other in category/entry pair to get entry

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

# DEVELOPING FUNCTIONS

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

def csv_url_2_list(urlAsStr):
    response = urllib2.urlopen(urlAsStr)
    reader = csv.reader(response)
    return list(reader)

def get_station_data_as_list():
    return csv_url_2_list("http://portal.its.pdx.edu/api/downloads/get_stations/")

def get_station_data_as_dict():
    station_arr = get_station_data_as_list()
    stations_by_id = {}
    headers = station_arr[0][:]
    print headers

    for row in station_arr[1:]:
        station_info = {}
        for head, element in zip(headers, row):
            try:
                station_info[head] = STATION_ATTRS[head](element)
            except:
                station_info[head] = None
        stations_by_id[int(row[0])] = station_info
    print stations_by_id
    return stations_by_id

def get_station_ids():
    tmp_arr = get_station_data_from_file(['stationid'])[1:]
    return [item for sublist in tmp_arr for item in sublist]

def station_lookup(stationid):
    data_arr = get_station_data_from_file()
    station_index = get_station_ids().index(stationid)
    return data_arr[station_index+1]

def station_dictionary(stationid):
    data_arr = station_lookup(stationid)
    station_dict = {}
    for i,j in zip(STATION_ATTRIBUTES,data_arr):
        station_dict[i] = j
    return station_dict

# MAIN FUNCTIONS

def create_station_data_backup(return_arr=True, force_station_data_update=False):

    if not os.path.exists(STATION_DATA_BACKUP_PATH) or force_station_data_update:
        station_data = get_station_data_as_list()
        save_as_csv(station_data, STATION_DATA_BACKUP_PATH)
    else:
        station_data = get_station_data_from_file()

    if return_arr:
        return station_data

def get_station_data_from_file(return_cols=['stationid','agencyid','highwayid','highwayname','milepost','description','upstreamstation','downstreamstation','oppositestation','lon','lat']):

    if 'stationid' not in return_cols:
        return_cols = ['stationid'] + return_cols

    tmpArr = get_array_from_csv()

    if return_cols == ['stationid','agencyid','highwayid','highwayname','milepost','description','upstreamstation','downstreamstation','oppositestation','lon','lat']:
        return tmpArr
    else:
        arr = [[] for i in range(0, len(tmpArr))]
        #      Use loop to make sure empty array has enough columns so that the zip() works.  [[]] will only allow for
        #      1 row with the zip function.  zip() must match lengths

        for col_name in return_cols:
            col_arr = get_col(tmpArr, col_name)
            arr = [row + i for row, i in zip(arr, col_arr)]
        return arr

def get_col(arr, col_name, return_as_2d_array=True):
    j = arr[0].index(col_name)
    rtn_arr = []
    for i in range(0,len(arr)):
        if return_as_2d_array:
            rtn_arr.append([arr[i][j]])
        else:
            rtn_arr.append(arr[i][j])
    return rtn_arr

# SCRIPT MAIN

def main():

    #create_station_data_backup()
    print get_station_data_from_file(['stationid','agencyid'])

if __name__ == '__main__':     # if the function is the main function ...
    main() # ...call it