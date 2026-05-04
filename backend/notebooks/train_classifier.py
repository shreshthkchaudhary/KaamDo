"""
Train Task Classifier — TF-IDF + Logistic Regression
=====================================================

This script trains a text classifier that categorizes task descriptions into
one of 7 categories. It generates synthetic training data (300+ samples),
trains the model, evaluates it, and saves the .pkl file.

Run this script to generate the classifier model:
    python train_classifier.py
"""

import os
import random
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

random.seed(42)
np.random.seed(42)

# ═══════════════════════════════════════════════════════════════
# 1. SYNTHETIC TRAINING DATA — ~50 examples per category
# ═══════════════════════════════════════════════════════════════

training_data = {
    'Home Repair': [
        "Fix the ceiling fan in my bedroom, it's making noise",
        "Repair a leaking kitchen tap urgently",
        "Need an electrician to fix wiring in my house",
        "My bathroom door hinge is broken, need repair",
        "Paint two rooms in my apartment, walls are peeling",
        "Fix the broken window glass in the living room",
        "Plumber needed to unclog the bathroom drain",
        "Replace the old switchboard in the kitchen",
        "Install a new exhaust fan in the bathroom",
        "Fix the broken tile on the kitchen floor",
        "Need someone to repair a broken water pipe",
        "Carpenter needed to fix my wooden cupboard",
        "AC repair needed, not cooling properly",
        "Install a new door lock for front door",
        "Fix a cracked wall in the bedroom",
        "Repair the main gate, the hinge broke",
        "Need plumber to fix the geyser, not heating",
        "Electrician needed to install new tube lights",
        "Repaint the exterior wall of my house",
        "Fix the washing machine outlet pipe leak",
        "Replace a broken window pane in bedroom",
        "Need someone to repair a dripping faucet",
        "Fix the short circuit in living room wiring",
        "Carpenter needed for door frame repair",
        "Install a ceiling light in the new room",
        "Fix the broken railing on the staircase",
        "Repair the roof where water is leaking",
        "Need electrician to fix power socket issue",
        "Fix the toilet flush mechanism, it's stuck",
        "Repaint my kitchen cabinets, they look old",
        "Need someone to fix my inverter connection",
        "Repair cracked bathroom tiles near shower",
        "Fix the broken latch on the balcony door",
        "Need a plumber to install a new washbasin",
        "Repair the chimney hood, not working properly",
        "Replace old rusted water taps in bathroom",
        "Fix my doorbell, it stopped working",
        "Need carpenter to build a shoe rack",
        "Install a new mirror with proper wall mount",
        "Fix the sagging false ceiling in hall",
        "Repair the garage door motor mechanism",
        "Need electrician for MCB tripping issue",
        "Fix the broken towel rod in bathroom",
        "Install curtain rods in three rooms",
        "Repair the grout between kitchen tiles",
    ],
    'Education': [
        "Need a math tutor for my 10th grade son",
        "Looking for someone to teach Python programming",
        "English speaking classes needed for 3 months",
        "Help my daughter prepare for JEE Main exam",
        "Need a science teacher for class 8 student",
        "Teach me guitar at my home on weekends",
        "Looking for IELTS preparation coaching",
        "Need help with college assignment in physics",
        "Hindi teacher needed for a foreign student",
        "Prepare my child for CBSE board exams",
        "Music teacher needed for piano lessons at home",
        "Help me learn basic accounting and tally",
        "Need a tutor for competitive exam preparation",
        "Teach spoken French, beginner level",
        "Need help with MBA entrance exam coaching",
        "Chemistry tutor needed for class 12 student",
        "Looking for a drawing teacher for kids",
        "Teach me Excel and data analysis basics",
        "Need someone to help with school homework daily",
        "Biology tutoring for NEET preparation",
        "Private tutor for class 5 all subjects",
        "Need coaching for government job exams",
        "Teach me digital marketing from scratch",
        "Looking for a dance teacher for Bharatanatyam",
        "Need GRE coaching and study material guidance",
        "Help me prepare for CA inter exams",
        "Yoga instructor needed for home sessions",
        "Teach my kid basic swimming techniques",
        "Need a tutor for Sanskrit language",
        "Help with research paper writing in English",
        "Looking for spoken German language teacher",
        "Statistics tutor for B.Com student needed",
        "Teach me video editing using Premiere Pro",
        "Need a vocal music teacher for classical training",
        "Help with thesis writing and formatting",
        "Looking for a teacher for Vedic mathematics",
        "Computer science tutor for BCA student",
        "Need coaching for UPSC prelims exam",
        "Teach me calligraphy at my home",
        "Help me learn basic web development HTML CSS",
        "Need personal trainer for fitness coaching",
        "Looking for art teacher for oil painting",
        "Teach me cooking different cuisines at home",
        "Help my child with reading and phonics",
        "Need someone for competitive coding guidance",
    ],
    'Delivery': [
        "Pick up a parcel from Koramangala and deliver to HSR Layout",
        "Need someone to deliver food from my restaurant daily",
        "Courier a document from my office to another branch",
        "Pick up medicine from Apollo pharmacy and deliver home",
        "Deliver birthday cake from bakery to my friend's house",
        "Need someone to drop my laptop for repair and pick it up",
        "Transport important files from home to office quickly",
        "Pick up grocery order from BigBasket warehouse",
        "Deliver flowers to an address for anniversary surprise",
        "Need a courier for returning an Amazon package",
        "Pick up clothes from the dry cleaner",
        "Deliver invitation cards to 10 different addresses",
        "Bring my tiffin box from home to office before lunch",
        "Pick up a printed banner from the shop",
        "Deliver some books to my friend in the next colony",
        "Transport a small package to the post office",
        "Pick up shoes from the cobbler and deliver home",
        "Need someone to deliver diwali gifts to 5 addresses",
        "Collect my passport from VFS centre",
        "Deliver a bouquet to my mother's workplace",
        "Transport medical reports from lab to doctor's clinic",
        "Pick up repaired phone from the service centre",
        "Deliver exam forms to university before deadline",
        "Send a parcel to another city via bus service",
        "Pick up pet food from the store and deliver",
        "Deliver a small furniture item to a nearby address",
        "Collect visa documents from embassy and bring home",
        "Transport homemade food to elderly parents' house",
        "Pick up customized T-shirts from the print shop",
        "Deliver spare key to my roommate at the office",
        "Transport freshly baked goods to the event venue",
        "Pick up my watch from the repair shop",
        "Send legal documents to lawyer's office urgently",
        "Deliver craft supplies to school for exhibition",
        "Pick up art supplies from the stationery store",
        "Deliver lunch boxes to construction site workers",
        "Transport a birthday gift to a surprise party venue",
        "Pick up a cycle from the repair shop nearby",
        "Deliver monthly groceries to my parents' house",
        "Send a return package via DTDC courier office",
        "Pick up framed photo from the framing shop",
        "Deliver medicines to my grandmother's home",
        "Transport study materials to hostel",
        "Pick up an order from Decathlon store",
        "Deliver prasad boxes to temple visitors",
    ],
    'Labour & Moving': [
        "Need help shifting furniture from 2nd floor to ground floor",
        "Laborers needed to load truck with warehouse goods",
        "Help me relocate to a new flat, need 3 workers",
        "Unload a truck full of construction material",
        "Need help carrying heavy boxes up to 4th floor",
        "Workers needed to arrange furniture in new office",
        "Help pack and move my entire apartment",
        "Need manual labor for garden digging work",
        "Help lift and install a heavy AC outdoor unit",
        "Moving office furniture to new building",
        "Need 2 people to help move a washing machine",
        "Labor for loading furniture into a moving truck",
        "Help shift heavy almirahs to the storage room",
        "Need workers to demolish old brick wall",
        "Pack and relocate kitchen items to new house",
        "Help rearrange all furniture in living room",
        "Need manual help for rooftop water tank installation",
        "Workers to carry sand bags to the construction site",
        "Help dismantling old furniture for disposal",
        "Moving heavy gym equipment to the basement",
        "Need someone to carry boxes during house shifting",
        "Labor needed for warehouse stock arrangement",
        "Help with packing fragile items for moving",
        "Lift and place heavy sofa set in the hall",
        "Need workers for unloading building materials",
        "Help moving fridge and TV to new apartment",
        "Manual labor needed for clearing old godown",
        "Workers required for event stage setup",
        "Help pack books and crockery for relocation",
        "Need laborers to lay paver blocks in driveway",
        "Move all belongings from hostel room to home",
        "Labor for dismantling temporary shed structure",
        "Help carry mattresses and beds upstairs",
        "Workers to arrange chairs for wedding function",
        "Need people to move piano to the first floor",
        "Unload container of imported goods at shop",
        "Help shift industrial equipment to factory floor",
        "Need laborers for brick stacking at construction site",
        "Move old furniture to charity donation centre",
        "Help with heavy lifting during renovation work",
        "Workers needed for loading scrap metal into truck",
        "Shifting generator to the terrace area",
        "Need help relocating aquarium to new place safely",
        "Move items from one storage unit to another",
        "Labor for breaking and removing old floor tiles",
    ],
    'Cleaning': [
        "Deep clean my 3BHK apartment before Diwali",
        "Need someone to clean the sofa and carpet",
        "Bathroom deep cleaning, heavy limescale buildup",
        "Clean and organize the kitchen thoroughly",
        "Window cleaning for my 10th floor apartment",
        "Need help cleaning after a house party",
        "Sanitize and clean an office space, 500 sq ft",
        "Clean the terrace and remove bird droppings",
        "Deep cleaning of AC ducts and filters",
        "Wash and iron a large pile of clothes",
        "Need someone to mop the entire house daily",
        "Car interior cleaning and vacuuming needed",
        "Clean and polish all the wooden furniture",
        "Wash heavy curtains and bed covers",
        "Kitchen exhaust chimney cleaning needed",
        "Post-construction cleaning of new flat",
        "Clean the water tank and sump",
        "Need someone for daily sweeping and mopping",
        "Clean the garden area and remove dry leaves",
        "Upholstery cleaning for dining chairs",
        "Deep clean oven and microwave inside out",
        "Need weekly house cleaning service",
        "Clean garage and organize stored items",
        "Scrub and clean bathroom tiles and grout",
        "Vacuum clean all carpets in the living room",
        "Need someone to clean swimming pool area",
        "Polish marble floors in the entire house",
        "Clean and disinfect baby room completely",
        "Remove stains from walls and repaint spots",
        "Deep cleaning before moving into rented flat",
        "Clean the exhaust fan and kitchen hood",
        "Wash car exterior and polish for wedding",
        "Need help with spring cleaning entire house",
        "Clean behind heavy furniture in bedroom",
        "Sanitize the house after COVID recovery",
        "Clean air cooler before summer season",
        "Dust and clean all bookshelves and showpieces",
        "Clean water purifier and replace filters",
        "Post-renovation dust cleaning of apartment",
        "Need someone to iron clothes twice a week",
        "Clean balcony and remove cobwebs",
        "Organize and clean children's play area",
        "Wash and clean all ceiling fans in house",
        "Deep clean the fridge inside and outside",
        "Clean copper and brass utensils for festival",
    ],
    'Tech Help': [
        "Format my laptop and install Windows fresh",
        "Need help setting up WiFi router at home",
        "Fix my printer, it's not connecting to the computer",
        "Install antivirus software on my office computers",
        "Help transfer data from old phone to new phone",
        "Set up my new smart TV and connect to internet",
        "My computer is very slow, need someone to speed it up",
        "Help install CCTV cameras in my shop",
        "Fix Bluetooth connectivity issue on my laptop",
        "Need help building a simple website for my business",
        "Set up email on all office computers",
        "Recover data from a corrupted hard drive",
        "Help me set up a home server for file sharing",
        "Install and configure a projector for office use",
        "Fix my desktop computer, it's not turning on",
        "Need help with Google Workspace setup for team",
        "Install dual monitor setup on my work desk",
        "Help fix mobile phone screen display issue",
        "Set up POS billing system in my retail shop",
        "Configure firewall and network security for office",
        "Need someone to fix the intercom system",
        "Install and configure NAS storage device",
        "Help with social media account setup for business",
        "Fix my gaming console, not reading discs",
        "Set up Alexa and smart home devices",
        "Repair my UPS battery backup system",
        "Need help migrating data to cloud storage",
        "Install software for CCTV remote viewing",
        "Fix touchpad not working on my laptop",
        "Set up zoom and online meeting tools for office",
        "Help install operating system on assembled PC",
        "Configure biometric attendance machine",
        "Need help creating app for my small business",
        "Fix network printer sharing issue in office",
        "Set up automated backup system for computers",
        "Help with MacBook troubleshooting and repair",
        "Install Tally accounting software and train",
        "Fix audio issues on desktop speakers",
        "Need website maintenance and hosting setup",
        "Set up security cameras with mobile viewing",
        "Help debug errors in my Python project",
        "Configure VPN for remote office access",
        "Fix slow internet and optimize WiFi coverage",
        "Set up digital signage display for shop",
        "Need help with data entry automation Excel macros",
    ],
    'General': [
        "Need someone to walk my dog twice a day",
        "Looking for a photographer for birthday party",
        "Need help decorating for a house warming party",
        "Stand in queue for me at passport office",
        "Need a cook for a dinner party of 20 people",
        "Help me organize my book collection at home",
        "Need someone to water my plants while I travel",
        "Babysitter needed for evening hours this weekend",
        "Help with filling out government forms online",
        "Need someone to do grocery shopping for me",
        "Looking for a mehendi artist for wedding",
        "Pet grooming needed for my golden retriever",
        "Need help assembling furniture from IKEA",
        "Looking for someone to manage event registration",
        "Help pick up my kids from school daily",
        "Need a DJ for house party this Saturday",
        "Looking for someone to design a birthday banner",
        "Help me plan and organize a surprise party",
        "Need someone to feed my cats while I'm away",
        "Looking for a tailor for blouse stitching",
        "Help with garden maintenance and lawn mowing",
        "Need someone for grocery delivery every week",
        "Looking for help with wedding invitation writing",
        "Need a helper for elderly care during daytime",
        "Personal assistant needed for daily errands",
        "Help me declutter and organize my wardrobe",
        "Need volunteer helpers for community cleanup drive",
        "Looking for event planner for small party",
        "Help me file my income tax returns online",
        "Need someone to take care of my aquarium fish",
        "Looking for a makeup artist for engagement",
        "Help me set up a small home garden",
        "Need someone to accompany elderly to hospital",
        "Looking for a standup comedian for office party",
        "Help paint artwork for my living room wall",
        "Need someone for part-time data entry work",
        "Help me arrange a pooja ceremony at home",
        "Looking for a calligrapher for wedding cards",
        "Need a driver for airport drop early morning",
        "Help me organize storage room and attic",
        "Looking for someone to help with party catering",
        "Need a temporary receptionist for one week",
        "Help me create a photo album of memories",
        "Looking for house sitter while I'm on vacation",
        "Need someone to take passport photos at home",
    ],
}

