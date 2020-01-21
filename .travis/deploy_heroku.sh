#!/bin/sh

wget -qO- https://toolbelt.heroku.com/install-ubuntu.sh | sh
heroku plugins:install heroku-container-registry
docker login -u _ --password=$HEROKU_API_KEY registry.heroku.com

heroku config:set TELEGRAM_API_TOKEN=$TELEGRAM_API_TOKEN --app $HEROKU_APP_NAME
heroku config:set TELEGRAM_ADMIN_ID=$TELEGRAM_ADMIN_ID --app $HEROKU_APP_NAME

heroku config:set DB_USER=$DB_USER --app $HEROKU_APP_NAME
heroku config:set DB_PASSWORD=$DB_PASSWORD --app $HEROKU_APP_NAME
heroku config:set DB_HOST=$DB_HOST --app $HEROKU_APP_NAME
heroku config:set DB_NAME=$DB_NAME --app $HEROKU_APP_NAME
heroku config:set DB_USER_COLLECTION_NAME=$DB_USER_COLLECTION_NAME --app $HEROKU_APP_NAME
heroku config:set DB_CATEGORY_COLLECTION_NAME=$DB_CATEGORY_COLLECTION_NAME --app $HEROKU_APP_NAME


heroku container:push web --app $HEROKU_APP_NAME
heroku container:release web --app $HEROKU_APP_NAME
heroku ps:scale web=1 --app $HEROKU_APP_NAME