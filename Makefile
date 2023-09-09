up:
	docker-compose up -d

down:
	docker-compose -f docker-compose.yaml down && docker down --remove-orphans

up-ci:
	docker-compose -f docker-compose-ci.yaml up -d

up-rebuild-ci:
	docker-compose -f docker-compose-ci.yaml up --build -d

down-ci:
	docker-compose -f docker-compose-ci.yaml down --remove-orphans
