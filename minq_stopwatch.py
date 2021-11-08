#! /usr/bin/env python3

# TODO
# multiple saves
# argparse

import time
import os
import art # pip3 install art
import shutil
from threading import Thread


SAVE_DIR = os.path.expanduser("~/.minq_stopwatch/")
SAVE_FILE = SAVE_DIR + "last_time"
SAVE_FILE_TMP = SAVE_FILE + "_tmp"


class Bucket:
    def __init__(s, val):
        s.val = val


def main():
    main_loop()


def main_loop():

    if not os.path.isdir(SAVE_DIR):
        os.mkdir(SAVE_DIR)

    start = time.time()

    if os.path.isfile(SAVE_FILE):
        f = open(SAVE_FILE, 'r')
        elapsed = f.read()
        f.close()
        start -= float(elapsed)

    running = Bucket(True)
    Thread(target=press_enter, args=(running,)).start()

    while running.val:
        now = time.time()
        
        elapsed = now - start
        elapsed_sec = int(elapsed)

        elapsed_min = int(elapsed_sec/60)
        elapsed_sec -= elapsed_min * 60

        elapsed_h = int(elapsed_min/60)
        elapsed_min -= elapsed_h * 60

        formatted = f"{elapsed_h}h:{elapsed_min}m:{elapsed_sec}s"
        formatted = art.text2art(formatted)
        formatted = center_text_y(formatted)
        formatted = center_text_x(formatted)
        print(formatted)

        f = open(SAVE_FILE_TMP, "w")
        f.write(str(elapsed))
        f.close()

        os.replace(SAVE_FILE_TMP, SAVE_FILE)

        time.sleep(1)


def press_enter(running):
    input()
    running.val = False


def center_text_y(txt):
    longest = 0
    for line in txt.split('\n'):
        l = len(line)
        if l > longest:
            longest = l

    term_width = shutil.get_terminal_size().columns
    free_space = term_width - longest

    if free_space <= 0:
        return txt
    else:
        to_insert = int(free_space / 2)
        centered = ""
        for line in txt.split('\n'):
            centered += ' '*to_insert + line + '\n'

        return centered


def center_text_x(txt):
    size = txt.count('\n')
    term_height = shutil.get_terminal_size().lines
    free_space = term_height - size

    if free_space <= 0:
        return txt
    else:
        to_insert = int(free_space / 2)
        return '\n'*to_insert + txt + '\n'*to_insert


if __name__ == '__main__':
    main()
