#! /usr/bin/env python3

# TODO
# stop on q press and not enter
# use tmp files

import time
import os
import art # pip3 install art
import shutil
from threading import Thread
import argparse
import glob
from tempfile import NamedTemporaryFile
import shutil


SAVE_DIR = os.path.expanduser("~/.minq_stopwatch/")
DEFAULT_NAME = "DEFAULT-STOPWATCH"


class Bucket:
    def __init__(s, val):
        s.val = val


def main():
    parser = argparse.ArgumentParser(description="A cool stopwatch")
    parser.add_argument('name', nargs='?', type=str, help="The name of the timer")
    parser.add_argument('--restart', action='store_true', help="This will restart the stopwatch to 0h0m0s")
    parser.add_argument('--list', action='store_true', help="This will restart the stopwatch to 0h0m0s")
    args = parser.parse_args()

    if args.name == None:
        name = DEFAULT_NAME
    else:
        name = args.name

    if args.list:
        for timer in get_timers():
            print(timer)
        return

    if args.restart:
        print(f"Are you sure you want to restart '{name}'? Press enter to confirm")
        input()
        delete_timer(name)
        return

    main_loop(name)


def main_loop(timer_name):

    if not os.path.isdir(SAVE_DIR):
        os.mkdir(SAVE_DIR)

    start = time.time()
    elapsed = load_time(timer_name)
    start -= elapsed

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

        save_time(timer_name, elapsed)

        time.sleep(1)


def get_timers():
    dir = SAVE_DIR
    return glob.glob(dir+'*')

def load_time(timer_name):
    dir = SAVE_DIR + timer_name

    if os.path.isfile(dir):
        f = open(dir, 'r')
        elapsed = f.read()
        f.close()
        return float(elapsed)
    else:
        return 0

def save_time(timer_name, elapsed):
    dir = SAVE_DIR + timer_name

    with NamedTemporaryFile(prefix=f'minq_timer_{timer_name}_', delete=False, mode="w") as f:
        f.write(str(elapsed))
        tmp = f.name

    shutil.move(tmp, dir)

def delete_timer(timer_name):
    dir = SAVE_DIR + timer_name
    try:
        os.remove(dir)
    except FileNotFoundError:
        print("Timer already deleted...")

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
