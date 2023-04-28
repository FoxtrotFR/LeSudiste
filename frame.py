import os
import sys
import time

class Frames: pass

def read_frames(filename, color=None):
    frames = Frames()
    frames.list = []
    frames.finished = False
    with open(filename, 'r') as f:
        frame = ""
        for line in f:
            if line.strip() == "frame":
                frames.list.append(frame)
                frame = ""
            else:
                if color is not None:
                    # ajouter la séquence d'échappement ANSI pour la couleur spécifiée
                    line = f"\033[{color}m{line.strip()}\033[0m"
                frame += line
        frames.list.append(frame) # ajouter le dernier frame
    return frames


def clear_screen():
    if os.name == 'nt': # pour Windows
        _ = os.system('cls')
    else: # pour Linux et Mac
        _ = os.system('clear')

def display_frames(frames,delay=None):
    for frame in frames.list:
        clear_screen()
        print(frame)
        # Attendre 0.1 seconde avant de passer au frame suivant
        sys.stdout.flush()
        if delay == None:
            delay = 0.1
        time.sleep(delay)
    frames.finished = True
    return frames
def get_frame_finished(frames):
    return frames.finished

if __name__ == "__main__":
    frames = read_frames("intro.txt")
    display_frames(frames,delay=5)
