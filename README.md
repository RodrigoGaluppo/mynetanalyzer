# mynetanalyzer

coded by rodrigo galuppo russo

##instructions

get docker image for PostgreSQL with TimeScaleDB and run it on localhost with default port

install nodejs
install python

open host folder 
install libraries with pip install -r requirements.txt
change configuration on default.conf server to localhost
execute main.py

open bll
	open producer folder
	edit default.conf file with the configuration to log on the DB
	install libraries with pip install -r requirements.txt
	execute main.py

	open manager folder
	edit default.conf file with the configuration to log on the DB
	install libraries with pip install -r requirements.txt
	execute main.py

	open consumer folder
	edit default.conf file with the configuration to log on the DB
	install libraries with pip install -r requirements.txt
	execute main.py

open frontend folder
	run npm i on the folder to install libraries
	change the config on apiClient file wiht ip of the consumer and the manager, both localhost, and keep the ports unless if you changed on default.conf
	run npm start, to start on localhost:3000 by default the frontend

login on the portal with default credentials unless if you changed on default.conf on the manager folder
	admin
	password123

chnage password t a chosen one
	
