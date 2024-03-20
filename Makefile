ROOT = src

RESULTS = $(ROOT)/performance/results/copasi \
	 	  $(ROOT)/performance/results/roadrunner \
	 	  $(ROOT)/performance/results/simbio-numba-lsoda \
	 	  $(ROOT)/performance/results/simbio-numba-numbalsoda \
	 	  $(ROOT)/performance/results/simbio-numpy-lsoda

article.html: article.qmd \
			  $(ROOT)/performance/figures/performance.png \
			  $(ROOT)/ide/ide1.png \
			  $(ROOT)/ide/ide2.png
	quarto render article.qmd --to html

$(ROOT)/performance/figures/performance.png: $(RESULTS)
	python -m performance.plot save

$(RESULTS): $(ROOT)/performance/models.txt
	python -m performance.timer $(notdir $@)
