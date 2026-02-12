import tkinter as tk
from tkinter import ttk, scrolledtext
from PIL import Image, ImageTk
import os
import glob
import re
import cv2
import numpy as np
import sys

# --- CONFIGURATION ---
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# This tells the script where to find the images inside the EXE
IMAGE_FOLDER = resource_path("Monster Plates")

# The rest of your settings...
FACE_BOX = (445, 133, 657, 323)
TARGET_COLOR_RGB = (254, 226, 192) 
TOLERANCE = 40

# 1. FACE SETTINGS
FACE_BOX = (445, 133, 657, 323)

# 2. GIFT LIST SETTINGS
TARGET_COLOR_RGB = (254, 226, 192) 
TOLERANCE = 40 

# 3. COLORS
COLOR_VERMILION = '#9e0912'
COLOR_ROYAL_PURPLE = '#7851a9'
COLOR_TEXT_WHITE = '#ffffff'
COLOR_BG_MAIN = '#202020'
COLOR_INPUT_BG = '#333333'
COLOR_BTN_BG = '#444444'
COLOR_HIGHLIGHT = '#fee2c0' # Beige
# ---------------------

# --- THE MONSTER DATABASE ---
MONSTER_DB = [
    {"Name": "Balbo", "Home": "Damp Cave", "Gifts": "Manuka Honey, 2-Scoop Ice Cream, Cotton Candy, Zesty Crepes, Classic Donuts, Chocolate Bar, Steamed Cake, Black Tapioca, Nata de Coco, Meteorite, Homemade Cookies, Iron Ore, Extra-Fine Shaved Ice, Bronze Ore, Rustic Red Bean Cake, Silver Ore, Roast Sweet Potato, Gold Ore"},
    {"Name": "Mozar", "Home": "Damp Cave", "Gifts": "Regular Tea, Sweet Juice, Dark Roast Coffee, Fresh Milk, Gold-Label Soda, Vintage Soda Pop, Black Tea"},
    {"Name": "Babyshroom", "Home": "Damp Cave", "Gifts": "Fresh Carrot, Regular Cucumber, Fresh Eggplant, Fresh Bell Pepper, Rough Daikon Radish, Tough Avocado, Manuka Honey, Tiny Onion, 2-Scoop Ice Cream, Cotton Candy, Snow Potato, Zesty Crepes, Chunky Pumpkin, Classic Donuts, Tasty Tomato, Homemade Cookies, Chewy Mushroom, Extra-Fine Shaved Ice, Rustic Red Bean Cake, Roast Sweet Potato, Chocolate Bar, Steamed Cake, Black Tapioca, Nata de Coco"},
    {"Name": "Gnaw-naw", "Home": "Damp Cave", "Gifts": "Fresh Carrot, Regular Cucumber, Fresh Eggplant, Fresh Bell Pepper, Tiny Onion, Snow Potato, Rough Daikon Radish, Tough Avocado, Protective Garlic, Spicy Corn, Meteorite, Iron Ore, Chunky Pumpkin, Bronze Ore, Tasty Tomato, Silver Ore, Chewy Mushroom, Gold Ore"},
    {"Name": "Mush-Roo", "Home": "Damp Cave", "Gifts": "Fresh Carrot, Regular Cucumber, Fresh Eggplant, Fresh Bell Pepper, Rough Daikon Radish, Tough Avocado, Manuka Honey, Tiny Onion, 2-Scoop Ice Cream, Cotton Candy, Snow Potato, Zesty Crepes, Chunky Pumpkin, Classic Donuts, Tasty Tomato, Homemade Cookies, Chewy Mushroom, Extra-Fine Shaved Ice, Rustic Red Bean Cake, Roast Sweet Potato, Chocolate Bar, Steamed Cake, Black Tapioca, Nata de Coco"},
    {"Name": "Tropical Balbo", "Home": "Damp Cave", "Gifts": "Manuka Honey, 2-Scoop Ice Cream, Cotton Candy, Zesty Crepes, Classic Donuts, Homemade Cookies, Extra-Fine Shaved Ice, Chocolate Bar, Steamed Cake, Black Tapioca, Nata de Coco, Rustic Red Bean Cake, Roast Sweet Potato"},
    {"Name": "Shrood", "Home": "Damp Cave", "Gifts": "Regular Cucumber, Fresh Eggplant, Fresh Bell Pepper, Tiny Onion, Fresh Carrot, Rough Daikon Radish, Tough Avocado, Boiled Octopus, Sleepy Squid, Snow Potato, Chunky Pumpkin, Tasty Tomato, Chewy Mushroom, Fatty Tuna, Crunchy Shrimp"},
    {"Name": "Enokaiser", "Home": "Damp Cave", "Gifts": "Basic Bread, Spicy Curry, Soy Sauce Noodles, Stewed Uden Noodles, Basic Stew, Fresh Eggplant, Fresh Bell Pepper, Tiny Onion, Snow Potato, Chunky Pumpkin, Sushi, Pizza Margherita, Tasty Tomato, Chewy Mushroom, Rough Daikon Radish, Regular Cucumber, Tough Avocado, Fresh Carrot, Scissors, Pocket Mirror, Wind-up Doll, Fluffy Blanket, Firework Rocket, Silver Spoon, Playing Cards, Broom, Sleepy Pillow, Pink Trumpet, Grand Piano, Fan Letter, Party Pinata, Antique Key, Plushie, Master Violin"},
    {"Name": "Mandragora", "Home": "Damp Cave", "Gifts": "Fresh Carrot, Regular Cucumber, Fresh Eggplant, Fresh Bell Pepper, Tiny Onion, Rough Daikon Radish, Tough Avocado, Giant Watermelon, Pineapple, Seaside Lemon, Rosy Apple, Tropical Coconut, Steamed Cake, Scissors, Pocket Mirror, Ripe Melon, Wild Strawberry, Snow Potato, XL Orange, Chunky Pumpkin, Dragon Fruit, Tasty Tomato, Ripe Banana, Wind-up Doll, Chewy Mushroom, Juicy Peach, Fluffy Blanket, Sleepy Pillow, Fan Letter, Party Pinata, Antique Key, Plushie, Firework Rocket, Silver Spoon"},
    {"Name": "Stumpton", "Home": "Nearby Forest", "Gifts": "Regular Tea, Sweet Juice, Dark Roast Coffee, Fresh Milk, Gold-Label Soda, Vintage Soda Pop, Black Tea, Protective Garlic, Spicy Corn"},
    {"Name": "Turtoid", "Home": "Nearby Forest", "Gifts": "Meat Buns, Octopus Fritters, Spicy Hot Pot, Giant Watermelon, Ripe Melon, Wild Strawberry, XL Orange, Dragon Fruit, Ripe Banana, Juicy Peach, Pineapple, Seaside Lemon, Rosy Apple, Tropical Coconut, Mellow Cheese, Yogurt, Fresh Egg, Aged Soy Beans, Beehive, Bat Wing, Lizard Tail, Bird's Nest, Doll, Magic Lamp, Crystal Ball, Fire Spellbook, Ice Spellbook, Lightning Spellbook, Darkness Spellbook, Healing Spellbook"},
    {"Name": "Turfton", "Home": "Nearby Forest", "Gifts": "Fresh Carrot, Regular Cucumber, Fresh Eggplant, Fresh Bell Pepper, Tiny Onion, Snow Potato, Rough Daikon Radish, Tough Avocado, Manuka Honey, 2-Scoop Ice Cream, Cotton Candy, Chunky Pumpkin, Zesty Crepes, Classic Donuts, Tasty Tomato, Homemade Cookies, Chewy Mushroom, Extra-Fine Shaved Ice, Rustic Red Bean Cake, Roast Sweet Potato, Chocolate Bar, Steamed Cake, Black Tapioca, Nata de Coco"},
    {"Name": "Snailailai", "Home": "Nearby Forest", "Gifts": "Regular Tea, Sweet Juice, Bronze Ore, Silver Ore, Dark Roast Coffee, Gold Ore, Fresh Milk, Gold-Label Soda, Vintage Soda Pop, Black Tea, Meteorite, Iron Ore"},
    {"Name": "Trunket", "Home": "Nearby Forest", "Gifts": "Regular Tea, Sweet Juice, Dark Roast Coffee, Fresh Milk, Gold-Label Soda, Vintage Soda Pop, Black Tea, Scissors, Pocket Mirror, Wind-up Doll, Fluffy Blanket, Sleepy Pillow, Fan Letter, Party Pinata, Antique Key, Plushie, Firework Rocket, Silver Spoon, Playing Cards, Broom, Pink Trumpet, Grand Piano, Master Violin, Tulips, Morning Glory, Sunflowers, Steel Pipe, 1000-Year Bonsai, Eye-Catching Piece, Meteorite, Iron Ore, Bronze Ore, Silver Ore, Gold Ore"},
    {"Name": "Holycorn", "Home": "Nearby Forest", "Gifts": "Regular Tea, Sweet Juice, Dark Roast Coffee, Fresh Milk, Gold-Label Soda, Vintage Soda Pop, Black Tea"},
    {"Name": "Azuroise", "Home": "Nearby Forest", "Gifts": "Fresh Carrot, Regular Cucumber, Fresh Eggplant, Fresh Bell Pepper, Tiny Onion, Snow Potato, Chunky Pumpkin, Tasty Tomato, Chewy Mushroom, Rough Daikon Radish, Tough Avocado, Protective Garlic, Spicy Corn, Boiled Octopus, Sleepy Squid, Fatty Tuna, Pocket Mirror, Wind-up Doll, Fluffy Blanket, Sleepy Pillow, Fan Letter, Party Pinata, Antique Key, Crunchy Shrimp, Plushie, Scissors, Firework Rocket, Silver Spoon, Playing Cards, Broom, Pink Trumpet, Grand Piano, Master Violin"},
    {"Name": "Geriatree", "Home": "Nearby Forest", "Gifts": "Regular Tea, Sweet Juice, Dark Roast Coffee, Fresh Milk, Gold-Label Soda, Vintage Soda Pop, Black Tea"},
    {"Name": "Pow-Pow", "Home": "Pretty Meadow", "Gifts": "Protective Garlic, Spicy Corn, Steamed Cake, Meteorite, Iron Ore, Bronze Ore, Silver Ore, Gold Ore"},
    {"Name": "Wormrow", "Home": "Pretty Meadow", "Gifts": "Meat Buns, Octopus Fritters, Spicy Hot Pot, Mellow Cheese, Yogurt, Fresh Egg, Aged Soy Beans, Beehive, Bat Wing, Lizard Tail, Bird's Nest, Magic Lamp, Doll, Crystal Ball, Healing Spellbook, Meteorite, Iron Ore, Bronze Ore, Silver Ore, Fire Spellbook, Gold Ore, Ice Spellbook, Lightning Spellbook, Darkness Spellbook"},
    {"Name": "Bilbo", "Home": "Pretty Meadow", "Gifts": "Basic Bread, Spicy Curry, Soy Sauce Noodles, Stewed Udon Noodles, Basic Stew, Sushi, Pizza Margherita, Manuka Honey, 2-Scoop Ice Cream, Cotton Candy, Zesty Crepes, Classic Donuts, Black Tapioca, Nata de Coco, Beehive, Fire Spellbook, Ice Spellbook, Lightning Spellbook, Homemade Cookies, Bat Wing, Darkness Spellbook, Extra-Fine Shaved Ice, Lizard Tail, Healing Spellbook, Rustic Red Bean Cake, Bird's Nest, Meteorite, Roast Sweet Potato, Chocolate Bar, Steamed Cake, Magic Lamp, Doll, Iron Ore, Bronze Ore, Crystal Ball"},
    {"Name": "Electrood", "Home": "Pretty Meadow", "Gifts": "Basic Bread, Spicy Curry, Soy Sauce Noodles, Fresh Eggplant, Fresh Bell Pepper, Tiny Onion, Snow Potato, Chunky Pumpkin, Stewed Udon Noodles, Basic Stew, Sushi, Tasty Tomato, Pizza Margherita, Chewy Mushroom, Fresh Carrot, Rough Daikon Radish, Regular Cucumber, Tough Avocado, Giant Watermelon, Ripe Melon, Wild Strawberry, XL Orange, Dragon Fruit, Ripe Banana, Juicy Peach, Pineapple, Seaside Lemon, Rosy Apple, Tropical Coconut"},
    {"Name": "Pupaman", "Home": "Pretty Meadow", "Gifts": "Protective Garlic, Spicy Corn, Manuka Honey, 2-Scoop Ice Cream, Cotton Candy, Zesty Crepes, Classic Donuts, Homemade Cookies, Extra-Fine Shaved ice, Broom, Rustic Red Bean Cake, Roast Sweet Potato, Fluffy Blanket, Sleepy Pillow, Pink Trumpet, Chocolate Bar, Fan Letter, Grand Piano, Steamed Cake, Party Pinata, Antique Key, Plushie, Master Violin, Tulips, Black Tapioca, Nata de Coco, Scissors, Pocket Mirror, Wind-up Doll, Firework Rocket, Silver Spoon, Playing Cards, Morning Glory, Sunflowers, Steel Pipe"},
    {"Name": "Cragolem", "Home": "Pretty Meadow", "Gifts": "Basic Bread, Spicy Curry, Soy Sauce Noodles, Fresh Eggplant, Fresh Bell Pepper, Tiny Onion, Meteorite, Iron Ore, Bronze Ore, Stewed Udon Noodles, Snow Potato, Silver Ore, Basic Stew, Chunky Pumpkin, Gold Ore, Sushi, Tasty Tomato, Pizza Margherita, Chewy Mushroom, Fresh Carrot, Rough Daikon Radish, Regular Cucumber, Tough Avocado"},
    {"Name": "Arrowtail", "Home": "Pretty Meadow", "Gifts": "Regular Tea, Sweet Juice, Dark Roast Coffee, Fresh Milk, Gold-Label Soda, Vintage Soda Pop, Black Tea, Manuka Honey"},
    {"Name": "Puddikin", "Home": "Pretty Meadow", "Gifts": "Giant Watermelon, Ripe Melon, Wild Strawberry, XL Orange, Dragon Fruit, Ripe Banana, Juicy Peach, Pineapple, Seaside Lemon, Rosy Apple, Tropical Coconut, Beehive, Bat Wing, Lizard Tail, Bird's Nest, Magic Lamp, Doll, Crystal Ball, Fire Spellbook, Ice Spellbook, Lightning Spellbook, Darkness Spellbook, Healing Spellbook"},
    {"Name": "Lapine", "Home": "Dojo", "Gifts": "Manuka Honey, 2-Scoop Ice Cream, Cotton Candy, Zesty Crepes, Classic Donuts, Chocolate Bar, Steamed Cake, Black Tapioca, Nata de Coco, Meteorite, Homemade Cookies, Iron Ore, Extra-Fine Shaved Ice, Bronze Ore, Rustic Red Bean Cake, Silver Ore, Roast Sweet Potato, Gold Ore"},
    {"Name": "Mojo-Jobo", "Home": "Dojo", "Gifts": "Dark Roast Coffee, Fresh Milk, Regular Tea, Sweet Juice, Fresh Eggplant, Fresh Bell Pepper, Tiny Onion, Snow Potato, Sweet ' Sour Meatbalis, Honey-Roast Ham, Crystal Ball, Fire Spellbook, Marbled Steak, Beehive, Ice Spellbook, Lightning Spellbook, Gold-Label Soda, Chunky Pumpkin, Bat Wing, Darkness Spellbook, Vintage Soda Pop, Tasty Tomato, Lizard Tail, Healing Spellbook, Black Tea, Chewy Mushroom, Bird's Nest, Fresh Carrot, Regular Cucumber, Rough Daikon Radish, Tough Avocado, Magic Lamp, Doll"},
    {"Name": "LoxO", "Home": "Dojo", "Gifts": "Basic Bread, Spicy Curry, Soy Sauce Noodles, Fresh Eggplant, Fresh Bell Pepper, Tiny Onion, Snow Potato, Chunky Pumpkin, Stewed Udon Noodles, Basic Stew, Sushi, Tasty Tomato, Pizza Margherita, Chewy Mushroom, Fresh Carrot, Rough Daikon Radish, Regular Cucumber, Tough Avocado, Beehive, Bat Wing, Lizard Tail, Bird's Nest, Magic Lamp, Doll, Crystal Ball, Fire Spellbook, Ice Spellbook, Lightning Spellbook, Darkness Spellbook, Healing Spellbook"},
    {"Name": "Hercurilla", "Home": "Dojo", "Gifts": "Meat Buns, Octopus Fritters, Spicy Hot Pot, Ripe Banana, Mellow Cheese, Yogurt, Fresh Egg, Aged Soy Beans"},
    {"Name": "Lapoon", "Home": "Dojo", "Gifts": "Meat Buns, Octopus Fritters, Spicy Hot Pot, Mellow Cheese, Yogurt, Fresh Egg, Aged Soy Beans, Scissors, Pocket Mirror, Wind-up Doll, Fluffy Blanket, Sleepy Pillow, Fan Letter, Party Pinata, Antique Key, Plushie, Firework Rocket, Silver Spoon, Playing Cards, Broom, Pink Trumpet, Grand Piano, Master Violin, Tulips, Morning Glory, Sunflowers, Steel Pipe, 1000-Year Bonsai, Eye-Catching Piece"},
    {"Name": "Boxobot", "Home": "Dojo", "Gifts": "Giant Watermelon, Ripe Melon, Wild Strawberry, XL Orange, Dragon Fruit, Ripe Banana, Juicy Peach, Pineapple, Seaside Lemon, Rosy Apple, Tropical Coconut, Honey-Roast Ham, Sweet 'n Sour Meatballs, Marbled Steak"},
    {"Name": "Glacierilla", "Home": "Dojo", "Gifts": "Giant Watermelon, Ripe Melon, Wild Strawberry, Rosy Apple, Tropical Coconut, XL Orange, Dragon Fruit, Ripe Banana, Juicy Peach, Pineapple, Seaside Lemon"},
    {"Name": "Draggi", "Home": "Dojo", "Gifts": "Basic Bread, Dark Roast Coffee, Spicy Curry, Fresh Milk, Soy Sauce Noodles, Gold-Label Soda, Stewed Udon Noodies, Basic Stew, Sushi, Pizza Margherita, Regular Tea, Sweet Juice, Vintage Soda Pop, Black Tea, Giant Watermelon, Ripe Melon, Wild Strawberry, XL Orange, Dragon Fruit, Cotton Candy, Zesty Crepes, Classic Donuts, Homemade Cookies, Ripe Banana, Juicy Peach, Pineapple, Seaside Lemon, Rosy Apple, Tropical Coconut, Manuka Honey, 2-Scoop Ice Cream"},
    {"Name": "Kakakari", "Home": "Mystery Pyramid", "Gifts": "Honey-Roast Ham, Sweet 'n' Sour Meatballs, Marbled Steak, Basic Bread, Spicy Curry, Soy Sauce Noodles, Stewed Udon Noodles, Basic Stew, Sushi, Pizza Margherita, Meat Buns, Octopus Fritters, Spicy Hot Pot, Giant Watermelon, Ripe Melon, Wild Strawberry, XL Orange, Dragon Fruit, Ripe Banana, Juicy Peach, Pineapple, Seaside Lemon, Rosy Apple, Tropical Coconut, Mellow Cheese, Yogurt, Fresh Egg"},
    {"Name": "Orblob", "Home": "Mystery Pyramid", "Gifts": "Honey-Roast Ham, Sweet 'n' Sour Meatballs, Marbled Steak, Boiled Octopus, Sleepy Squid, Fatty Tuna, Crunchy Shrimp, Beehive, Bat Wing, Lizard Tail, Bird's Nest, Magic Lamp, Doll, Crystal Ball, Fire Spellbook, Ice Spellbook, Lightning Spellbook, Darkness Spellbook, Healing Spellbook"},
    {"Name": "Sandclomper", "Home": "Mystery Pyramid", "Gifts": "Meat Buns, Octopus Fritters, Spicy Hot Pot, Protective Garlic, Spicy Corn, Yogurt, Fresh Egg, Aged Soy Beans, Honey-Roast Ham, Sweet 'n' Sour Meatballs, Marbled Steak, Mellow Cheese"},
    {"Name": "Snek", "Home": "Mystery Pyramid", "Gifts": "Protective Garlic, Meat Buns, Chunky Pumpkin, Spicy Corn, Octopus Fritters, Tasty Tomato, Basic Bread, Spicy Hot Pot, Chewy Mushroom, Spicy Curry, Fresh Carrot, Rough Daikon Radish, Soy Sauce Noodles, Regular Cucumber, Giant Watermelon, Stewed Udon Noodles, Fresh Eggplant, Ripe Melon, Basic Stew, Sushi, Fresh Bell Pepper, Tiny Onion, Wild Strawberry, XL Orange, Pizza Margherita, Snow Potato"},
    {"Name": "Slabby", "Home": "Mystery Pyramid", "Gifts": "Protective Garlic, Spicy Corn, Giant Watermelon, Ripe Melon, Wild Strawberry, XL Orange, Dragon Fruit, Ripe Banana, Juicy Peach, Pineapple, Seaside Lemon, Rosy Apple, Tropical Coconut, Scissors, Pocket Mirror, Wind-up Doll, Fluffy Blanket, Sleepy Pillow, Fan Letter, Party Pinata, Antique Key, Plushie, Firework Rocket, Silver Spoon, Playing Cards, Broom, Pink Trumpet, Grand Piano, Master Violin, Tulips, Morning Glory, Sunflowers, Steel Pipe, 1000-Year Bonsai, Eye-Catching Piece"},
    {"Name": "Geckoron", "Home": "Mystery Pyramid", "Gifts": "Giant Watermelon, Ripe Melon, Wild Strawberry, XL Orange, Dragon Fruit, Ripe Banana, Juicy Peach, Pineapple, Seaside Lemon, Rosy Apple, Tropical Coconut"},
    {"Name": "Blobby", "Home": "Mystery Pyramid", "Gifts": "Meat Buns, Chunky Pumpkin, Beehive, Lightning Spellbook, Octopus Fritters, Tasty Tomato, Bat Wing, Darkness Spellbook, Spicy Hot Pot, Fresh Carrot, Chewy Mushroom, Lizard Tail, Healing Spellbook, Regular Cucumber, Rough Daikon Radish, Tough Avocado, Bird's Nest, Magic Lamp, Fresh Eggplant, Fresh Bell Pepper, Tiny Onion, Snow Potato, Sleepy Squid, Fatty Tuna, Crunchy Shrimp, Fire Spellbook, Ice Spellbook, Boiled Octopus, Doll, Crystal Ball"},
    {"Name": "Sand Lizard", "Home": "Mystery Pyramid", "Gifts": "Beehive, Bat Wing, Lizard Tail, Bird's Nest, Magic Lamp, Doll, Crystal Ball, Fire Spellbook, Ice Spellbook, Lightning Spelibook, Darkness Spellbook, Healing Spellbook"},
    {"Name": "Scalene", "Home": "Mystery Pyramid", "Gifts": "Honey-Roast Ham, Sweet 'n' Sour Meatballs, Marbled Steak, Boiled Octopus, Sleepy Squid, Fatty Tuna, Crunchy Shrimp"},
    {"Name": "2-Ply Roller", "Home": "Mystery Pyramid", "Gifts": "Basic Bread, Spicy Curry, Soy Sauce Noodles, Stewed Udon Noodles, Basic Stew, Sushi, Pizza Margherita, Regular Tea, Sweet Juice, Dark Roast Coffee, Fresh Milk, Gold-Label Soda, Vintage Soda Pop, Black Tea, Protective Garlic, Spicy Corn"},
    {"Name": "Crabkin", "Home": "Tropical Coast", "Gifts": "Fresh Carrot, Rough Daikon Radish, Regular Cucumber, Tough Avocado, Fresh Eggplant, Fresh Bell Pepper, Tiny Onion, Snow Potato, Chunky Pumpkin, Tasty Tomato, Chewy Mushroom"},
    {"Name": "Shellox", "Home": "Tropical Coast", "Gifts": "Fresh Carrot, Rough Daikon Radish, Regular Cucumber, Tough Avocado, Fresh Eggplant, Honey-Roast Ham, Fresh Bell Pepper, Sweet' Sour Meatballs, Tiny Onion, Marbled Steak, Snow Potato, Chunky Pumpkin, Tasty Tomato, Chewy Mushroom"},
    {"Name": "Banang", "Home": "Tropical Coast", "Gifts": "Fresh Carrot, Regular Cucumber, Fresh Eggplant, Fresh Bell Pepper, Tiny Onion, Snow Potato, Chunky Pumpkin, Tasty Tomato, Chewy Mushroom, Rough Daikon Radish, Tough Avocado, Ripe Banana"},
    {"Name": "Hermit Crabby", "Home": "Tropical Coast", "Gifts": "Meat Buns, Octopus Fritters, Spicy Hot Pot, Regular Tea, Sweet Juice, Dark Roast Coffee, Fresh Milk, Gold-Label Soda, Vintage Soda Pop, Black Tea, Giant Watermelon, Ripe Melon, Wild Strawberry, XL Orange, Dragon Fruit, Ripe Banana, Juicy Peach, Pineapple, Seaside Lemon, Rosy Apple, Tropical Coconut, Honey-Roast Ham, Sweet Sour Meatballs, Marbled Steak"},
    {"Name": "Boxy", "Home": "Tropical Coast", "Gifts": "Meat Buns, Octopus Fritters, Spicy Hot Pot, Regular Tea, Sweet Juice, Black Tea, Mellow Cheese, Yogurt, Fresh Egg, Classic Donuts, Homemade Cookies, Extra-Fine Shaved ice, Rustic Red Bean Cake, Dark Roast Coffee, Aged Soy Beans, Manuka Honey, Roast Sweet Potato, Fresh Milk, Gold-Label Soda, Vintage Soda Pop, 2-Scoop Ice Cream, Cotton Candy, Zesty Crepes, Chocolate Bar, Steamed Cake, Black Tapioca, Nata de Coco"},
    {"Name": "Bananagro", "Home": "Tropical Coast", "Gifts": "Fresh Carrot, Regular Cucumber, Fresh Eggplant, Fresh Bell Pepper, Tiny Onion, Snow Potato, Chunky Pumpkin, Tasty Tomato, Chewy Mushroom, Rough Daikon Radish, Tough Avocado, Ripe Banana"},
    {"Name": "Dragtoise", "Home": "Tropical Coast", "Gifts": "Basic Bread, Spicy Curry, Fatty Tuna, Crunchy Shrimp, Soy Sauce Noodles, Stewed Udon Noodies, Basic Stew, Sushi, Pizza Margherita, Boiled Octopus, Sleepy Squid"},
    {"Name": "Tropinana", "Home": "Tropical Coast", "Gifts": "Protective Garlic, Spicy Corn, Giant Watermelon, Ripe Melon, Wild Strawberry, XL Orange, Dragon Fruit, Ripe Banana, Juicy Peach, Pineapple, Seaside Lemon, Rosy Apple, Tropical Coconut"},
    {"Name": "Snow D-Not", "Home": "Frozen Mountains", "Gifts": "Regular Tea, Sweet Juice, Dark Roast Coffee, Fresh Milk, Fatty Tuna, Crunchy Shrimp, Scissors, Pocket Mirror, Wind-up Doll, Fluffy Blanket, Sleepy Pillow, Antique Key, Plushie, Firework Rocket, Silver Spoon, Playing Cards, Broom, Tulips, Morning Glory, Sunflowers, Steel Pipe, Gold-Label Soda, Vintage Soda Pop, Black Tea, 1000-Year Bonsai, Eye-Catching Piece, Pink Trumpet, Boiled Octopus, Fan Letter, Grand Piano, Sleepy Squid, Party Pinata, Master Violin"},
    {"Name": "Snowpik", "Home": "Frozen Mountains", "Gifts": "Protective Garlic, Spicy Corn, Meteorite, Iron Ore, Bronze Ore, Silver Ore, Gold Ore"},
    {"Name": "I. C. Blok", "Home": "Frozen Mountains", "Gifts": "Meat Buns, Octopus Fritters, Spicy Hot Pot, Fresh Carrot, Regular Cucumber, Fresh Eggplant, Fresh Bell Pepper, Tiny Onion, Snow Potato, Chunky Pumpkin, Tasty Tomato, Chewy Mushroom, Rough Daikon Radish, Tough Avocado, Protective Garlic, Spicy Corn, Mellow Cheese, Yogurt, Fresh Egg, Aged Soy Beans, Extra-Fine Shaved Ice"},
    {"Name": "Reinbear", "Home": "Frozen Mountains", "Gifts": "Basic Bread, Spicy Curry, Soy Sauce Noodles, Stewed Udon Noodles, Basic Stew, Sushi, Pizza Margherita, Extra-Fine Shaved ice"},
    {"Name": "Chester Draw", "Home": "Frozen Mountains", "Gifts": "Basic Bread, Spicy Curry, Soy Sauce Noodles, Stewed Udon Noodles, Basic Stew, Sushi, Pizza Margherita, Regular Tea, Sweet Juice, Dark Roast Coffee, Extra-Fine Shaved Ice, Scissors, Antique Key, Plushie, Firework Rocket, Pocket Mirror, Wind-up Doll, Fluffy Blanket, Sleepy Pillow, Silver Spoon, Playing Cards, Broom, Fan Letter, Party Pinata, Pink Trumpet, Grand Piano, Master Violin, Tulips, Morning Glory, Sunflowers, Steel Pipe, 1000-Year Bonsai, Eye-Catching Piece"},
    {"Name": "Kerrrack", "Home": "Frozen Mountains", "Gifts": "Basic Bread, Spicy Curry, Soy Sauce Noodles, Stewed Udon Noodles, Basic Stew, Sushi, Pizza Margherita, Protective Garlic, Spicy Corn, Honey-Roast Ham, Sweet 'n Sour Meatballs, Marbled Steak, Extra-Fine Shaved Ice"},
    {"Name": "Iglor", "Home": "Frozen Mountains", "Gifts": "Regular Tea, Sweet Juice, Fresh Eggplant, Fresh Bell Pepper, Tiny Onion, Snow Potato, Dark Roast Coffee, Fresh Milk, Gold-Label Soda, Chunky Pumpkin, Vintage Soda Pop, Black Tea, Tasty Tomato, Chewy Mushroom, Fresh Carrot, Regular Cucumber, Rough Daikon Radish, Tough Avocado, Protective Garlic, Spicy Corn, Boiled Octopus, Sleepy Squid, Fatty Tuna, Crunchy Shrimp, Manuka Honey, 82-Scoop Ice Cream, Cotton Candy, Zesty Crepes, Classic Donuts, Homemade Cookies, Extra-Fine Shaved Ice, Rustic Red Bean Cake, Roast Sweet Potato, Chocolate Bar, Steamed Cake"},
    {"Name": "Frosty Claws", "Home": "Frozen Mountains", "Gifts": "Giant Watermelon, Ripe Melon, Wild Strawberry, XL Orange, Dragon Fruit, Ripe Banana, Juicy Peach, Pineapple, Seaside Lemon, Rosy Apple, Tropical Coconut, Extra-Fine Shaved ice"},
    {"Name": "Tuxy Hopper", "Home": "Frozen Mountains", "Gifts": "Giant Watermelon, Ripe Melon, Wild Strawberry, XL Orange, Dragon Fruit, Ripe Banana, Juicy Peach, Pineapple, Seaside Lemon, Rosy Apple, Tropical Coconut, Manuka Honey, 2-Scoop Ice Cream, Rustic Red Bean Cake, Roast Sweet Potato, Cotton Candy, Zesty Crepes, Classic Donuts, Homemade Cookies, Extra-Fine Shaved ice, Chocolate Bar, Steamed Cake, Black Tapioca, Nata de Coco, Beehive, Bat Wing, Lizard Tail, Bird's Nest, Magic Lamp, Doll, Crystal Ball, Fire Spellbook, Ice Spellbook, Lightning Spellbook, Darkness Spellbook, Healing Spellbook"},
    {"Name": "Icestein", "Home": "Frozen Mountains", "Gifts": "Fresh Carrot, Regular Cucumber, Fresh Eggplant, Fresh Bell Pepper, Tiny Onion, Snow Potato, Chunky Pumpkin, Tasty Tomato, Chewy Mushroom, Rough Daikon Radish, Tough Avocado, Honey-Roast Ham, Sweet Sour Meatballs, Marbled Steak, Extra-Fine Shaved Ice"},
    {"Name": "Electric Jellyfish", "Home": "Robot Research Lab", "Gifts": "Fresh Carrot, Regular Cucumber, Fresh Eggplant, Fresh Bell Pepper, Tiny Onion, Snow Potato, Chunky Pumpkin, Tasty Tomato, Chewy Mushroom, Rough Daikon Radish, Tough Avocado, Manuka Honey, 2-Scoop Ice Cream, Cotton Candy, Zesty Crepes, Classic Donuts, Homemade Cookies, Extra-Fine Shaved Ice, Rustic Red Bean Cake, Roast Sweet Potato, Chocolate Bar, Steamed Cake, Black Tapioca, Nata de Coco, Scissors, Pocket Mirror, Wind-up Doll, Fluffy Blanket, Sleepy Pillow, Fan Letter, Party Pinata, Antique Key, Plushie, Dap"},
    {"Name": "Billygoar", "Home": "Robot Research Lab", "Gifts": "Protective Garlic, Spicy Corn, Boiled Octopus, Sleepy Squid, Fatty Tuna, Crunchy Shrimp, Scissors, Pocket Mirror, Wind-up Doll, Fluffy Blanket, Sleepy Pillow, Fan Letter, Party Pinata, Antique Key, Plushie, Firework Rocket, Silver Spoon, Playing Cards, Broom, Pink Trumpet, Grand Piano, Master Violin, Tulips, Morning Glory, Sunflowers, Steel Pipe, 1000-Year Bonsai, Eye-Catching Piece"},
    {"Name": "Nana-Matic", "Home": "Robot Research Lab", "Gifts": "Protective Garlic, Spicy Corn, Giant Watermelon, Ripe Melon, Wild Strawberry, XL Orange, Dragon Fruit, Ripe Banana, Juicy Peach, Pineapple, Seaside Lemon, Rosy Apple, Tropical Coconut, Beehive, Bat Wing, Lizard Tail, Bird's Nest, Magic Lamp, Doll, Crystal Ball, Fire Spellbook, Ice Spellbook, Lightning Spellbook, Darkness Spellbook, Healing Spellbook, Meteorite, Iron Ore, Bronze Ore, Silver Ore, Gold Ore"},
    {"Name": "Maskoro", "Home": "Robot Research Lab", "Gifts": "Giant Watermelon, Ripe Melon, Wild Strawberry, Rosy Apple, Tropical Coconut, Fluffy Blanket, Sleepy Pillow, Boiled Octopus, XL Orange, Dragon Fruit, Ripe Banana, Juicy Peach, Pineapple, Seaside Lemon, Wind-up Doll, Sleepy Squid, Fatty Tuna, Party Pinata, Antique Key, Broom, Pink Trumpet, Grand Piano, Master Violin, Tulips, Crunchy Shrimp, Scissors, Plushie, Firework Rocket, Morning Glory, Sunflowers, Pocket Mirror, Silver Spoon, Steel Pipe, Playing Cards"},
    {"Name": "Boar X", "Home": "Robot Research Lab", "Gifts": "Basic Bread, Spicy Curry, Soy Sauce Noodles, Stewed Udon Noodles, Fresh Eggplant, Fresh Bell Pepper, Tiny Onion, Snow Potato, Manuka Honey, Chocolate Bar, Basic Stew, Chunky Pumpkin, 2-Scoop Ice Cream, Cotton Candy, Zesty Crepes, Classic Donuts, Steamed Cake, Black Tapioca, Nata de Coco, Beehive, Sushi, Pizza Margherita, Tasty Tomato, Chewy Mushroom, Homemade Cookies, Extra-Fine Shaved Ice, Bat Wing, Lizard Tail, Fresh Carrot, Rough Daikon Radish, Rustic Red Bean Cake, Regular Cucumber, Tough Avocado, Roast Sweet Potato"},
    {"Name": "Simibot", "Home": "Robot Research Lab", "Gifts": "Basic Bread, Spicy Curry, Soy Sauce Noodles, Stewed Udon Noodies, Basic Stew, Sushi, Pizza Margherita, Regular Tea, Sweet Juice, Dark Roast Coffee, Fresh Milk, Gold-Label Soda, Giant Watermelon, Ripe Melon, Wild Strawberry, XL Orange, Dragon Fruit, Ripe Banana, Juicy Peach, Pineapple, Seaside Lemon, Rosy Apple, Tropical Coconut, Scissors, Pocket Mirror, Wind-up Doll, Fluffy Blanket, Sleepy Pillow, Fan Letter, Party Pinata, Antique Key, Plushie, Firework Rocket, Silver Spoon"},
    {"Name": "Dragofsky", "Home": "Robot Research Lab", "Gifts": "Scissors, Pocket Mirror, Wind-up Doll, Fluffy Blanket, Sleepy Pillow, Party Pinata, Antique Key, Plushie, Firework Rocket, Silver Spoon, Playing Cards, Broom, Pink Trumpet, Grand Piano, Master Violin, Tulips, Morning Glory, Sunflowers, Steel Pipe, 1000-Year Bonsai, Eye-Catching Piece"},
    {"Name": "Donucchi", "Home": "Candy House", "Gifts": "Meat Buns, Octopus Fritters, Spicy Hot Pot, Honey-Roast Ham, Sweet 'n' Sour Meatballs, Marbled Steak, Mellow Cheese, Yogurt, Fresh Egg, Aged Soy Beans, Homemade Cookies, Beehive, Bat Wing, Lizard Tail, Bird's Nest, Magic Lamp, Doll, Crystal Ball, Fire Spellbook, Ice Spellbook, Lightning Spellbook, Darkness Spellbook, Healing Spellbook"},
    {"Name": "Metabok", "Home": "Candy House", "Gifts": "Basic Bread, Spicy Curry, Spicy Hot Pot, Fresh Carrot, Soy Sauce Noodles, Stewed Udon Noodles, Regular Cucumber, Fresh Eggplant, Chewy Mushroom, Rough Daikon Radish, Tough Avocado, Giant Watermelon, Juicy Peach, Pineapple, Basic Stew, Fresh Bell Pepper, Sushi, Pizza Margherita, Meat Buns, Octopus Fritters, Tiny Onion, Snow Potato, Chunky Pumpkin, Tasty Tomato, Ripe Melon, Wild Strawberry, XL Orange, Dragon Fruit, Ripe Banana, Seaside Lemon, Rosy Apple, Tropical Coconut"},
    {"Name": "Hatskee", "Home": "Candy House", "Gifts": "Beehive, Lightning Spellbook, Bat Wing, Darkness Spellbook, Lizard Tail, Healing Spellbook, Bird's Nest, Meteorite, Magic Lamp, Iron Ore, Doll, Bronze Ore, Crystal Ball, Silver Ore, Fire Spellbook, Gold Ore, Ice Spellbook"},
    {"Name": "Mechasaurus", "Home": "Candy House", "Gifts": "Mellow Cheese, Yogurt, Fresh Egg, Aged Soy Beans, Meat Buns, Octopus Fritters, Spicy Hot Pot"},
    {"Name": "Kuchenov", "Home": "Candy House", "Gifts": "Giant Watermelon, Ripe Melon, Wild Strawberry, XL Orange, Rosy Apple, Tropical Coconut, Manuka Honey, 2-Scoop Ice Cream, Rustic Red Bean Cake, Roast Sweet Potato, Chocolate Bar, Steamed Cake, Dragon Fruit, Ripe Banana, Juicy Peach, Pineapple, Seaside Lemon, Cotton Candy, Zesty Crepes, Classic Donuts, Homemade Cookies, Extra-Fine Shaved ice, Black Tapioca, Nata de Coco"},
    {"Name": "Magi Hatskee", "Home": "Candy House", "Gifts": "Regular Tea, Sweet Juice, Dark Roast Coffee, Fresh Milk, Gold-Label Soda, Vintage Soda Pop, Black Tea, Protective Garlic, Beehive, Bat Wing, Fan Letter, Lizard Tail, Bird's Nest, Scissors, Party Pinata, Antique Key, Plushie, Firework Rocket, Pocket Mirror, Silver Spoon, Spicy Corn, Wind-up Doll, Fluffy Blanket, Sleepy Pillow, Magic Lamp, Doll, Crystal Ball, Playing Cards, Broom, Pink Trumpet, Grand Piano, Master Violin, Fire Spellbook"},
    {"Name": "Tiss-U-Bok", "Home": "Candy House", "Gifts": "Meat Buns, Octopus Fritters, Spicy Hot Pot, Mellow Cheese, Yogurt, Fresh Egg, Aged Soy Beans, Beehive, Bat Wing, Lizard Tail, Bird's Nest, Scissors, Pocket Mirror, Wind-up Doll, Fluffy Blanket, Sleepy Pillow, Fan Letter, Party Pinata, Antique Key, Plushie, Firework Rocket, Silver Spoon, Magic Lamp, Doll, Crystal Ball, Playing Cards, Broom, Pink Trumpet, Grand Piano, Master Violin, Fire Spellbook, Ice Spellbook, Lightning Spellbook, Darkness Spellbook, Healing Spellbook"},
    {"Name": "Dragga", "Home": "Candy House", "Gifts": "Honey-Roast Ham, Sweet 'n' Sour Meatballs, Marbled Steak, Manuka Honey, 2-Scoop Ice Cream, Cotton Candy, Zesty Crepes, Extra Fine Shaved Ice, Rustic Red Bean Cake, Roast Sweet Potato, Chocolate Bar, Steamed Cake, Black Tapioca, Nata de Coco, Classic Donuts, Homemade Cookies"},
    {"Name": "Sugar Bawl", "Home": "Candy House", "Gifts": "Beehive, Bat Wing, Lizard Tail, Bird's Nest, Magic Lamp, Doll, Crystal Ball, Fire Spellbook, Ice Spellbook, Lightning Spellbook, Darkness Spellbook, Healing Spellbook"},
    {"Name": "Sparkee", "Home": "Rumbling Volcano", "Gifts": "Scissors, Pocket Mirror, Wind-up Doll, Fluffy Blanket, Sleepy Pillow, Firework Rocket, Silver Spoon, Playing Cards, Broom, Sunflowers, Steel Pipe, 1000-Year Bonsai, Eye-Catching Piece, Meteorite, Fan Letter, Pink Trumpet, Grand Piano, Iron Ore, Party Pinata, Antique Key, Plushie, Master Violin, Tulips, Morning Glory, Gold Ore, Bronze Ore, Silver Ore"},
    {"Name": "Moldmonch", "Home": "Rumbling Volcano", "Gifts": "Regular Tea, Sweet Juice, Dark Roast Coffee, Fresh Milk, Gold-Label Soda, Vintage Soda Pop, Black Tea, Giant Watermelon, Ripe Melon, Wild Strawberry, XL Orange, Dragon Fruit, Ripe Banana, Juicy Peach, Pineapple, Seaside Lemon, Manuka Honey, 2-Scoop Ice Cream, Cotton Candy, Zesty Crepes, Classic Donuts, Homemade Cookies, Extra-Fine Shaved Ice, Rosy Apple, Tropical Coconut, Rustic Red Bean Cake, Roast Sweet Potato, Chocolate Bar, Steamed Cake, Black Tapioca, Nata de Coco"},
    {"Name": "Skelefish", "Home": "Rumbling Volcano", "Gifts": "Giant Watermelon, Rosy Apple, Ripe Melon, Tropical Coconut, Wild Strawberry, XL Orange, Dragon Fruit, Ripe Banana, Juicy Peach, Pineapple, Seaside Lemon"},
    {"Name": "Magmate", "Home": "Rumbling Volcano", "Gifts": "Meat Buns, Octopus Fritters, Spicy Hot Pot, Regular Tea, Sweet Juice, Dark Roast Coffee, Fresh Milk, Gold-Label Soda, Vintage Soda Pop, Black Tea, Mellow Cheese, Yogurt, Fresh Egg, Aged Soy Beans"},
    {"Name": "Silencion", "Home": "Rumbling Volcano", "Gifts": "Lightning Spellbook, Bat Wing, Darkness Spellbook, Lizard Tail, Healing Spellbook, Bird's Nest, Meteorite, Magic Lamp, Iron Ore, Doll, Bronze Ore, Crystal Ball, Silver Ore, Fire Spellbook, Gold Ore, Ice Spellbook"},
    {"Name": "Gyropol", "Home": "Rumbling Volcano", "Gifts": "Honey-Roast Ham, Sweet 'n' Sour Meatballs, Marbled Steak, Basic Bread, Spicy Curry, Soy Sauce Noodles, Stewed Udon Noodles, Basic Stew, Sushi, Pizza Margherita, Protective Garlic, Spicy Corn, Boiled Octopus, Sleepy Squid, Fatty Tuna, Crunchy Shrimp"},
    {"Name": "Mag Max", "Home": "A Rumbling Volcano", "Gifts": "Protective Garlic, Fire Spellbook, Spicy Corn, Ice Spellbook, Beehive, Lightning Spellbook, Bat Wing, Lizard Tail, Bird's Nest, Magic Lamp, Darkness Spellbook, Healing Spellbook, Doll, Crystal Ball"},
    {"Name": "Dragtwins", "Home": "Rumbling Volcano", "Gifts": "Meat Buns, Octopus Fritters, Spicy Hot Pot, Mellow Cheese, Classic Donuts, Homemade Cookies, Cotton Candy, Zesty Crepes, Black Tapioca, Nata de Coco, Scissors, Antique Key, Plushie, Firework Rocket, Silver Spoon, Pocket Mirror, Yogurt, Extra-Fine Shaved Ice, Wind-up Doll, Playing Cards, Fresh Egg, Rustic Red Bean Cake, Fluffy Blanket, Broom, Aged Soy Beans, Manuka Honey, Roast Sweet Potato, Sleepy Pillow, Pink Trumpet, 2-Scoop Ice Cream, Chocolate Bar, Steamed Cake, Fan Letter, Party Pinata"},
    {"Name": "Banshetta", "Home": "Bustling Graveyard", "Gifts": "Basic Bread, Spicy Curry, Soy Sauce Noodles, Stewed Udon Noodles, Basic Stew, Sushi, Pizza Margherita, Regular Tea, Sweet Juice, Dark Roast Coffee, Fresh Milk, Gold-Label Soda, Vintage Soda Pop, Black Tea, Protective Garlic, Spicy Corn, Honey-Roast Ham, Sweet 'n Sour Meatballs, Marbled Steak, Manuka Honey, 2-Scoop Ice Cream, Cotton Candy, Zesty Crepes, Classic Donuts, Homemade Cookies, Extra-Fine Shaved Ice, Rustic Red Bean Cake, Roast Sweet Potato, Chocolate Bar, Steamed Cake, Black Tapioca, Nata de Coco"},
    {"Name": "Arachnon", "Home": "Bustling Graveyard", "Gifts": "Beehive, Bat Wing, Lizard Tail, Lightning Spellbook, Darkness Spellbook, Healing Spellbook, Bird's Nest, Magic Lamp, Doll, Crystal Ball, Fire Spellbook, Ice Spellbook"},
    {"Name": "Cariborn", "Home": "Bustling Graveyard", "Gifts": "Meat Buns, Octopus Fritters, Spicy Hot Pot, Honey-Roast Ham, Sweet 'n' Sour Meatballs, Marbled Steak, Mellow Cheese, Yogurt, Fresh Egg, Aged Soy Beans"},
    {"Name": "Pumpkeen", "Home": "Bustling Graveyard", "Gifts": "Chunky Pumpkin, Protective Garlic, Spicy Corn, Boiled Octopus, Sleepy Squid, Fatty Tuna, Crunchy Shrimp"},
    {"Name": "Gyozan", "Home": "Bustling Graveyard", "Gifts": "Giant Watermelon, Ripe Melon, Wild Strawberry, XL Orange, Dragon Fruit, Ripe Banana, Juicy Peach, Pineapple, Seaside Lemon, Rosy Apple, Tropical Coconut, Honey-Roast Ham, Classic Donuts, Homemade Cookies, Extra-Fine Shaved Ice, Sweet' Sour Meatballs, Rustic Red Bean Cake, Marbled Steak, Manuka Honey, 82-Scoop Ice Cream, Cotton Candy, Zesty Crepes, Roast Sweet Potato, Chocolate Bar, Steamed Cake, Black Tapioca, Nata de Coco"},
    {"Name": "Devvino", "Home": "Bustling Graveyard", "Gifts": "Basic Bread, Spicy Curry, Soy Sauce Noodles, Stewed Udon Noodies, Basic Stew, Sushi, Pizza Margherita, Wild Strawberry, XL Orange, Dragon Fruit, Ripe Banana, Juicy Peach, Pineapple, Seaside Lemon, Beehive, Lightning Spellbook, Darkness Spellbook, Lizard Tail, Healing Spellbook, Bat Wing, Bird's Nest, Magic Lamp, Doll, Crystal Ball, Fire Spellbook, Giant Watermelon, Ripe Melon, Rosy Apple, Tropical Coconut, Ice Spellbook"},
    {"Name": "Spiky", "Home": "Bustling Graveyard", "Gifts": "Basic Bread, Spicy Curry, Soy Sauce Noodles, Stewed Udon Noodles, Basic Stew, Sushi, Pizza Margherita, Regular Tea, Sweet Juice, Dark Roast Coffee, Fresh Milk, Gold-Label Soda, Vintage Soda Pop, Black Tea, Fresh Carrot, Regular Cucumber, Fresh Eggplant, Fresh Bell Pepper, Tiny Onion, Snow Potato, Chunky Pumpkin, Tasty Tomato, Chewy Mushroom, Rough Daikon Radish, Tough Avocado"},
    {"Name": "Jack O'", "Home": "Bustling Graveyard", "Gifts": "Chunky Pumpkin, Giant Watermelon, Ripe Melon, Wild Strawberry, XL Orange, Dragon Fruit, Ripe Banana, Juicy Peach, Pineapple, Seaside Lemon, Rosy Apple, Tropical Coconut, Honey-Roast Ham, Sweet' Sour Meatballs, Marbled Steak, Scissors, Pocket Mirror, Wind-up Doll, Fluffy Blanket, Sleepy Pillow, Fan Letter, Party Pinata, Antique Key, Plushie, Firework Rocket, Silver Spoon, Playing Cards, Broom, Pink Trumpet, Grand Piano, Master Violin, Tulips, Morning Glory, Sunflowers"},
    {"Name": "Ninjette", "Home": "Bustling Graveyard", "Gifts": "All Gems, Gold Ingot, No Likes"},
    {"Name": "Pellpo", "Home": "Towering Tower", "Gifts": "Protective Garlic, Boiled Octopus, Spicy Corn, Sleepy Squid, Basic Bread, Spicy Curry, Fatty Tuna, Crunchy Shrimp, Soy Sauce Noodies, Stewed Udon Noodles, Basic Stew, Sushi, Pizza Margherita"},
    {"Name": "Skwarkon", "Home": "Towering Tower", "Gifts": "Basic Bread, Spicy Curry, Soy Sauce Noodles, Stewed Udon Noodles, Basic Stew, Sushi, Pizza Margherita"},
    {"Name": "Boney Bones", "Home": "Towering Tower", "Gifts": "Honey-Roast Ham, Sweet 'n' Sour Meatballs, Marbled Steak, Fresh Carrot, Regular Cucumber, Fresh Eggplant, Fresh Bell Pepper, Tiny Onion, Snow Potato, Chunky Pumpkin, Tasty Tomato, Chewy Mushroom, Rough Daikon Radish, Tough Avocado, Protective Garlic, Spicy Corn, Boiled Octopus, Sleepy Squid, Fatty Tuna, Crunchy Shrimp, Scissors, Pocket Mirror, Wind-up Doll, Fluffy Blanket, Sleepy Pillow, Fan Letter, Party Pinata, Antique Key, Plushie, Firework Rocket, Silver Spoon, Playing Cards"},
    {"Name": "Mothard", "Home": "Towering Tower", "Gifts": "Protective Garlic, Spicy Corn, Honey-Roast Ham, Sweet 'n' Sour Meatballs, Magic Lamp, Doll, Crystal Ball, Fire Spellbook, Marbled Steak, Ice Spellbook, Beehive, Lightning Spellbook, Bat Wing, Darkness Spellbook, Lizard Tail, Healing Spellbook, Bird's Nest"},
    {"Name": "Pegasee", "Home": "Towering Tower", "Gifts": "Marbled Steak, Boiled Octopus, Sleepy Squid, Classic Donuts, Homemade Cookies, Extra-Fine Shaved Ice, Rustic Red Bean Cake, Basic Bread, Spicy Curry, Soy Sauce Noodles, Stewed Udon Noodies, Basic Stew, Sushi, Fatty Tuna, Crunchy Shrimp, Manuka Honey, Roast Sweet Potato, Pizza Margherita, Honey-Roast Ham, Sweet 'n' Sour Meatballs, 2-Scoop Ice Cream, Cotton Candy, Zesty Crepes, Chocolate Bar, Steamed Cake, Black Tapioca, Nata de Coco, Scissors, Pocket Mirror, Wind-up Doll, Fluffy Blanket, Sleepy Pillow"}
]

