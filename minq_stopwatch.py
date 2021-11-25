#! /usr/bin/env python3

# TODO
# stop on q press and not enter
# fix the regex loop

import time
import os
import art # pip3 install art
import shutil
from threading import Thread
import argparse
import glob
from tempfile import NamedTemporaryFile
import shutil
import re


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
    parser.add_argument('--countdown-hours', type=float, help="This is in hours. Subtracts this from the current time")
    parser.add_argument('--divide', type=float, help="Divides the resulting time by this")
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

    countdown = args.countdown_hours
    if countdown != None:
        countdown *= 60 * 60 # transform from H to sec

    main_loop(name, countdown, args.divide)


def main_loop(timer_name, countdown, divide):

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

        elapsed_sec = elapsed
        if countdown != None:
            elapsed_sec = countdown - elapsed_sec
        if divide != None:
            elapsed_sec /= divide

        elapsed_sec = int(elapsed_sec)

        elapsed_min = int(elapsed_sec/60)
        elapsed_sec -= elapsed_min * 60

        elapsed_h = int(elapsed_min/60)
        elapsed_min -= elapsed_h * 60

        formatted = f"{elapsed_h}h:{elapsed_min}m:{elapsed_sec}s"
        formatted = art.text2art(formatted)
        formatted = fix_the_fucking_default_font(formatted)
        formatted = center_text(formatted)
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
    pass
    input()
    running.val = False


def fix_the_fucking_default_font(txt):

    while True:
        res = re.search('^\n +\n', txt)
        if res == None:
            break
        start, end = res.span()
        txt = txt[end:]

    while True:
        res = re.search('\n +\n$', txt)
        if res == None:
            break
        start, end = res.span()
        txt = txt[:start]
        
    return txt


def center_text(txt):

    # get x size
    longest = 0
    for line in txt.split('\n'):
        l = len(line)
        if l > longest:
            longest = l

    # get y size
    size_y = txt.count('\n')

    term = shutil.get_terminal_size()
    term_width = term.columns
    term_height = term.lines
    
    free_space_x = term_width - longest
    free_space_y = term_height - size_y

    if free_space_x > 0:
        to_insert = int(free_space_x / 2)
        centered = ""
        for line in txt.split('\n'):
            centered += ' '*to_insert + line + '\n'

        txt = centered

    if free_space_y > 0:
        to_insert = int(free_space_y / 2)
        txt = ('\n'*to_insert) + txt + ('\n'*to_insert)

    return txt


if __name__ == '__main__':
    main()
