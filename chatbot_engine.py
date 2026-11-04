"""
KrishiMitra Rule-Based Intelligent Chatbot Engine
Supports English & Telugu agricultural queries, voice assistant processing,
and intent matching with structured recommendations.
"""

import re
from sample_data import MANDI_PRICES, CROP_DISEASES, GOVERNMENT_SCHEMES

def detect_language(text):
    """Detect if the input text contains Telugu Unicode characters."""
    for char in text:
        if '\u0c00' <= char <= '\u0c7f':
            return 'te'
    return 'en'


def match_intent(query):
    """Classify the user prompt into agricultural intent categories."""
    q = query.lower().strip()
    
    # Greetings
    if any(w in q for w in ['hello', 'hi', 'hey', 'namaste', 'namaskaram', 'నమస్కారం', 'హలో', 'బాగున్నారా', 'good morning', 'good evening']):
        return 'greeting'
        
    # Emergency / Helpline
    if any(w in q for w in ['emergency', 'helpline', 'contact', 'call center', 'officer', 'sos', 'help me', 'సహాయం', 'హెల్ప్‌లైన్', 'నంబర్', 'కాల్']):
        return 'emergency'
        
    # Weather
    if any(w in q for w in ['weather', 'rain', 'temperature', 'forecast', 'wind', 'వాతావరణం', 'వర్షం', 'తుఫాను', 'ఎండ']):
        return 'weather'
        
    # Mandi / Market Prices
    if any(w in q for w in ['mandi', 'price', 'rate', 'bhav', 'market', 'ధర', 'రేటు', 'మార్కెట్', 'మండి']):
        return 'mandi_prices'
        
    # Government Schemes
    if any(w in q for w in ['scheme', 'pm kisan', 'pmkisan', 'fasal bima', 'pmfby', 'rythu bandhu', 'subsidy', 'kcc', 'పథకం', 'పథకాలు', 'కిసాన్', 'సబ్సిడీ', 'రైతు బంధు']):
        return 'schemes'
        
    # Organic Farming / Jeevamrutha
    if any(w in q for w in ['organic', 'jeevamrutha', 'neem oil', 'natural farming', 'panchagavya', 'జీవామృతం', 'సేంద్రీయ', 'వేప కషాయం', 'జీవామృతం']):
        return 'organic'
        
    # Fertilizers / Soil
    if any(w in q for w in ['fertilizer', 'urea', 'dap', 'potash', 'npk', 'soil health', 'ఎరువులు', 'యూరియా', 'పొటాష్', 'నేల']):
        return 'fertilizer'
        
    # Crop Specific: Paddy / Rice
    if any(w in q for w in ['paddy', 'rice', 'dhan', 'వరి', 'వరి సాగు', 'అగ్గితెగులు', 'మొగి పురుగు']):
        return 'crop_paddy'
        
    # Crop Specific: Cotton
    if any(w in q for w in ['cotton', 'kapas', 'bollworm', 'పత్తి', 'గులాబీ రంగు పురుగు', 'పత్తి సాగు']):
        return 'crop_cotton'
        
    # Crop Specific: Chilli
    if any(w in q for w in ['chilli', 'mirchi', 'leaf curl', 'thrips', 'మిరప', 'ఆకుముడుత', 'తామర పురుగులు']):
        return 'crop_chilli'
        
    # Crop Specific: Maize
    if any(w in q for w in ['maize', 'corn', 'makka', 'armyworm', 'మొక్కజొన్న', 'కత్తెర పురుగు']):
        return 'crop_maize'
        
    # Crop Specific: Wheat
    if any(w in q for w in ['wheat', 'rust', 'gehun', 'గోధుమ', 'కుంకుమ తెగులు']):
        return 'crop_wheat'
        
    # General Disease / Pest query
    if any(w in q for w in ['disease', 'pest', 'fungus', 'spray', 'cure', 'leaves drying', 'yellowing', 'తెగులు', 'పురుగు', 'మందు', 'స్ప్రే']):
        return 'disease_general'
        
    # Crop Tracking / App Navigation
    if any(w in q for w in ['dashboard', 'track', 'add crop', 'profile', 'డాష్‌బోర్డ్', 'పంట ట్రాకింగ్']):
        return 'app_navigation'
        
    return 'fallback'


