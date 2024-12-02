import os
import pygame
import random
from game import *

# Constantes
GRID_SIZE = 8
CELL_SIZE = 40
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)


image_path = r"C:\Users\cheml\Desktop\POO 2\POO\image"
class Unit:
    """
    Classe pour représenter une unité.

    ...
    Attributs
    ---------
    x : int
        La position x de l'unité sur la grille.
    y : int
        La position y de l'unité sur la grille.
    health : int
        La santé de l'unité.
    attack_power : int
        La puissance d'attaque de l'unité.
    team : str
        L'équipe de l'unité ('player' ou 'enemy').
    is_selected : bool
        Si l'unité est sélectionnée ou non.

    Méthodes
    --------
    move(dx, dy)
        Déplace l'unité de dx, dy.
    attack(target)
        Attaque une unité cible.
    draw(screen)
        Dessine l'unité sur la grille.
    """

    def __init__(self, x, y, health, attack_power, team):
        """
        Construit une unité avec une position, une santé, une puissance d'attaque et une équipe.

        Paramètres
        ----------
        x : int
            La position x de l'unité sur la grille.
        y : int
            La position y de l'unité sur la grille.
        health : int
            La santé de l'unité.
        attack_power : int
            La puissance d'attaque de l'unité.
        team : str
            L'équipe de l'unité ('player' ou 'enemy').
        """
        self.x = x
        self.y = y
        self.health = health
        self.attack_power = attack_power
        self.team = team  # 'player' ou 'enemy'
        self.is_selected = False

   
       

    def attack(self, target):
        """Attaque une unité cible."""
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            target.health -= self.attack_power

    def draw(self, surface):
            # """Dessiner l'unité avec une image si disponible, sinon dessiner un cercle."""
        if self.image:  # Si l'image est disponible
            surface.blit(self.image, (self.x * CELL_SIZE, self.y * CELL_SIZE))
        else:  # Sinon, dessiner un cercle
            color = BLUE if self.team == 'player' else RED
            pygame.draw.circle(surface, color, (self.x * CELL_SIZE + CELL_SIZE // 2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)





class Type_Unite:
    def __init__(self, nom, x, y, vie, attaque, equipe, defense, deplacement_distance, competences, image_path):
        self.nom = nom
        self.x = x
        self.y = y
        self.vie = vie
        self.attaque = attaque
        self.equipe = equipe
        self.defense = defense
        self.deplacement_distance = deplacement_distance  # La distance que l'unité peut parcourir en une fois
        self.competences = competences
        self.image_path = image_path
        self.image = pygame.image.load(image_path) if image_path else None
        self.is_selected = False

    def move(self, dx, dy, terrain):
        """Déplace l'unité d'une case en fonction de sa capacité de déplacement."""
        # Calculer la nouvelle position
        new_x = self.x + dx
        new_y = self.y + dy
        
        # Vérifier si la position est valide
        if 0 <= new_x < len(terrain.cases) and 0 <= new_y < len(terrain.cases[0]):
            target_case = terrain.cases[new_x][new_y]

            # Si la case est un obstacle, l'unité ne peut pas avancer
            if target_case.type_case == 'obstacle':
                return False

            # Si l'unité passe sur de l'eau ou du feu, elle meurt
            if target_case.type_case == 'eau' or target_case.type_case == 'feu':
                self.vie = 0
                pygame.quit()
                exit()  # L'unité meurt

            # Si tout est valide, on déplace l'unité d'une case
            self.x = new_x
            self.y = new_y
            return True
        else:
            return False  # Si la case cible est en dehors des limites



    def attaquer(self, cible):
        """Effectuer une attaque en prenant en compte la défense de la cible."""
        degats = max(0, self.attaque - cible.defense)
        cible.recevoir_degats(degats)

    def recevoir_degats(self, degats):
        """Réduire les points de vie en fonction des dégâts subis."""
        self.vie -= degats
        if self.vie < 0:
            self.vie = 0

    def utiliser_competence(self, index, cible):
        """Utiliser une compétence sur une cible."""
        if 0 <= index < len(self.competences):
            self.competences[index].appliquer(cible)

    def draw(self, surface):
        if self.image:
            surface.blit(self.image, (self.x * CELL_SIZE, self.y * CELL_SIZE))
        else:
            color = BLUE if self.equipe == 'player' else RED
            pygame.draw.circle(surface, color, (self.x * CELL_SIZE + CELL_SIZE // 2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)


# Exemple de compétence et effet
class Competence:
    def __init__(self, nom, description, effet):
        self.nom = nom
        self.description = description
        self.effet = effet

    def appliquer(self, cible):
        """Appliquer un effet à une cible."""
        self.effet(cible)


def soin_effet(cible):
    cible.health += 20
    if cible.health > 100:  # Supposons que 100 est le maximum
        cible.health = 100


def attaque_puissante_effet(cible):
    degats = 50
    cible.recevoir_degats(degats)





