#Liste des variables

##### Define registry

## url
reg_url = ":5000"

## Login
reg_log = ""

## Password
reg_pwd = ""


##### Define base images WCS v9 docker + tag

## crs-app image
crs_app = "commerce/crs-app:9.0.0.2"

## search-app
search_app = "commerce/search-app:9.0.0.2"

## ts-app
ts_app = "commerce/ts-app:9.0.0.2"

## ts-utils
ts_utils = "commerce/ts-utils:9.0.0.2"

## ts-web
ts_web = "commerce/ts-web:9.0.0.2"

## xc-app
xc_app = "commerce/xc-app:9.0.0.2"

## DB2
ibm_db2 = "ubuntu/db2:11.1"


##### Define db2 vars

db2_srv = "db"			#Serveur db2 
db2_port = "50000"
db2_admin = "db2inst1" 
db2_admin_pwd = ""
db2_user = "wcs"
db2_user_pwd = ""
db2_db = ""			#NE PAS MODIFIER


##### Define SPIUSER Password 

spiuser_name = "spiuser"
spiuser_pwd = ""


#### Define MERCHANTKEY

merchantkey=""


### Define wcsadmin password

wcsadmin_pwd = ""


### Define salt string for encrypt

salt_str = ""


#### define path for docker-compose.yml

docker_compose="/dev/images/python/docker-compose.yml"
