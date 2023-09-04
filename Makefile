up:
	docker-compose up -d

down:
	docker-compose -f docker-compose.yaml down && docker network prune --force

run:
	docker-compose -f docker-compose-ci.yaml up -d
