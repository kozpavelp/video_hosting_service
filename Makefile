up:
	docker-compose up -d

down:
	docker-compose -f docker-compose.yaml down && docker network prune --force
