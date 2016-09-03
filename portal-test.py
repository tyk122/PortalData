__author__ = 'Troy'

import portal

def station_basics():
    a = portal.PortalDataSet.from_url(portal.TEST_URL)

def main():
    station_basics()

if __name__ == '__main__':     # if the function is the main function ...
    main() # ...call it