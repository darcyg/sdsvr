ROOTDIR=$(shell pwd)
WORKDIR=$(ROOTDIR)/build


test:
	python dbi.py
	

run:

clean:
	rm -rf $(ROOTDIR)/*.pyc
