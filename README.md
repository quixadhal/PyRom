## Welcome to the Pyom project! ##

*Pyom* is a re-authoring of the *Rom DikuMUD* derivative, using version 3 of the
python programming language.  We've tried to use as few external modules as
possible, but are using the excellent *Miniboa* telnet stack as our core.

In most cases, we're trying to keep the overall feel of the code to be
familiar to people who have worked on the original C implementation of Rom.
Changes are being made where they have to be, often due to *Rom* relying on C
specific memory handling tricks, or where it simplifies something by
re-factoring it.

For example, the old **send_to_char()** function has been replaced by a send()
method in the character class, giving us the much simpler **ch.send()** method.

The initial goal of the project is to provide a fully working copy of *Rom*, in
python, which can act as a stepping stone to help others convert their aging C
dikurivatives to a more modern language.  On today's hardware, there is little
value in over-optimizing such a small project, and a great deal to gain by
allowing fast and easy coding.

We've included a modified version of *Miniboa*.  The original can be found [here](https://code.google.com/p/miniboa/).

and for Python 3, [here](https://code.google.com/p/miniboa-py3/).

You are, of course, required to follow all the licenses of everything this
code was derived from.  This includes the *Miniboa* license, and the licenses
for *Rom*, *Merc*, and *DikuMUD*.

The original C source and data files are included for comparison.  The root
of the python project itself is in **./Rom24/pysrc/**, and this should be used as
the source directory for any IDE you might use.

## Installation and Usage ##

### Windows ###

1. Grab and install a copy of the latest version of Python3 (currently tested on 3.4.x)
1. Ensure that the Python directory is available on your PATH environment variable
1. Open a new command prompt window
1. Navigate to "~/pyom/Rom24/pysrc/"
1. Run "python pyom.py"

If all went well, you should be seeing a barrage of initialization messages and the MUD will be booting up. By default the MUD uses port 1337. You can connect to localhost:1337 and login.

A basic interactive shell is available in **shell.py**.  Various configuration
options can be adjusted in **settings.py**.  If you're running from a command
line, 
```
#!bash

cd ./Rom24/pysrc && python3 ./pyom.py
```
 should get things started.  If
you're using an IDE, make sure you set **pyom.py** as the start file.

## Configuring an Implementor Character ##

An Implementor is a superadmin/root/GM/immortal that has all privilages. To set your first character up as an Implementor:

1. Create a character
1. Get to level 2
1. Save and log out
1. Locate your character file in "~pyom/Rom24/player/<yourname>.json"
1. Open and modify the Trust (Tru) and Level (Levl) variables to 60
1. Save the file
1. Log back into your character
1. If you have access to commands like "load" "restore" and "vnum" then you are an implementor

This isn't finished, and we're still learning python, so things may be
flat-out broken, or done in a really inefficient or silly way, as we unlearn
bad habits C has taught us.

In case you found this elsewhere, the actual up-to-date home of the project
is [here](https://bitbucket.org/mudbytes/pyom).

You can also contact our project lead, Davion, via PM at [mudbytes](http://www.mudbytes.net/).

We hope you have fun with this, and find it useful!

                                                                   -Quixadhal.