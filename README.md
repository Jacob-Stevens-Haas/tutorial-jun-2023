NOTE: To enable CI actions on forks, you need to navigate to the "actions" tab on your fork, then click "enable actions on fork".  Any 
commits to your fork's `master` branch afterwrards should trigger the github action on your fork.  Post an issue here if there's
any difficulty!

# AI Institute for Dynamical Systems - ML Workshop 2023
[slides](https://docs.google.com/presentation/d/15KVsWfko4CWu30c_59Hss7pz4KbnE7-GR8dUxXfNC2o/edit?usp=sharing)

This is an example repository for my talk on "Software Engineering Best
Practices for Research".  It's a simple package with one function: gridsearch.
I wrote the original function for practical work, but this version is heavily
modified to (a) have more poorly factored code, and (b) remove a bunch of
distracting functionality.

The goal is to get the CI to pass the three failing jobs.  BAlready there's one
job that is green and should remain green as you refactor.  Begin by forking
this repository.  Then, read the following prompts (and optionally, 
.github/workflows/main.yml) and start committing to your fork.

# Problem 1: code formatting
Adding a pre-commit for black, the python formatter, will turn the linting
CI green.  Of course, downloading and manually running black would also work,
but not the point.

# Problem 2: pyproject.toml missing dependencies (and \[optional\] dependencies)

This package depends upon numpy.  Development work requires pytest and
pytest-fail-slow.  We'd like people to just be able to run 

```
pip install /path/to/project
```

But that won't also install dependencies unless they're declared in project
metadata.  Likewise, we want developers to be able to install all of the
development dependencies with 

```
pip install /path/to/project[dev]
```

# Problem 3: Test is too slow - refactor code

The main function, `gridsearch()` allows users to pass `skinny_specs` in order
to short-circuit the exhaustive gridsearch (default) by specifying which axes
of the grid are not mutually important.  This is exactly the kind of index-heavy
computation, with it's own limited semantics, that's best extracted from another
function.

In particular, our (1) test for `gridsearch()` requires an experiment, which is
slow to run (simulating a large matrix inversion for a part that is difficult
to mock up).  By refactoring out the indexing computation about `skinny_specs`,
we can test that part separately.  That means that any integration tests to
`gridsearch()` wouldn't need to test out that argument.

So find the essential lines of code that you believe need to be extracted,
create a test for the extracted function, and shrink the test for the overall
logic of `gridsearch()` to just testing how it deals with `SquaredError` and
`AbsoluteError` experiments.  When the tests are each < 2 seconds, this CI job
will turn green.

There's also some low-hanging fruit around indirection and unneccessary
`isinstance() conditionals.

Disclaimer: 
Making a problem that is nuanced enough to not be trivial but solveable in a
short amount of time is pretty tricky.  I may have obscured too much of the
functionality to make the refactoring clear, or I may have left distracting
artifacts from code I removed. :shrug: YMMV.
