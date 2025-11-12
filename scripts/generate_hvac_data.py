import numpy as np
import pandas as pd
import os
from datetime import datetime

output_dir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'output',
    f'hvac_service_jobs_{datetime.now().strftime("%m-%d")}'
)
os.makedirs(output_dir, exist_ok=True)

rng = np.random.default_rng(42)

# Config
N_JOBS = 25000
YEAR = 2025

# Helper distributions
months = np.arange(1, 13)
month_names = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

# Seasonality weights (more jobs in extreme temps)
# Higher in Jan, Feb, Jul, Aug; lower in Apr, May, Oct
base_month_weights = np.array([1.15, 1.10, 0.95, 0.90, 0.92, 1.05, 1.25, 1.20, 0.95, 0.90, 1.00, 1.13])
base_month_weights = base_month_weights / base_month_weights.sum()

# Division mix baseline (HVAC dominates; plumbing/electrical present; IAQ smaller)
divisions = ['HVAC', 'Plumbing', 'Electrical', 'IAQ']
div_weights = np.array([0.60, 0.22, 0.12, 0.06])

# Within HVAC: service_category and type vary by season
hvac_service_types = ['Install', 'Repair', 'Maintenance', 'Inspection', 'Replacement']
plumb_service_types = ['Repair', 'Maintenance', 'Install', 'Inspection', 'Replacement']
elec_service_types = ['Install', 'Repair', 'Maintenance', 'Inspection', 'Replacement']
iaq_service_types = ['Install', 'Maintenance', 'Inspection', 'Repair', 'Replacement']

# Equipment types per division
hvac_equipment = ['furnace', 'boiler', 'central_ac', 'mini_split', 'heat_pump', 'thermostat', 'ducts']
plumb_equipment = ['water_heater', 'tankless', 'sewer_line', 'drain', 'sump_pump', 'ejector_pump', 'softener']
elec_equipment = ['panel', 'wiring', 'lighting', 'generator', 'ev_charger', 'gfcis_afcis']
iaq_equipment = ['air_purifier', 'filtration', 'humidifier', 'dehumidifier', 'erv_hrv']

# Marketing channels
lead_sources = ['organic_search', 'PPC', 'referral', 'email', 'direct', 'mailers']
lead_base_weights = np.array([0.35, 0.22, 0.18, 0.08, 0.10, 0.07])

# Membership distribution
membership_tiers = ['None', 'Basic', 'Plus']
membership_weights = np.array([0.72, 0.18, 0.10])

# Cities/zips simple pool (sample Chicago suburbs)
cities = [
    'Crystal Lake','Hinsdale','Oak Brook','Elmhurst','Huntley','Lake Zurich',
    'Barrington','Mundelein','Cary','Algonquin','Western Springs','Lake in the Hills',
    'McHenry','Oakbrook Terrace','Hillside'
]
zips = [60014, 60521, 60523, 60126, 60142, 60047, 60010, 60060, 60013, 60102, 60558, 60156, 60050, 60181, 60162]
geo_clusters = ['North', 'Northwest', 'West', 'Southwest']

def month_day_sampler(year, n, month_weights):
    # Sample month, then day within month
    month = rng.choice(months, size=n, p=month_weights)
    days_in_month = pd.PeriodIndex([pd.Period(f'{year}-{m:02d}') for m in month], freq='M').days_in_month
    day = rng.integers(1, days_in_month + 1)
    hour = rng.integers(7, 21)  # typical arrival window 7am-8pm
    minute = rng.integers(0, 60)
    dt = pd.to_datetime({
        'year': np.full(n, year),
        'month': month,
        'day': day,
        'hour': hour,
        'minute': minute
    })
    return dt, month

