from copy import copy
from typing import Sequence, Optional, Callable, Union

import numpy as np

OtherSliceDef = tuple[Union[int, Callable]]
SkinnySpecs = Optional[tuple[tuple[int, ...], tuple[OtherSliceDef, ...]]]



def gridsearch(
    grid_params: list[str],
    grid_vals: list[Sequence],
    other_params: dict,
    experiment,
    skinny_specs: SkinnySpecs = None,
):
    curr_other_params = copy(other_params)
    gridpoint_selector = []
    if skinny_specs is not None:
        ind_skinny, thin_slices = skinny_specs
    else:
        ind_skinny = tuple(range(len(grid_params)))
        thin_slices = None
    full_results_shape = tuple(len(grid) for grid in grid_vals)
    ndindexer = np.ndindex(full_results_shape)
    full_results = np.empty(full_results_shape)
    full_results.fill(-np.inf)
    for multi_index in ndindexer:
        matches = []
        for ax1, where_others in zip(ind_skinny, thin_slices, strict=True):
            other_axes = list(ind_skinny)
            other_axes.remove(ax1)
            match = True
            # check whether multi_index meets criteria of a particular thin_axis
            for ax2, slice_ind in zip(other_axes, where_others, strict=True):
                if callable(slice_ind):
                    slice_ind = slice_ind(multi_index[ax1])
                # would check: "== slice_ind", but must allow slice_ind = -1
                match *= (multi_index[ax2] == range(full_results_shape[ax2])[slice_ind])
            matches.append(match)
        if any(matches):
            gridpoint_selector.append(multi_index)
    for ind in gridpoint_selector:
        for axis_ind, key, val_list in zip(ind, grid_params, grid_vals):
            curr_other_params[key] = val_list[axis_ind]
        curr_results = experiment.run(
            **curr_other_params, display=False, return_all=True
        )
        if isinstance(experiment, SquaredError):
            curr_results **= 2
        elif isinstance(experiment, AbsoluteError):
            curr_results = np.abs(curr_results)
        full_results[ind] = curr_results
    max_axes = (ind for ind in range(full_results.ndim) if ind not in skinny_specs[0])
    return full_results.max(axis = tuple(max_axes))


# Creating classes in a single line
Experiment = type("Experiemnt", (), {})
AbsoluteError = type("AbsoluteError", (Experiment,), {})
SquaredError = type("SquaredError", (Experiment,), {})


def zip(*iterables, strict=False):
    """PEP618 zip syntax, made available in 3.10"""
    if not iterables:
        return
    iterators = tuple(iter(iterable) for iterable in iterables)
    try:
        while True:
            items = []
            for iterator in iterators:
                items.append(next(iterator))
            yield tuple(items)
    except StopIteration:
        if not strict:
            return
    if items:
        i = len(items)
        plural = " " if i == 1 else "s 1-"
        msg = f"zip() argument {i+1} is shorter than argument{plural}{i}"
        raise ValueError(msg)
    sentinel = object()
    for i, iterator in enumerate(iterators[1:], 1):
        if next(iterator, sentinel) is not sentinel:
            plural = " " if i == 1 else "s 1-"
            msg = f"zip() argument {i+1} is longer than argument{plural}{i}"
            raise ValueError(msg)