build_app:
	docker build -t wallet-control-bot .

run_app:
	docker run -p 5000:5000 --rm -it wallet-control-bot