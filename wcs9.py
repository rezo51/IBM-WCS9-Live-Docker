#!/usr/bin/python

import subprocess
import os 
import docker
import sys
import commands
import json

#import variables
from vars import *

#hide traceback
sys.tracebacklimit = 0

#docker pull images wcs
#login to private registry
myRegistry = docker.DockerClient();
myRegistry.login(username=reg_log, password=reg_pwd, registry=reg_url)

answer = raw_input("Do you wanna pull originals images IBM WCSv9 ? (y/n) : ")
print("")
if answer == 'y':

    # pull images
    print("Pulling originals images WCSv9 ...")
    Image = myRegistry.images.pull(reg_url + "/" + crs_app)
    print(Image, "OK")
    Image = myRegistry.images.pull(reg_url + "/" + search_app)
    print(Image, "OK")
    Image = myRegistry.images.pull(reg_url + "/" + ts_app)
    print(Image, "OK")
    Image = myRegistry.images.pull(reg_url + "/" + ts_utils)
    print(Image, "OK")
    Image = myRegistry.images.pull(reg_url + "/" + ts_web)
    print(Image,"OK")
    Image = myRegistry.images.pull(reg_url + "/" + xc_app)
    print(Image, "OK")
    print("")
    print("######################################")
    print("OK - All originals images WCSv9 pulled")
    print("######################################")
    print("")


elif answer == 'n':
    print("") 


#docker pull images db2
answer = raw_input("Do you wanna pull an image IBM DB2 11 ? (y/n) : ")
print("")
if answer == 'y':

    # pull image db2

    print("Pulling image DB2 ...")
    Image = myRegistry.images.pull(reg_url + "/" + ibm_db2)
    print(Image, "OK")
    print("")
    print("#####################")
    print("OK - Image DB2 pulled")
    print("#####################")
    print("") 

elif answer == 'n':
    print("") 

 
#Define encrypted spiuer password
args = "echo spiuser:" + spiuser_pwd + " | base64"
spiuser_pwd_en64 = subprocess.check_output(args, shell=True)
spiuser_pwd_en64 = spiuser_pwd_en64.rstrip('\n')

#Replace variables in docker-compose.yml
with open('docker-compose.template', 'r') as input_file:
    file = input_file.read()
    file = file.replace("DB2INST1_PASSWORD=", "DB2INST1_PASSWORD=" + db2_admin_pwd)
    file = file.replace("DBUSER=", "DBUSER=" + db2_user)
    file = file.replace("DBADMIN=", "DBADMIN=" + db2_admin)
    file = file.replace("image_db2", reg_url + "/" + ibm_db2)
    file = file.replace("image_utils", reg_url + "/" + ts_utils)
    file = file.replace("image_ts_app", reg_url + "/" + ts_app)
    file = file.replace("image_web", reg_url + "/" + ts_web)
    file = file.replace("image_search_app", reg_url + "/" + search_app)
    file = file.replace("image_crs_app", reg_url + "/" + crs_app)
    file = file.replace("image_xc_app", reg_url + "/" + xc_app)
    file = file.replace("DBNAME=", "DBNAME=" + db2_db)
    file = file.replace("adminPassword=", "adminPassword=" + wcsadmin_pwd)
    file = file.replace("SPIUSER_NAME=", "SPIUSER_NAME=" + spiuser_name)
    file = file.replace("DBPASS=", "DBPASS=" + db2_user_pwd )
    file = file.replace("DBHOST=", "DBHOST=" + db2_srv )
    file = file.replace("DBPORT=", "DBPORT=" + db2_port )
with open('docker-compose.yml', 'w') as output_file:
    output_file.write(file)

#start containers db2
print("Container DB2 starting ...")

args = "docker-compose -f " + docker_compose + " up -d db"
docker_start = subprocess.check_output(args, shell=True)

#identify db2 container
docker_db2 = subprocess.check_output('docker ps | grep db | cut -d" " -f1', shell=True)
docker_db2 = docker_db2.strip()

print("")
print("###########################")
print("OK - Container DB2 started")
print("###########################")
print("")

