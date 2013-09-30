hoonrunedocs
============

A series of scripts for gleaning information about the hoon runes.

To use, just run runegen.py in its directory.  This will create a series of files in the runes/ directory with information about all known hoon runes.  It will also create a csv file (tab delimited) with the same information.  Note that runegen.py depends on hoon.hoon and runelist.  You should be able to update hoon.hoon without issue, but if the format is changed significantly, then the script may require some tweaking.

Right now, it gets code information for all runes except those that are defined on mulitple lines (most sem) and those few that are defined at a different point in the script (most dot).

