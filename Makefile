ROOT = src/performance

RESULTS = $(ROOT)/results/copasi.csv \
	 	  $(ROOT)/results/roadrunner.csv \
	 	  $(ROOT)/results/simbio-numba-lsoda.csv \
	 	  $(ROOT)/results/simbio-numba-numbalsoda.csv \
	 	  $(ROOT)/results/simbio-numpy-lsoda.csv

all: $(RESULTS) $(ROOT)/figures/performance.png article.html
clean: $(RESULTS)
	rm $^

article.html: article.qmd $(ROOT)/figures/performance.png
	quarto render article.qmd --to html

$(ROOT)/figures/performance.png: $(RESULTS)
	python -m performance.plot save

$(ROOT)/results/roadrunner.csv: $(ROOT)/models.txt
	python -m performance.timer roadrunner
$(ROOT)/results/copasi.csv: $(ROOT)/models.txt
	python -m performance.timer copasi
$(ROOT)/results/simbio-numpy-lsoda.csv: $(ROOT)/models.txt
	python -m performance.timer simbio numpy lsoda
$(ROOT)/results/simbio-numba-lsoda.csv: $(ROOT)/models.txt
	python -m performance.timer simbio numba lsoda
$(ROOT)/results/simbio-numba-numbalsoda.csv: $(ROOT)/models.txt
	python -m performance.timer simbio numba numbalsoda
