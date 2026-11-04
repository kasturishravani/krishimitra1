"""
KrishiMitra - Agricultural Knowledge Base & Sample Local Datasets
Contains comprehensive local datasets for Weather, Mandi Prices, Diseases,
Government Schemes, Farming Tips, Emergency Contacts, Services, and Advisory.
"""

from datetime import datetime, timedelta

# ==========================================
# 1. WEATHER INFORMATION
# ==========================================
def get_weather_data(district="Nirmal"):
    """Returns dynamic current weather and 5-day forecast for given district."""
    today = datetime.now()
    districts = {
        "Nirmal": {"temp": 31, "condition": "Partly Cloudy", "humidity": 68, "wind": 14, "rain_prob": 20, "uv": 7, "air_quality": "Moderate (64)"},
        "Adilabad": {"temp": 32, "condition": "Sunny", "humidity": 62, "wind": 12, "rain_prob": 15, "uv": 8, "air_quality": "Good (48)"},
        "Nizamabad": {"temp": 30, "condition": "Clear Sky", "humidity": 65, "wind": 11, "rain_prob": 10, "uv": 8, "air_quality": "Moderate (58)"},
        "Warangal": {"temp": 29, "condition": "Light Rain Likely", "humidity": 78, "wind": 16, "rain_prob": 65, "uv": 5, "air_quality": "Good (42)"},
        "Karimnagar": {"temp": 31, "condition": "Partly Cloudy", "humidity": 66, "wind": 13, "rain_prob": 25, "uv": 7, "air_quality": "Good (52)"},
        "Guntur": {"temp": 33, "condition": "Humid & Sunny", "humidity": 74, "wind": 18, "rain_prob": 30, "uv": 9, "air_quality": "Moderate (71)"},
        "Khammam": {"temp": 32, "condition": "Cloudy", "humidity": 72, "wind": 15, "rain_prob": 40, "uv": 6, "air_quality": "Good (45)"},
        "Pune": {"temp": 28, "condition": "Pleasant Breeze", "humidity": 58, "wind": 10, "rain_prob": 5, "uv": 7, "air_quality": "Good (50)"},
        "Karnal": {"temp": 26, "condition": "Clear Sky", "humidity": 55, "wind": 9, "rain_prob": 0, "uv": 6, "air_quality": "Poor (120)"}
    }
    
    current = districts.get(district, districts["Nirmal"])
    
    forecast_days = []
    conditions_cycle = [
        ("Sunny", "bi-sun-fill", "text-warning", 15, 0),
        ("Partly Cloudy", "bi-cloud-sun-fill", "text-info", 25, 2),
        ("Scattered Showers", "bi-cloud-rain-fill", "text-primary", 65, 8),
        ("Thunderstorm", "bi-cloud-lightning-rain-fill", "text-secondary", 80, 22),
        ("Clear Sky", "bi-brightness-high-fill", "text-warning", 10, 0)
    ]
    
    for i in range(1, 6):
        f_date = today + timedelta(days=i)
        cond = conditions_cycle[(i - 1) % len(conditions_cycle)]
        forecast_days.append({
            "day": f_date.strftime("%a"),
            "date": f_date.strftime("%d %b"),
            "condition": cond[0],
            "icon": cond[1],
            "icon_color": cond[2],
            "max_temp": current["temp"] + (1 if i % 2 == 0 else -1),
            "min_temp": current["temp"] - 9 + (i % 3),
            "rain_prob": cond[3],
            "rainfall_mm": cond[4],
            "humidity": current["humidity"] + (5 if cond[3] > 50 else -3)
        })
        
    advisories = [
        {
            "category": "Pesticide Spraying",
            "status": "Safe in Morning" if current["rain_prob"] < 40 else "Avoid Today",
            "badge": "success" if current["rain_prob"] < 40 else "warning",
            "message": "Favorable dry window between 7:00 AM and 11:30 AM with gentle wind (< 15 km/h). Avoid afternoon if clouds build up." if current["rain_prob"] < 40 else "High rain probability detected. Postpone foliar sprays to prevent chemical wash-off."
        },
        {
            "category": "Irrigation Guidance",
            "status": "Standard Watering" if current["rain_prob"] < 50 else "Hold Irrigation",
            "badge": "info" if current["rain_prob"] < 50 else "warning",
            "message": "Continue regular light irrigation for vegetable and fruit crops during evening hours." if current["rain_prob"] < 50 else "Hold off watering today as scattered rainfall is predicted over the next 24-48 hours. Conserve groundwater."
        },
        {
            "category": "Disease Alert",
            "status": "Medium Fungal Risk",
            "badge": "warning",
            "message": "Relative humidity above 65% combined with warm temperatures creates favorable conditions for Paddy blast and Chilli powdery mildew. Inspect field edges."
        },
        {
            "category": "Harvesting Window",
            "status": "Favorable",
            "badge": "success",
            "message": "Optimal dry hours for threshing, drying, and field transport in the next 3 days before shower probabilities increase."
        }
    ]
    
    return {
        "district": district,
        "date_str": today.strftime("%A, %d %B %Y"),
        "current": current,
        "forecast": forecast_days,
        "advisories": advisories
    }


