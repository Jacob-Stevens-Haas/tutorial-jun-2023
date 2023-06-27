import time

import numpy as np

import tutorial_jun_2023


class BoringExperiment(tutorial_jun_2023.SquaredError):
    def __init__(self):
        self.counter = self._run()
        self._count = 0

    def run(self, *args, **kwargs):
        return next(self.counter)
    
    def _run(self):
        while True:
            time.sleep(.5)
            yield self._count
            self._count += 1


def test_gridsearch():
    skinny_specs = (0,1), ((0,),(-1,))
    exp = BoringExperiment()
    grid_params = ["t_end", "noise_stdev", "window_length"]
    grid_vals = [[1,10], [.1, .2], [3,8,11]]
    other_params = {"ic": (0,0), "diff_method": "savitsky-golay"}
    result = tutorial_jun_2023.gridsearch(
        grid_params,
        grid_vals,
        other_params,
        exp,
        skinny_specs=skinny_specs
    )
    expected = np.array([[4., -np.inf], [25., 64.]])

    np.testing.assert_array_equal(expected, result)
