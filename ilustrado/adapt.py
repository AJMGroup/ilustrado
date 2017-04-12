# coding: utf-8
""" This file contains a wrapper for mutation and crossover. """
from .mutate import mutate
from .crossover import crossover
import numpy as np
import logging


def adapt(possible_parents, mutation_rate, crossover_rate, mutations=None, max_num_mutations=3, debug=False):
    """ Take a list of possible parents and adapt
    according to given mutation weightings.
    """
    total_rate = mutation_rate + crossover_rate
    if total_rate != 1.0:
        logging.debug('Total mutation rate not 1 ({}), rescaling...'
                      .format(total_rate))
    mutation_rate /= total_rate
    crossover_rate /= total_rate
    assert mutation_rate + crossover_rate == 1.0
    mutation_rand_seed = np.random.rand()
    # turn specified mutations string into corresponding functions
    if mutations is not None:
        _mutations = []
        from .mutate import nudge_positions, null_nudge_positions, permute_atoms, random_strain, vacancy
        for mutation in mutations:
            if mutation is 'nudge_positions':
                _mutations.append(nudge_positions)
            elif mutation is 'null_nudge_positions':
                _mutations.append(null_nudge_positions)
            elif mutation is 'permute_atoms':
                _mutations.append(permute_atoms)
            elif mutation is 'random_strain':
                _mutations.append(random_strain)
            elif mutation is 'vacancy':
                _mutations.append(vacancy)
    else:
        _mutations = None

    # if random number is less than mutant rate, then mutate
    if mutation_rand_seed < mutation_rate:
        parent = np.random.choice(possible_parents)
        newborn = mutate(parent,
                         mutations=_mutations,
                         max_num_mutations=max_num_mutations,
                         debug=debug)
        parents = [parent]
    # otherwise, do crossover
    else:
        parents = np.random.choice(possible_parents, size=2, replace=False)
        newborn = crossover(parents, debug=debug)
    # set parents in newborn dict
    newborn['parents'] = []
    for parent in parents:
        for source in parent['source']:
            if source.endswith('.res') or source.endswith('.castep'):
                parent_source = source.split('/')[-1] \
                                      .replace('.res', '').replace('.castep', '')
        newborn['parents'].append(parent_source)
    return newborn
