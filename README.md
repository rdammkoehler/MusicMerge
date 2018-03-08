# Music Merge

A simple script to merge your Music folders. This is still a work in progress and has at least one known flaw in deduplication related to the order in which files get moved (if the numbered file is moved first then the unnumbered file will also be moved).

## Requirements:

* Built and tested with Python 3.5.1

* Uses /usr/bin/env to start python3

## Usage

```sh
./music_merge.py <target_dir> [--debug] <source_dir> ...
```

## Example:

The following will merge the music files from the 3 locations listed into the target directory. 

```
./music_merge.py /Users/me/AllMusic /Users/me/iTunes/Music "/Users/me/Amazon Music" /Users/me/old_iTunes/Music
```

## Details:

* For each source directory, traverse the directory structure creating any folders or files that are missing from the target directory.

* If the file ends with white-space folowed by a number, dot, and music file extension, check to see if the same file exists without the number (asong 1.mp3 and asong.mp3). If the file without the number exists, don't copy this file.

* Does not follow symlinks

* accepts a `--debug` flag on the command line to produce detailed (and copious) output. The `--debug` flag can be placed anywhere on the command line.

