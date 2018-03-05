#! /usr/bin/env python3

# usage:
# music_merge {target-dir} {source-dir}...
import logging
import os
import re
import sys
from shutil import copyfile

DEBUG_FLAG = '--debug'
DEBUGGING = DEBUG_FLAG in sys.argv
if DEBUGGING:
    logging.basicConfig(level=logging.DEBUG)


def setup(target_dir):
    if not os.path.isdir(target_dir):
        os.mkdir(target_dir)


def numbered_copy(target_name):
    numbered_music_file_expr = r'(.*)\s+\d+(\.(3gp|aa|aac|aax|act|aiff|amr|ape|au|awb|dct|dss|dvf|flac|gsm|iklax|ivs|m4a|m4b|m4p|mmf|mp3|mpc|msv|ogg|oga|mogg|opus|ra|rm|raw|sln|tta|vox|wav|wma|wv|webm|8svx))$'
    match = re.search(numbered_music_file_expr, target_name.lower())
    if match:
        unnumbered_target_name = match.group(1) + match.group(2)
    return match and os.path.isfile(unnumbered_target_name)


def copy_source_to_target(source_name, target_name):
    try:
        copyfile(source_name, target_name)
    except Exception as ex:
        message = 'x: failed to copy file: {}'.format(ex)
        if DEBUGGING:
            logging.exception(message)
        else:
            logging.error(message)


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
                    if numbered_copy(target_name):
                        logging.warning('w: skipping numbered duplicate {}'.format(source_name))
                    else:
                        target_d = os.path.dirname(target_name)
                        if not os.path.isdir(target_d):
                            logging.debug('m: {}'.format(target_d))
                            os.makedirs(target_d)
                        logging.debug('c: {} {}'.format(source_name, target_name))
                        copy_source_to_target(source_name, target_name)
                else:
                    if os.path.getsize(source_name) > os.path.getsize(target_name):
                        copy_source_to_target(source_name, target_name)


def merge(target_dir, source_dirs):
    for source_dir in source_dirs:
        process_dir(target_dir, source_dir)


if __name__ == '__main__':
    args = sys.argv[0:sys.argv.index(DEBUG_FLAG)] + sys.argv[sys.argv.index(
        DEBUG_FLAG) + 1:] if DEBUG_FLAG in sys.argv else sys.argv
    target_dir = args[1]
    source_dirs = args[2:]
    logging.info('merging: target: {} sources: {}'.format(target_dir, ', '.join(source_dirs)))
    setup(target_dir)
    merge(target_dir, source_dirs)
