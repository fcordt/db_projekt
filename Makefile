db_pw = test123
db_sid = dbuebung
user_name = dbuser
user_pw = test
docker_name = db_uebung_ora_19c
pwd = $(shell pwd)
db_data_path = $(pwd)/oracle-19c/

.PHONY: create_db
create_db:
	mkdir -p $(db_data_path)/oradata
	sudo chown -R 54321:54321 $(db_data_path)
	sudo docker run --name $(docker_name) \
	-p 1521:1521 \
	-e ORACLE_SID=$(db_sid) \
	-e ORACLE_PWD=$(db_pw) \
	-e ORACLE_CHARACTERSET=UTF8 \
	-v $(db_data_path)/oradata/:/opt/oracle/oradata \
	-d doctorkirk/oracle-19c

.PHONY: start_db
start_db:
	sudo docker start $(docker_name)

.PHONY: initialize_db
initialize_db:
	make create_user
	make migrate_db

.PHONY: create_user
create_user:
	./scripts/create_user.sh $(db_pw) $(db_sid) $(user_name) $(user_pw)

.PHONY: stop_db
stop_db:
	sudo docker stop $(docker_name) || true

.PHONY: remove_db
remove_db:
	make stop_db
	sudo docker rm $(docker_name) || true
	sudo rm -R $(db_data_path)
	
.PHONY: recreate_db
recreate_db:
	make remove_db
	make create_db

.PHONY: migrate_db
migrate_db:
	flyway -user=$(user_name) -password=$(user_pw) -url=jdbc:oracle:thin:@localhost:1521/$(db_sid) migrate