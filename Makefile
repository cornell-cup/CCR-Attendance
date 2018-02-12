.PHONY: all test clean node

all : test

test: 
	cd test && pytest

clean:
	rm -rf src/*.pyc
	
node:
	python run_node.py res/client_secret.json CCR_Attendance_Node res/config.json