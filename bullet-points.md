# Titles

- SimBio: a static typing, modern Python package to simulate reaction networks
- SimBio: a flexible and extendible Python package for systems modelling

Bioinformatics: Application Notes
- up to 4 pages (approx. 2,600 words or 2,000 words plus one figure)

# Introduction

- Generic introduction:
    - Systems biology modelling
    - Kinetic modelling
    - Tools available, 
- Problem statement, defining gaps
    - Defining and simulating reaction systems:
        - collaborative and iterative construction and testing of models
        - writing equations directly is error-prone and not easily reusable
- Other Python tools
    - (some) wrappers to (non-extendable) external libraries
    - What gap does SimBio address?

- Writing models - 
    - GUI (e.g., COPASI)
    - DSL (e.g, Antimony)
    - Python (e.g, PySB)
- Why writing models with SimBio is better 
- Benefits of IDE integration (syntax highlighting, etc) - error free model coding?

- Our contribution: SimBio
    - standard modern Python to integrate with IDE
    - written in pure Python to easily extend from Python
    - focus on user experience, maintainability, and scalability (other aspect will be discussed in the reproducibility paper)
    - Clean API to create tools (graphs, tables, etc)

# Results

- Introduce 3 layers: symbolite, poincare and simbio
    - easier to understand and develop
    - usable, extendable, and maintainable by a broader community
- symbolite: create symbolic expressions and compile to different backends
- poincare: define and simulate dynamical systems
    - simulate second-order system
    - compose system
    - show typing errors
- simbio: define and simulate reaction networks, mass-action, SBML, SED-ML
    - simulate system with predefined reactions, and stoichiometries
    - load from biomodels and run
- Benchmarking 
    - Validated - reproduced diverse models from BioModels
    - Tellurium vs Simbio -  models
    - pyCOPASI vs Simbio - models testing
- Cool stuff
    - Interactive
    - Sliders example
    - Pandas
    - Generate from sbml?
    - Speed leveraging backends

# Conclusion

- Modular and extensible set of python libraries
- Leverage IDE integration and static typing for model creation

# Notes

- Schematic of package structure
- Show the extendable compilation to different backends or simulation types
