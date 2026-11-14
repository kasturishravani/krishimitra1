import os
import functools
from datetime import datetime
from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, session, jsonify, abort
)
from werkzeug.security import generate_password_hash, check_password_hash

from config import Config
import database
import sample_data
import chatbot_engine
import pest_detector

app = Flask(__name__)
app.config.from_object(Config)

# Ensure database is initialized
with app.app_context():
    database.init_db()


# -----------------------------------------------------------------------------
# Context Processors & Template Helpers
# -----------------------------------------------------------------------------
@app.context_processor
def inject_globals():
    """Inject common variables across all Jinja templates."""
    farmer = None
    if 'farmer_id' in session:
        farmer = database.query_db(
            "SELECT id, full_name, mobile, email, state, district, village, land_size_acres, soil_type, preferred_language FROM farmers WHERE id = %s",
            (session['farmer_id'],),
            one=True
        )
    return {
        'current_year': datetime.now().year,
        'current_farmer': farmer,
        'app_name': Config.APP_NAME,
        'app_tagline': Config.TAGLINE
    }


def login_required(view):
    """Decorator to require login for protected routes."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'farmer_id' not in session:
            flash("Please sign in to access your farmer dashboard and tools.", "warning")
            return redirect(url_for('login', next=request.url))
        return view(**kwargs)
    return wrapped_view


# -----------------------------------------------------------------------------
# 1. LANDING & HOME
# -----------------------------------------------------------------------------
@app.route('/')
def index():
    weather_snippet = sample_data.get_weather_data("Nirmal")
    top_mandi = sample_data.MANDI_PRICES[:4]
    featured_schemes = sample_data.GOVERNMENT_SCHEMES[:3]
    recent_tips = sample_data.FARMING_TIPS[:3]
    return render_template(
        'index.html',
        weather=weather_snippet,
        mandi_prices=top_mandi,
        schemes=featured_schemes,
        tips=recent_tips
    )


# -----------------------------------------------------------------------------
# 2. FARMER AUTHENTICATION (REGISTER, LOGIN, LOGOUT)
# -----------------------------------------------------------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'farmer_id' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        mobile = request.form.get('mobile', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        state = request.form.get('state', 'Telangana').strip()
        district = request.form.get('district', 'Nirmal').strip()
        village = request.form.get('village', '').strip()
        land_size = request.form.get('land_size_acres', '2.5').strip()
        soil_type = request.form.get('soil_type', 'Black Soil').strip()
        preferred_language = request.form.get('preferred_language', 'en').strip()

        # Validation
        if not full_name or not mobile or not password:
            flash("Full name, mobile number, and password are required.", "danger")
            return render_template('auth/register.html')

        if len(mobile) != 10 or not mobile.isdigit():
            flash("Please enter a valid 10-digit mobile number.", "danger")
            return render_template('auth/register.html')

        if len(password) < 6:
            flash("Password must be at least 6 characters long.", "danger")
            return render_template('auth/register.html')

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template('auth/register.html')

        # Check existing mobile
        existing = database.query_db("SELECT id FROM farmers WHERE mobile = %s", (mobile,), one=True)
        if existing:
            flash("A farmer with this mobile number is already registered. Please login.", "warning")
            return redirect(url_for('login'))

        # Create farmer
        hashed_pw = generate_password_hash(password)
        try:
            land_val = float(land_size) if land_size else 2.5
        except ValueError:
            land_val = 2.5

        new_farmer_id = database.query_db(
            """INSERT INTO farmers 
            (full_name, mobile, email, password_hash, state, district, village, land_size_acres, soil_type, preferred_language) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (full_name, mobile, email, hashed_pw, state, district, village, land_val, soil_type, preferred_language),
            commit=True,
            return_id=True
        )

        session['farmer_id'] = new_farmer_id
        session['farmer_name'] = full_name
        session['mobile'] = mobile
        session['district'] = district
        flash(f"Welcome to KrishiMitra, {full_name}! Your account has been created successfully.", "success")
        return redirect(url_for('dashboard'))

    return render_template('auth/register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'farmer_id' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        login_id = request.form.get('login_id', '').strip()  # Mobile or Email
        password = request.form.get('password', '')

        if not login_id or not password:
            flash("Please provide your registered mobile number and password.", "danger")
            return render_template('auth/login.html')

        farmer = database.query_db(
            "SELECT * FROM farmers WHERE mobile = %s OR email = %s",
            (login_id, login_id),
            one=True
        )

        if not farmer or not check_password_hash(farmer['password_hash'], password):
            flash("Invalid mobile number/email or password. For demo, try 9876543210 / farmer123", "danger")
            return render_template('auth/login.html')

        session['farmer_id'] = farmer['id']
        session['farmer_name'] = farmer['full_name']
        session['mobile'] = farmer['mobile']
        session['district'] = farmer['district']
        flash(f"Welcome back, {farmer['full_name']}!", "success")
        next_page = request.args.get('next')
        return redirect(next_page if next_page else url_for('dashboard'))

    return render_template('auth/login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash("You have been signed out successfully.", "info")
    return redirect(url_for('login'))


# -----------------------------------------------------------------------------
# 3. FARMER DASHBOARD & PROFILE
# -----------------------------------------------------------------------------
@app.route('/dashboard')
@login_required
def dashboard():
    farmer_id = session['farmer_id']
    farmer = database.query_db("SELECT * FROM farmers WHERE id = %s", (farmer_id,), one=True)
    crops = database.query_db("SELECT * FROM crops WHERE farmer_id = %s ORDER BY created_at DESC", (farmer_id,))
    
    # Calculate statistics
    total_crops = len(crops)
    healthy_crops = sum(1 for c in crops if c.get('health_status') == 'Healthy')
    attention_crops = sum(1 for c in crops if c.get('health_status') in ['At Risk', 'Diseased'])
    total_acres = sum(float(c.get('area_acres', 0)) for c in crops)
    
    # Recent activities
    activities = []
    if crops:
        crop_ids = [str(c['id']) for c in crops]
        # Fetch up to 5 recent activities
        activities = database.query_db(
            f"""SELECT a.*, c.crop_name, c.variety 
            FROM crop_activities a 
            JOIN crops c ON a.crop_id = c.id 
            WHERE a.crop_id IN ({','.join(crop_ids)}) 
            ORDER BY a.activity_date DESC LIMIT 5"""
        )

    # Weather widget data
    district = farmer.get('district', 'Nirmal') if farmer else 'Nirmal'
    weather = sample_data.get_weather_data(district)

    # Top Mandi rates
    mandi_preview = sample_data.MANDI_PRICES[:5]

    # Active SOS alert if any
    active_sos = database.query_db(
        "SELECT * FROM emergency_sos WHERE farmer_id = %s ORDER BY created_at DESC LIMIT 1",
        (farmer_id,),
        one=True
    )

    return render_template(
        'dashboard/index.html',
        farmer=farmer,
        crops=crops,
        total_crops=total_crops,
        healthy_crops=healthy_crops,
        attention_crops=attention_crops,
        total_acres=total_acres,
        activities=activities,
        weather=weather,
        mandi_preview=mandi_preview,
        active_sos=active_sos
    )


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    farmer_id = session['farmer_id']
    farmer = database.query_db("SELECT * FROM farmers WHERE id = %s", (farmer_id,), one=True)

    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip()
        state = request.form.get('state', '').strip()
        district = request.form.get('district', '').strip()
        village = request.form.get('village', '').strip()
        land_size = request.form.get('land_size_acres', '').strip()
        soil_type = request.form.get('soil_type', '').strip()
        preferred_language = request.form.get('preferred_language', 'en').strip()
        new_password = request.form.get('new_password', '').strip()

        if not full_name:
            flash("Full name cannot be empty.", "danger")
            return render_template('dashboard/profile.html', farmer=farmer)

        try:
            land_val = float(land_size) if land_size else farmer['land_size_acres']
        except ValueError:
            land_val = farmer['land_size_acres']

        if new_password:
            if len(new_password) < 6:
                flash("New password must be at least 6 characters.", "danger")
                return render_template('dashboard/profile.html', farmer=farmer)
            hashed_pw = generate_password_hash(new_password)
            database.query_db(
                """UPDATE farmers SET full_name = %s, email = %s, state = %s, district = %s, 
                village = %s, land_size_acres = %s, soil_type = %s, preferred_language = %s, 
                password_hash = %s WHERE id = %s""",
                (full_name, email, state, district, village, land_val, soil_type, preferred_language, hashed_pw, farmer_id),
                commit=True
            )
            flash("Profile and password updated successfully!", "success")
        else:
            database.query_db(
                """UPDATE farmers SET full_name = %s, email = %s, state = %s, district = %s, 
                village = %s, land_size_acres = %s, soil_type = %s, preferred_language = %s WHERE id = %s""",
                (full_name, email, state, district, village, land_val, soil_type, preferred_language, farmer_id),
                commit=True
            )
            flash("Profile details updated successfully!", "success")

        session['farmer_name'] = full_name
        session['district'] = district
        return redirect(url_for('profile'))

    return render_template('dashboard/profile.html', farmer=farmer)


# -----------------------------------------------------------------------------
# 4. CROP TRACKING (CRUD) & ADVISORY
# -----------------------------------------------------------------------------
@app.route('/crops')
@login_required
def crops_list():
    farmer_id = session['farmer_id']
    search_q = request.args.get('q', '').strip()
    status_filter = request.args.get('status', '').strip()
    stage_filter = request.args.get('stage', '').strip()

    sql = "SELECT * FROM crops WHERE farmer_id = %s"
    params = [farmer_id]

    if search_q:
        sql += " AND (crop_name LIKE %s OR variety LIKE %s)"
        params.extend([f"%{search_q}%", f"%{search_q}%"])
    if status_filter:
        sql += " AND health_status = %s"
        params.append(status_filter)
    if stage_filter:
        sql += " AND stage = %s"
        params.append(stage_filter)

    sql += " ORDER BY created_at DESC"
    crops = database.query_db(sql, params)
    return render_template(
        'crops/list.html',
        crops=crops,
        search_q=search_q,
        status_filter=status_filter,
        stage_filter=stage_filter
    )


@app.route('/crops/add', methods=['GET', 'POST'])
@login_required
def crops_add():
    farmer_id = session['farmer_id']
    farmer = database.query_db("SELECT soil_type FROM farmers WHERE id = %s", (farmer_id,), one=True)
    default_soil = farmer['soil_type'] if farmer else 'Black Soil'

    if request.method == 'POST':
        crop_name = request.form.get('crop_name', '').strip()
        variety = request.form.get('variety', '').strip()
        sowing_date = request.form.get('sowing_date', '').strip()
        area_acres = request.form.get('area_acres', '1.0').strip()
        soil_type = request.form.get('soil_type', default_soil).strip()
        stage = request.form.get('stage', 'Vegetative').strip()
        health_status = request.form.get('health_status', 'Healthy').strip()
        expected_harvest = request.form.get('expected_harvest_date', '').strip() or None
        notes = request.form.get('notes', '').strip()

        if not crop_name or not sowing_date:
            flash("Crop name and sowing date are required fields.", "danger")
            return render_template('crops/add.html', default_soil=default_soil)

        try:
            area_val = float(area_acres)
        except ValueError:
            area_val = 1.0

        new_crop_id = database.query_db(
            """INSERT INTO crops 
            (farmer_id, crop_name, variety, sowing_date, area_acres, soil_type, stage, health_status, expected_harvest_date, notes) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (farmer_id, crop_name, variety, sowing_date, area_val, soil_type, stage, health_status, expected_harvest, notes),
            commit=True,
            return_id=True
        )

        # Log initial activity
        database.query_db(
            "INSERT INTO crop_activities (crop_id, activity_type, activity_date, notes) VALUES (%s, %s, %s, %s)",
            (new_crop_id, 'Inspection', sowing_date, f'Crop {crop_name} ({variety}) registered in platform.'),
            commit=True
        )

        flash(f"Crop '{crop_name}' has been added to your tracking list!", "success")
        return redirect(url_for('crop_detail', crop_id=new_crop_id))

    return render_template('crops/add.html', default_soil=default_soil)


@app.route('/crops/<int:crop_id>')
@login_required
def crop_detail(crop_id):
    farmer_id = session['farmer_id']
    crop = database.query_db(
        "SELECT * FROM crops WHERE id = %s AND farmer_id = %s",
        (crop_id, farmer_id),
        one=True
    )
    if not crop:
        flash("Crop record not found or access denied.", "danger")
        return redirect(url_for('crops_list'))

    activities = database.query_db(
        "SELECT * FROM crop_activities WHERE crop_id = %s ORDER BY activity_date DESC, id DESC",
        (crop_id,)
    )

    # Calculate growth percentage according to stage
    stages = ['Sowing', 'Germination', 'Vegetative', 'Flowering', 'Yield Formation', 'Ripening', 'Harvested']
    current_stage = crop.get('stage', 'Vegetative')
    stage_index = stages.index(current_stage) if current_stage in stages else 2
    progress_pct = int(((stage_index + 1) / len(stages)) * 100)

    # Relevant disease tips for this crop
    crop_keywords = crop['crop_name'].lower()
    related_diseases = [
        d for d in sample_data.CROP_DISEASES
        if any(k in crop_keywords for k in d['keywords']) or d['crop'].lower() in crop_keywords
    ]

    return render_template(
        'crops/detail.html',
        crop=crop,
        activities=activities,
        stages=stages,
        stage_index=stage_index,
        progress_pct=progress_pct,
        related_diseases=related_diseases
    )


@app.route('/crops/<int:crop_id>/edit', methods=['GET', 'POST'])
@login_required
def crop_edit(crop_id):
    farmer_id = session['farmer_id']
    crop = database.query_db(
        "SELECT * FROM crops WHERE id = %s AND farmer_id = %s",
        (crop_id, farmer_id),
        one=True
    )
    if not crop:
        flash("Crop record not found.", "danger")
        return redirect(url_for('crops_list'))

    if request.method == 'POST':
        crop_name = request.form.get('crop_name', '').strip()
        variety = request.form.get('variety', '').strip()
        sowing_date = request.form.get('sowing_date', '').strip()
        area_acres = request.form.get('area_acres', '1.0').strip()
        soil_type = request.form.get('soil_type', crop['soil_type']).strip()
        stage = request.form.get('stage', crop['stage']).strip()
        health_status = request.form.get('health_status', crop['health_status']).strip()
        expected_harvest = request.form.get('expected_harvest_date', '').strip() or None
        notes = request.form.get('notes', '').strip()

        try:
            area_val = float(area_acres)
        except ValueError:
            area_val = crop['area_acres']

        database.query_db(
            """UPDATE crops SET crop_name = %s, variety = %s, sowing_date = %s, 
            area_acres = %s, soil_type = %s, stage = %s, health_status = %s, 
            expected_harvest_date = %s, notes = %s WHERE id = %s AND farmer_id = %s""",
            (crop_name, variety, sowing_date, area_val, soil_type, stage, health_status, expected_harvest, notes, crop_id, farmer_id),
            commit=True
        )

        flash(f"Crop '{crop_name}' details updated successfully!", "success")
        return redirect(url_for('crop_detail', crop_id=crop_id))

    return render_template('crops/edit.html', crop=crop)


@app.route('/crops/<int:crop_id>/delete', methods=['POST'])
@login_required
def crop_delete(crop_id):
    farmer_id = session['farmer_id']
    crop = database.query_db(
        "SELECT crop_name FROM crops WHERE id = %s AND farmer_id = %s",
        (crop_id, farmer_id),
        one=True
    )
    if crop:
        database.query_db("DELETE FROM crops WHERE id = %s AND farmer_id = %s", (crop_id, farmer_id), commit=True)
        flash(f"Crop '{crop['crop_name']}' has been removed from tracking.", "info")
    else:
        flash("Crop not found or could not be removed.", "danger")
    return redirect(url_for('crops_list'))


@app.route('/crops/<int:crop_id>/activity', methods=['POST'])
@login_required
def crop_add_activity(crop_id):
    farmer_id = session['farmer_id']
    crop = database.query_db("SELECT id FROM crops WHERE id = %s AND farmer_id = %s", (crop_id, farmer_id), one=True)
    if not crop:
        flash("Crop record not found.", "danger")
        return redirect(url_for('crops_list'))

    activity_type = request.form.get('activity_type', 'Inspection')
    activity_date = request.form.get('activity_date', datetime.now().strftime('%Y-%m-%d'))
    notes = request.form.get('notes', '').strip()

    database.query_db(
        "INSERT INTO crop_activities (crop_id, activity_type, activity_date, notes) VALUES (%s, %s, %s, %s)",
        (crop_id, activity_type, activity_date, notes),
        commit=True
    )

    flash("Activity recorded successfully in your crop log!", "success")
    return redirect(url_for('crop_detail', crop_id=crop_id))


@app.route('/crops/advisory', methods=['GET', 'POST'])
def crop_advisory():
    selected_soil = request.args.get('soil', 'Black Soil')
    selected_season = request.args.get('season', 'Kharif')

    if request.method == 'POST':
        selected_soil = request.form.get('soil_type', 'Black Soil')
        selected_season = request.form.get('season', 'Kharif')

    rules = sample_data.CROP_ADVISORY_RULES.get(selected_soil, sample_data.CROP_ADVISORY_RULES["Black Soil"])
    recommended_crops = rules.get(selected_season, rules.get('Kharif', []))

    return render_template(
        'crops/advisory.html',
        selected_soil=selected_soil,
        selected_season=selected_season,
        recommended_crops=recommended_crops
    )


# -----------------------------------------------------------------------------
# 5. CROP DISEASE & PEST DIRECTORY
# -----------------------------------------------------------------------------
@app.route('/diseases')
def diseases_list():
    search_q = request.args.get('q', '').strip().lower()
    crop_filter = request.args.get('crop', '').strip()
    type_filter = request.args.get('type', '').strip()

    diseases = sample_data.CROP_DISEASES

    if search_q:
        diseases = [
            d for d in diseases
            if search_q in d['name'].lower()
            or search_q in d['te_name'].lower()
            or search_q in d['symptoms'].lower()
            or search_q in d['crop'].lower()
            or any(search_q in k for k in d['keywords'])
        ]
    if crop_filter:
        diseases = [d for d in diseases if crop_filter.lower() in d['crop'].lower()]
    if type_filter:
        diseases = [d for d in diseases if type_filter.lower() in d['type'].lower()]

    crops_available = sorted(list(set(d['crop'] for d in sample_data.CROP_DISEASES)))
    return render_template(
        'diseases/index.html',
        diseases=diseases,
        crops_available=crops_available,
        search_q=search_q,
        crop_filter=crop_filter,
        type_filter=type_filter
    )


@app.route('/diseases/<int:disease_id>')
def disease_detail(disease_id):
    disease = next((d for d in sample_data.CROP_DISEASES if d['id'] == disease_id), None)
    if not disease:
        flash("Disease profile not found.", "danger")
        return redirect(url_for('diseases_list'))

    related = [d for d in sample_data.CROP_DISEASES if d['crop'] == disease['crop'] and d['id'] != disease['id']]
    return render_template('diseases/detail.html', disease=disease, related=related)


@app.route('/api/identify-pest', methods=['POST'])
def api_identify_pest():
    """
    AI Identification Endpoint for Crop Pests & Diseases.
    Accepts image file (multipart/form-data) or base64 JSON from camera capture.
    """
    try:
        file_obj = request.files.get('file')
        base64_str = None
        crop_hint = None

        if request.is_json:
            json_data = request.get_json() or {}
            base64_str = json_data.get('image')
            crop_hint = json_data.get('crop')
        else:
            base64_str = request.form.get('image')
            crop_hint = request.form.get('crop')

        image_bytes, filename, err = pest_detector.decode_image_input(file_obj=file_obj, base64_str=base64_str)
        if err or not image_bytes:
            return jsonify({
                'status': 'error',
                'message': err or 'No valid image provided. Please capture or upload a clear photo of the affected leaf.'
            }), 400

        result = pest_detector.identify_pest_and_disease(image_bytes, filename=filename or 'leaf.jpg', crop_hint=crop_hint)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f"Image analysis encountered an issue: {str(e)}. Please retry with a clear crop photo."
        }), 500


# -----------------------------------------------------------------------------
# 6. WEATHER INFORMATION
# -----------------------------------------------------------------------------
@app.route('/weather')
def weather():
    district = request.args.get('district', session.get('district', 'Nirmal'))
    data = sample_data.get_weather_data(district)
    available_districts = ["Nirmal", "Adilabad", "Nizamabad", "Warangal", "Karimnagar", "Guntur", "Khammam", "Pune", "Karnal"]
    return render_template('weather/index.html', weather=data, districts=available_districts, current_district=district)


# -----------------------------------------------------------------------------
# 7. MARKET PRICES (MANDI BHAV)
# -----------------------------------------------------------------------------
@app.route('/market')
def market():
    commodity_filter = request.args.get('commodity', '').strip().lower()
    district_filter = request.args.get('district', '').strip().lower()
    search_q = request.args.get('q', '').strip().lower()

    prices = sample_data.MANDI_PRICES

    if search_q:
        prices = [
            p for p in prices
            if search_q in p['commodity'].lower()
            or search_q in p['mandi'].lower()
            or search_q in p['variety'].lower()
            or search_q in p['district'].lower()
        ]
    if commodity_filter:
        prices = [p for p in prices if commodity_filter in p['commodity'].lower()]
    if district_filter:
        prices = [p for p in prices if district_filter in p['district'].lower()]

    commodities = sorted(list(set(p['commodity'] for p in sample_data.MANDI_PRICES)))
    districts = sorted(list(set(p['district'] for p in sample_data.MANDI_PRICES)))

    return render_template(
        'market/index.html',
        prices=prices,
        commodities=commodities,
        districts=districts,
        historical_trends=sample_data.MANDI_HISTORICAL_TRENDS,
        msp_data=sample_data.MSP_DATA,
        commodity_filter=commodity_filter,
        district_filter=district_filter,
        search_q=search_q
    )


# -----------------------------------------------------------------------------
# 8. GOVERNMENT SCHEMES
# -----------------------------------------------------------------------------
@app.route('/schemes')
def schemes_list():
    category_filter = request.args.get('category', '').strip()
    search_q = request.args.get('q', '').strip().lower()

    schemes = sample_data.GOVERNMENT_SCHEMES

    if search_q:
        schemes = [
            s for s in schemes
            if search_q in s['title'].lower()
            or search_q in s['code'].lower()
            or search_q in s['te_title'].lower()
            or search_q in s['benefit'].lower()
        ]
    if category_filter:
        schemes = [s for s in schemes if category_filter.lower() in s['category'].lower()]

    categories = sorted(list(set(s['category'] for s in sample_data.GOVERNMENT_SCHEMES)))
    return render_template(
        'schemes/index.html',
        schemes=schemes,
        categories=categories,
        category_filter=category_filter,
        search_q=search_q
    )


@app.route('/schemes/<int:scheme_id>')
def scheme_detail(scheme_id):
    scheme = next((s for s in sample_data.GOVERNMENT_SCHEMES if s['id'] == scheme_id), None)
    if not scheme:
        flash("Government scheme details not found.", "danger")
        return redirect(url_for('schemes_list'))

    other_schemes = [s for s in sample_data.GOVERNMENT_SCHEMES if s['id'] != scheme_id][:3]
    return render_template('schemes/detail.html', scheme=scheme, other_schemes=other_schemes)


# -----------------------------------------------------------------------------
# 9. FARMING TIPS
# -----------------------------------------------------------------------------
@app.route('/tips')
def tips():
    category_filter = request.args.get('category', '').strip()
    search_q = request.args.get('q', '').strip().lower()

    all_tips = sample_data.FARMING_TIPS

    if search_q:
        all_tips = [
            t for t in all_tips
            if search_q in t['title'].lower()
            or search_q in t['te_title'].lower()
            or search_q in t['summary'].lower()
            or any(search_q in s.lower() for s in t['steps'])
        ]
    if category_filter:
        all_tips = [t for t in all_tips if category_filter.lower() in t['category'].lower()]

    categories = sorted(list(set(t['category'] for t in sample_data.FARMING_TIPS)))
    return render_template(
        'tips/index.html',
        tips=all_tips,
        categories=categories,
        category_filter=category_filter,
        search_q=search_q
    )


# -----------------------------------------------------------------------------
# 10. EMERGENCY HELP & SOS
# -----------------------------------------------------------------------------
@app.route('/emergency', methods=['GET', 'POST'])
def emergency():
    farmer_id = session.get('farmer_id')
    user_requests = []
    if farmer_id:
        user_requests = database.query_db(
            "SELECT * FROM emergency_sos WHERE farmer_id = %s ORDER BY created_at DESC",
            (farmer_id,)
        )

    if request.method == 'POST':
        farmer_name = request.form.get('farmer_name', '').strip()
        contact_number = request.form.get('contact_number', '').strip()
        district = request.form.get('district', 'Nirmal').strip()
        village = request.form.get('village', '').strip()
        issue_type = request.form.get('issue_type', 'Pest Attack Alert').strip()
        severity = request.form.get('severity', 'High').strip()
        description = request.form.get('description', '').strip()

        if not farmer_name or not contact_number or not description or not village:
            flash("Please provide your name, contact phone, village, and description of the emergency.", "danger")
            return redirect(url_for('emergency'))

        database.query_db(
            """INSERT INTO emergency_sos 
            (farmer_id, farmer_name, contact_number, district, village, issue_type, severity, description, status) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'Pending')""",
            (farmer_id, farmer_name, contact_number, district, village, issue_type, severity, description),
            commit=True
        )

        flash("Emergency SOS submitted! Local agricultural rapid response unit has been notified.", "success")
        return redirect(url_for('emergency'))

    return render_template(
        'emergency/index.html',
        helplines=sample_data.EMERGENCY_CONTACTS,
        user_requests=user_requests
    )


# -----------------------------------------------------------------------------
# 11. NEARBY AGRICULTURAL SERVICES
# -----------------------------------------------------------------------------
@app.route('/services')
def services():
    category_filter = request.args.get('category', '').strip()
    search_q = request.args.get('q', '').strip().lower()

    all_services = sample_data.NEARBY_SERVICES

    if search_q:
        all_services = [
            s for s in all_services
            if search_q in s['name'].lower()
            or search_q in s['address'].lower()
            or search_q in s['contact_person'].lower()
            or any(search_q in item.lower() for item in s['services'])
        ]
    if category_filter:
        all_services = [s for s in all_services if category_filter.lower() in s['category'].lower()]

    categories = sorted(list(set(s['category'] for s in sample_data.NEARBY_SERVICES)))
    return render_template(
        'services/index.html',
        services=all_services,
        categories=categories,
        category_filter=category_filter,
        search_q=search_q
    )


# -----------------------------------------------------------------------------
# 12. AI CHATBOT & VOICE ASSISTANT APIS
# -----------------------------------------------------------------------------
@app.route('/chatbot')
def chatbot_page():
    """Dedicated full-page chatbot interface."""
    return render_template('chatbot/index.html')


@app.route('/api/chat', methods=['POST'])
def api_chat():
    """JSON API for chatbot queries (both typed and voice transcribed)."""
    data = request.get_json() or {}
    message = data.get('message', '').strip()
    
    if not message:
        return jsonify({
            'status': 'error',
            'response_text': 'Please enter or speak an agricultural query.',
            'voice_text': 'Please ask a question.',
            'language': 'en',
            'suggested_chips': []
        }), 400

    bot_res = chatbot_engine.generate_response(message)
    farmer_id = session.get('farmer_id')

    # Optionally log chat in database
    try:
        database.query_db(
            "INSERT INTO chat_logs (farmer_id, user_message, bot_response, language) VALUES (%s, %s, %s, %s)",
            (farmer_id, message, bot_res['response_text'], bot_res['language']),
            commit=True
        )
    except Exception:
        pass

    return jsonify({
        'status': 'success',
        'query': message,
        'response_text': bot_res['response_text'],
        'voice_text': bot_res['voice_text'],
        'language': bot_res['language'],
        'suggested_chips': bot_res.get('suggested_chips', []),
        'action_url': bot_res.get('action_url')
    })


@app.route('/api/voice-command', methods=['POST'])
def api_voice_command():
    """Direct route for executing navigation voice commands."""
    data = request.get_json() or {}
    transcript = data.get('transcript', '').strip().lower()
    
    # Navigation mappings
    routes_map = {
        'dashboard': url_for('dashboard'),
        'డాష్‌బోర్డ్': url_for('dashboard'),
        'weather': url_for('weather'),
        'వాతావరణం': url_for('weather'),
        'mandi': url_for('market'),
        'market': url_for('market'),
        'ధరలు': url_for('market'),
        'మార్కెట్': url_for('market'),
        'crops': url_for('crops_list'),
        'పంటలు': url_for('crops_list'),
        'diseases': url_for('diseases_list'),
        'తెగుళ్లు': url_for('diseases_list'),
        'camera': url_for('diseases_list'),
        'photo': url_for('diseases_list'),
        'scan': url_for('diseases_list'),
        'కెమెరా': url_for('diseases_list'),
        'స్కాన్': url_for('diseases_list'),
        'schemes': url_for('schemes_list'),
        'పథకాలు': url_for('schemes_list'),
        'tips': url_for('tips'),
        'సలహాలు': url_for('tips'),
        'emergency': url_for('emergency'),
        'సహాయం': url_for('emergency'),
        'services': url_for('services'),
        'సేవలు': url_for('services')
    }
    
    for key, redirect_url in routes_map.items():
        if key in transcript:
            return jsonify({
                'status': 'redirect',
                'url': redirect_url,
                'message': f"Opening {key.capitalize()}",
                'voice_text': f"Opening {key}"
            })
            
    # If not a pure navigation command, process via chatbot engine
    bot_res = chatbot_engine.generate_response(transcript)
    return jsonify({
        'status': 'chat',
        'response_text': bot_res['response_text'],
        'voice_text': bot_res['voice_text'],
        'language': bot_res['language'],
        'action_url': bot_res.get('action_url')
    })


# -----------------------------------------------------------------------------
# ERROR HANDLERS
# -----------------------------------------------------------------------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template('base.html', not_found=True), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('base.html', server_error=True), 500


if __name__ == '__main__':
    # Default to 0.0.0.0 and port 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
