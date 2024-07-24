# mynetanalyzer

coded by rodrigo galuppo russo

# Problem Solution 
The chosen problem is the lack of visibility and control over the packets going through a network. This problem is current on the life of network engineers, who must deal with networking, to make them both safe and efficient. Therefore, a solution that could make the network more transparent, with charts and insights would be highly useful for these professionals. This project is called “MyNetAnalyzer”.

# Solution Design
When designing the solution, the goal was to make it at the same time scalable, secure and easy to manage and implement, since it was a tool to be used by network engineers, it could not be a bottleneck on the network infrastructure. Therefore, it was designed based on a microservices architecture. 

With the base concept of microservices in mind, I decided to build a distributed system, where a program would be running on chosen hosts and then they would be broadcasting information in a stream to the server, that would store this information in a database made to work with data streams and provide useful real-time insights on a back-office application.



Having it in mind, A graphical tool was used to draw the solution logically. Dividing it into main 4 layers:

•	Host Layer: Distributed programs in python that would run on the hosts across the network and extract information about the traffic going through the host with Scapy python library and stream it in real time with WebSockets.

•	DB Layer: Database system PostgreSQL with TimeScaleDB extension, for both fast and read capabilities, keeping structured data.


•	Client Layer: Web application with a responsive layout, using ChartJS and ReactJS to show the data in an insightful way. Also using typescript to ensure strong typed data on the frontend, making the program more resilient.

•	Business Logic Layer: Services deployed on docker containers, controlling the logics of the application and communicating with each other via Rest API or WebSockets for the continuous data stream.
	Split into 3 services:
		
o	Producer: Service responsible for receiving the data stream with the information about the traffic of hosts and saving it to the database.
o	Consumer: Service responsible for reading the data from the database and streaming it to the frontend application in real time with WebSockets, working on the data to deliver it processed and ready to be used on the charts.
o	Manager: Service responsible for managing the access control of the user of the frontend application with Flask and JWT token, and responsible for CRUD of entities of the database.



At the end, the whole structure was planned to be delivered on a Proxmox server with 4 host VMs for simulating a network infrastructure, that would interact with the server with their microservices running on docker containers orchestrated by Docker-Compose, for high scalability. The DB was also deployed on a container. While the client react application would be installed on a device using the PWA (Progressive Web App) technology or could be loaded from the browser.


As a security measure, the communication between the producer and the hosts is done via a secure channel with asymmetric encryption, so the hosts have a public key of the producer to encrypt data, while the producer has the private key to decrypt it.
The diagram looked like this:

![image](https://github.com/user-attachments/assets/bb518fe5-0f89-4d51-85f1-647417cb499d)

since a normal database would not be able to handle the high volume of data stream on real timee, it was decided to use the TimeScaleDB extension on PostgreSQL 

# Testing and Validation
During the testing phase an infrastructure was setup on a Proxmox hypervisor environment, to simulate a real scenario, similarity to the diagram 4 virtual machines (VMs) were deployed on the host layer and were used to navigate on the internet, while a server with the services running was processing the requests. Then to find bugs, I went through the pattern-action rules listed on the requirements, to trigger them, and validate if the result was the expected or not.

Link for the DEMO:
https://youtu.be/Feelhz0_djU

# Conclusion
The project met the expectations, because it is a robust, scalable and maintainable solution for the problem it was supposed to solve, meeting all the requirements that were presented, and even being tested in a simulated virtualized environment, planned to mimic a real-world scenario. This project is the result of intense research and development on fields such as software development, cybersecurity, and network engineering, mixed with problem solving techniques to come with an adequate solution for the problem of lack of insights taken from packets going through a network.


# instructions to execute

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
	