# ==========================================
# 2. MANDI PRICES (MARKET RATES / E-NAM)
# ==========================================
MANDI_PRICES = [
    {
        "id": 1,
        "state": "Telangana",
        "district": "Nirmal",
        "mandi": "Nirmal APMC Market",
        "commodity": "Paddy (Dhan)",
        "variety": "BPT 5204 (Samba Mahsuri)",
        "min_price": 2350,
        "max_price": 2680,
        "modal_price": 2520,
        "unit": "Rs / Quintal",
        "trend": "up",
        "change_pct": "+2.8%",
        "arrivals_tonnes": 480,
        "date": "Today"
    },
    {
        "id": 2,
        "state": "Telangana",
        "district": "Adilabad",
        "mandi": "Adilabad Cotton Yard",
        "commodity": "Cotton (Kapas)",
        "variety": "Long Staple (Bunny/Bt)",
        "min_price": 7200,
        "max_price": 7850,
        "modal_price": 7580,
        "unit": "Rs / Quintal",
        "trend": "up",
        "change_pct": "+1.6%",
        "arrivals_tonnes": 620,
        "date": "Today"
    },
    {
        "id": 3,
        "state": "Telangana",
        "district": "Warangal",
        "mandi": "Enumamula Agricultural Market",
        "commodity": "Chilli (Red Mirchi)",
        "variety": "Teja Hot",
        "min_price": 17500,
        "max_price": 22400,
        "modal_price": 20200,
        "unit": "Rs / Quintal",
        "trend": "down",
        "change_pct": "-1.4%",
        "arrivals_tonnes": 310,
        "date": "Today"
    },
    {
        "id": 4,
        "state": "Telangana",
        "district": "Nizamabad",
        "mandi": "Nizamabad Grain Mandi",
        "commodity": "Turmeric (Haldi)",
        "variety": "Finger Salem / Rajapore",
        "min_price": 12800,
        "max_price": 15600,
        "modal_price": 14250,
        "unit": "Rs / Quintal",
        "trend": "up",
        "change_pct": "+4.1%",
        "arrivals_tonnes": 240,
        "date": "Today"
    },
    {
        "id": 5,
        "state": "Telangana",
        "district": "Nirmal",
        "mandi": "Bhainsa Sub-Market",
        "commodity": "Soybean",
        "variety": "JS 335 / Yellow",
        "min_price": 4300,
        "max_price": 4720,
        "modal_price": 4580,
        "unit": "Rs / Quintal",
        "trend": "stable",
        "change_pct": "0.0%",
        "arrivals_tonnes": 390,
        "date": "Today"
    },
    {
        "id": 6,
        "state": "Telangana",
        "district": "Karimnagar",
        "mandi": "Karimnagar APMC",
        "commodity": "Maize (Makka)",
        "variety": "Hybrid Yellow",
        "min_price": 2050,
        "max_price": 2320,
        "modal_price": 2210,
        "unit": "Rs / Quintal",
        "trend": "up",
        "change_pct": "+1.9%",
        "arrivals_tonnes": 510,
        "date": "Today"
    },
    {
        "id": 7,
        "state": "Telangana",
        "district": "Tandur",
        "mandi": "Tandur Dal Market",
        "commodity": "Red Gram (Tur/Arhar)",
        "variety": "Tandur GI Desi",
        "min_price": 8900,
        "max_price": 10400,
        "modal_price": 9850,
        "unit": "Rs / Quintal",
        "trend": "up",
        "change_pct": "+3.2%",
        "arrivals_tonnes": 180,
        "date": "Today"
    },
    {
        "id": 8,
        "state": "Andhra Pradesh",
        "district": "Guntur",
        "mandi": "Guntur Mirchi Yard",
        "commodity": "Chilli (Red Mirchi)",
        "variety": "Guntur 334 / Sannam",
        "min_price": 18200,
        "max_price": 23500,
        "modal_price": 21100,
        "unit": "Rs / Quintal",
        "trend": "up",
        "change_pct": "+2.1%",
        "arrivals_tonnes": 850,
        "date": "Today"
    },
    {
        "id": 9,
        "state": "Andhra Pradesh",
        "district": "Kurnool",
        "mandi": "Kurnool Commercial Yard",
        "commodity": "Groundnut (Moongphali)",
        "variety": "Pod TMV-2",
        "min_price": 6100,
        "max_price": 6850,
        "modal_price": 6550,
        "unit": "Rs / Quintal",
        "trend": "stable",
        "change_pct": "+0.5%",
        "arrivals_tonnes": 260,
        "date": "Today"
    },
    {
        "id": 10,
        "state": "Andhra Pradesh",
        "district": "Chittoor",
        "mandi": "Madanapalle Tomato Yard",
        "commodity": "Tomato",
        "variety": "Hybrid Desi / Sahu",
        "min_price": 1400,
        "max_price": 2200,
        "modal_price": 1800,
        "unit": "Rs / Quintal",
        "trend": "down",
        "change_pct": "-4.2%",
        "arrivals_tonnes": 720,
        "date": "Today"
    },
    {
        "id": 11,
        "state": "Haryana",
        "district": "Karnal",
        "mandi": "Karnal Grain Market",
        "commodity": "Wheat (Gehun)",
        "variety": "Sharbati / HD 2967",
        "min_price": 2400,
        "max_price": 2750,
        "modal_price": 2580,
        "unit": "Rs / Quintal",
        "trend": "up",
        "change_pct": "+1.1%",
        "arrivals_tonnes": 920,
        "date": "Today"
    }
]

# Historical 6-month price trends for Chart.js
MANDI_HISTORICAL_TRENDS = {
    "months": ["Jun", "Jul", "Aug", "Sep", "Oct", "Nov"],
    "paddy": [2180, 2220, 2300, 2390, 2460, 2520],
    "cotton": [7100, 7250, 7150, 7350, 7480, 7580],
    "chilli": [22500, 21800, 21000, 20500, 19800, 20200],
    "maize": [1980, 2030, 2100, 2150, 2180, 2210]
}

# MSP (Minimum Support Price) Reference Guide
MSP_DATA = [
    {"commodity": "Paddy (Common)", "msp_2024_25": 2300, "msp_2025_26": 2420, "increase": "+120"},
    {"commodity": "Cotton (Medium Staple)", "msp_2024_25": 7121, "msp_2025_26": 7521, "increase": "+400"},
    {"commodity": "Maize", "msp_2024_25": 2090, "msp_2025_26": 2225, "increase": "+135"},
    {"commodity": "Soybean (Yellow)", "msp_2024_25": 4600, "msp_2025_26": 4892, "increase": "+292"},
    {"commodity": "Tur / Arhar (Red Gram)", "msp_2024_25": 7550, "msp_2025_26": 8100, "increase": "+550"},
    {"commodity": "Groundnut", "msp_2024_25": 6783, "msp_2025_26": 7130, "increase": "+347"},
    {"commodity": "Wheat", "msp_2024_25": 2275, "msp_2025_26": 2425, "increase": "+150"}
]


