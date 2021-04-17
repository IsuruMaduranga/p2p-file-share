Node_Ids = 1 2 3
Main_Client_Name = Sadil
Main_Client_UDP_Server_Port = 6500
Main_Client_Flask_Server_Port = 6000

start:
	cd BS/ && java BootstrapServer >> demo.log 2>&1 &
	for num in $(Node_Ids); do \
	python3 node.py $$((5500 + $$num)) $$((5000 + $$num)) node$$num >> demo.log 2>&1 & \
	done
	python3 node.py $(Main_Client_UDP_Server_Port) $(Main_Client_Flask_Server_Port) $(Main_Client_Name)

clear:
	kill -9 $$(ps -aux | grep -E '[n]ode.py|[B]ootstrapServer' | awk '{print $$2}')
	rm -rf data/*
	rm demo.log
	cd BS/ && rm demo.log	

join:
	python3 node.py $(Main_Client_UDP_Server_Port) $(Main_Client_Flask_Server_Port) $(Main_Client_Name)