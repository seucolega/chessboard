.PHONY:	start-docker docker-user install-local start-local local-user
APP_PATH=chessboard

start-docker:
	@docker-compose up --build
docker-user:
	@docker-compose exec web bash -c "python manage.py createsuperuser"
install-local:
	@cd $(APP_PATH) && make install
start-local:
	@cd $(APP_PATH) && make start
local-user:
	@cd $(APP_PATH) && make user