answer = raw_input("Do you wanna create DB2 Database and its user (y/n) : ")
print("")
if answer == 'y':

    # add db user + pwd
    print("Creating DB2 user ... (5mn)")

    print("")
    print("############################")
    print("OK - User " + db2_user + " created")
    print("############################")
    print("")
    args = "docker exec " + docker_db2 + " useradd -ms /bin/bash " + db2_user
    add_db2_user = subprocess.check_output(args, shell=True)

    args = "docker exec " + docker_db2 + " su -c 'echo " + db2_user + ":" + db2_user_pwd + " | chpasswd'"
    config_db2_pwd = subprocess.check_output(args, shell=True)

    #copy script
    args = "docker cp create_database_db2.sh " + docker_db2 + ":/tmp"
    config_db2 = subprocess.check_output(args, shell=True)
    args =  "docker exec " + docker_db2 + " chmod 655 /tmp/create_database_db2.sh"
    config_db2 = subprocess.check_output(args, shell=True)

    # create database
    print("Creating DB2 Database ...")
    args = "docker exec " + docker_db2 + " su - " + db2_admin + " -c '/tmp/create_database_db2.sh " + db2_db + " " + db2_admin + " " + db2_admin_pwd + " " + db2_user + "'"
    print commands.getstatusoutput(args)
    print("")
    print("####################################")
    print("OK - Database " + db2_db + " created")
    print("####################################")
    print("")

elif answer == 'n':
    print("")


#start containers
print("Container utils starting ...")

args = "docker-compose -f " + docker_compose + " up -d utils"
docker_start = subprocess.check_output(args, shell=True)

#identify utils container
docker_utils = subprocess.check_output('docker ps | grep utils | cut -d" " -f1', shell=True)
docker_utils = docker_utils.strip()

print("")
print("#############################")
print("OK - Container Utils started")
print("#############################")
print("")


answer = raw_input("Do you want add sample data in database (y/n) : ")
print("")
if answer == 'y':

    # add sample data
    print("Preparing Database schema and adding sample data ... (30mn)")
    args = "docker exec " + docker_utils + " su - -c 'cd /opt/WebSphere/CommerceServer90/bin/ && ./initdb_db2_sample.sh production " + db2_db + " " + db2_srv + " " +  db2_port + " " + db2_admin + " " + db2_admin_pwd + " " + db2_user + " " +  db2_user_pwd + " " + merchantkey + " " + salt_str + " " + wcsadmin_pwd + " " + salt_str + " " + spiuser_pwd  + " sampleData'"
    print commands.getstatusoutput(args)

if answer == 'n':

    print("")
    print("Preparing Database schema with no sample data ...(30mn)")
    args = "docker exec " + docker_utils + " su - -c 'cd /opt/WebSphere/CommerceServer90/bin/ && ./initdb_db2_sample.sh production " + db2_db + " " + db2_srv + " " + db2_port + " " + db2_admin + " " + db2_admin_pwd + " " + db2_user + " " +  db2_user_pwd + " " + merchantkey + " " + salt_str + " " + wcsadmin_pwd + " " + salt_str + " " + spiuser_pwd  + " noSample'"
    print commands.getstatusoutput(args)


# configure encrypted merchant key
args = "docker exec " + docker_utils + " su - -c 'cd /opt/WebSphere/CommerceServer90/bin/ && ./wcs_encrypt.sh " + merchantkey + " 1234567890abcdef1234567890abcdef'"
args = subprocess.check_output(args, shell=True)
merkantkey_en = args[213:301]

# configure spiuser_pwd
args = "docker exec " + docker_utils + " su - -c 'cd /opt/WebSphere/CommerceServer90/bin/ && ./wcs_encrypt.sh " + spiuser_pwd + "'"
args = subprocess.check_output(args, shell=True)
spiuser_pwd_en = args[213:257]

#Replace lasts variables in docker-compose.yml
with open('docker-compose.yml', 'r') as input_file:
    file = input_file.read()
    file = file.replace("SPIUSER_PWD=", "SPIUSER_PWD=" + spiuser_pwd_en)
    file = file.replace("MERCHANTKEY_ENCRYPT=", "MERCHANTKEY_ENCRYPT=" + merkantkey_en )
    file = file.replace("<ENCRYPTED_SPIUSER_PASSWORD_BAS64>", spiuser_pwd_en64 )
with open('docker-compose.yml', 'w') as output_file:
    output_file.write(file)

