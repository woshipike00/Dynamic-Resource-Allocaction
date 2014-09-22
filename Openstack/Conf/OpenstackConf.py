__author__ = 'pike'

CONTROLLER_HOST = "114.212.189.134"
COMPUTE1_HOST = "114.212.189.139"
COMPUTE2_HOST = "114.212.189.133"
#NETWORKING_HOST = ""
CEILOMETER_HOST = CONTROLLER_HOST

AUTH_URL = "http://%s:35357" % CONTROLLER_HOST
NOVA_URL = "http://%s:8774" % CONTROLLER_HOST

HOST_USERNAME = "nju"
HOST_PASSWORD = "cs"

HOST_ROOT_USERNAME = "root"
HOST_ROOT_PASSWORD = "cs"

USERNAME = "admin"
TENANTNAME = "admin"
PASSWORD = "ADMIN_PASS"

# environment variables
PARAMS = "--os-username %s " % USERNAME + \
         "--os-tenant-name %s " % TENANTNAME + \
         "--os-auth-url %s/v2.0 " % AUTH_URL + \
         "--os-password %s" % PASSWORD

