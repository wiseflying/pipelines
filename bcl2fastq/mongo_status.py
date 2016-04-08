#!/usr/bin/env python3
"""MongoDB_status from Bcl2fastq pipeline
"""
# standard library imports
import logging
import sys
import os
import argparse
import getpass

# third party imports
import pymongo

#--- project specific imports
#
from pipelines import generate_timestamp

__author__ = "Lavanya Veeravalli"
__email__ = "veeravallil@gis.a-star.edu.sg"
__copyright__ = "2016 Genome Institute of Singapore"
__license__ = "The MIT License (MIT)"


# global logger
# http://docs.python.org/library/logging.html
LOG = logging.getLogger("")
logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s [%(asctime)s]: %(message)s')


def usage():
    """print usage info"""
    sys.stderr.write("useage: {} [-1]".format(
        os.path.basename(sys.argv[0])))

def mongodb_conn(test_server=False):
    """start connection to server and return conncetion"""
    LOG.warning("TESTING")
    if test_server:
        LOG.warning("Using test server connection")
        conn_str = "qlap33:27017"
        
    else:
        LOG.warning("Using Productionserver connection")
        #conn_str = "qldb01:27017,qlap37:27017,qlap38:27017,qlap39:27017"

    try:
        connection = pymongo.MongoClient(conn_str)
    except pymongo.errors.ConnectionFailure:
        LOG.fatal("Could not connect to the mongoDB server")
        sys.exit(1)
    return connection
    
        
def main():
    """main function"""        
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-r', "--runid",
                        help="Run ID plus flowcell ID",required=True,)
    parser.add_argument('-s', "--status",
                        help="Analysis status",required=True,
                        choices=['START', 'SUCCESS', 'FAILED'])
    parser.add_argument('-id', "--id",
                        help="Analysis id",required=True)                   
    parser.add_argument('-n', "--dry-run", action='store_true')
    parser.add_argument('-t', "--test_server", action='store_true')
    args = parser.parse_args()
    
    connection = mongodb_conn(args.test_server)
    LOG.info("Database connection established")
    db = connection.gisds.test_runcomplete
    results = db.find()
    for record in results:
        # print out the document
        print("test")
        print(record)
    run_number = args.runid
    start_time = args.id
    print (start_time)
    
    user_name = getpass.getuser()
    
    if args.status == "START":
        LOG.info("Send START message")
        db.update({"run": run_number},
        {"$push": 
            {"analysis": {
                "analysis_id" : start_time,
                "startTime" : start_time,
                "userName" : user_name
        }}})
        LOG.info("START message sent")
    elif args.status == "SUCCESS":
        LOG.info("Send SUCCESS message")
        end_time = generate_timestamp()
        print (end_time)
        db.update({"run": run_number, 'analysis.analysis_id' : start_time},
            {"$set": 
                {"analysis.$": {
                    "analysis_id" : start_time,
                    "startTime" : start_time,
                    "EndTimes" : end_time,
                    "userName" : user_name,
                    "Status" :  "SUCCESS"
        }}})
        LOG.info("SUCCESS message sent")
    elif args.status == "FAILED":
        LOG.info("Send FAILEURE message")
        end_time = generate_timestamp()
        print (end_time)
        db.update({"run": run_number, 'analysis.analysis_id' : start_time},
            {"$set": 
                {"analysis.$": {
                    "analysis_id" : start_time,
                    "startTime" : start_time,
                    "Ended" : end_time,
                    "userName" : user_name,
                    "Status" :  "FAILED"
        }}})
        LOG.info("FAILEURE message sent")
        
    # close the connection to MongoDB
    connection.close()
    
    

if __name__ == "__main__":
    LOG.info("MongoDB status update starting")
    main()
    LOG.info("Successful program exit")