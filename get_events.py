"""
Detect filesystem events and logs them to stream.
"""

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import argparse
import logging
import os
import platform
import sys
import time


# ------------------------------------------------------------------------
# general
# ------------------------------------------------------------------------


def setup_logging():
    """Setup a StreamHandler and overwrite base logger.
    """

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter(
            datefmt="%Y-%m-%d %H:%M:%S",
            fmt="%(asctime)s - %(message)s"
        )
    )

    # have to overwrite base logger because LoggingEventHandler uses it
    logging.basicConfig(level=logging.INFO,
                        handler=handler)


def argument_parsing():
    """Parses the command line arguments used.
    """

    parser = argparse.ArgumentParser()

    parser.add_argument("--dir",
                        type=str,
                        help="The directory to watch.",
                        default="./")

    parser.add_argument("--lib",
                        type=str,
                        choices=["watchdog", "inotify"],
                        help="Which library to use.")

    return parser.parse_args()


def _main():
    setup_logging()

    args = argument_parsing()
    print("watching directory", args.dir)

    use_watchdog = args.lib == "watchdog"

    if platform.system() == "Windows" or use_watchdog:
        main_windows(args.dir)
    else:
        main_linux(args.dir)


# ------------------------------------------------------------------------
# Linux
# ------------------------------------------------------------------------

def main_linux(data_dir):
    """Notify about events triggered base on inotify.

    Args:
        data_dir: The directory to watch.
    """
    from inotifyx import init, add_watch, get_events

    inotify_fd = init()
    wd_to_path = {}

    try:
        # get all subdirs
        # do not register right away because it will trigger events
        dirs = []
        for root, _, _ in os.walk(data_dir):
            dirs.append(root)

        for i in dirs:
            wd_to_path[add_watch(inotify_fd, i)] = i

        try:
            while True:
                events = get_events(inotify_fd)
                for event in events:
                    path = wd_to_path[event.wd]
                    parts = event.get_mask_description()

                    logging.info("%s: %s/%s",
                                 parts, path, event.name)

#                    is_created = ("IN_CREATE" in parts)
#                    is_dir = ("IN_ISDIR" in parts)
#                    is_closed = ("IN_CLOSE" in a_array
#                                 or "IN_CLOSE_WRITE" in a_array)

                    # if a new directory is created inside the monitored one,
                    # this one has to be monitored as well
#                    if is_created and is_dir and event.name:
                    if ("IN_CREATE" in parts
                            and "IN_ISDIR" in parts
                            and event.name):
                        dirname = path + os.sep + event.name
                        wd_to_path[add_watch(inotify_fd, dirname)] = dirname

        except KeyboardInterrupt:
            pass
    finally:
        os.close(inotify_fd)


# ------------------------------------------------------------------------
# Windows
# ------------------------------------------------------------------------

def main_windows(data_dir):
    """Notify about events triggered base on the watchdog library.

    Args:
        data_dir: The directory to watch.
    """
    from watchdog.observers import Observer
    from watchdog.events import LoggingEventHandler

    observer = Observer()
    observer.schedule(LoggingEventHandler(), path=data_dir, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        observer.stop()

    observer.stop()
    observer.join()


if __name__ == '__main__':
    _main()
