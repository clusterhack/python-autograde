<style type="text/css">
  pre code.language-console { line-height: normal; }
</style>

# Python autograding framework for GradeScope

A simple (and quite opinonated) "framework" for Gradescope autograders,
written in Python, for Python assignments.

## Gradescope container

We use the limited shellscript-based method to create the autograder container.  Since the `gradescope/auto-build` container is based on Ubuntu Focal [sic], with no option to use a more recent O/S version, we set up Python from source (using `pyenv`, as of this writing).


### Directory structure summary

```console
📁 /autograder
├─ 📁 source
│  ├─ skeleton.zip [*1]
│  ├─ 📁 assignment [*1]
│  ├─ 📁 pyscope
│  ├─ 📁 etc
│  ├─ run_autograder
│  └─ setup.sh
├─ run_autograder [*2]
├─ setup.sh [*2]
├─ 📁 submission [*2]
└─ 📁 results [*2]
```

Certain design choices were made in order to support backwards compatibility with our prior unit-testing tooling for homework assingment.  In particular, the autograder zipfile may optionally include a `skeleton.zip` file, whose contents will be unzipped into the `assignment` folder.  The latter does not need to exist in the zipfile.  Other than these two items [*1], everything else does not change between assignments.

Gradescope sets up everything else [*2].  We have consciously chosen to re-arrange things within the `source` folder, which should hopefully simplify testing/debugging the setup on a local machine (i.e., without requiring the full Gradescope environment). Also, decoupling the framework from Gradescope (as much as possible) can't be a bad thing, long term...

### Summary of workflow

TODO
