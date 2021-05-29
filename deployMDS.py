import sys
import os


def helpUsage():
    print('Usage: deployMDS.py [-help]')
    print('      [-fromLocation] MDS jar location')
    exit()


for i in range(len(sys.argv)):
    if sys.argv[i] in ("-help"):
        helpUsage()
    elif sys.argv[i] in ("-fromLocation"):
        if i+1 < len(sys.argv):
            pfromLocation = sys.argv[i+1]

if len(pfromLocation) == 0:
    print('Missing required arguments (-fromLocation)')
    print(' ')
    helpUsage()

try:
    print("INFO: Connecting to Admin Server")
    connect(os.environ["SOA_CREDENTIALS_USR"],
            os.environ["SOA_CREDENTIALS_PSW"], os.environ["SOA_ADMIN_SERVER_URL"])
except:
    print("ERROR: Connecting to Admin Server")
    raise

try:
    print("INFO: Importing MDS")
    importMetadata(application=os.environ["SOA_APP_NAME"], server=os.environ["SOA_MS_SERVER_NAME"], fromLocation=pfromLocation, remote=true, docs='/**')
except:
    print("ERROR: Importing MDS ", sys.exc_info()[0])
    raise

exit()
