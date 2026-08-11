# data_loader.py

import json
import os
import logging

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_cards(region):
    """
    Load crop/farming practice cards from a JSON file based on the region.
    """
    try:
        file_path = os.path.join(BASE_DIR, 'data', f'{region.lower()}_cards.json')
        with open(file_path, 'r') as f:
            cards = json.load(f)
        return cards
    except Exception as e:
        logging.error(f"Error loading cards for {region}: {e}")
        return []

def load_dynamic_messages(region):
    """
    Load dynamic messages from a text file based on the region.
    """
    try:
        file_path = os.path.join(BASE_DIR, 'static', 'messages', f'{region.lower()}_messages.txt')
        with open(file_path, 'r') as f:
            messages = [line.strip().strip('"') for line in f if line.strip()]
        return messages
    except Exception as e:
        logging.error(f"Error loading messages for {region}: {e}")
        return ["Welcome to the Crop Recommendation System!"]

def load_top_messages():
    """
    Load top messages from topmessage.txt.
    """
    try:
        file_path = os.path.join(BASE_DIR, 'static', 'messages', 'topmessage.txt')
        with open(file_path, 'r') as f:
            messages = [line.strip().strip('"') for line in f if line.strip()]
        return messages
    except Exception as e:
        logging.error(f"Error loading top messages: {e}")
        return ["Welcome to the Crop Recommendation System!"]
