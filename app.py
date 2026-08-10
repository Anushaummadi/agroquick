from flask import Flask, render_template, request, redirect, session
import os

app = Flask(__name__)
app.secret_key = "agroquick123"


# =========================================================
# PRODUCT CATALOG
# =========================================================

PRODUCTS = [

    # SEEDS
    {
        "name": "Rice Seeds",
        "category": "Seeds",
        "price": 100,
        "url": "/seeds",
        "keywords": [
            "rice", "seed", "seeds", "paddy",
            "వరి", "వరి విత్తనాలు",
            "బియ్యం", "बीज", "धान", "तांदूळ"
        ]
    },

    {
        "name": "Wheat Seeds",
        "category": "Seeds",
        "price": 120,
        "url": "/seeds",
        "keywords": [
            "wheat", "seed", "seeds",
            "గోధుమ", "గోధుమ విత్తనాలు",
            "गेहूं", "गहू", "கோதுமை", "ಗೋಧಿ"
        ]
    },

    {
        "name": "Maize Seeds",
        "category": "Seeds",
        "price": 150,
        "url": "/seeds",
        "keywords": [
            "maize", "corn", "seed", "seeds",
            "మొక్కజొన్న", "మొక్కజొన్న విత్తనాలు",
            "मक्का", "மக்காச்சோளம்", "ಮೆಕ್ಕೆಜೋಳ"
        ]
    },

    {
        "name": "Vegetable Seeds",
        "category": "Seeds",
        "price": 80,
        "url": "/seeds",
        "keywords": [
            "vegetable", "vegetables",
            "seed", "seeds",
            "కూరగాయలు", "కూరగాయల విత్తనాలు",
            "सब्जी", "भाजी", "காய்கறி", "ತರಕಾರಿ"
        ]
    },


    # FERTILIZER
    {
        "name": "Urea Fertilizer",
        "category": "Fertilizer",
        "price": 500,
        "url": "/fertilizer",
        "keywords": [
            "urea",
            "యూరియా",
            "यूरिया",
            "युरिया",
            "யூரியா",
            "ಯೂರಿಯಾ"
        ]
    },

    {
        "name": "Fertilizer",
        "category": "Fertilizer",
        "price": 450,
        "url": "/fertilizer",
        "keywords": [
            "fertilizer", "fertilizers", "manure",
            "ఎరువు", "ఎరువులు",
            "खाद", "उर्वरक", "खत",
            "உரம்", "ರಸಗೊಬ್ಬರ"
        ]
    },


    # EQUIPMENT
    {
        "name": "Water Pump",
        "category": "Equipment",
        "price": 2500,
        "url": "/equipment",
        "keywords": [
            "water pump", "pump", "watering",
            "water", "irrigation",
            "నీటి పంపు", "నీటి మోటార్",
            "పారుదల",
            "पानी का पंप", "सिंचाई",
            "पाण्याचा पंप",
            "தண்ணீர் பம்ப்",
            "நீர்ப்பாசனம்",
            "ನೀರಿನ ಪಂಪ್"
        ]
    },

    {
        "name": "Seed Drill",
        "category": "Equipment",
        "price": 8000,
        "url": "/equipment",
        "keywords": [
            "seed drill", "planting", "sowing",
            "seed planting", "seeds planting",
            "విత్తడం", "విత్తనాలు వేయడం",
            "बुवाई", "बीज बोना",
            "पेरणी",
            "விதைப்பு",
            "ಬಿತ್ತನೆ"
        ]
    },

    {
        "name": "Mini Cultivator",
        "category": "Equipment",
        "price": 12000,
        "url": "/equipment",
        "keywords": [
            "cultivator", "cultivation",
            "soil cultivation", "soil",
            "plough", "plowing",
            "నేల", "నేల సాగు",
            "मिट्टी", "जुताई",
            "माती", "नांगरणी",
            "மண்", "உழவு",
            "ಮಣ್ಣು", "ಉಳುಮೆ"
        ]
    },

    {
        "name": "Sprayer",
        "category": "Equipment",
        "price": 3500,
        "url": "/equipment",
        "keywords": [
            "sprayer", "spraying", "spray",
            "crop spraying", "pesticide spraying",
            "స్ప్రేయర్", "పిచికారీ",
            "स्प्रे", "छिड़काव",
            "फवारणी",
            "தெளிப்பான்",
            "ಸಿಂಪಡಣೆ"
        ]
    },


    # TOOLS
    {
        "name": "Hand Hoe",
        "category": "Tools",
        "price": 450,
        "url": "/tools",
        "keywords": [
            "hoe", "hand hoe", "dig", "digging",
            "soil preparation", "soil",
            "మట్టి తవ్వడం", "మట్టి",
            "खुदाई", "मिट्टी",
            "खोदणे",
            "தோண்டுதல்",
            "ಮಣ್ಣು ಅಗೆಯುವುದು"
        ]
    },

    {
        "name": "Pruning Shears",
        "category": "Tools",
        "price": 350,
        "url": "/tools",
        "keywords": [
            "pruning", "pruning shears",
            "cut branches", "cutting branches",
            "trim plants", "cut plants",
            "కొమ్మలు కత్తిరించడం",
            "पौधे काटना", "शाखाएं काटना",
            "फांद्या कापणे",
            "கிளைகளை வெட்ட",
            "ಕೊಂಬೆಗಳನ್ನು ಕತ್ತರಿಸುವುದು"
        ]
    },

    {
        "name": "Water