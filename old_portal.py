__author__ = 'Troy'

from portal import *

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

def old_get_all_info_from_url(urlAsString, withHeader=True):
    param_dict = build_param_dict_from_url(urlAsString)
    return get_all_info(param_dict, withHeader)

def old_get_all_info(paramDict, withHeader=True, acceptPartialDataRows=False):
    '''
    :param url:
    :return:
    '''

    # GET INITIAL DATA AS DICTIONARY
    param_dict = paramDict
    print param_dict
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
                    arr_with_correct_types.append(rowArr)
                except:
                    print "Error " + row
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

    # CHECK THAT ALL NECESSARY STATION INFORMATION IS IN KWARGS
    for attribute in URL_ORDER:
        url_param_dict.setdefault(DEFAULT_PARAM_DICT[attribute], url_param_dict[attribute])

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

    return arr_with_correct_typesdef csv_url_to_2d_array(urlAsString, withHeader=True):
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

def vmt(segment_vol, influence_area):
    return segment_vol * influence_area

def vht(segment_vol, influence_area, segment_ave_speed):
    return segment_vol * influence_area / segment_ave_speed

def pmt(segment_vol, influence_area, persons):
    return vmt(segment_vol, influence_area) * persons

def pht(segment_vol, influence_area, segment_ave_speed, persons):
    return vht(segment_vol, influence_area, segment_ave_speed) * persons

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
        self.data_dict = {}
        print self.station_data

        PortalDataSet.SET_COUNT += 1
        self.id = PortalDataSet.SET_COUNT
        PortalDataSet.SETS_ACTIVE[self.id] = self

    def simple_graph(self,y_axis_type):
        plt.plot(self.data_dict['starttime'],self.data_dict[y_axis_type], label=(y_axis_type+" data"))

    def basic_graph_all(self):
        fig, ax = plt.subplots(4, 2)
        n=0
        for i in range(0,4):
            for j in range(0,2):
                ax[i,j].plot(self.data_dict['starttime'],self.data_dict[QTY_OPTIONS[n]])
                ax[i,j].set_title('Time-'+QTY_OPTIONS[n]+' Chart')
                n+=1

    def advanced_graph(self,y_axis_type):

        #years = mp.dates.mdates.YearLocator()   # every year
        #months = mp.dates.mdates.MonthLocator()  # every month
        #days = mp.dates.mdates.DayLocator()  # every month
        #hours = mp.dates.mdates.HourLocator()  # every month
        #dateFormat = mp.dates.mdates.DateFormatter('%I:%M %p')

        # format the ticks

        fig = plt.figure()
        ax = fig.add_subplot(111)

        main_plot, = plt.plot(self.data_dict['starttime'],self.data_dict[y_axis_type], label=(y_axis_type+" data"))

        ax.legend(handles=main_plot)
        ax.legend(bbox_to_anchor=(1.05,1), loc=2, borderaxespad=0.)

        #ax.xaxis.set_major_locator(hours)
        #ax.xaxis.set_major_formatter(yearsFmt)
        #ax.xaxis.set_minor_locator(months)
        fig.autofmt_xdate()

        plt.xlabel('Time', fontsize=16, color='black', weight='bold')
        plt.ylabel(y_axis_type, fontsize=16, color='black', weight='bold')
        plt.title('Time-'+y_axis_type+' Diagram',fontsize=24, color='black', weight='bold')

        return fig,ax

    @classmethod
    def from_url(cls, url_as_str):
        param_dict = build_param_dict_from_url(url_as_str)
        return PortalDataSet(**param_dict)