# ==========================================
# 3. CROP DISEASE & PEST DIRECTORY
# ==========================================
CROP_DISEASES = [
    {
        "id": 1,
        "crop": "Paddy (Rice)",
        "name": "Rice Blast (Pyricularia oryzae)",
        "te_name": "వరి అగ్గితెగులు (బ్లాస్ట్)",
        "type": "Fungal",
        "severity": "Severe",
        "badge": "danger",
        "symptoms": "Spindle-shaped or eye-shaped lesions with gray/whitish centers and reddish-brown borders on leaves. Neck blast causes blackening of panicle nodes, causing heads to break and grain to remain empty/chaffy.",
        "causes": "High humidity (> 85%), prolonged leaf wetness (dew or light drizzles), night temperatures around 20-24°C, excessive nitrogenous fertilizer application.",
        "organic_remedy": "Foliar spray of 5% Neem Seed Kernel Extract (NSKE) or Pseudomonas fluorescens @ 10g/liter of water. Avoid water stagnation.",
        "chemical_remedy": "Tricyclazole 75% WP @ 0.6 g/liter OR Isoprothiolane 40% EC @ 1.5 ml/liter OR Kasugamycin 3% SL @ 2.5 ml/liter. Repeat after 10-12 days if required.",
        "prevention": "Treat seeds with Carbendazim 2g/kg seed before nursery sowing. Avoid excessive split application of Urea. Maintain optimal plant spacing.",
        "keywords": ["blast", "spindle", "leaf spots", "chaffy grain", "neck rot", "వరి అగ్గితెగులు", "వరి"]
    },
    {
        "id": 2,
        "crop": "Cotton",
        "name": "Pink Bollworm (Pectinophora gossypiella)",
        "te_name": "పత్తి గులాబీ రంగు కాయతొలుచు పురుగు",
        "type": "Pest / Insect",
        "severity": "Severe",
        "badge": "danger",
        "symptoms": "Rosetted flowers that fail to open properly. Larvae burrow into developing bolls, eating seeds and staining lint. Small exit holes with brown frass.",
        "causes": "Late planting, continuous monocropping of cotton, high temperature with moderate humidity during flowering and boll formation.",
        "organic_remedy": "Install 5-8 Pheromone Traps per acre with Gossyplure septa for monitoring and mass trapping. Release Trichogramma egg parasitoids @ 60,000/acre.",
        "chemical_remedy": "Chlorantraniliprole 18.5% SC @ 0.3 ml/liter OR Emamectin Benzoate 5% SG @ 0.4 g/liter OR Profenofos 50% EC @ 2 ml/liter during peak moth flight.",
        "prevention": "Destroy cotton stalks after harvest; do not ratoon the crop. Plant non-Bt refuge crops around borders. Pick bolls cleanly.",
        "keywords": ["pink bollworm", "rosetted flower", "boll damage", "caterpillar", "cotton pest", "గులాబీ రంగు పురుగు", "పత్తి"]
    },
    {
        "id": 3,
        "crop": "Chilli",
        "name": "Chilli Leaf Curl (Gemini Virus / Thrips-Mites complex)",
        "te_name": "మిరప ఆకుముడుత తెగులు",
        "type": "Viral / Vector-Borne",
        "severity": "Severe",
        "badge": "danger",
        "symptoms": "Upward curling and boat-shaped leaves indicate thrips attack; downward curling and thickening of leaves indicate yellow mite damage. Severe stunting with reduced fruit set.",
        "causes": "Warm and dry weather favors thrips multiplication; humid cloudy weather favors yellow mites. Whiteflies transmit the Gemini virus.",
        "organic_remedy": "Install 15-20 Yellow and Blue Sticky Traps per acre. Spray 10,000 PPM Neem Oil @ 2 ml/liter + soap nut solution. Spray Sour buttermilk (5 liters fermented in 100L water).",
        "chemical_remedy": "For Thrips: Fipronil 5% SC @ 2 ml/liter OR Spinetoram 11.7% SC @ 0.9 ml/liter. For Mites: Diafenthiuron 50% WP @ 1.2 g/liter OR Spiromesifen 22.9% SC @ 1 ml/liter.",
        "prevention": "Erect barrier crops of 3-4 rows of Maize, Sorghum, or Bajra around chilli fields to block vector insects. Maintain clean bunds.",
        "keywords": ["leaf curl", "upward curl", "downward curl", "thrips", "mites", "stunted chilli", "ఆకుముడుత", "మిరప"]
    },
    {
        "id": 4,
        "crop": "Paddy (Rice)",
        "name": "Yellow Stem Borer (Scirpophaga incertulas)",
        "te_name": "వరి కాండం తొలుచు పురుగు (మొగి పురుగు)",
        "type": "Pest / Insect",
        "severity": "Moderate",
        "badge": "warning",
        "symptoms": "Drying of central shoot in vegetative stage causing 'Dead Heart' which easily pulls out. At flowering/panicle stage, panicles turn white and dry completely, known as 'White Earhead'.",
        "causes": "Excessive nitrogen, standing deep water, delayed transplanting.",
        "organic_remedy": "Clip seedling leaf tips before transplanting to destroy egg masses. Set up light traps (1 trap/acre). Release egg parasitoid Trichogramma japonicum.",
        "chemical_remedy": "Cartap Hydrochloride 4% GR @ 7.5 kg/acre broadcast in moist soil OR Chlorantraniliprole 0.4% G @ 4 kg/acre OR Spray Cartap 50% SP @ 2 g/liter.",
        "prevention": "Harvest at ground level. Deep summer plowing to expose pupae to birds and sun.",
        "keywords": ["stem borer", "dead heart", "white earhead", "mogi purugu", "వరి కాండం తొలుచు పురుగు", "వరి"]
    },
    {
        "id": 5,
        "crop": "Tomato",
        "name": "Early Blight (Alternaria solani)",
        "te_name": "టమోటా ముందస్తు ఎండు తెగులు",
        "type": "Fungal",
        "severity": "Moderate",
        "badge": "warning",
        "symptoms": "Dark brown to black target-like concentric rings on older leaves near the soil. Leaves turn yellow around spots and drop prematurely. Sunken lesions near stem.",
        "causes": "Warm temperatures (24-29°C) and high humidity or frequent overhead irrigation.",
        "organic_remedy": "Mulch soil around plants to prevent soil spores splashing onto lower leaves. Spray Panchagavya (3%) or Trichoderma harzianum @ 5g/liter.",
        "chemical_remedy": "Mancozeb 75% WP @ 2.5 g/liter OR Chlorothalonil 75% WP @ 2 g/liter OR Azoxystrobin 23% SC @ 1 ml/liter.",
        "prevention": "Adopt drip irrigation instead of sprinkler/flood. Practice 2-year crop rotation with non-solanaceous crops. Prune lower diseased foliage.",
        "keywords": ["tomato blight", "concentric rings", "leaf drop", "yellowing", "టమోటా తెగులు"]
    },
    {
        "id": 6,
        "crop": "Maize (Corn)",
        "name": "Fall Armyworm (Spodoptera frugiperda)",
        "te_name": "మొక్కజొన్న కత్తెర పురుగు",
        "type": "Pest / Insect",
        "severity": "Severe",
        "badge": "danger",
        "symptoms": "Pinholes and large windowpanes on whorl leaves. Significant sawdust-like fecal matter (frass) accumulated in leaf whorls. Head with inverted 'Y' mark.",
        "causes": "Warm and dry weather spells followed by vegetative flush.",
        "organic_remedy": "Application of sand mixed with dry neem seed powder (9:1 ratio) directly into central whorls. Spray Metarhizium rileyi or Bacillus thuringiensis (Bt) @ 2 g/liter.",
        "chemical_remedy": "Emamectin Benzoate 5% SG @ 0.4 g/liter OR Spinetoram 11.7% SC @ 0.5 ml/liter directed into the leaf whorl using knapsack sprayer with nozzle cap removed.",
        "prevention": "Intercrop maize with cowpea or pigeon pea. Early synchronous sowing across community fields.",
        "keywords": ["fall armyworm", "whorl damage", "sawdust frass", "faw", "కత్తెర పురుగు", "మొక్కజొన్న"]
    },
    {
        "id": 7,
        "crop": "Wheat",
        "name": "Yellow / Stripe Rust (Puccinia striiformis)",
        "te_name": "గోధుమ పసుపు రంగు కుంకుమ తెగులు",
        "type": "Fungal",
        "severity": "Severe",
        "badge": "danger",
        "symptoms": "Yellowish-orange pustules arranged in linear stripes/rows on leaf blades, leaf sheaths, and glumes. Golden powder rubs off on fingers.",
        "causes": "Cool and moist weather (night temp 10-15°C) with persistent fog or dew.",
        "organic_remedy": "Spray fermented garlic-chilli extract. Dust sulphur powder at initial disease notice.",
        "chemical_remedy": "Propiconazole 25% EC (Tilt) @ 1 ml/liter OR Tebuconazole 25.9% EC @ 1 ml/liter immediately upon noticing first yellow stripe foci.",
        "prevention": "Plant rust-resistant certified varieties (HD 3086, DBW 187, DBW 222). Avoid late sowing.",
        "keywords": ["wheat rust", "yellow stripe", "pustules", "powder", "కుంకుమ తెగులు", "గోధుమ"]
    },
    {
        "id": 8,
        "crop": "Groundnut",
        "name": "Tikka Leaf Spot (Cercospora personata)",
        "te_name": "వేరుశనగ తిక్కా ఆకుమచ్చ తెగులు",
        "type": "Fungal",
        "severity": "Moderate",
        "badge": "warning",
        "symptoms": "Circular to irregular dark brown spots surrounded by yellow halos on leaves. Severe spotting leads to complete defoliation, leaving bare stems.",
        "causes": "Prolonged high humidity, heavy dew, temperature between 25-30°C.",
        "organic_remedy": "Spray cow urine solution (10% diluted) mixed with neem leaf extract. Soil application of Trichoderma viride enriched FYM.",
        "chemical_remedy": "Carbendazim 12% + Mancozeb 63% WP (Saaf) @ 2 g/liter OR Hexaconazole 5% EC @ 2 ml/liter.",
        "prevention": "Seed treatment with Thiram or Trichoderma before sowing. Destroy crop debris after digging.",
        "keywords": ["tikka", "leaf spot", "groundnut defoliation", "వేరుశనగ తిక్కా తెగులు", "వేరుశనగ"]
    }
]


