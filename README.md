Welcome to the Pyom project!

Pyom is a reauthoring of the Rom DikuMUD derivative, using version 3 of the
python programming language.  We've tried to use as few external modules as
possible, but are using the excellent Miniboa telnet stack as our core.

In most cases, we're trying to keep the overall feel of the code to be
familiar to people who have worked on the original C implementation of Rom.
Changes are being made where they have to be, often due to Rom relying on C
specific memory handling tricks, or where it simplifies something by
refactoring it.

For example, the old send_to_char() function has been replaced by a send()
method in the character class, giving us the much simpler ch.send() method.

The initial goal of the project is to provide a fully working copy of Rom, in
python, which can act as a stepping stone to help others convert their aging C
Dikurivatives to a more modern language.  On today's hardware, there is little
value in over-optimizing such a small project, and a great deal to gain by
allowing fast and easy coding.

We've included a modified version of Miniboa.  The original can be found here:

https://code.google.com/p/miniboa/

and for Python 3, https://code.google.com/p/miniboa-py3/

You are, of course, required to follow all the licenses of everything this
code was derived from.  This includes the Miniboa license, and the licenses
for Rom, Merc, and DikuMUD.

The original C source and data files are included for comparison.  The root
of the python project itself is in ./Rom24/pysrc/, and this should be used as
the source directory for any IDE you might use.

A basic interactive shell is available in shell.py.  Various configuration
options can be adjusted in settings.py.  If you're running from a command
line, cd ./Rom24/pysrc && python3 ./pyom.py should get things started.  If
you're using an IDE, make sure you set pyom.py as the start file.

This isn't finished, and we're still learning python, so things may be
flat-out broken, or done in a really inefficient or silly way, as we unlearn
bad habits C has taught us.

In case you found this elsewhere, the actual up-to-date home of the project
is https://bitbucket.org/mudbytes/pyom 

You can also contact our project lead, Davion,
via PM at: http://www.mudbytes.net/

We hope you have fun with this, and find it useful!

                                                                   -Quixadhal.
