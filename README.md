# RabbitMQ

0. docker rm -f $(docker ps -aq) , and create data folder inside project folder

1. Create a rabbinet network 
docker network create rabbitnet

2. Modify the .env files IP address using the output of below
docker network inspect rabbitnet -f '{{range .IPAM.Config}}{{.Gateway}}{{end}}'

3. docker-compose up --build

4. 
http://localhost:5000/insert_record/PES1/Test1/A
http://localhost:5000/delete_record?SRN=PES1
http://localhost:5000/read_database
http://localhost:5000/health_check?message=hi

4. On MongoDB Compass you can connect to DB using this connection string
"mongodb://root:cc_project@localhost:27018/"