# --- SEARCH LOGIC ---

def get_sorted_image_files():
    if not os.path.exists(IMAGE_FOLDER):
        return []
    all_files = glob.glob(os.path.join(IMAGE_FOLDER, "*DCSmonsgift*"))
    image_files = [f for f in all_files if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
    def extract_number(filename):
        match_enc = re.search(r'%28(\d+)%29', os.path.basename(filename))
        if match_enc: return int(match_enc.group(1))
        match_std = re.search(r'\((\d+)\)', os.path.basename(filename))
        if match_std: return int(match_std.group(1))
        match_any = re.search(r'(\d+)', os.path.basename(filename))
        if match_any: return int(match_any.group(1))
        return 999999 
    return sorted(image_files, key=extract_number)

def perform_search(search_type):
    query = entry_search.get().lower().strip()
    text_results.config(state=tk.NORMAL)
    text_results.delete(1.0, tk.END)
    text_results.images = [] 

    if not query:
        text_results.insert(tk.END, "Please type a search term.")
        text_results.config(state=tk.DISABLED)
        return

    # Filter logic
    matches = []
    for index, m in enumerate(MONSTER_DB):
        if search_type == "name":
            if query in m["Name"].lower():
                matches.append((index, m))
        elif search_type == "item":
            if query in m["Gifts"].lower():
                matches.append((index, m))

    if not matches:
        text_results.insert(tk.END, f"No results found for '{query}'.")
    else:
        all_images = get_sorted_image_files()
        
        for i, (index, m) in enumerate(matches):
            if index < len(all_images):
                img_path = all_images[index]
                try:
                    pil_img = Image.open(img_path)
                    
                    # 1. CROP FACE 
                    face_img = pil_img.crop(FACE_BOX)
                    photo_face = ImageTk.PhotoImage(face_img)
                    text_results.images.append(photo_face)
                    
                    # 2. DETECT BEIGE GIFT LIST
                    img_np = np.array(pil_img)
                    target = np.array(TARGET_COLOR_RGB)
                    lower = np.clip(target - TOLERANCE, 0, 255)
                    upper = np.clip(target + TOLERANCE, 0, 255)
                    mask = cv2.inRange(img_np, lower, upper)
                    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    
                    gift_photo = None
                    if contours:
                        largest = max(contours, key=cv2.contourArea)
                        x, y, w, h = cv2.boundingRect(largest)
                        if w > 100 and h > 100:
                            gift_crop = pil_img.crop((x, y, x+w, y+h))
                            gift_photo = ImageTk.PhotoImage(gift_crop)
                            text_results.images.append(gift_photo)
                    
                    # --- DISPLAY ---
                    text_results.image_create(tk.END, image=photo_face)
                    text_results.insert(tk.END, "\n\n")
                    
                    text_results.insert(tk.END, f"Monster: {m['Name']}\n", "header")
                    text_results.insert(tk.END, f"Home: {m['Home']}\n", "home")
                    text_results.insert(tk.END, "\n")
                    
                    text_results.insert(tk.END, "Gift Effectiveness\n", "visual_header")
                    if gift_photo:
                        text_results.insert(tk.END, "\n") 
                        text_results.image_create(tk.END, image=gift_photo)
                    else:
                        text_results.insert(tk.END, "[Could not auto-detect list]\n")
                    
                    text_results.insert(tk.END, "\n") 
                    
                except Exception as e:
                    text_results.insert(tk.END, f"[Img Error: {e}] ")
            else:
                text_results.insert(tk.END, "[No Image Found] ")
            
            # --- TEXT LIST ---
            text_results.insert(tk.END, "\nExtracted Gift List\n\n", "text_header")
            
            raw_gifts = m['Gifts']
            if raw_gifts:
                gift_list = [g.strip() for g in raw_gifts.split(',')]
                gift_list.sort(key=lambda s: s.lower())
                
                # LOOP through gifts to highlight matches
                for j, gift in enumerate(gift_list):
                    # Partial match highlight logic
                    if search_type == "item" and query and query in gift.lower():
                        text_results.insert(tk.END, gift, "highlight")
                    else:
                        text_results.insert(tk.END, gift)
                    
                    # Comma separator
                    if j < len(gift_list) - 1:
                        text_results.insert(tk.END, ", ")
                        
                text_results.insert(tk.END, "\n")

            # --- SEPARATOR LOGIC ---
            # Add line if more than 1 result found, and NOT the last item
            if len(matches) > 1 and i < len(matches) - 1:
                text_results.insert(tk.END, "-"*215 + "\n\n")
            else:
                text_results.insert(tk.END, "\n\n")

    text_results.config(state=tk.DISABLED)

def search_by_name(event=None):
    perform_search("name")

def search_by_item():
    perform_search("item")

# --- GUI SETUP ---

root = tk.Tk()
root.title("Demon Castle Gift Search")
root.geometry("1235x930")
root.configure(bg=COLOR_BG_MAIN)

# Input Frame
frame_top = tk.Frame(root, padx=10, pady=10, bg=COLOR_BG_MAIN)
frame_top.pack(fill=tk.X)

lbl_instr = tk.Label(frame_top, text="Enter Search Term:", bg=COLOR_BG_MAIN, fg=COLOR_TEXT_WHITE, font=("Helvetica", 11))
lbl_instr.pack(side=tk.LEFT)

entry_search = tk.Entry(frame_top, bg=COLOR_INPUT_BG, fg=COLOR_TEXT_WHITE, insertbackground='white', font=("Helvetica", 11))
entry_search.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
entry_search.bind("<Return>", search_by_name) 

# Buttons
btn_name = tk.Button(frame_top, text="Search Monster", command=search_by_name, bg=COLOR_BTN_BG, fg=COLOR_TEXT_WHITE, font=("Helvetica", 10, "bold"), padx=10)
btn_name.pack(side=tk.LEFT, padx=5)

btn_item = tk.Button(frame_top, text="Search Item", command=search_by_item, bg=COLOR_BTN_BG, fg=COLOR_TEXT_WHITE, font=("Helvetica", 10, "bold"), padx=10)
btn_item.pack(side=tk.LEFT, padx=5)

# Results Area
text_results = scrolledtext.ScrolledText(root, wrap=tk.WORD, padx=20, pady=20, bg=COLOR_BG_MAIN, fg=COLOR_TEXT_WHITE, insertbackground='white', font=("Helvetica", 11))
text_results.pack(fill=tk.BOTH, expand=True)

# Styling Tags
text_results.tag_config("header", font=("Helvetica", 16, "bold underline"), foreground=COLOR_VERMILION)
text_results.tag_config("home", font=("Helvetica", 14, "bold italic"), foreground=COLOR_ROYAL_PURPLE)
text_results.tag_config("visual_header", font=("Helvetica", 16, "bold underline"), foreground=COLOR_VERMILION)
text_results.tag_config("text_header", font=("Helvetica", 14, "bold underline"), foreground=COLOR_VERMILION)
text_results.tag_config("highlight", background=COLOR_HIGHLIGHT, foreground="black")

text_results.images = []

root.mainloop()