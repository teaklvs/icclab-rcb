'''
Created on Jan 3, 2014

@author: kolv
'''

import ceilometer_api
import compute_api
import keystone_api
import textwrap
import sys

def main(argv):
    print "Hello There. This is a simple test application making a test API call to OpenStack"
    auth_uri = 'http://160.85.231.80:35357' #internal test-setup, replace it with your own value
    #auth_uri = 'http://160.85.4.11:5000' #internal test-setup, replace it with your own value
    status, token_data = keystone_api.get_token_v3(auth_uri)
    if status:
        print 'The authentication was successful, below are the data we got:'
        print '--------------------------------------------------------------------------------------------------------'
        print '%1s %32s %2s %64s %1s' % ('|', 'key', '|', 'value', '|')
        print '--------------------------------------------------------------------------------------------------------'
        for key, value in token_data.iteritems():
            if key not in {'token-id'}:
                print '%1s %32s %2s %64s %1s' % ('|', key, '|', value, '|')
        print '--------------------------------------------------------------------------------------------------------'
        print 'The authentication token is: ', token_data["token-id"]
        pom=token_data["token-id"]
        #wrapped_text = textwrap.wrap(token_data["token-id"], 104)
        #for i in range(len(wrapped_text)):
        #    print wrapped_text[i]
    else:
        print "Authentication was not successful."
    if status:
        
        status, server_list = compute_api.get_server_list(token_data["token-id"], token_data["computev3"])
        if status:
            print "The list of servers are printed next."
            print server_list
        status, meter_list = ceilometer_api.get_meter_list(pom, token_data["metering"])
        if status:
            print "The list of available meters are printed next."
            print '--------------------------------------------------------------------------------------------------------------------------'
            print '%1s %16s %2s %10s %2s %10s %2s %70s %1s' % ('|','meter-name', '|', 'meter-type', '|', 'meter-unit', '|', 'meter-id', '|')
            print '--------------------------------------------------------------------------------------------------------------------------'
            for i in range(len(meter_list)):
                print '%1s %16s %2s %10s %2s %10s %2s %70s %1s' % ('|', meter_list[i]["meter-name"], '|', meter_list[i]["meter-type"], '|', meter_list[i]["meter-unit"], '|', meter_list[i]["meter-id"].strip(), '|')
            print '--------------------------------------------------------------------------------------------------------------------------'
            #print meter_list
            #st,stat_list=ceilometer_api.meter_statistics(meter_list[1]["meter-id"],token_data["metering"],token_data["token-id"])
        st,stat_list=ceilometer_api.meter_statistics(meter_list[0]["meter-name"], token_data["metering"],pom)
        if status:
            print "The statistics for your meters is printed next."
            print '--------------------------------------------------------------------------------------------------------------------------'
            
            for i in range(len(stat_list)):
                print "Average: " + str(stat_list[i]["average"]) 
                print "Count: " + str(stat_list[i]["count"])
                print "Duration: "+ str(stat_list[i]["duration"]) 
                print "Duration end: " + str(stat_list[i]["duration-end"]) 
                print "Duration start: "+ str(stat_list[i]["duration-start"]) 
                print "Max: " + str(stat_list[i]["max"])
                print "Min: " + str(stat_list[i]["min"]) 
                print "Period: " + str(stat_list[i]["period"]) 
                print "Period end: " + str(stat_list[i]["period-end"]) 
                print "Period start: " + str(stat_list[i]["period-start"]) 
                print "Sum: " + str(stat_list[i]["sum"]) 
                print "Unit: " + str(stat_list[i]["unit"]) 
                print "Group by: " + str(stat_list[i]["group-by"]) 
            print '--------------------------------------------------------------------------------------------------------------------------'
            
    return True
    
if __name__ == '__main__':
    main(sys.argv[1:])