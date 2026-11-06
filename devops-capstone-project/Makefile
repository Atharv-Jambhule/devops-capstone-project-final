install:
	python -m pip install -r requirements.txt

test:
	nosetests

lint:
	flake8 service tests run.py

coverage:
	coverage report

docker-build:
	docker build -t customer-accounts:latest .

k8s-deploy:
	kubectl apply -f k8s/
