# SimBio paper

To read the current HTML version, visit:
https://maurosilber.github.io/simbio-paper

The following instructions assume you have cloned the repository

```bash
git clone https://github.com/maurosilber/simbio-paper
```

and are inside the `simbio-paper` directory.

## Install dependencies

To run the benchmarking code and compile the article,
you must install some dependencies.

If you have `conda` installed,
create an environment from the included `environment.yml` file:

```bash
conda env create
```

and install the Python package included in the repository:

```bash
pip install -e .
```

To compile the article,
you must also install Quarto:
https://quarto.org

## Run benchmarks and compile article

```bash
make
```

> Note:
> as `src/perfomance/figures/performance.png` was commited to the repository,
> the benchmarking code is not actually triggered by the Makefile.
> Remove that file to re-run the benchmarks with `make`.
