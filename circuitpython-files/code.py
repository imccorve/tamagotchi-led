# SPDX-FileCopyrightText: 2020 Liz Clark for Adafruit Industries
#
# SPDX-License-Identifier: MIT
import time
import board
import displayio
from adafruit_matrixportal.matrix import Matrix
import adafruit_imageload
import analog_input
from analog_input import handle_analog_input

#  create matrix display
matrix = Matrix(width=32, height=32)
display = matrix.display

group = displayio.Group()

# Animations
def create_animation_grid(path):
    anim_bit, anim_pal = adafruit_imageload.load(
        path, bitmap=displayio.Bitmap, palette=displayio.Palette
    )

    anim_grid = displayio.TileGrid(
        anim_bit,
        pixel_shader=anim_pal,
        width=1,
        height=1,
        tile_height=32,
        tile_width=32,
        default_tile=10,
        x=0,
        y=0,
    )

    return anim_grid

# load in idle bitmap
idle_grid = create_animation_grid("/idle.bmp")

# load in eat bitmap
eat_grid = create_animation_grid("/food.bmp")

# load in eat bitmap
praise_grid = create_animation_grid("/praise.bmp")

# load in eat bitmap
kiss_grid = create_animation_grid("/kiss.bmp")

class TamagotchiAnimation:
    party = 0  #  time.monotonic() holder
    curr_frame = 0  #  index for tilegrid
    anim_cycles = 0  #  count for animation cycles
    curr_anim = idle_grid
    total_frames = 2

    isMemetchiBusy = False # will prevent certain actions from being interrupted

    def __init__(self):
        display.refresh()
        display.show(group)

    def set_animation(self, frames, anim, isInterruptable = False):
        self.isMemetchiBusy = not isInterruptable

        self.anim_cycles = 0
        self.curr_frame = 0
        self.curr_anim = anim
        self.total_frames = frames

        group.pop()
        group.append(self.curr_anim)
        display.refresh()

tA = TamagotchiAnimation()

group.append(idle_grid)
display.show(group)

def play_idle():
    tA.set_animation(2, idle_grid, True)

def play_eat():
    tA.set_animation(3, eat_grid)

def play_praise():
    tA.set_animation(2, praise_grid)

def play_kiss():
    tA.set_animation(2, kiss_grid)

# constants
ANIM_DELAY = 0.6 # delay between each frame
MAX_ANIM_CYCLES = 3

play_idle()

while True:
    if tA.isMemetchiBusy == False:
        num_button_pressed = -1
        num_button_pressed = handle_analog_input()
        if num_button_pressed == 0:
            print("eating")
            play_eat()
        if num_button_pressed == 1:
            print("praise")
            play_praise()
        if num_button_pressed == 2:
            print("kiss")
            play_kiss()

    #  every 0.6 seconds...
    if (tA.party + ANIM_DELAY) < time.monotonic():
        tA.curr_anim[0] = tA.curr_frame
        #  curr_frame is the tilegrid index location
        tA.curr_frame += 1
        tA.party = time.monotonic()
        #  if an animation cycle ends
        if tA.curr_frame > tA.total_frames - 1:
            #  index is reset
            tA.curr_frame = 0
            #  animation cycle count is updated
            tA.anim_cycles += 1
            print(tA.curr_anim, tA.anim_cycles, tA.total_frames)
        #  after 3 animations cycles...
        if tA.anim_cycles > MAX_ANIM_CYCLES:
            play_idle()