def choose_service_type(division, m):
    # Seasonality & trend logic:
    # Winter (Dec-Feb): HVAC heating repair/replacement spike
    # Summer (Jun-Aug): HVAC AC repair/emergency spike
    # Shoulder: maintenance/installs more common
    if division == 'HVAC':
        if m in [12,1,2]:
            return rng.choice(
                hvac_service_types,
                p=[0.20, 0.42, 0.18, 0.04, 0.16]
            )
        elif m in [6,7,8]:
            return rng.choice(
                hvac_service_types,
                p=[0.18, 0.45, 0.18, 0.04, 0.15]
            )
        else:
            return rng.choice(
                hvac_service_types,
                p=[0.28, 0.25, 0.32, 0.05, 0.10]
            )
    elif division == 'Plumbing':
        return rng.choice(plumb_service_types, p=[0.18,0.28,0.30,0.06,0.18])
    elif division == 'Electrical':
        return rng.choice(elec_service_types, p=[0.32,0.28,0.25,0.05,0.10])
    else:
        return rng.choice(iaq_service_types, p=[0.35,0.40,0.10,0.10,0.05])

def choose_equipment(division, m):
    if division == 'HVAC':
        if m in [12,1,2]:
            weights = np.array([0.35,0.18,0.08,0.05,0.08,0.14,0.12])  # more furnace/boiler in winter
        elif m in [6,7,8]:
            weights = np.array([0.08,0.05,0.46,0.18,0.12,0.07,0.04])  # more central AC/mini-split in summer
        else:
            weights = np.array([0.20,0.10,0.25,0.12,0.15,0.10,0.08])
        weights = weights / weights.sum()
        return rng.choice(hvac_equipment, p=weights)
    elif division == 'Plumbing':
        return rng.choice(plumb_equipment, p=[0.30,0.12,0.10,0.18,0.16,0.04,0.10])
    elif division == 'Electrical':
        return rng.choice(elec_equipment, p=[0.28,0.20,0.22,0.12,0.10,0.08])
    else:
        return rng.choice(iaq_equipment, p=[0.25,0.30,0.15,0.15,0.15])

def lead_source_for_month(m):
    # Trend: PPC and mailers heavier in Jan–Mar; referrals grow later
    w = lead_base_weights.copy()
    if m in [1,2,3]:
        # boost PPC and mailers
        w = w * np.array([1.0, 1.35, 0.95, 1.0, 1.0, 1.35])
    elif m in [7]:
        # heat wave -> more direct/organic
        w = w * np.array([1.2, 1.0, 1.0, 1.0, 1.15, 1.0])
    elif m in [10,11,12]:
        # referrals up after strong service year
        w = w * np.array([1.0, 0.95, 1.3, 1.0, 1.0, 1.0])
    w = w / w.sum()
    return rng.choice(lead_sources, p=w)

def membership_for_customer():
    return rng.choice(membership_tiers, p=membership_weights)

def emergency_flag(division, m, service_type):
    base = 0.10
    if division == 'HVAC':
        if m in [12,1,2,7,8]:
            base += 0.08  # extreme temp pressure
        if service_type == 'Repair':
            base += 0.07
    elif division == 'Plumbing':
        base += 0.02
    # Members less likely to hit emergency
    # this probability will be adjusted later after membership known
    return base