# ═══════════════════════════════════════════════════════════════
# 2. CREATE DATAFRAME
# ═══════════════════════════════════════════════════════════════

texts = []
labels = []
for category, examples in training_data.items():
    for example in examples:
        texts.append(example)
        labels.append(category)

df = pd.DataFrame({'description': texts, 'category': labels})
print(f"Total training samples: {len(df)}")
print(f"\nCategory distribution:\n{df['category'].value_counts()}")

# ═══════════════════════════════════════════════════════════════
# 3. TRAIN–TEST SPLIT & MODEL TRAINING
# ═══════════════════════════════════════════════════════════════

X_train, X_test, y_train, y_test = train_test_split(
    df['description'], df['category'],
    test_size=0.2, random_state=42, stratify=df['category']
)

print(f"\nTrain size: {len(X_train)}, Test size: {len(X_test)}")

# Build a pipeline: TF-IDF → Logistic Regression
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2),
        stop_words='english',
        min_df=1
    )),
    ('clf', LogisticRegression(
        max_iter=1000,
        random_state=42,
        C=10,
        class_weight='balanced'
    ))
])

pipeline.fit(X_train, y_train)

# ═══════════════════════════════════════════════════════════════
# 4. EVALUATION
# ═══════════════════════════════════════════════════════════════

