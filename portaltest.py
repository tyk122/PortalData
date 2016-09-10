__author__ = 'Troy'

import portal

def instantiate_pds_from_url():
    return portal.PortalDataSet.from_url(portal.TEST_URL)

def station_basics():
    a = portal.PortalDataSet.from_url(portal.TEST_URL)
    a.simple_graph("volume")
    a.basic_graph_all()
    return a

def graph_all_test():
    a = instantiate_pds_from_url()
    a.basic_graph_all()

def main():
   print station_basics()

if __name__ == '__main__':     # if the function is the main function ...
    main() # ...call it