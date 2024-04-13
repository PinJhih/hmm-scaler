all: server collector detector
.PHONY : all

server:
	docker build -t pj29/server ./api-server

collector:
	docker build -t pj29/collector ./metric-collector

detector:
	docker build -t pj29/detector ./scaling-detector