# ==========================================
# 4. GOVERNMENT SCHEMES INFORMATION
# ==========================================
GOVERNMENT_SCHEMES = [
    {
        "id": 1,
        "code": "PM-KISAN",
        "title": "Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)",
        "te_title": "ప్రధాన మంత్రి కిసాన్ సమ్మాన్ నిధి",
        "category": "Direct Income Support",
        "badge": "success",
        "benefit": "Rs 6,000 per year directly transferred to bank account in 3 equal four-monthly installments of Rs 2,000 each.",
        "eligibility": "All landholding farmer families having cultivable landholding in their names (subject to exclusion criteria for high income / institutional landholders).",
        "documents": ["Aadhaar Card linked with Mobile", "Land ownership documents (Pattadar Passbook / RoR 1B)", "Active Bank Account with NPCI Direct Benefit Transfer (DBT) enabled", "Citizenship proof"],
        "how_to_apply": "1. Visit the official portal pmkisan.gov.in -> 'Farmer Corner'.\n2. Click on 'New Farmer Registration'.\n3. Enter Aadhaar number, state, and mobile number to receive OTP.\n4. Fill survey number, khata number, and land extent.\n5. Alternatively, register at your nearest CSC (Common Service Centre) or MeeSeva.",
        "official_url": "https://pmkisan.gov.in",
        "contact_helpline": "155261 / 011-24300606"
    },
    {
        "id": 2,
        "code": "PMFBY",
        "title": "Pradhan Mantri Fasal Bima Yojana (Crop Insurance)",
        "te_title": "ప్రధాన మంత్రి ఫసల్ బీమా యోజన",
        "category": "Crop Insurance & Risk",
        "badge": "primary",
        "benefit": "Comprehensive financial protection against non-preventable crop yield losses due to natural calamities, drought, floods, pests & diseases. Premium: only 1.5% for Rabi, 2% for Kharif, 5% for commercial/horticultural crops; rest paid by Govt.",
        "eligibility": "All farmers including sharecroppers and tenant farmers growing notified crops in notified areas.",
        "documents": ["Aadhaar Card", "Land Possession Certificate / Sowing Certificate", "Bank Passbook copy", "Cropping Declaration verified by Village Revenue Officer (VRO)"],
        "how_to_apply": "1. Apply online on pmfby.gov.in before cutoff date (usually July 31 for Kharif, Dec 31 for Rabi).\n2. Loanee farmers are enrolled through their financing bank branches.\n3. Non-loanee farmers can register through CSC or local banking correspondent.",
        "official_url": "https://pmfby.gov.in",
        "contact_helpline": "1800-180-1551"
    },
    {
        "id": 3,
        "code": "SOIL-HEALTH",
        "title": "Soil Health Card Scheme",
        "te_title": "సాయిల్ హెల్త్ కార్డు పథకం (నేల ఆరోగ్య పత్రం)",
        "category": "Soil Testing & Fertility",
        "badge": "info",
        "benefit": "Free customized report showing 12 parameters (N, P, K, S, Zn, Fe, Cu, Mn, Bo, pH, EC, OC) of farmer's field soil along with crop-wise optimal fertilizer and manure recommendations.",
        "eligibility": "All farmers across India possessing agricultural land.",
        "documents": ["Farmer ID / Aadhaar", "Field location (Survey Number, Village, Mandal)", "Land record details"],
        "how_to_apply": "1. Contact local Agriculture Extension Officer (AEO) or nearest Krishi Vigyan Kendra (KVK).\n2. Soil samples are collected following zigzag grid method by extension staff.\n3. Card is generated and distributed after laboratory analysis with dosage guidelines.",
        "official_url": "https://soilhealth.dac.gov.in",
        "contact_helpline": "011-23382012"
    },
    {
        "id": 4,
        "code": "KCC",
        "title": "Kisan Credit Card (KCC) Scheme",
        "te_title": "కిసాన్ క్రెడిట్ కార్డు పథకం",
        "category": "Affordable Farm Credit",
        "badge": "warning",
        "benefit": "Hassle-free institutional crop loan up to Rs 3,00,000 at concessional interest rate of 4% per annum (with 3% prompt repayment incentive). Collateral-free limit up to Rs 1.60 lakh.",
        "eligibility": "Individual/joint farmers, owner cultivators, tenant farmers, oral lessees, and Self Help Groups (SHGs) of farmers.",
        "documents": ["Duly filled application form", "Two passport size photographs", "ID proof (Aadhaar/Voter ID)", "Address proof", "Land records certified by revenue authorities"],
        "how_to_apply": "1. Download form from bank website (SBI, PNB, Apex Cooperative Banks).\n2. Submit to bank branch with revenue land extract.\n3. Loan sanctioned within 14 days and KCC RuPay smart card issued.",
        "official_url": "https://www.myscheme.gov.in/schemes/kcc",
        "contact_helpline": "1800-180-1551"
    },
    {
        "id": 5,
        "code": "SMAM",
        "title": "Sub-Mission on Agricultural Mechanization (SMAM)",
        "te_title": "వ్యవసాయ యాంత్రీకరణ పథకం (సబ్సిడీ పరికరాలు)",
        "category": "Farm Machinery Subsidy",
        "badge": "secondary",
        "benefit": "40% to 50% subsidy on purchase of agricultural machinery such as Tractors, Power Tillers, Rotavators, Multi-crop Threshers, Laser Levelers, and Agricultural Drones.",
        "eligibility": "Small and marginal farmers, women farmers, SC/ST farmers given highest priority.",
        "documents": ["Aadhaar Card", "Pattadar Passbook", "Caste Certificate (if applicable)", "Bank account copy with IFSC", "Quotation from authorized implement dealer"],
        "how_to_apply": "1. Register on agrimachinery.nic.in portal.\n2. Select requested machinery and nearest registered dealer.\n3. Department inspects and issues administrative sanction.\n4. Subsidy directly credited through DBT to bank account.",
        "official_url": "https://agrimachinery.nic.in",
        "contact_helpline": "011-23381012"
    },
    {
        "id": 6,
        "code": "PMKSY",
        "title": "Pradhan Mantri Krishi Sinchayee Yojana (Per Drop More Crop)",
        "te_title": "ప్రధాన మంత్రి కృషి సించాయి యోజన (బిందు సేద్యం)",
        "category": "Micro Irrigation Subsidy",
        "badge": "success",
        "benefit": "Up to 55% for small/marginal farmers and 45% for other farmers for installation of Drip and Sprinkler irrigation systems to save 40-50% water.",
        "eligibility": "Farmers with an assured irrigation water source (Borewell/Well/Canal) and title deed.",
        "documents": ["Aadhaar Card", "Pattadar Passbook / 1B", "Borewell certificate / Electricity consumer bill", "Soil and Water testing report"],
        "how_to_apply": "Apply through State Horticulture / Micro Irrigation department portal or Mandal Agriculture Office.",
        "official_url": "https://pmksy.gov.in",
        "contact_helpline": "1800-425-3577"
    },
    {
        "id": 7,
        "code": "RYTHU-BANDHU",
        "title": "Rythu Bandhu & Rythu Bima (Telangana State)",
        "te_title": "రైతు బంధు & రైతు బీమా (తెలంగాణ)",
        "category": "State Investment Support",
        "badge": "primary",
        "benefit": "Investment support of Rs 10,000 per acre per year (Rs 5,000 per season) directly to bank account, plus Rs 5,00,000 free life insurance cover for farmers aged 18-59.",
        "eligibility": "All titleholder farmers registered in Dharani portal in Telangana.",
        "documents": ["Dharani Digital Passbook / Khatadar number", "Aadhaar Card", "Aadhaar-linked Bank Passbook"],
        "how_to_apply": "Automatic DBT based on revenue land records in Dharani portal. Check status on rythubandhu.telangana.gov.in.",
        "official_url": "http://rythubandhu.telangana.gov.in",
        "contact_helpline": "040-2338-3520"
    }
]


