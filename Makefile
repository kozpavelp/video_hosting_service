up:
	docker-compose up -d

down:
	docker-compose -f docker-compose.yaml down && docker network prune --force

up-ci:
	docker-compose -f docker-compose-ci.yaml up -d
up_ci_rebuild:
	docker-compose -f docker-compose-ci.yaml up --build -d

down_ci:
	docker-compose -f docker-compose-ci.yaml down --remove-orphans
