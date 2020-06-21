
.PHONY: run plot config install
all: run plot 
run:
	python3 bgm.py
plot:
	python3 plot_wav.py
config:
	python3 wavecfg.py
install:
	./pip3.userinstall.sh