# ==========================================
# 5. FARMING TIPS & BEST PRACTICES
# ==========================================
FARMING_TIPS = [
    {
        "id": 1,
        "category": "Soil Health & Composting",
        "title": "Preparation & Application of Jeevamrutha (జీవామృతం)",
        "te_title": "జీవామృతం తయారీ మరియు వినియోగం",
        "icon": "bi-flower1",
        "difficulty": "Easy",
        "summary": "Jeevamrutha is a potent natural bio-inoculant that multiplies beneficial soil microorganisms, improves aeration, and enhances plant nutrient uptake.",
        "steps": [
            "Take a 200-liter plastic drum and add 10 kg fresh indigenous cow dung and 10 liters cow urine.",
            "Add 2 kg jaggery (organic cane sugar) and 2 kg pulse flour (gram flour / besan).",
            "Add a handful of virgin forest soil or fertile field bund soil.",
            "Fill with clean water to 200 liters and stir clockwise with a wooden stick for 5 minutes twice a day.",
            "Keep covered in shade with a jute gunny bag for 48 hours for microbial fermentation.",
            "Apply via irrigation water (200 liters/acre) or spray filtered liquid (10% solution) every 15-20 days."
        ]
    },
    {
        "id": 2,
        "category": "Water Management",
        "title": "Alternate Wetting and Drying (AWD) in Paddy",
        "te_title": "వరిలో తడి మరియు ఆరబెట్టు పద్ధతి",
        "icon": "bi-droplet-half",
        "difficulty": "Moderate",
        "summary": "AWD saves up to 30% irrigation water and reduces methane emissions in rice without reducing crop yields.",
        "steps": [
            "Install a 30 cm long perforated PVC field pipe (10-15 cm diameter) into the soil, keeping 10 cm above ground.",
            "Remove soil from inside the pipe so bottom water level can be viewed easily.",
            "Irrigate to 5 cm standing water level after transplanting.",
            "Allow water level to naturally recede until it drops 15 cm below soil surface inside the pipe.",
            "Re-irrigate only when water disappears 15 cm below surface. Maintain continuous water only during flowering stage."
        ]
    },
    {
        "id": 3,
        "category": "Organic Pest Control",
        "title": "5% Neem Seed Kernel Extract (NSKE) Spray",
        "te_title": "5% వేప గింజల కషాయం తయారీ",
        "icon": "bi-shield-check",
        "difficulty": "Easy",
        "summary": "Natural broad-spectrum repellent and anti-feedant effective against sucking pests, leaf folders, and caterpillars.",
        "steps": [
            "Take 5 kg well-dried neem seed kernels and crush them into a coarse powder.",
            "Tie the powder in a clean muslin cloth bag and soak overnight in 10 liters of clean water.",
            "Squeeze the pouch repeatedly next morning until the decoction turns milky light brown.",
            "Filter the solution and dilute with water to make a total volume of 100 liters.",
            "Add 100 grams of soap flakes or 50 ml mild detergent as sticking agent before spraying."
        ]
    },
    {
        "id": 4,
        "category": "Crop Rotation & Intercropping",
        "title": "Legume Intercropping in Cotton & Maize",
        "te_title": "పత్తి మరియు మొక్కజొన్నలో అంతర పంటలు",
        "icon": "bi-grid-3x3-gap-fill",
        "difficulty": "Easy",
        "summary": "Growing pulses like Cowpea, Green Gram, or Black Gram as an intercrop fixes atmospheric nitrogen and controls weed growth.",
        "steps": [
            "Plant 1 row of Cowpea or Green Gram between two rows of Cotton or Maize (1:1 or 2:1 ratio).",
            "Legume root nodules fix 30-40 kg atmospheric nitrogen per hectare, saving chemical fertilizer costs.",
            "Acts as live mulch, reducing soil moisture evaporation by 25%.",
            "Provides additional income in 60-70 days before main crop canopy closes."
        ]
    },
    {
        "id": 5,
        "category": "Post-Harvest Management",
        "title": "Safe Grain Storage & Moisture Management",
        "te_title": "ధాన్యాల సురక్షిత నిల్వ విధానం",
        "icon": "bi-box-seam",
        "difficulty": "Easy",
        "summary": "Prevent storage weevils, fungal rotting, and mycotoxins by bringing moisture content below threshold before bagging.",
        "steps": [
            "Sun-dry paddy grains until moisture drops below 13-14%; for maize and pulses, maintain below 10-12%.",
            "Perform fingernail test: thoroughly dried grains crack with a crisp sound when pressed with thumbnail.",
            "Clean and fumigate storage bins. Line metal silos with neem leaves to ward off storage beetles.",
            "Use hermetic multi-layer bags (PICS bags) for long-term pesticide-free grain preservation."
        ]
    }
]


