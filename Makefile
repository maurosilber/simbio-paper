ROOT = src

RESULTS = $(ROOT)/performance/results/copasi.csv \
	 	  $(ROOT)/performance/results/roadrunner.csv \
	 	  $(ROOT)/performance/results/simbio-numba-lsoda.csv \
	 	  $(ROOT)/performance/results/simbio-numba-numbalsoda.csv \
	 	  $(ROOT)/performance/results/simbio-numpy-lsoda.csv

article.html: article.qmd \
			  $(ROOT)/performance/figures/performance.png \
			  $(ROOT)/ide/ide1.png \
			  $(ROOT)/ide/ide2.png
	quarto render article.qmd --to html

$(ROOT)/performance/figures/performance.png: $(RESULTS)
	python -m performance.plot save

$(ROOT)/performance/results/roadrunner.csv: $(ROOT)/performance/models.txt
	python -m performance.timer roadrunner
$(ROOT)/performance/results/copasi.csv: $(ROOT)/performance/models.txt
	python -m performance.timer copasi
$(ROOT)/performance/results/simbio-numpy-lsoda.csv: $(ROOT)/performance/models.txt
	python -m performance.timer simbio numpy lsoda
$(ROOT)/performance/results/simbio-numba-lsoda.csv: $(ROOT)/performance/models.txt
	python -m performance.timer simbio numba lsoda
$(ROOT)/performance/results/simbio-numba-numbalsoda.csv: $(ROOT)/performance/models.txt
	python -m performance.timer simbio numba numbalsoda

clean: $(RESULTS)
	rm $^
