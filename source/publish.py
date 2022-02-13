#!/usr/bin/env python

"""
Build documentation by compiling README.md, .md, and .rst and publish it to GitHub Pages.

Note:
    This script should NOT be run from source directory, use its link in root directory of this repository
    to build the documentation.
"""

import os
import glob
import shutil
import sys

import cmder

CWD = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(CWD, 'source')
CACHE = os.path.join(SOURCE, 'cache')
PROJECT = os.path.join(SOURCE, 'notes')
os.makedirs(CACHE, exist_ok=True)


def update_doc():
    """
    Update top level doc by replacing placeholder __TOC__ with .md and .rst files list.
    
    :return: a list of top level docs.
    """
    
    folders, toc = os.listdir(PROJECT), []
    for folder in folders:
        source = os.path.join(PROJECT, folder, 'README.md')
        target = os.path.join(CACHE, folder, f'{folder}.md')
        if os.path.exists(source):
            os.makedirs(os.path.join(CACHE, folder), exist_ok=True)
            toc.append(os.path.join(os.path.basename(CACHE), folder, f'{folder}.md'))

            os.chdir(os.path.join(PROJECT, folder))
            files = [file for file in glob.iglob('*.md') if not file.endswith('README.md')]
            files += glob.glob('*.rst')
            
            for file in files:
                shutil.copy(file, os.path.join(CACHE, folder, file))

            with open(source) as f, open(target, 'w') as o:
                o.write(f.read().replace('__TOC__', '\n'.join(files)))
    return toc


def update_master_doc(toc):
    """
    Update master doc by replacing placeholder __TOC__ with top level doc list.
    
    :param toc: list, a list of top level docs.
    :return:
    """
    
    with open(os.path.join(SOURCE, 'index.template.md')) as f, open(os.path.join(SOURCE, 'index.md'), 'w') as o:
        o.write(f.read().replace('__TOC__', '\n'.join(sorted(toc))))


def main():
    try:
        message = sys.argv[1]
        toc = update_doc()
        update_master_doc(toc)
        cmder.run('make html', cwd=CWD, debug=True, msg='Building new docs ...')
        cmder.run('rm -r source/cache', cwd=CWD, log_cmd=False)
        cmder.run('rm -r docs/*', cwd=CWD, log_cmd=False)
        cmder.run('mv build/html/* docs/', cwd=CWD, log_cmd=False)
        cmder.run('touch docs/.nojekyll', cwd=CWD, log_cmd=False)
        cmder.run('rm -rf build', cwd=CWD, log_cmd=False)
        cmder.run(f'git add docs', debug=True, cwd=CWD)
        cmder.run(f'git commit -m "{message}"', debug=True, fmt_cmd=False, cwd=CWD)
        cmder.run(f'git push origin main', debug=True, cwd=CWD)
    except IndexError:
        cmder.logger.error('No commit message was provided, please provide a message to build and publish docs.')
    

if __name__ == '__main__':
    main()