# ==========================================
# 6. EMERGENCY CONTACTS & HELPLINES
# ==========================================
EMERGENCY_CONTACTS = [
    {
        "name": "Kisan Call Center (KCC) - National Toll Free",
        "te_name": "కిసాన్ కాల్ సెంటర్ (టోల్ ఫ్రీ)",
        "number": "1800-180-1551",
        "timing": "6:00 AM to 10:00 PM (All 7 Days)",
        "badge": "success",
        "description": "Direct consultation with agricultural scientists and experts in Telugu, Hindi, English, and other regional languages for crop, pest, weather, and market advisories."
    },
    {
        "name": "District Agriculture Officer (DAO) - Nirmal",
        "te_name": "జిల్లా వ్యవసాయ అధికారి కార్యాలయం - నిర్మల్",
        "number": "08734-222450",
        "timing": "10:00 AM to 5:30 PM (Working Days)",
        "badge": "primary",
        "description": "District administrative assistance for fertilizer shortage complaints, spurious seed verification, and government subsidy applications."
    },
    {
        "name": "Krishi Vigyan Kendra (KVK) Emergency Desk",
        "te_name": "కృషి విజ్ఞాన కేంద్రం (KVK) హెల్ప్‌లైన్",
        "number": "08734-295111",
        "timing": "9:30 AM to 5:00 PM",
        "badge": "info",
        "description": "On-field technical guidance, plant pathology diagnostics, and live pest outbreak rescue support from university agricultural researchers."
    },
    {
        "name": "Telangana State Agriculture Disaster Helpdesk",
        "te_name": "తెలంగాణ వ్యవసాయ విపత్తు నియంత్రణ కేంద్రం",
        "number": "040-2338-3520",
        "timing": "24 Hours Emergency",
        "badge": "danger",
        "description": "Emergency coordination for flood inundation, hailstorm crop loss surveys, and sudden cyclone damage assessments."
    },
    {
        "name": "Spurious Seeds & Fertilizer Vigilance Cell",
        "te_name": "నకిలీ విత్తనాలు, ఎరువుల నిరోధక విజిలెన్స్ సెల్",
        "number": "1800-425-0033",
        "timing": "10:00 AM to 6:00 PM",
        "badge": "warning",
        "description": "Confidential reporting line to report fake pesticides, spurious seeds, or black market overcharging of fertilizers."
    }
]


