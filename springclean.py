import argparse
import os
import shutil
import sys
import traceback

# These are a mapping of file extensions to the name of the directory these files should be stored in
known_extensions = {
    # audio
    '.mp3': 'audio',
    '.wav': 'audio',
    # code/source
    '.java': 'java',
    '.js': 'js',
    # compression
    '.7z': '7-zip',
    '.bz2': 'bz2',
    '.gz': 'gzip',
    '.rar': 'rar',
    '.tar': 'tarball',
    '.tgz': 'tarball',
    '.zip': 'zip',
    # disc images
    '.img': 'img',
    '.iso': 'iso',
    # executables
    '.exe': 'exe',
    '.msi': 'msi',
    # images
    '.gif': 'gif',
    '.jpg': 'jpg',
    '.jpeg': 'jpg',
    '.png': 'png',
    # text/documents
    '.cfg': 'cfg',
    '.pdf': 'pdf',
    '.txt': 'txt',
    # video
    '.mkv': 'video',
    '.mp4': 'video',
    # web formats
    '.htm': 'html',
    '.html': 'html',
    '.json': 'json',
    '.css': 'css'
    # unknown
}


def clean_dir(path, assume_name, exts):
    """
    Cleans the given directory by moving files into directories according to their extension

    :param path: directory to clean. Must be a valid directory
    :param assume_name: True to use file extension for the directory name, False to look up in exts
    :param exts: mapping of file extensions to the name of the directory they should be moved to. Used when assume_name is False
    """
    if not type(exts) is dict:
        raise TypeError("exts parameter should be a dictionary mapping file extensions to their target directory names")
    if not type(assume_name) is bool:
        raise TypeError("assume_name parameter should be a boolean")
    if path is '.':
        path = os.path.dirname(os.path.realpath(__file__))
    elif not os.path.isabs(path):
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), path)
    if not os.path.exists(path) and not os.path.isdir(path):
        raise ValueError("Path to clean should point to a directory!")
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        filename = ''
        directory = ''
        if os.path.isfile(file_path):
            filename, file_ext = os.path.splitext(file)
            try:
                if assume_name:
                    directory = os.path.join(path, file_ext[1:])
                else:
                    directory = os.path.join(path, exts[file_ext])
            except KeyError:
                file_ext = 'unknown'
                pass
            if filename.startswith('.') and not file_ext:
                # so it's a dot file
                directory = os.path.join(path, 'missing-extension')
            elif not file_ext or file_ext is 'unknown':
                # unknown file type or empty (not handling empty ones causes naming conflicts with directories)
                directory = os.path.join(path, 'unknown-type')
            if not os.path.exists(directory) and directory:
                os.makedirs(directory)
        if filename and directory:
            try:
                dst = os.path.join(path, directory)
                shutil.move(file_path, dst)
            except IOError as e:
                traceback.print_exc(e)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="springclean", description="This program is used to bin loose files into folders based off file extension. It operates only in the directory provided and does not traverse down the folder tree. Symlinks not yet supported.")
    parser.add_argument("-d", dest="path", help="the path to the directory which is to be organised. Use of \".\" is supported but \"..\" is not")
    parser.add_argument("--ext", dest="name", action="store_true", help="indicates the file extension should be used as the directory name. When absent the built in list of known extensions will be used and anything else will be binned as unknown")
    if len(sys.argv[1:]) == 0:
        parser.print_help()
        parser.exit()
    args = parser.parse_args()

    if args.path is not None:
        clean_dir(args.path, args.name, known_extensions)
