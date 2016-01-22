__author__ = 'Troy'

import csv
import urllib2
import openpyxl, pprint

def get_portal_data():
    url = 'http://portal.its.pdx.edu/Portal//index.php/api/highways/simplerange/id/1/start/01-16-2016/stop/01-16-2016/starttime/00:00/endtime/23:59/corridor/1/qty1/speed/qty2/volume/res/1hr/group/no/days/0-1-2-3-4-5-6/format/csv/name/traffic_data.csv'
    response = urllib2.urlopen(url)
    cr = csv.reader(response)

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

QTY1_OPTIONS = {
    'speed': 'speed',
    'volume': 'volume'
}

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

# SCRIPT MAIN

def main():
    # define the variable 'current_time' as a tuple of time.localtime()
    arr = csv_url_to_2d_array(TEST_URL)
    save_as_excel(arr)
    print arr

if __name__ == '__main__':     # if the function is the main function ...
    main() # ...call it