def generate_response(query):
    """
    Generate agricultural advice based on intent and query language.
    Returns: {
        'response_text': Clean plain/formatted text,
        'voice_text': Concise speech-optimized text for TTS,
        'language': 'en' or 'te',
        'suggested_chips': List of clickable prompt chips,
        'action_url': Optional link to relevant platform module
    }
    """
    lang = detect_language(query)
    intent = match_intent(query)
    q = query.lower()
    
    # ----------------------------------------------------
    # GREETING
    # ----------------------------------------------------
    if intent == 'greeting':
        if lang == 'te':
            text = "నమస్కారం రైతు సోదరా! నేను కృషిమిత్ర AI సహాయకుడిని. మీకు పంట సలహాలు, తెగుళ్ల నివారణ, మండి ధరలు, ప్రభుత్వ పథకాలు లేదా వాతావరణ సమాచారం గురించి సహాయం చేయగలను. మీరు ఏమి తెలుసుకోవాలనుకుంటున్నారు?"
            voice = "నమస్కారం! నేను కృషిమిత్ర సహాయకుడిని. మీకు ఏమి సమాచారం కావాలి?"
        else:
            text = "Namaste! Welcome to KrishiMitra AI Assistant. I can help you with crop advisory, pest & disease remedies, mandi rates, government schemes, weather advisories, and farming tips. How can I assist you today?"
            voice = "Hello! I am KrishiMitra Assistant. How can I help with your crops or farm today?"
            
        return {
            "response_text": text,
            "voice_text": voice,
            "language": lang,
            "suggested_chips": ["Paddy Blast Remedy", "Cotton Mandi Price", "PM-KISAN Status", "Make Jeevamrutha", "వరి తెగుళ్లు"],
            "action_url": "/dashboard"
        }

    # ----------------------------------------------------
    # EMERGENCY / HELPLINE
    # ----------------------------------------------------
    elif intent == 'emergency':
        if lang == 'te':
            text = """రైతు అత్యవసర సహాయం (Emergency Help):
1. జాతీయ కిసాన్ కాల్ సెంటర్ (Kisan Call Center): టోల్ ఫ్రీ 1800-180-1551 (ఉదయం 6 నుండి రాత్రి 10 వరకు, తెలుగులో మాట్లాడవచ్చు).
2. జిల్లా వ్యవసాయ అధికారి (DAO నిర్మల్): 08734-222450.
3. KVK బాసర హెల్ప్‌లైన్: 08734-295111.
4. విపత్తు / నకిలీ విత్తనాల ఫిర్యాదు: 1800-425-0033.
మా ప్లాట్‌ఫారమ్‌లో మీరు తక్షణ అత్యవసర SOS రిక్వెస్ట్ కూడా నమోదు చేయవచ్చు."""
            voice = "అత్యవసర సహాయం కోసం కిసాన్ కాల్ సెంటర్ 1 8 0 0 1 8 0 1 5 5 1 కు డయల్ చేయండి."
        else:
            text = """Emergency Agricultural Assistance:
1. Kisan Call Center (National Toll-Free): 1800-180-1551 (6:00 AM to 10:00 PM in regional languages).
2. District Agriculture Officer (DAO Nirmal): 08734-222450.
3. Krishi Vigyan Kendra (KVK Basar) Helpdesk: 08734-295111.
4. Spurious Seeds & Fertilizer Vigilance: 1800-425-0033.
You can also submit an urgent SOS request directly on our Emergency Help module."""
            voice = "For immediate agricultural emergency, call Kisan Call Center at 1800 180 1551."
            
        return {
            "response_text": text,
            "voice_text": voice,
            "language": lang,
            "suggested_chips": ["Log SOS Request", "Nearby KVK Center", "Weather Advisory"],
            "action_url": "/emergency"
        }

    # ----------------------------------------------------
    # WEATHER
    # ----------------------------------------------------
    elif intent == 'weather':
        if lang == 'te':
            text = "ప్రస్తుత వాతావరణ సూచన: నిర్మల్/బాసర ప్రాంతంలో ఉష్ణోగ్రత 31°C, తేమ 68%. వచ్చే 48 గంటల్లో చిరుజల్లులు కురిసే అవకాశం 20-25% ఉంది. సలహా: పురుగుమందుల పిచికారీ ఉదయం 7 నుండి 11 గంటల మధ్య మాత్రమే చేయండి. వర్షం సంకేతం ఉంటే పిచికారీ వాయిదా వేయండి."
            voice = "వాతావరణం అనుకూలంగా ఉంది. ఉదయం వేళల్లో పురుగుమందుల పిచికారీ చేయవచ్చు."
        else:
            text = "Current Agricultural Weather Update: Nirmal/Basar region is 31°C, partly cloudy with 68% humidity. Spraying advisory: Safe between 7:00 AM and 11:30 AM. Light isolated showers predicted in 48 hours; check field drainage."
            voice = "Current temperature is 31 degrees Celsius. Safe spraying window is open during morning hours."
            
        return {
            "response_text": text,
            "voice_text": voice,
            "language": lang,
            "suggested_chips": ["5-Day Weather Forecast", "Spraying Advisory", "Mandi Prices"],
            "action_url": "/weather"
        }

    # ----------------------------------------------------
    # MANDI PRICES / MARKET RATES
    # ----------------------------------------------------
    elif intent == 'mandi_prices':
        if lang == 'te':
            text = """నేటి ప్రధాన మార్కెట్ ధరలు (రూ./క్వింటాల్):
• వరి (ధాన్యం BPT 5204): రూ. 2,520 (నిర్మల్ APMC) [↑ +2.8%]
• పత్తి (Kapas Bt): రూ. 7,580 (ఆదిలాబాద్ యార్డ్) [↑ +1.6%]
• మిరప (తేజ వెరైటీ): రూ. 20,200 (వరంగల్ యార్డ్)
• మొక్కజొన్న: రూ. 2,210 (కరీంనగర్ APMC)
• పసుపు: రూ. 14,250 (నిజామాబాద్ APMC) [↑ +4.1%]
వివరాల కోసం మార్కెట్ పేజీని చూడండి."""
            voice = "నేడు నిర్మల్ మార్కెట్లో వరి ధర క్వింటాలుకు 2520 రూపాయలు, పత్తి ధర 7580 రూపాయలుగా నమోదైంది."
        else:
            text = """Today's Key Mandi Prices (Rs / Quintal):
• Paddy (BPT 5204): Rs 2,520 (Nirmal APMC) [Trend: Up +2.8%]
• Cotton (Bt Long Staple): Rs 7,580 (Adilabad Cotton Yard) [Trend: Up +1.6%]
• Red Chilli (Teja Hot): Rs 20,200 (Warangal Yard)
• Maize (Hybrid): Rs 2,210 (Karimnagar APMC)
• Turmeric (Finger): Rs 14,250 (Nizamabad Mandi) [Trend: Up +4.1%]
Visit our Market Prices section for live charts and district-wise filters."""
            voice = "Today Paddy is trading at 2520 rupees and Cotton at 7580 rupees per quintal."
            
        return {
            "response_text": text,
            "voice_text": voice,
            "language": lang,
            "suggested_chips": ["Cotton Price Today", "Paddy Rate Nirmal", "MSP Reference Guide"],
            "action_url": "/market"
        }

    # ----------------------------------------------------
    # GOVERNMENT SCHEMES
    # ----------------------------------------------------
    elif intent == 'schemes':
        if lang == 'te':
            text = """రైతులకు అందుబాటులో ఉన్న ముఖ్య ప్రభుత్వ పథకాలు:
1. పీఎం-కిసాన్ (PM-KISAN): ఏటా రూ. 6,000 (రూ. 2000 చొప్పున 3 విడతల్లో). దరఖాస్తు: pmkisan.gov.in.
2. ప్రధాన మంత్రి ఫసల్ బీమా (PMFBY): పంట నష్టపరిహార బీమా. ఖరీఫ్ కు 2%, రబీకి 1.5% ప్రీమియం.
3. సాయిల్ హెల్త్ కార్డు: ఉచిత నేల పరీక్ష మరియు ఎరువుల సిఫార్సు కార్డు.
4. రైతు బంధు (తెలంగాణ): ఎకరానికి ఏడాదికి రూ. 10,000 పెట్టుబడి సహాయం.
5. కిసాన్ క్రెడిట్ కార్డు (KCC): 4% వడ్డీతో రూ. 3 లక్షల వరకు సులభ రుణం."""
            voice = "పీఎం కిసాన్ పథకం ద్వారా ఏడాదికి 6000 రూపాయలు మరియు ఫసల్ బీమా ద్వారా పంట రక్షణ లభిస్తుంది."
        else:
            text = """Key Government Agricultural Schemes:
1. PM-KISAN: Rs 6,000/year in 3 installments of Rs 2,000 directly via DBT. Apply on pmkisan.gov.in.
2. PM Fasal Bima Yojana (PMFBY): Comprehensive crop insurance against weather and pest damage.
3. Soil Health Card Scheme: Free 12-parameter soil testing with customized nutrient recommendations.
4. Kisan Credit Card (KCC): Concessional farm credit up to Rs 3 Lakhs at 4% interest.
5. SMAM Scheme: 40% to 50% subsidy on tractors and agricultural machinery.
Explore our Schemes module for eligibility and application steps."""
            voice = "Major schemes include PM-KISAN providing 6000 rupees annually and PM Fasal Bima crop insurance."
            
        return {
            "response_text": text,
            "voice_text": voice,
            "language": lang,
            "suggested_chips": ["PM-KISAN Eligibility", "Crop Insurance Apply", "Subsidized Tractors"],
            "action_url": "/schemes"
        }

    # ----------------------------------------------------
    # ORGANIC FARMING / JEEVAMRUTHA
    # ----------------------------------------------------
    elif intent == 'organic':
        if lang == 'te':
            text = """జీవామృతం తయారీ విధానం (200 లీటర్లు - 1 ఎకరాకు):
1. 200 లీటర్ల డ్రమ్ములో 10 కిలోల తాజా నాటు ఆవు పేడ, 10 లీటర్ల ఆవు మూత్రం కలపండి.
2. 2 కిలోల బెల్లం, 2 కిలోల శనగపిండి, గుప్పెడు పుట్ట మట్టి లేదా గట్టు మట్టి చేర్చండి.
3. నీటితో నింపి కర్రతో రోజుకు రెండుసార్లు సవ్యదిశలో తిప్పండి.
4. గోనె సంచితో కప్పి నీడలో 48 గంటలు పులియబెట్టండి.
5. సాగునీటితో పాటు ఎకరాకు 200 లీటర్లు పారించండి లేదా వడకట్టి 10% ద్రావణాన్ని పిచికారీ చేయండి."""
            voice = "జీవామృతం తయారీకి 10 కిలోల ఆవు పేడ, 10 లీటర్ల గోమూత్రం, 2 కిలోల బెల్లం మరియు శనగపిండి అవసరం."
        else:
            text = """Jeevamrutha Preparation Guide (200 Liters for 1 Acre):
1. In a 200L barrel, mix 10 kg indigenous cow dung + 10 liters cow urine.
2. Add 2 kg jaggery + 2 kg pulse flour (besan) + a handful of fertile undisturbed soil.
3. Fill with water and stir clockwise twice daily for 5 minutes.
4. Keep in shade covered with a gunny bag for 48 hours for microbial fermentation.
5. Apply with irrigation water or filter and spray 10% solution to boost beneficial microbes and plant vigor."""
            voice = "To prepare Jeevamrutha, mix 10 kg cow dung, 10 liters cow urine, 2 kg jaggery, and pulse flour in water."
            
        return {
            "response_text": text,
            "voice_text": voice,
            "language": lang,
            "suggested_chips": ["Neem Seed Spray (NSKE)", "Natural Pest Repellent", "Organic Compost"],
            "action_url": "/tips"
        }

    # ----------------------------------------------------
    # FERTILIZERS / SOIL
    # ----------------------------------------------------
    elif intent == 'fertilizer':
        if lang == 'te':
            text = """రసాయన ఎరువుల సమతుల్య వినియోగ సలహా:
• యూరియాను ఒకేసారి వేయకూడదు; పంట దశలను బట్టి 2 నుండి 3 దఫాలుగా వేయాలి.
• భాస్వరం (DAP / SSP) ఎరువును విత్తే సమయంలో లేదా నాటు వేసే సమయంలో దుక్కిలోనే వేయాలి.
• పొటాష్ (MOP) పూత మరియు గింజ పాలుపోసుకునే దశలో బలాన్ని ఇస్తుంది.
• నేల పరీక్ష (Soil Health Card) ఆధారంగా మాత్రమే జింక్ సల్ఫేట్ (ఎకరాకు 10 కిలోలు) వాడాలి. యూరియాతో కలిపి జింక్ వేయరాదు."""
            voice = "ఎరువులను సిఫార్సు చేసిన మోతాదులోనే వేయండి. యూరియాను రెండు మూడు దఫాలుగా విభజించి వేయండి."
        else:
            text = """Balanced Fertilizer & Nutrient Management Tips:
• Split Application: Never dump all Nitrogen (Urea) at once. Apply in 2-3 splits (basal, tillering, panicle/flowering).
• Phosphatic Fertilizers (DAP/SSP): Always apply as basal dose at sowing/transplanting near root zone.
• Potash (MOP): Crucial for grain filling, disease resistance, and drought tolerance.
• Micronutrients: Apply Zinc Sulphate (10 kg/acre) separately; never mix Zinc directly with DAP or SSP."""
            voice = "Apply fertilizers in split doses according to crop stages and avoid overusing urea."
            
        return {
            "response_text": text,
            "voice_text": voice,
            "language": lang,
            "suggested_chips": ["Soil Health Card", "Paddy Fertilizer Schedule", "Cotton NPK Dosage"],
            "action_url": "/crops/advisory"
        }

    # ----------------------------------------------------
    # CROP SPECIFIC: PADDY (RICE)
    # ----------------------------------------------------
    elif intent == 'crop_paddy':
        if lang == 'te':
            text = """వరి పంట ముఖ్య సలహాలు:
1. అగ్గితెగులు (Blast): ఆకులపై కంటి ఆకారపు మచ్చలు కనిపిస్తే ట్రైసైక్లాజోల్ 75% WP @ 0.6 గ్రా./లీటర్ నీటికి కలిపి పిచికారీ చేయండి.
2. కాండం తొలుచు పురుగు (మొగి పురుగు): కార్టాప్ హైడ్రోక్లోరైడ్ 4G గుళికలు ఎకరాకు 7.5 కిలోలు తగినంత తేమ ఉన్నప్పుడు చల్లండి.
3. నీటి యాజమాన్యం: పూత దశలో 3-5 సెం.మీ నిల్వ నీరు ఉంచండి. మిగిలిన సమయాల్లో ఆరబెట్టి తడిపెట్టే పద్ధతి (AWD) పాటించండి."""
            voice = "వరిలో అగ్గితెగులు నివారణకు ట్రైసైక్లాజోల్ లేదా కార్టాప్ హైడ్రోక్లోరైడ్ పిచికారీ చేయండి."
        else:
            text = """Paddy (Rice) Management & Pest Remedies:
• Rice Blast: Look for spindle-shaped eye lesions. Spray Tricyclazole 75% WP @ 0.6 g/liter OR Isoprothiolane 40% EC @ 1.5 ml/liter.
• Stem Borer (Dead Heart/White Earhead): Broadcast Cartap Hydrochloride 4G granules @ 7.5 kg/acre in standing moist soil.
• Water Management: Maintain 3-5 cm standing water during panicle emergence and grain filling. Practice AWD in vegetative phase."""
            voice = "For Paddy blast, spray Tricyclazole at 0.6 grams per liter. For stem borer, apply Cartap granules."
            
        return {
            "response_text": text,
            "voice_text": voice,
            "language": lang,
            "suggested_chips": ["Paddy Blast Detail", "Paddy Mandi Rate", "Track My Paddy Crop"],
            "action_url": "/diseases"
        }

    # ----------------------------------------------------
    # CROP SPECIFIC: COTTON
    # ----------------------------------------------------
    elif intent == 'crop_cotton':
        if lang == 'te':
            text = """పత్తి పంట సంరక్షణ సలహాలు:
1. గులాబీ రంగు పురుగు (Pink Bollworm): ఎకరాకు 5-8 లింగాకర్షక బుట్టలు (Pheromone Traps) అమర్చండి. ఉధృతి ఉంటే క్లోరాంట్రానిలిప్రోల్ 18.5% SC @ 0.3 మి.లీ/లీటర్ లేదా ఇమామెక్టిన్ బెంజోయేట్ 5% SG @ 0.4 గ్రా./లీటర్ పిచికారీ చేయండి.
2. రసం పీల్చు పురుగులు (తెల్లదోమ/పేనుబంక): 5% వేప గింజల కషాయం లేదా ఫిప్రోనిల్ 5% SC @ 2 మి.లీ/లీటర్ పిచికారీ చేయండి.
3. పూత రాలకుండా ఉండటానికి ప్లానోఫిక్స్ (Planofix) 1 మి.లీ 4.5 లీటర్ల నీటికి కలిపి పిచికారీ చేయండి."""
            voice = "పత్తిలో గులాబీ రంగు పురుగు నివారణకు లింగాకర్షక బుట్టలు మరియు క్లోరాంట్రానిలిప్రోల్ మందు వాడండి."
        else:
            text = """Cotton Agronomy & Pest Control:
• Pink Bollworm: Install 5-8 Pheromone Traps per acre. Spray Chlorantraniliprole 18.5% SC @ 0.3 ml/liter OR Emamectin Benzoate 5% SG @ 0.4 g/liter during peak flowering/boll stage.
• Sucking Pests (Whitefly/Jassids): Spray 5% Neem Seed Kernel Extract (NSKE) or Diafenthiuron 50% WP @ 1.2 g/liter.
• Boll Drop Prevention: Spray NAA (Planofix) @ 1 ml per 4.5 liters of water during early flowering."""
            voice = "For Pink Bollworm in cotton, use pheromone traps and spray Chlorantraniliprole as needed."
            
        return {
            "response_text": text,
            "voice_text": voice,
            "language": lang,
            "suggested_chips": ["Pink Bollworm Guide", "Cotton Mandi Rate", "Track My Cotton Crop"],
            "action_url": "/diseases"
        }

    # ----------------------------------------------------
    # CROP SPECIFIC: CHILLI
    # ----------------------------------------------------
    elif intent == 'crop_chilli':
        if lang == 'te':
            text = """మిరప పంట - ఆకుముడుత నివారణ (Chilli Leaf Curl & Thrips):
• పై ముడుత (తామర పురుగులు / Thrips): ఆకులు పైకి దోనెలా ముడుచుకుంటాయి. నివారణకు స్పైనెటోరమ్ 11.7% SC @ 0.9 మి.లీ లేదా ఫిప్రోనిల్ 5% SC @ 2 మి.లీ/లీటర్ పిచికారీ చేయండి.
• కింది ముడుత (నల్లి / Mites): ఆకులు కిందికి ముడుచుకుంటాయి. డైఫెంథియురాన్ 50% WP @ 1.2 గ్రా. లేదా స్పైరోమెసిఫెన్ 22.9% SC @ 1 మి.లీ/లీటర్ పిచికారీ చేయండి.
• ఎకరాకు 15-20 పసుపు, నీలి జిగురు అట్టలు (Sticky Traps) అమర్చండి."""
            voice = "మిరప ఆకుముడుత నివారణకు నీలి మరియు పసుపు జిగురు అట్టలు అమర్చండి మరియు ఫిప్రోనిల్ పిచికారీ చేయండి."
        else:
            text = """Chilli Leaf Curl & Pest Management:
• Upward Curl (Thrips): Spray Spinetoram 11.7% SC @ 0.9 ml/liter OR Fipronil 5% SC @ 2 ml/liter.
• Downward Curl (Yellow Mites): Spray Diafenthiuron 50% WP @ 1.2 g/liter OR Spiromesifen 22.9% SC @ 1 ml/liter.
• Cultural Practice: Install 15-20 Yellow & Blue Sticky Traps per acre; erect border crops of maize or sorghum to block sucking insect vectors."""
            voice = "For chilli leaf curl, identify if curling is upward due to thrips or downward due to mites and spray accordingly."
            
        return {
            "response_text": text,
            "voice_text": voice,
            "language": lang,
            "suggested_chips": ["Chilli Disease Guide", "Chilli Mandi Prices", "Fertilizer Schedule"],
            "action_url": "/diseases"
        }

    # ----------------------------------------------------
    # CROP SPECIFIC: MAIZE
    # ----------------------------------------------------
    elif intent == 'crop_maize':
        if lang == 'te':
            text = """మొక్కజొన్న కత్తెర పురుగు (Fall Armyworm) నివారణ:
1. గుడ్ల దశ & చిన్న లార్వాలు: అజాడిరక్తిన్ 1500 PPM (వేప నూనె) @ 5 మి.లీ/లీటర్ నీటికి పిచికారీ చేయండి.
2. సుడిలో ఇసుక మరియు వేప పిండి మిశ్రమాన్ని (9:1 నిష్పత్తిలో) వేయడం ద్వారా సమర్థవంతంగా అరికట్టవచ్చు.
3. ఉధృతి ఎక్కువగా ఉంటే: ఇమామెక్టిన్ బెంజోయేట్ 5% SG @ 0.4 గ్రా./లీటర్ లేదా క్లోరాంట్రానిలిప్రోల్ 18.5% SC @ 0.4 మి.లీ/లీటర్ సుడిలో పడేలా పిచికారీ చేయండి."""
            voice = "మొక్కజొన్న కత్తెర పురుగు నివారణకు సుడిలో ఇసుక వేప పిండి వేయండి లేదా ఇమామెక్టిన్ పిచికారీ చేయండి."
        else:
            text = """Maize Fall Armyworm (FAW) Management:
• Early Stage: Spray Azadirachtin (Neem Oil 1500 ppm) @ 5 ml/liter or apply sand mixed with neem cake powder (9:1) into leaf whorls.
• Severe Outbreak: Spray Emamectin Benzoate 5% SG @ 0.4 g/liter OR Spinetoram 11.7% SC @ 0.5 ml/liter directed strictly into the plant whorls."""
            voice = "Direct spray of Emamectin Benzoate or whorl application of sand and neem cake controls maize armyworm."
            
        return {
            "response_text": text,
            "voice_text": voice,
            "language": lang,
            "suggested_chips": ["Fall Armyworm Details", "Maize Mandi Rate", "Add Maize Crop"],
            "action_url": "/diseases"
        }

    # ----------------------------------------------------
    # CROP SPECIFIC: WHEAT
    # ----------------------------------------------------
    elif intent == 'crop_wheat':
        if lang == 'te':
            text = """గోధుమ కుంకుమ తెగులు (Yellow/Stripe Rust) నివారణ:
ఆకులపై పసుపు రంగు చారల పొడి కనిపిస్తే వెంటనే ప్రొపికొనాజోల్ 25% EC (Tilt) @ 1 మి.లీ/లీటర్ నీటికి కలిపి పిచికారీ చేయండి. తెగులును తట్టుకునే రకాలైన HD 3086, DBW 187 విత్తనాలను ఎంచుకోండి."""
            voice = "గోధుమలో పసుపు కుంకుమ తెగులు కనిపించిన వెంటనే ప్రొపికొనాజోల్ పిచికారీ చేయండి."
        else:
            text = """Wheat Stripe Rust (Yellow Rust) Advisory:
Upon first appearance of yellowish-orange stripe pustules, spray Propiconazole 25% EC @ 1 ml/liter water. Plant certified resistant seeds (HD 3086, DBW 187)."""
            voice = "For wheat yellow rust, immediately spray Propiconazole at 1 ml per liter."
            
        return {
            "response_text": text,
            "voice_text": voice,
            "language": lang,
            "suggested_chips": ["Wheat Disease Details", "Wheat Mandi Price", "Crop Advisory"],
            "action_url": "/diseases"
        }

    # ----------------------------------------------------
    # GENERAL DISEASE
    # ----------------------------------------------------
    elif intent == 'disease_general':
        if lang == 'te':
            text = "పంట తెగులు లేదా పురుగుల నివారణకు: ముందుగా పంట పేరు మరియు లక్షణాలను తెలియజేయండి (ఉదాహరణకు: ఆకులు పసుపు రంగులోకి మారడం, ముడుచుకోవడం, మచ్చలు పడడం). మా 'పంట వ్యాధులు' పేజీలో వివరణాత్మక ఫోటోలు మరియు నివారణ మార్గాలు ఉన్నాయి."
            voice = "మీ పంటలో ఏ విధమైన లక్షణాలు కనిపిస్తున్నాయో స్పష్టంగా చెబితే సరైన నివారణ మందును సూచిస్తాను."
        else:
            text = "For disease identification: Please mention the crop name and symptoms (e.g. yellowing, leaf curling, spots, stem rot, or wilting). You can also browse our Disease & Pest Directory for photos, symptoms, and biological or chemical remedies."
            voice = "Please specify the crop name and observed symptoms so I can recommend the exact treatment."
            
        return {
            "response_text": text,
            "voice_text": voice,
            "language": lang,
            "suggested_chips": ["Paddy Blast", "Cotton Bollworm", "Chilli Leaf Curl", "Tomato Blight"],
            "action_url": "/diseases"
        }

    # ----------------------------------------------------
    # APP NAVIGATION
    # ----------------------------------------------------
    elif intent == 'app_navigation':
        if lang == 'te':
            text = "మీరు డాష్‌బోర్డ్‌లో పంటల వివరాలు ట్రాక్ చేయవచ్చు, కొత్త పంటను జోడించవచ్చు లేదా మీ ప్రొఫైల్ నవీకరించవచ్చు."
            voice = "డాష్ బోర్డ్ ఓపెన్ చేస్తున్నాను."
        else:
            text = "You can track your existing crops, monitor stage timelines, add new fields, or check statistics on your Dashboard."
            voice = "Navigating to your farmer dashboard."
            
        return {
            "response_text": text,
            "voice_text": voice,
            "language": lang,
            "suggested_chips": ["View My Crops", "Add New Crop", "Weather Forecast", "Mandi Rates"],
            "action_url": "/dashboard"
        }

    # ----------------------------------------------------
    # FALLBACK
    # ----------------------------------------------------
    else:
        if lang == 'te':
            text = f"క్షమించండి, మీ ప్రశ్న: '{query}' కు సంబంధించిన నిర్దిష్ట సమాచారం లభించలేదు. దయచేసి 'వరి తెగుళ్లు', 'పత్తి ధర', 'పీఎం కిసాన్', 'జీవామృతం' లేదా 'వాతావరణం' వంటి కీలక పదాలతో అడగండి."
            voice = "దయచేసి మీ ప్రశ్నను మరింత స్పష్టంగా లేదా నిర్దిష్ట పంట పేరుతో అడగండి."
        else:
            text = f"I'm here to assist with your farm! I couldn't find a direct match for: '{query}'. You can ask me about: crop diseases (Paddy, Cotton, Chilli), mandi prices, weather forecasts, government schemes (PM-KISAN), organic sprays, or emergency contacts."
            voice = "I didn't quite understand that. Please ask about crop diseases, mandi prices, weather, or government schemes."
            
        return {
            "response_text": text,
            "voice_text": voice,
            "language": lang,
            "suggested_chips": ["Paddy Advisory", "Cotton Price", "Weather Today", "PM-KISAN Scheme", "Emergency Helpline"],
            "action_url": None
        }
