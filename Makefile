db_pw = test123
db_sid = db_uebung
docker_name = db_uebung_ora_19c
pwd = $(shell pwd)
db_data_path = $(pwd)/oracle-19c/

.PHONY: initialize_db
initialize_db:
	mkdir -p $(db_data_path)/oradata
	sudo chown -R 54321:54321 $(db_data_path)
	sudo docker run --name $(docker_name) \
	-p 1521:1521 \
	-e ORACLE_SID=$(db_sid) \
	-e ORACLE_PWD=$(db_pw) \
	-e ORACLE_CHARACTERSET=AL16UTF8 \
	-v $(db_data_path)/oradata/:/opt/oracle/oradata \
	-d doctorkirk/oracle-19c

.PHONY: start_db
start_db:
	sudo docker start -d $(docker_name)

.PHONY: stop_db
stop_db:
	sudo docker stop $(docker_name)

.PHONY: remove_db
remove_db:
	make stop_db
	sudo docker rm $(docker_name)
	sudo rm -R $(db_data_path)
	
.PHONY: reinitialize_db
	make remove_db
	make initialize_db