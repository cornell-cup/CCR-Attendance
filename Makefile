.PHONY: all test clean node register

all : test

test: 
	cd test && pytest

clean:
	rm -rf src/*.pyc

register:
	python register_card.py res/client_secret.json CCR_Attendance_Node res/config.json

node:
	python run_node.py res/client_secret.json CCR_Attendance_Node res/config.json