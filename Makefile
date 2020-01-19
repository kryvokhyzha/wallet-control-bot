build_app:
	docker build -t wallet-control-bot .

run_app:
	docker run -p 5000:5000 --env TELEGRAM_API_TOKEN=${TELEGRAM_API_TOKEN} --env TELEGRAM_ADMIN_ID=${TELEGRAM_ADMIN_ID} --rm -it wallet-control-bot