#!/usr/bin/env python

_MODULE_NAME = "job_generator"
_MODULE_VERSION = "v0.1.0"
_REVISION_DATE = "2015-06-24"
_AUTHORS = "Johannes Hachmann (hachmann@buffalo.edu) and William Evangelista (wevangel@buffalo.edu)"
_DESCRIPTION = "This module generates the computational chemistry jobs."

# Version history timeline:
# v0.1.0 (2015-06-24): basic implementation
# v0.1.1 (2016-02-25): changed so you can select a library

###################################################################################################
# TASKS OF THIS MODULE:
# -generate the computational chemistry jobs
# -prioritize the jobs pool
###################################################################################################

###################################################################################################
# TODO:
#
###################################################################################################

import sys
import os
import shutil
import curses

from misc import (chk_mkdir)
from template_generator import generate_template, runmenu, showresult


###################################################################################################

def generate_jobs():
    """
        This function generates the computational chemistry jobs.
    """
    cwd = os.getcwd()

    menu = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    curses.start_color()
    menu.keypad(1)

    libraries = ['Available libraries', 'Please choose a library: ', 'Exit Program']
    jtype = ['Available job types', 'Please choose a length for your jobs: ', 'short', 'long', 'priority', 'Previous Menu']
    files = []
    for root, directories, filenames in os.walk(cwd + '/screeninglib'):
        for directory in directories:
            if filter(os.path.isdir, [os.path.join(root + '/' + directory, file) for file in
                                      os.listdir(os.path.join(root, directory))]):
                files.append(os.listdir(os.path.join(root, directory))[0:10])
                libraries.insert(-1, os.path.join(root, directory))

    menus = {0: libraries, 1: jtype}
    menu_names = {0: 'Library', 1: 'Job Type'}
    options = {0: '', 1: ''}
    i = 0
    while i <= len(menus):
        if i == len(menus):
            pos = showresult(menu, menu_names, options)
            if pos == 1:
                i = 0
            else:
                break
        pos = runmenu(menu, menus[i])
        options[i] = menus[i][pos]
        if i == 0 and pos == menus[0].index('Exit Program'):
            break
        elif i != 0 and pos == menus[i].index('Previous Menu'):
            i += -1
        else:
            i += 1
    
    library = options[0]
    library_name = library.rsplit('/')[-1]
    job_type = options[1] + '/'

    curses.nocbreak()
    curses.echo()
    curses.curs_set(1)
    menu.keypad(0)
    curses.endwin()

    if library != 'Exit Program':
        lib = os.listdir(library)
    else:
        sys.exit(0)

    # Not sure this is the best way to get the template should maybe ask which template to use
    template = generate_template()
    with open(template, 'r', 0) as jt:
        job_template = jt.readlines()
    job_template = tuple(job_template)
    for folder in lib:
        if '.dat' in folder:
            pass
        else:
            folder_dir = cwd + '/jobpool/' + job_type + library_name + '_' + folder
            chk_mkdir(folder_dir)
            for geo in os.listdir(library + '/' + folder):
                temp = list(job_template)
                job_file = library + '/' + folder + '/' + geo
                job_dir = folder_dir + '/' + geo.split('.')[0]
                chk_mkdir(job_dir)
                shutil.copy(job_file, job_dir + '/' + geo)
                temp.append('* xyzfile 0 1 ' + geo + '\n')
                with open(job_dir + '/' + geo.split('.')[0] + '.inp', 'w') as tmp:
                    tmp.writelines(temp)


def prioritize_pool():
    """
        This function prioritizes the jobs pool.
    """

# TODO: write this function creating all the stuff in the dummy_project, including the config file containing the project name
