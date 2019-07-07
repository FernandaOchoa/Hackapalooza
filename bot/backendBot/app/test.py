
CLOUDANT_USERNAME="87a61610-7d39-4987-8aa7-5857c13e02b1-bluemix"
CLOUDANT_PASSWORD="2e36a4c5d2cac81aa643ccd2cc767aac8ff46b23fefea12d0c775c4f58c24575"
CLOUDANT_URL="https://87a61610-7d39-4987-8aa7-5857c13e02b1-bluemix:2e36a4c5d2cac81aa643ccd2cc767aac8ff46b23fefea12d0c775c4f58c24575@87a61610-7d39-4987-8aa7-5857c13e02b1-bluemix.cloudantnosqldb.appdomain.cloud"
# Use Cloudant to create a Cloudant client using account
from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey
# Authenticate using an IAM API key
client = Cloudant(CLOUDANT_USERNAME, CLOUDANT_PASSWORD, url=CLOUDANT_URL, connect=True)

session = client.session()
print('Username: {0}'.format(session['userCtx']['name']))
print('Databases: {0}'.format(client.all_dbs()))

result_collection = Result(client["prueba"].all_docs, include_docs=True)
print("Retrieved minimal document:\n{0}\n".format(result_collection[0]))

# Disconnect from the server
client.disconnect()