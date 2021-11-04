"""
Converts MIDI input to keyboard keypresses
Heavily based on https://github.com/xamox/pygame/blob/master/examples/midi.py
"""
import pydirectinput as pyautogui
import sys
import os
import json

import pygame
from pygame import event
import pygame.midi
from pygame.locals import *

pyautogui.PAUSE = 0.01

# load stored keybinds
with open("convert.txt") as f:
    data = f.read()
key_to_keyboard = json.loads(data)

"""
Defaults if you ever need to return to them

key_to_keyboard = {'60': 'a', '62': 's', '64': 'd', '61': 'w', '63': ' '}

"""


def print_device_info():
    pygame.midi.init()
    _print_device_info()
    pygame.midi.quit()


def _print_device_info():
    for i in range(pygame.midi.get_count()):
        r = pygame.midi.get_device_info(i)
        (interf, name, input, output, opened) = r

        in_out = ""
        if input:
            in_out = "(input)"
        if output:
            in_out = "(output)"

        print(
            "%2i: interface :%s:, name :%s:, opened :%s:  %s"
            % (i, interf, name, opened, in_out)
        )


def input_main(device_id=None):
    pygame.init()
    pygame.fastevent.init()
    pygame.midi.init()
    pygame.font.init()

    _print_device_info()

    device_name = pygame.midi.get_device_info(device_id)[1]
    device_name = device_name.decode("utf-8")

    if device_id is None:
        input_id = pygame.midi.get_default_input_id()
    else:
        input_id = device_id
    print("Using input_id :%s:" % input_id, device_name)

    # Display stuff
    res = (900, 300)
    background_color = (0, 0, 0)
    key_length = 50
    key_width = 10

    screen = pygame.display.set_mode(res)
    pygame.display.set_caption("MIDI to Keyboard")
    screen.fill(background_color)
    myfont = pygame.font.SysFont("Times New Roman", 20)
    pygame.display.flip()

    # Draws layout of keys
    for j in range(0, 88):
        pygame.draw.rect(
            screen, (255, 255, 255), [j * key_width, 30, key_width, key_length], 1
        )

    textsurface = myfont.render(
        "Device Name: " + str(device_name), False, (0, 170, 250)
    )
    screen.blit(textsurface, (0, 0))
    pygame.display.flip()

    event_get = pygame.fastevent.get
    i = pygame.midi.Input(input_id)

    going = True
    while going:
        events = event_get()
        for e in events:
            if e.type in [QUIT]:
                going = False

            if e.type in [pygame.midi.MIDIIN]:
                print(e)

            """Key binder
            User clicks on the piano key they wish to rebind and then
            enters the keyboard key they wish to rebind to
            """
            if e.type == pygame.MOUSEBUTTONDOWN:
                key_value = int(int(e.pos[0]) / key_width) + 20

                pygame.draw.rect(
                    screen,
                    (255, 102, 0),
                    [(key_value - 20) * key_width, 30, key_width, key_length],
                    1,
                )  # Highlight piano key
                pygame.display.flip()
                print("Rebinding", key_value)
                x = input("Enter key to bind to: ")

                key_to_keyboard[str(int(int(e.pos[0]) / key_width) + 20)] = x
                pygame.draw.rect(
                    screen,
                    (255, 255, 255),
                    [(key_value - 20) * key_width, 30, key_width, key_length],
                    1,
                )  # un highlight piano key
                pygame.display.flip()

        if i.poll():
            midi_events = i.read(10)

            x = ""
            try:
                x = key_to_keyboard[str(midi_events[0][0][1])]
            except KeyError:
                pass

            key_value = midi_events[0][0][1]

            """
            Checks if key is pressed or released
            144 - pressed
            129 - released
            midi_events = [[status, key, ..., ...,], timestamp]
            """
            if midi_events[0][0][0] == 144:
                pyautogui.keyDown(x)

                pygame.draw.rect(
                    screen,
                    (255, 0, 0),
                    [(key_value - 20) * key_width, 30, key_width, key_length],
                )
                pygame.display.flip()

            elif midi_events[0][0][0] == 128:
                pyautogui.keyUp(x)

                pygame.draw.rect(
                    screen,
                    (0, 0, 0),
                    [(key_value - 20) * key_width, 30, key_width, key_length],
                )
                pygame.draw.rect(
                    screen,
                    (255, 255, 255),
                    [(key_value - 20) * key_width, 30, key_width, key_length],
                    1,
                )
                pygame.display.flip()

    del i
    pygame.midi.quit()

    # Save keybinds to convert.txt
    print("\nSaving these keybinds: ", key_to_keyboard)
    with open("convert.txt", "w") as convert_file:
        convert_file.write(json.dumps(key_to_keyboard))


def usage():
    print("--input [device_id] : control keyboard with midi device")
    print("--list : list available midi devices")


def main(mode="list", device_id=None):

    if mode == "input":
        input_main(device_id)
    elif mode == "list":
        print_device_info()
    else:
        raise ValueError("Unknown mode option '%s'" % mode)


if __name__ == "__main__":

    try:
        device_id = int(sys.argv[-1])
    except:
        device_id = None

    if "--input" in sys.argv or "-i" in sys.argv:
        input_main(device_id)
    elif "--list" in sys.argv or "-l" in sys.argv:
        print_device_info()
    else:
        usage()
