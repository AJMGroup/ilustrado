# `ilustrado`

## Summary

`ilustrado` is a Python package that implements a highly-customisable massively-parallel genetic algorithm for *ab initio* crystal structure prediction (CSP), with a focus on mapping out compositional phase diagrams. The aim of `ilustrado` was to provide a method of extending CSP results generated with random structure searching (AIRSS) or extrapolating from known chemically-relevant systems (species-swapping/prototyping).

The API is [fully-documented](http://www.tcm.phy.cam.ac.uk/~me388/ilustrado) and the source code can be found on [BitBucket](https://bitbucket.org/me388/ilustrado). `ilustrado` makes extensive use of the [matador](https://tcm.phy.cam.ac.uk/~me388/matador) API and interfaces with [CASTEP](http://www.castep.org/) for DFT-level relaxations. Written by [Matthew Evans](http://www.tcm.phy.cam.ac.uk/~me388) (me388@cam.ac.uk).

By default, fitnesses are evaluated as the distance from a binary or ternary convex hull that is passed as input. Duplicate structures are filtered out post-relaxation based on pair distribution function overlap. The standard mutation operators are implemented: cell and position noise, vacancies, and atom permutation and transmutation. Additionally a Voronoi-based mutation has been implemented:
1. Each of the $N$ atoms of randomly chosen species $\mathrm{A}$ are removed from the cell.
2. The Voronoi decomposition of the remaining atoms is calculated.
3. $K$-means clustering is applied to the Voronoi points to split them into $N\pm\Delta$ clusters, where $\Delta$ is a random integer less than $\sqrt(N)$.
4. $N\pm\Delta$ atoms of species $\mathrm{A}$ are added to the cell at the centres of these clusters.
This mutation is effective when studying materials that have one light, mobile element, for example Li. The species $\mathrm{A}$ can be specified by the user or chosen randomly.

Crossover is performed with the standard cut-and-splice method [1] to ensure transferrability over many types of material systems. This method cuts a random fraction from each parent cell and splices them back together; in `ilustrado` efforts are made to align the cells such that the cutting axes are approximately commensurate before crossover.

Several physical constraints (minimum atomic separations, densities, cell shapes) are applied to the trial structures before relaxation to improve efficiency. In order to maintain population diversity as the simulation progresses, the user can optionally disfavour frequently-visited regions of composition space.

The entrypoint is a Python script that creates an `ArtificialSelector` object with the desired parameters (documented [here](http://www.tcm.phy.cam.ac.uk/~me388/ilustrado/ilustrado.html#ilustrado.ilustrado.ArtificialSelector)). Many examples can be found in `examples/`. There are two `compute_mode`s in which to run `ilustrado`.
- `compute_mode='direct'` involves one `ilustrado` processes spawning `mpirun` calls either on local or remote partitions (i.e. either a node list is passed for running on a local cluster, or `ilustrado` itself is submitted as a HPC job). In this case, the user must manually restart the GA when the job finishes.
- `compute_mode='slurm'` performs the GA in interruptible steps; submitting `ilustrado` as a job will lead to the submission of many slurm array jobs for the relaxation, and a dependency job that re-runs the `ilustrado` process to check on the relaxations. In this case, the user only needs to submit one job (tested on 6400 cores/200 nodes without issue).

[1] Deaven, D. M.; Ho, K. M. Molecular Geometry Optimization with a Genetic Algorithm. Phys. Rev. Lett. 1995, 75, 288, (10.1103/PhysRevLett.75.288)[https://doi.org/10.1103/PhysRevLett.75.288]


## New in v0.3b:

- `sandbagging` of composition space
- `compute_mode='slurm'` that makes use of array jobs for "infinite" horizontal scalability
- improved documentation and examples

## API Docs

- [Auto-generated API docs](http://www.tcm.phy.cam.ac.uk/~me388/ilustrado/ilustrado.html)
