build_app:
	docker build -t wallet-control-bot .

run_app:	
	docker run -p 5000:5000 --env TELEGRAM_API_TOKEN=${TELEGRAM_API_TOKEN} \
							--env TELEGRAM_ADMIN_ID=${TELEGRAM_ADMIN_ID} \
							--env DB_USER=${DB_USER} \
							--env DB_PASSWORD=${DB_PASSWORD} \
							--env DB_HOST=${DB_HOST} \
							--env DB_NAME=${DB_NAME} \
							--env DB_USER_COLLECTION_NAME=${DB_USER_COLLECTION_NAME} \
							--env DB_CATEGORY_COLLECTION_NAME=${DB_CATEGORY_COLLECTION_NAME} \
							 --rm -it wallet-control-bot