## Welcome to the Pyom project! ##

![pytest](https://github.com/bubthegreat/rom24/actions/workflows/pytest.yml/badge.svg)

*rom24* is a re-authoring of the *Rom DikuMUD* derivative using python3.
We've tried to use as few external modules as
possible, but are using the excellent *Miniboa* telnet stack as our core.

The initial goal of the project is to provide a fully working copy of *Rom*, in
python, which can act as a stepping stone to help others convert their aging C
dikurivatives to a more modern language.  On today's hardware, there is little
value in over-optimizing such a small project, and a great deal to gain by
allowing fast and easy coding.

Licensing is still in force, please see the docs for licensing information.

## Installation and Usage ##

```
cd PyRom
pip install -e .
rom24
```
Normal python install via pip should get things started.

The more up-to-date home of the project that this was not forked from is [here](https://bitbucket.org/mudbytes/pyom).

## TO DO ##

* Straighten out legacy loads vs. new loads and remove anything legacy
* Make data consistently relative and make it deployable in docker with volumes
* Add docker and compose for simple local build and testing
* start adding some unit testing
* Move to a more functional paradigm for as much as possible to improve iteration speed (less stateful class shenanigans is better imho)
* Add docstrings to everything as I figure out what the hell it's doing
* Make sure licensing and credits are all still there
* Fix lots and lots of bugs
* Investigate sqllite or another alternative instead of straight json files for performance and sanity
* Change to a real data structure instead of custom class json hooks
* add debug logging everywhere under the sun so it's easier to tell why things are breaking
* Refactor to remove circular dependencies (This is going to be a lot of work, and means stateful classes and functions will have to be redone) but will be worth it.

## Contributing ##

For the love of god, someone please help - I'm doing this because it's fun, but it's more fun to do it together!  Just PR changes - I'm not going to be very picky as long as they're an improvement.

Even if you just pull it and test it locally to open bugs, opening bugs is awesome and appreciated.  If you're interested in becoming an owner on the repo, send me an email at bubthegreat@gmail.com

The typing is incredibly loose with lots of Any getting thrown around - as we add more typing, we'll find more bugs ahead of time.  We're using black for formatting to keep formatting consistent.

If you're going to contribute, please use the pre-commit hooks.  It's got some things that will keep consistent formatting, clean up line endings, etc.
```
pip install -r requirements.txt
pre-commit install
```