def price_and_cost(division, service_type, equipment, is_member, month):
    # Base pricing by division/equipment/type
    base_price = 250
    if division == 'HVAC':
        if service_type in ['Install','Replacement']:
            if equipment in ['heat_pump','central_ac','mini_split','furnace','boiler']:
                base_price = rng.normal(6800, 900)
            else:
                base_price = rng.normal(900, 150)
        elif service_type == 'Maintenance' or service_type == 'Inspection':
            base_price = rng.normal(189, 25)
        else:  # Repair
            base_price = rng.normal(550, 140)
    elif division == 'Plumbing':
        if equipment in ['water_heater','tankless'] and service_type in ['Install','Replacement']:
            base_price = rng.normal(3200, 500)
        elif service_type in ['Maintenance','Inspection']:
            base_price = rng.normal(175, 25)
        elif service_type == 'Repair':
            base_price = rng.normal(450, 120)
        else:
            base_price = rng.normal(700, 180)
    elif division == 'Electrical':
        if equipment in ['panel','generator','ev_charger'] and service_type in ['Install','Replacement']:
            base_price = rng.normal(4100, 700)
        elif service_type in ['Maintenance','Inspection']:
            base_price = rng.normal(160, 25)
        elif service_type == 'Install':
            base_price = rng.normal(750, 200)
        else:
            base_price = rng.normal(420, 120)
    else:  # IAQ
        if service_type in ['Install','Replacement']:
            base_price = rng.normal(1400, 250)
        elif service_type in ['Maintenance','Inspection']:
            base_price = rng.normal(160, 20)
        else:
            base_price = rng.normal(350, 90)

    # Trend: utility rebates encouraging heat pump/mini-split installs in Q2–Q3
    utility_rebate = 0.0
    if division == 'HVAC' and service_type in ['Install','Replacement'] and equipment in ['heat_pump','mini_split']:
        if month in [4,5,6,7,8,9]:
            utility_rebate = max(0, rng.normal(600, 150))  # toward point-of-sale incentives

    # Membership discounts on service/repair/maintenance
    discount = 0.0
    if is_member and service_type in ['Repair','Maintenance','Inspection']:
        discount = abs(rng.normal(25, 10))
    # Rare promo codes (mostly early year)
    promo = 0.0
    if month in [1,2,3] and rng.random() < 0.12:
        promo = abs(rng.normal(35, 15))

    price_quoted = max(50, base_price - discount - promo)
    # Small slippage or upsell
    price_actual = max(40, price_quoted + rng.normal(0, price_quoted * 0.03))

    # Simple cost model
    materials_cost = max(0, price_actual * rng.uniform(0.12, 0.28))
    labor_cost = max(0, price_actual * rng.uniform(0.18, 0.35))
    gross_margin = price_actual - (materials_cost + labor_cost)

    return float(price_quoted), float(price_actual), float(materials_cost), float(labor_cost), float(gross_margin), float(utility_rebate), float(discount + promo)

def csat_nps(is_emergency, is_member, callback):
    # Members happier; emergencies volatile; callbacks depress scores
    csat_base = rng.normal(4.6, 0.35) if is_member else rng.normal(4.3, 0.45)
    if is_emergency:
        csat_base += rng.normal(-0.1, 0.25)
    if callback:
        csat_base -= rng.normal(0.5, 0.25)
    csat = float(np.clip(csat_base, 1.0, 5.0))

    # Map to NPS-ish score
    if csat >= 4.5:
        nps = rng.integers(60, 90)
    elif csat >= 4.0:
        nps = rng.integers(30, 60)
    elif csat >= 3.0:
        nps = rng.integers(-10, 30)
    else:
        nps = rng.integers(-100, -10)
    return csat, int(nps)