y_pred = pipeline.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"\n{'='*60}")
print(f"ACCURACY: {accuracy:.4f} ({accuracy*100:.1f}%)")
print(f"{'='*60}")

print(f"\nClassification Report:\n")
print(classification_report(y_test, y_pred))

print(f"\nConfusion Matrix:\n")
cm = confusion_matrix(y_test, y_pred, labels=pipeline.classes_)
print(f"Labels: {list(pipeline.classes_)}")
print(cm)

# ═══════════════════════════════════════════════════════════════
# 5. SAVE MODEL
# ═══════════════════════════════════════════════════════════════

model_dir = os.path.join(os.path.dirname(__file__), '..', 'ai', 'models')
os.makedirs(model_dir, exist_ok=True)

model_path = os.path.join(model_dir, 'classifier.pkl')
joblib.dump(pipeline, model_path)
print(f"\nModel saved to: {model_path}")

# ═══════════════════════════════════════════════════════════════
# 6. TEST WITH NEW EXAMPLES
# ═══════════════════════════════════════════════════════════════

test_descriptions = [
    "My kitchen tap is leaking badly",
    "Need someone to teach my son math for board exams",
    "Deliver a package from MG Road to Whitefield",
    "Help me shift my entire apartment furniture",
    "Deep clean my house before the festival",
    "My laptop screen is broken, need repair",
    "Need a photographer for my wedding reception",
]

print(f"\n{'='*60}")
print("LIVE PREDICTIONS ON NEW EXAMPLES")
print(f"{'='*60}\n")

for desc in test_descriptions:
    cat = pipeline.predict([desc])[0]
    conf = pipeline.predict_proba([desc]).max() * 100
    print(f"  \"{desc}\"")
    print(f"  -> {cat} (confidence: {conf:.1f}%)\n")
