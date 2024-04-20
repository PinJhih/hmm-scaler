all: server collector detector
.PHONY : all

server:
	docker build -t pj29/server ./api-server

collector:
	docker build -t pj29/collector ./metric-collector

detector:
	docker build -t pj29/detector ./scaling-detector

push: push-server push-collector push-detector
.PHONY: push

push-server:
	docker push pj29/server

push-collector:
	docker push pj29/collector

push-detector:
	docker push pj29/detector