def generate():
    dt, month = month_day_sampler(YEAR, N_JOBS, base_month_weights)

    division = rng.choice(divisions, size=N_JOBS, p=div_weights)
    city = rng.choice(cities, size=N_JOBS)
    zipc = rng.choice(zips, size=N_JOBS)
    geo = rng.choice(geo_clusters, size=N_JOBS)

    # per-row fields to fill
    service_type = []
    equipment = []
    lead_source = []
    membership = []
    is_member_flag = []
    is_emergency = []
    price_quoted = np.zeros(N_JOBS)
    price_actual = np.zeros(N_JOBS)
    materials_cost = np.zeros(N_JOBS)
    labor_cost = np.zeros(N_JOBS)
    gross_margin = np.zeros(N_JOBS)
    utility_rebate = np.zeros(N_JOBS)
    discounts_total = np.zeros(N_JOBS)
    callback_30 = []
    csat = np.zeros(N_JOBS)
    nps = np.zeros(N_JOBS)

    # Create IDs
    job_id = np.arange(1, N_JOBS + 1)

    for i in range(N_JOBS):
        m = int(month[i])
        div = division[i]
        st = choose_service_type(div, m)
        eq = choose_equipment(div, m)
        ls = lead_source_for_month(m)

        mem = membership_for_customer()
        member_flag = mem != 'None'

        # Emergency probability adjusted for membership
        e_prob = emergency_flag(div, m, st)
        if member_flag:
            e_prob = max(0, e_prob - 0.04)
        emerg = rng.random() < e_prob

        # Callback (revisit) trend: lower for members and maintenance
        cb_prob = 0.06
        if member_flag:
            cb_prob -= 0.02
        if st in ['Maintenance','Inspection']:
            cb_prob -= 0.025
        if emerg:
            cb_prob += 0.02
        callback = rng.random() < max(0.005, cb_prob)

        pq, pa, mc, lc, gm, ur, disc = price_and_cost(div, st, eq, member_flag, m)

        # Customer experience
        cs, nps_score = csat_nps(emerg, member_flag, callback)

        service_type.append(st)
        equipment.append(eq)
        lead_source.append(ls)
        membership.append(mem)
        is_member_flag.append(member_flag)
        is_emergency.append(emerg)
        price_quoted[i] = pq
        price_actual[i] = pa
        materials_cost[i] = mc
        labor_cost[i] = lc
        gross_margin[i] = gm
        utility_rebate[i] = ur
        discounts_total[i] = disc
        callback_30.append(callback)
        csat[i] = cs
        nps[i] = nps_score

    df = pd.DataFrame({
        'job_id': job_id,
        'date': dt,
        'month': month,
        'month_name': [month_names[m-1] for m in month],
        'division': division,
        'service_type': service_type,
        'equipment': equipment,
        'lead_source': lead_source,
        'membership_tier': membership,
        'is_member': is_member_flag,
        'city': city,
        'zip': zipc,
        'geo_cluster': geo,
        'is_emergency': is_emergency,
        'price_quoted': np.round(price_quoted, 2),
        'price_actual': np.round(price_actual, 2),
        'materials_cost': np.round(materials_cost, 2),
        'labor_cost': np.round(labor_cost, 2),
        'gross_margin': np.round(gross_margin, 2),
        'utility_rebate_amount': np.round(utility_rebate, 2),
        'discounts_total': np.round(discounts_total, 2),
        'callback_within_30_days': callback_30,
        'csat_score_1_5': np.round(csat, 2),
        'nps_score': nps
    })

    # Derive some flags
    df['heating_job'] = (df['division'].eq('HVAC')) & (df['equipment'].isin(['furnace','boiler']))
    df['cooling_job'] = (df['division'].eq('HVAC')) & (df['equipment'].isin(['central_ac','mini_split','heat_pump']))

    return df

df = generate()
# Filter for records with 'date' before today
df = df[pd.to_datetime(df['date']) < pd.to_datetime('today')]


# Monthly trend table for 2025
trend = (df.groupby(['month','month_name'])
           .agg(
               jobs=('job_id','count'),
               hvac_jobs=('division', lambda s: (s=='HVAC').sum()),
               plumbing_jobs=('division', lambda s: (s=='Plumbing').sum()),
               electrical_jobs=('division', lambda s: (s=='Electrical').sum()),
               iaq_jobs=('division', lambda s: (s=='IAQ').sum()),
               heating_jobs=('heating_job','sum'),
               cooling_jobs=('cooling_job','sum'),
               emergencies=('is_emergency','sum'),
               members=('is_member','sum'),
               revenue=('price_actual','sum'),
               gross_margin=('gross_margin','sum'),
               callbacks=('callback_within_30_days','sum'),
               avg_csat=('csat_score_1_5','mean'),
               avg_nps=('nps_score','mean')
           )
           .reset_index()
           .sort_values('month'))

# Tidy output
trend['revenue'] = trend['revenue'].round(0)
trend['gross_margin'] = trend['gross_margin'].round(0)
trend['avg_csat'] = trend['avg_csat'].round(2)
trend['avg_nps'] = trend['avg_nps'].round(1)

print("Monthly Trends for 2025")
print(trend[['month','month_name','jobs','hvac_jobs','plumbing_jobs','electrical_jobs','iaq_jobs',
             'heating_jobs','cooling_jobs','emergencies','members','callbacks','revenue','gross_margin','avg_csat','avg_nps']])

df = df.drop(columns=['month', 'month_name'])


# Save full dataset
output_path = os.path.join(output_dir, f'hvac_service_jobs_{datetime.now().strftime("%m-%d")}.csv')
df.to_csv(output_path, index=False)
print(f"\nSaved dataset: {output_path}")