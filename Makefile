ROOTDIR=$(shell pwd)
WORKDIR=$(ROOTDIR)/build


test:
	python dbi.py
	

run:
	python app.py


clean:
	rm -rf $(ROOTDIR)/*.pyc
