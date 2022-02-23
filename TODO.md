# Misc notes on enhancement ideas (future plans / wishlist)

* Soon(ish): add `miniconda` option for Python setup (in `setup.sh`/`util.sh`)
* *Eventually* eliminate dependence on `gradescope-utils` package; in particular, a (non-exhaustive) wishlist:
  * Output (`result.json`) production is tied to a *successful* unit test run. E.g., informing users about prep/setup steps, is more complicated than it needs to be (if setup fails and tests never get to even start, we have to manually generate `result.json` from scratch; OTOH, if tests complete, then we have to use an undocumented(?) hook to mangle JSON test-runner output).
  * More importantly, support for grading schemes is rudimentary (e.g., "negative" schemes don't seem to be supported at all---beyond allowing negative `weight` values, that is).
  * Furthermore, the decorator setup is rather cumbersome (e.g., each test case has to be annotated *individually*). More generally, it seems it would be very difficult and/or messy to extend the `gradescope-utils` library for even relatively simple things?
* Add proper configuration classes and files (e.g., maybe using `dataclasses` + `click` ?); but first, should probably give some thought to "canonical" Gradescope-independent abstractions / organization...
* Clean up the `testrunner` module (if it can be called that); probably while or after re-doing unittest runners? Take a look at everything else when time.
* Fix up the CLI... `autograder.zip` prep, local unittesting (with or without Docker? -- needs "un-hardcoding" some things, i.e., config see above)... Maybe "steal" some ideas on output / logging APIs (see above) from Click?
