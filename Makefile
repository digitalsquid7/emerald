start-postgres:
	docker rm -f postgres
	docker run -d --rm --name postgres --network=bridge \
		-p 5432:5432 \
		-e POSTGRES_DB=emerald \
		-e POSTGRES_USER=test \
		-e POSTGRES_PASSWORD=test \
		postgres:latest

upgrade-database:
	alembic upgrade head

start-email-server:
	python3 -m smtpd -c DebuggingServer -n 127.0.0.1:1025
