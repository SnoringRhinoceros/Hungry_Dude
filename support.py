from os import walk
import pygame
from pathlib import Path


def import_folder(path):
    surface_list = []

    for _, _, img_files in walk(path):
        for image in img_files:
            full_path = Path(path + '/' + image)
            if 'Thumbs.db' not in str(full_path):
                image_surface = pygame.image.load(full_path).convert_alpha()
                surface_list.append(image_surface)

    return surface_list