# ==========================================
# 7. NEARBY AGRICULTURAL SERVICES
# ==========================================
NEARBY_SERVICES = [
    {
        "id": 1,
        "name": "Krishi Vigyan Kendra (KVK) Basar & Soil Testing Lab",
        "category": "Soil Testing & Research",
        "district": "Nirmal",
        "address": "Near RGUKT Campus, Mudhole Road, Basar, Telangana 504107",
        "contact_person": "Dr. V. Prabhakar (Sr. Scientist)",
        "phone": "+91 94401 23456",
        "timing": "9:30 AM - 5:30 PM",
        "services": ["Soil & Water Quality Testing", "Seed Multiplication", "Bio-fertilizer Distribution", "Farmer Training"],
        "distance_km": "2.4 km"
    },
    {
        "id": 2,
        "name": "Sri Lakshmi Agri Inputs & Fertilizers",
        "category": "Fertilizers & Seeds",
        "district": "Nirmal",
        "address": "Opposite Main Bus Stand, Basar Road, Nirmal, Telangana 504106",
        "contact_person": "M. Satyanarayana",
        "phone": "+91 98480 11223",
        "timing": "8:00 AM - 8:30 PM",
        "services": ["IFFCO / KRIBHCO Fertilizers (Urea, DAP, Potash)", "Certified Certified Seeds (Paddy BPT, Cotton Bt)", "Drip Irrigation Fittings"],
        "distance_km": "4.1 km"
    },
    {
        "id": 3,
        "name": "Basar Rythu Seva Custom Hiring Center (CHC)",
        "category": "Machinery & Equipment Rental",
        "district": "Nirmal",
        "address": "Village Panchayat Ground, Basar, Nirmal District",
        "contact_person": "K. Srinivas Reddy",
        "phone": "+91 99123 45678",
        "timing": "6:00 AM - 7:00 PM",
        "services": ["Tractor with Rotavator & MB Plough (Rs 800/hr)", "Combine Paddy Harvester (Rs 2,200/hr)", "Agricultural Spraying Drone (Rs 450/acre)"],
        "distance_km": "1.8 km"
    },
    {
        "id": 4,
        "name": "Telangana State Warehousing Corp & Cold Storage",
        "category": "Cold Storage & Warehousing",
        "district": "Nirmal",
        "address": "Industrial Area, Bhainsa Road, Nirmal District",
        "contact_person": "G. Venkatesh (Warehouse Manager)",
        "phone": "+91 87342 24590",
        "timing": "9:00 AM - 6:00 PM",
        "services": ["10,000 MT Capacity Scientific Storage", "Negotiable Warehouse Receipts (e-NWR) for pledge finance", "Pest-free fumigated bays"],
        "distance_km": "8.5 km"
    },
    {
        "id": 5,
        "name": "Govt Veterinary Hospital & Animal Care",
        "category": "Veterinary Services",
        "district": "Nirmal",
        "address": "Zilla Parishad Road, Mudhole, Nirmal District",
        "contact_person": "Dr. K. Anitha (Veterinary Asst Surgeon)",
        "phone": "+91 94901 88776",
        "timing": "8:30 AM - 1:30 PM & 3:30 PM - 5:30 PM",
        "services": ["Cattle Vaccination", "Artificial Insemination (AI)", "Fodder Seed Distribution", "Deworming"],
        "distance_km": "6.2 km"
    }
]


