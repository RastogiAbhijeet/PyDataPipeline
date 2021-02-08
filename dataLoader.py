import pyodbc
import redis
import time

from dbConnector import DatabaseConnection, SQL_DATABASES

# The Goal of this job is to run a job that will
# Pick data from a sql database
def dataExtractionBatchJobSQL(batchSize, offset, dbObject):
    if type(dbObject) == DatabaseConnection:
        data = dbObject.getData(
            query="SELECT * FROM Badges ORDER BY Id OFFSET "+str(offset)+" ROWS FETCH NEXT "+str(batchSize)+" ROWS ONLY;")

def runBatch(batchFunc, **kwargs):
    batchFunc(**kwargs)

if __name__ == "__main__":

    batchID = "1"
    batchSize = 100
    offset = 0

    # This parameter can be tweaked depending upon how much load we want to 
    # put on the machine that is running the DB and also the machine that is 
    # that is running the Batch Job
    # Lesser value will increase the load both on the client and the DB instance
    BATCH_JOB_TIMEOUT = 0.1 # value in seconds

    username = "SA"
    password = "Alaska2017"
    dbConnectionObject = DatabaseConnection(
        'DSN=MSSQLServerDatabase;UID='+username+';PWD=' + password, SQL_DATABASES["MSSQL"])

    redisClient = redis.Redis(host="localhost", port=6379, db=0)

    # Setting a offset count for when we are receiving the batch job invocation for the first time.
    for index in range(1000):

        try:

            redisClient.set(batchID, offset)

            #  Running the batch job
            print("Running batch job id : ", batchID, "Iteration : 1/", index )
            runBatch(dataExtractionBatchJobSQL, batchSize=batchSize, offset=str(offset),
                    dbObject=dbConnectionObject)

            # Getting the value of offset from cache.
            offset += batchSize
            redisClient.set(batchID, offset)

            time.sleep(BATCH_JOB_TIMEOUT)

        except Exception as err:
            print(err)
