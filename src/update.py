#! /usr/bin/env python
"""
This script copies the contents of the 'output' directory (i.e. the built site)
from the 'source' branch to the 'master' branch; Github user/organization pages
only serves websites from the 'master' branch of a repository.

After copying the files to the master directory, it will commit the changes,
and push them to Github.
"""
import subprocess as sp
import os
import os.path
import shutil
import datetime


def ls():
    sp.call(['ls'])
    print '-'*70

# make sure we are in the master branch
cmd = 'git checkout master'.split()
sp.call(cmd)
ls()


# these are associated with the source files we want to copy to master
source_branch = 'source'
source_dir = 'output'

# checkout the source files
cmd = ('git checkout %s -- %s' % (source_branch,
                                  source_dir)).split()
sp.call(cmd)
ls()

# this puts things into a a subdirectory in the master branched named
# after source_dir and stages them for commit
# first, unstage the changes
cmd = ('git reset HEAD %s' % source_dir).split()
sp.call(cmd)
ls()
# now copy the contents from source_dir into the current dir
for (dirpath, dirnames, filenames) in os.walk(source_dir):
    # these are the subdirectories RELATIVE to source_dir
    subdirs = [os.path.relpath(os.path.join(dirpath, dirname), source_dir)
               for dirname in dirnames]
    for filename in filenames:
        this_file = os.path.join(dirpath, filename)
        this_file_rel = os.path.relpath(this_file, source_dir)
        shutil.copy2(this_file, this_file_rel)
ls()
# remove source_dir
shutil.rmtree(source_dir)
# stage the new files for commit
cmd = 'git add .'.split()
sp.call(cmd)
# commit the new files
today = datetime.date.today()
cmd = 'git commit -m'.split() + ["changed on %s" % today]
sp.call(cmd)
# push back to Github
cmd = 'git push'.split()
sp.call(cmd)