# ==========================================
# 8. CROP ADVISORY RULES ENGINE
# ==========================================
CROP_ADVISORY_RULES = {
    "Black Soil": {
        "Kharif": [
            {
                "crop": "Cotton",
                "variety": "Bt Cotton RCH-659 / Bunny",
                "seed_rate": "1.5 - 2.0 kg / acre",
                "fertilizer": "NPK 120:60:60 kg/ha in 3 split doses",
                "water_need": "Medium (700-1200 mm)",
                "duration_days": "150 - 160 days",
                "expected_yield": "12 - 16 Quintals / acre",
                "tips": "Deep black soils have high water holding capacity. Ensure proper drainage channels to prevent water stagnation."
            },
            {
                "crop": "Soybean",
                "variety": "JS 335 / JS 95-60",
                "seed_rate": "25 - 30 kg / acre",
                "fertilizer": "NPK 20:60:40 kg/ha with Rhizobium seed inoculation",
                "water_need": "Low-Medium (450-650 mm)",
                "duration_days": "90 - 100 days",
                "expected_yield": "8 - 12 Quintals / acre",
                "tips": "Excellent remunerative short-duration crop in black cotton soils. Follow with Rabi Chickpea."
            }
        ],
        "Rabi": [
            {
                "crop": "Bengal Gram (Chickpea / Chana)",
                "variety": "JG 11 / JAKI 9218",
                "seed_rate": "25 - 30 kg / acre",
                "fertilizer": "NPK 20:40:20 kg/ha",
                "water_need": "Low (200-300 mm, 1-2 irrigations)",
                "duration_days": "95 - 105 days",
                "expected_yield": "7 - 10 Quintals / acre",
                "tips": "Thrives on residual moisture of deep black soils. Critical irrigation at branching and pod development."
            },
            {
                "crop": "Wheat",
                "variety": "GW 322 / HD 2967",
                "seed_rate": "40 kg / acre",
                "fertilizer": "NPK 100:50:40 kg/ha",
                "water_need": "Medium (4-5 light irrigations)",
                "duration_days": "110 - 120 days",
                "expected_yield": "15 - 18 Quintals / acre",
                "tips": "Sow in second fortnight of November. Apply crown root initiation (CRI) irrigation at 21 days."
            }
        ],
        "Zaid": [
            {
                "crop": "Green Gram (Moong)",
                "variety": "WGG 42 / IPM 02-3",
                "seed_rate": "6 - 8 kg / acre",
                "fertilizer": "NPK 15:30:0 kg/ha",
                "water_need": "Low (3-4 irrigations)",
                "duration_days": "65 - 70 days",
                "expected_yield": "5 - 7 Quintals / acre",
                "tips": "Fast-growing summer pulse. Restores soil fertility before next Kharif season."
            }
        ]
    },
    "Red Soil": {
        "Kharif": [
            {
                "crop": "Groundnut",
                "variety": "Kadiri 6 (K-6) / TAG-24",
                "seed_rate": "40 - 45 kg kernels / acre",
                "fertilizer": "NPK 20:40:40 kg/ha + 200 kg Gypsum at flowering",
                "water_need": "Medium (500-600 mm)",
                "duration_days": "105 - 115 days",
                "expected_yield": "8 - 12 Quintals / acre",
                "tips": "Red sandy loams offer easy peg penetration and pod development. Apply Gypsum at 45 days."
            },
            {
                "crop": "Maize (Corn)",
                "variety": "DHM 117 / Pioneer 3396",
                "seed_rate": "7 - 8 kg / acre",
                "fertilizer": "NPK 120:60:50 kg/ha with Zinc Sulphate 20 kg/ha",
                "water_need": "Medium (500-750 mm)",
                "duration_days": "100 - 110 days",
                "expected_yield": "25 - 32 Quintals / acre",
                "tips": "Very responsive to balanced fertigation. Avoid waterlogging during tasseling."
            }
        ],
        "Rabi": [
            {
                "crop": "Chilli (Red Pepper)",
                "variety": "Teja / LCA 334 / G4",
                "seed_rate": "250 - 300 g / acre (transplanted)",
                "fertilizer": "NPK 150:60:60 kg/ha with micronutrient sprays",
                "water_need": "Medium (Drip recommended)",
                "duration_days": "160 - 180 days",
                "expected_yield": "18 - 25 Quintals dry chilli / acre",
                "tips": "Well-drained red soils are ideal for high capsanthin pungency chilli. Adopt border crops."
            }
        ],
        "Zaid": [
            {
                "crop": "Sesame (Til)",
                "variety": "Swetha / Rajeshwari",
                "seed_rate": "2 - 2.5 kg / acre",
                "fertilizer": "NPK 30:20:20 kg/ha",
                "water_need": "Low (2-3 irrigations)",
                "duration_days": "80 - 85 days",
                "expected_yield": "3 - 5 Quintals / acre",
                "tips": "Highly drought tolerant. Excellent summer cash return with low investment."
            }
        ]
    },
    "Clay Loam": {
        "Kharif": [
            {
                "crop": "Paddy (Rice)",
                "variety": "BPT 5204 / MTU 1010 / RNR 15048 (Telangana Sona)",
                "seed_rate": "20 - 25 kg / acre",
                "fertilizer": "NPK 100:50:50 kg/ha with Zinc 20 kg/ha",
                "water_need": "High (1200-1400 mm standing water)",
                "duration_days": "125 - 140 days",
                "expected_yield": "26 - 32 Quintals / acre",
                "tips": "RNR 15048 is low-glycemic index rice with high market demand and blast resistance."
            }
        ],
        "Rabi": [
            {
                "crop": "Rabi Paddy",
                "variety": "KNM 118 / MTU 1010",
                "seed_rate": "25 kg / acre",
                "fertilizer": "NPK 120:60:60 kg/ha",
                "water_need": "High (Assured borewell/canal)",
                "duration_days": "125 - 130 days",
                "expected_yield": "28 - 34 Quintals / acre",
                "tips": "Ensure cold-tolerant variety for December nursery transplanting."
            }
        ],
        "Zaid": [
            {
                "crop": "Watermelon / Musk Melon",
                "variety": "Sugar Baby / Kiran",
                "seed_rate": "400 - 500 g / acre",
                "fertilizer": "NPK 80:50:60 kg/ha",
                "water_need": "Medium (Drip with silver mulching)",
                "duration_days": "75 - 85 days",
                "expected_yield": "12 - 18 Tonnes / acre",
                "tips": "High market price during summer peak. Use drip irrigation with soluble fertilizers."
            }
        ]
    }
}
