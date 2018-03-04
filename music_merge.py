#! /usr/bin/env python3

# usage:
# music_merge {target-dir} {source-dir}...
import logging
import os
import sys
from shutil import copyfile

logging.basicConfig(level=logging.DEBUG)


def setup(target_dir):
    if not os.path.isdir(target_dir):
        os.mkdir(target_dir)


def process_dir(target_dir, source_dir):
    logging.debug('p: {} {}'.format(target_dir, source_dir))
    for root, dirs, files in os.walk(source_dir):
        logging.debug('d: {} {} {}'.format(root, dirs, files))
        for file in files:
            if not file.startswith('.'):
                logging.debug('f: {} {}'.format(root, file))
                source_name = os.path.join(root, file)
                target_name = os.path.join(target_dir, root.replace(source_dir + '/', ''), file)
                if not os.path.isfile(target_name):
                    target_d = os.path.dirname(target_name)
                    if not os.path.isdir(target_d):
                        logging.debug('m: {}'.format(target_d))
                        os.makedirs(target_d)
                    logging.debug('c: {} {}'.format(source_name, target_name))
                    copyfile(source_name, target_name)
                else:  # target file exists, are we bigger or smaller than the target?
                    if os.path.getsize(source_name) > os.path.getsize(target_name):
                        copyfile(source_name, target_name)
    logging.debug('e:')


def merge(target_dir, source_dirs):
    for source_dir in source_dirs:
        process_dir(target_dir, source_dir)


if __name__ == '__main__':
    target_dir = sys.argv[1]
    source_dirs = sys.argv[2:]
    logging.info('merging: target: {} sources: {}'.format(target_dir, ', '.join(source_dirs)))
    setup(target_dir)
    merge(target_dir, source_dirs)
