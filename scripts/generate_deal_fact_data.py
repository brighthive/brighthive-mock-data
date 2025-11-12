import numpy as np
import pandas as pd
import os
from datetime import datetime, timedelta

output_dir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'output',
    f'hubspot_deals_{datetime.now().strftime("%m-%d")}'
)
os.makedirs(output_dir, exist_ok=True)

rng = np.random.default_rng(42)

# Config
N_DEALS = 2000000
YEAR = 2025

# Helper distributions
months = np.arange(1, 13)
month_names = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

# Seasonality weights (B2B typical: Q4 heavy, summer lighter)
base_month_weights = np.array([1.05, 1.00, 1.10, 0.95, 0.90, 0.85, 0.80, 0.88, 1.05, 1.15, 1.20, 1.25])
base_month_weights = base_month_weights / base_month_weights.sum()

# Brands
brands = ['Brand_A', 'Brand_B', 'Brand_C']
brand_weights = np.array([0.50, 0.35, 0.15])

# Deal types
deal_types = ['New Business', 'Renewal', 'Upsell', 'Cross-sell']
deal_type_weights = np.array([0.45, 0.30, 0.15, 0.10])

# Pipelines
pipelines = ['Sales Pipeline', 'Partner Pipeline', 'Enterprise Pipeline']
pipeline_weights = np.array([0.65, 0.20, 0.15])

# Deal stages
stages = [
    'appointmentscheduled',
    'qualifiedtobuy', 
    'presentationscheduled',
    'decisionmakerboughtin',
    'contractsent',
    'closedwon',
    'closedlost'
]
stage_names = [
    'Appointment Scheduled',
    'Qualified to Buy',
    'Presentation Scheduled', 
    'Decision Maker Bought In',
    'Contract Sent',
    'Closed Won',
    'Closed Lost'
]
stage_probabilities = [0.10, 0.25, 0.40, 0.60, 0.80, 1.00, 0.00]

# Deal owners
owners = [
    {'first': 'Sarah', 'last': 'Johnson', 'email': 'sjohnson@company.com', 'user_id': 'U001', 'team': 'Sales_Team_A'},
    {'first': 'Michael', 'last': 'Chen', 'email': 'mchen@company.com', 'user_id': 'U002', 'team': 'Sales_Team_A'},
    {'first': 'Emily', 'last': 'Rodriguez', 'email': 'erodriguez@company.com', 'user_id': 'U003', 'team': 'Sales_Team_B'},
    {'first': 'David', 'last': 'Kim', 'email': 'dkim@company.com', 'user_id': 'U004', 'team': 'Sales_Team_B'},
    {'first': 'Jessica', 'last': 'Williams', 'email': 'jwilliams@company.com', 'user_id': 'U005', 'team': 'Enterprise_Team'},
    {'first': 'Robert', 'last': 'Brown', 'email': 'rbrown@company.com', 'user_id': 'U006', 'team': 'Partner_Team'},
]

# Analytics sources
sources = ['ORGANIC_SEARCH', 'PAID_SEARCH', 'REFERRALS', 'DIRECT_TRAFFIC', 'EMAIL_MARKETING', 'SOCIAL_MEDIA', 'PAID_SOCIAL']
source_weights = np.array([0.25, 0.20, 0.18, 0.15, 0.10, 0.07, 0.05])

# Enrollment types
enrollment_types = ['Online', 'In-Person', 'Hybrid', 'Virtual']
enrollment_weights = np.array([0.40, 0.30, 0.20, 0.10])

# Delivery methods
delivery_methods = ['Digital', 'Physical', 'Hybrid', 'Service']
delivery_weights = np.array([0.45, 0.25, 0.20, 0.10])

# Education types
education_types = ['Higher_Ed', 'K12', 'Corporate', 'Professional_Dev', 'Vocational']
education_weights = np.array([0.30, 0.25, 0.25, 0.15, 0.05])

# States
states = ['IL', 'CA', 'NY', 'TX', 'FL', 'PA', 'OH', 'MI', 'GA', 'NC', 'WA', 'MA', 'VA', 'AZ', 'CO']
state_weights = np.array([0.15, 0.12, 0.10, 0.09, 0.08, 0.06, 0.05, 0.05, 0.05, 0.04, 0.04, 0.04, 0.04, 0.04, 0.05])

# Professions
professions = ['Teacher', 'Administrator', 'Counselor', 'Specialist', 'Coordinator', 'Director', 'Manager', 'Consultant']
profession_weights = np.array([0.25, 0.18, 0.12, 0.10, 0.10, 0.10, 0.08, 0.07])

# Closed reasons
closed_won_reasons = ['Budget Approved', 'ROI Demonstrated', 'Competitive Win', 'Renewal Success', 'Expansion']
closed_lost_reasons = ['Lost to Competitor', 'Budget Constraints', 'No Decision', 'Timing Issues', 'Not a Fit']

def month_day_sampler(year, n, month_weights):
    month = rng.choice(months, size=n, p=month_weights)
    days_in_month = pd.PeriodIndex([pd.Period(f'{year}-{m:02d}') for m in month], freq='M').days_in_month
    day = rng.integers(1, days_in_month + 1)
    hour = rng.integers(0, 24)
    minute = rng.integers(0, 60)
    second = rng.integers(0, 60)
    dt = pd.to_datetime({
        'year': np.full(n, year),
        'month': month,
        'day': day,
        'hour': hour,
        'minute': minute,
        'second': second
    })
    return dt, month

def choose_stage(month):
    # More closed won in Q4
    if month in [10, 11, 12]:
        weights = [0.05, 0.08, 0.10, 0.12, 0.15, 0.35, 0.15]
    else:
        weights = [0.10, 0.15, 0.18, 0.15, 0.12, 0.20, 0.10]
    weights = np.array(weights)
    weights = weights / weights.sum()
    return rng.choice(range(len(stages)), p=weights)

def calculate_deal_amount(deal_type, brand, enrollment_type, month):
    base = 25000
    
    if deal_type == 'New Business':
        base = rng.normal(45000, 12000)
    elif deal_type == 'Renewal':
        base = rng.normal(38000, 10000)
    elif deal_type == 'Upsell':
        base = rng.normal(28000, 8000)
    else:  # Cross-sell
        base = rng.normal(22000, 6000)
    
    if brand == 'Brand_A':
        base *= 1.2
    elif brand == 'Brand_C':
        base *= 0.8
    
    if enrollment_type == 'In-Person':
        base *= 1.15
    elif enrollment_type == 'Online':
        base *= 0.95
    
    # Q4 deals slightly larger
    if month in [10, 11, 12]:
        base *= 1.08
    
    return max(5000, base)

def calculate_days_between_stages():
    days = {}
    days['appointment_to_qualified'] = max(0, int(rng.normal(3, 2)))
    days['qualified_to_presentation'] = max(0, int(rng.normal(7, 3)))
    days['presentation_to_decision'] = max(0, int(rng.normal(10, 5)))
    days['decision_to_contract'] = max(0, int(rng.normal(5, 3)))
    days['contract_to_closed'] = max(0, int(rng.normal(8, 4)))
    return days

def generate():
    create_dt, create_month = month_day_sampler(YEAR, N_DEALS, base_month_weights)
    
    # Core fields
    unique_ids = [f'UID_{i:08d}' for i in range(1, N_DEALS + 1)]
    deal_ids = np.arange(1000000, 1000000 + N_DEALS)
    portal_ids = rng.choice([12345, 12346, 12347], size=N_DEALS)
    
    brands = rng.choice(['Brand_A', 'Brand_B', 'Brand_C'], size=N_DEALS, p=brand_weights)
    deal_types = rng.choice(['New Business', 'Renewal', 'Upsell', 'Cross-sell'], size=N_DEALS, p=deal_type_weights)
    pipelines = rng.choice(['Sales Pipeline', 'Partner Pipeline', 'Enterprise Pipeline'], size=N_DEALS, p=pipeline_weights)
    
    # Owner assignment
    owner_indices = rng.integers(0, len(owners), size=N_DEALS)
    
    # Sources
    latest_sources = rng.choice(sources, size=N_DEALS, p=source_weights)
    original_sources = rng.choice(sources, size=N_DEALS, p=source_weights)
    
    # Purchase details
    enrollment_types = rng.choice(['Online', 'In-Person', 'Hybrid', 'Virtual'], size=N_DEALS, p=enrollment_weights)
    delivery_methods = rng.choice(['Digital', 'Physical', 'Hybrid', 'Service'], size=N_DEALS, p=delivery_weights)
    education_types = rng.choice(['Higher_Ed', 'K12', 'Corporate', 'Professional_Dev', 'Vocational'], size=N_DEALS, p=education_weights)
    purchase_states = rng.choice(states, size=N_DEALS, p=state_weights)
    purchase_professions = rng.choice(professions, size=N_DEALS, p=profession_weights)
    
    # Arrays to fill
    deal_names = []
    stage_indices = []
    deal_amounts = []
    is_closed_flags = []
    is_won_flags = []
    close_dates = []
    days_to_close_list = []
    closed_won_reason_list = []
    closed_lost_reason_list = []
    
    # Stage timing
    appointment_dates = []
    qualified_dates = []
    presentation_dates = []
    decision_dates = []
    contract_dates = []
    
    # Engagement metrics
    contact_counts = []
    note_counts = []
    meeting_counts = []
    email_counts = []
    call_counts = []
    task_counts = []
    
    # Discount info
    discount_used_flags = []
    discount_amounts = []
    discount_percents = []
    
    # Membership
    membership_purchased_flags = []
    package_purchased_flags = []
    
    # Contact info
    first_names = ['John', 'Sarah', 'Michael', 'Emily', 'David', 'Jessica', 'Robert', 'Jennifer', 'William', 'Ashley']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']
    
    contact_first_names = []
    contact_last_names = []
    contact_emails = []
    contact_phones = []
    
    for i in range(N_DEALS):
        month = int(create_month[i])
        brand = brands[i]
        deal_type = deal_types[i]
        enrollment_type = enrollment_types[i]
        
        # Deal name
        deal_name = f"{brand} - {deal_type} - {rng.choice(['Q1', 'Q2', 'Q3', 'Q4'])} 2025"
        deal_names.append(deal_name)
        
        # Stage
        stage_idx = choose_stage(month)
        stage_indices.append(stage_idx)
        
        # Amount
        amount = calculate_deal_amount(deal_type, brand, enrollment_type, month)
        deal_amounts.append(amount)
        
        # Closed status
        is_closed = stage_idx >= 5  # closedwon or closedlost
        is_won = stage_idx == 5
        is_closed_flags.append(is_closed)
        is_won_flags.append(is_won)
        
        # Close date and days to close
        if is_closed:
            days_to_close = max(1, int(rng.normal(45, 20)))
            close_date = create_dt[i] + timedelta(days=days_to_close)
            close_dates.append(close_date)
            days_to_close_list.append(days_to_close)
            
            if is_won:
                closed_won_reason_list.append(rng.choice(closed_won_reasons))
                closed_lost_reason_list.append(None)
            else:
                closed_won_reason_list.append(None)
                closed_lost_reason_list.append(rng.choice(closed_lost_reasons))
        else:
            close_dates.append(None)
            days_to_close_list.append(None)
            closed_won_reason_list.append(None)
            closed_lost_reason_list.append(None)
        
        # Stage timing
        stage_days = calculate_days_between_stages()
        appt_date = create_dt[i] + timedelta(days=int(rng.integers(0, 3)))
        appointment_dates.append(appt_date if stage_idx >= 0 else None)
        
        qual_date = appt_date + timedelta(days=stage_days['appointment_to_qualified'])
        qualified_dates.append(qual_date if stage_idx >= 1 else None)
        
        pres_date = qual_date + timedelta(days=stage_days['qualified_to_presentation'])
        presentation_dates.append(pres_date if stage_idx >= 2 else None)
        
        dec_date = pres_date + timedelta(days=stage_days['presentation_to_decision'])
        decision_dates.append(dec_date if stage_idx >= 3 else None)
        
        contract_date = dec_date + timedelta(days=stage_days['decision_to_contract'])
        contract_dates.append(contract_date if stage_idx >= 4 else None)
        
        # Engagement
        contact_counts.append(rng.integers(1, 15))
        note_counts.append(rng.integers(0, 25))
        meeting_counts.append(rng.integers(0, 8))
        email_counts.append(rng.integers(2, 30))
        call_counts.append(rng.integers(0, 12))
        task_counts.append(rng.integers(0, 10))
        
        # Discounts
        has_discount = rng.random() < 0.25
        discount_used_flags.append(has_discount)
        if has_discount:
            disc_pct = rng.uniform(0.05, 0.20)
            disc_amt = amount * disc_pct
            discount_amounts.append(disc_amt)
            discount_percents.append(disc_pct * 100)
        else:
            discount_amounts.append(0)
            discount_percents.append(0)
        
        # Membership/Package
        membership_purchased_flags.append(rng.random() < 0.35)
        package_purchased_flags.append(rng.random() < 0.40)
        
        # Contact info
        fname = rng.choice(first_names)
        lname = rng.choice(last_names)
        contact_first_names.append(fname)
        contact_last_names.append(lname)
        contact_emails.append(f"{fname.lower()}.{lname.lower()}@example.com")
        contact_phones.append(f"+1-{rng.integers(200, 999)}-{rng.integers(200, 999)}-{rng.integers(1000, 9999)}")
    
    # Build DataFrame
    df = pd.DataFrame({
        'unique_id': unique_ids,
        'source_model': ['HubSpot'] * N_DEALS,
        'brand': brands,
        'deal_id': deal_ids,
        'portal_id': portal_ids,
        'deal_name': deal_names,
        'deal_type': deal_types,
        'pipeline': pipelines,
        'deal_stage': [stages[idx] for idx in stage_indices],
        'is_deleted': [False] * N_DEALS,
        'deal_owner': [owners[idx]['email'] for idx in owner_indices],
        'hubspot_team': [owners[idx]['team'] for idx in owner_indices],
        'owner_assigned_date': create_dt,
        'owner_first_name': [owners[idx]['first'] for idx in owner_indices],
        'owner_last_name': [owners[idx]['last'] for idx in owner_indices],
        'owner_full_name': [f"{owners[idx]['first']} {owners[idx]['last']}" for idx in owner_indices],
        'owner_email': [owners[idx]['email'] for idx in owner_indices],
        'owner_user_id': [owners[idx]['user_id'] for idx in owner_indices],
        'owner_is_active': [True] * N_DEALS,
        'stage_name': [stage_names[idx] for idx in stage_indices],
        'stage_display_order': [idx + 1 for idx in stage_indices],
        'stage_probability': [stage_probabilities[idx] for idx in stage_indices],
        'deal_amount': np.round(deal_amounts, 2),
        'amount_in_home_currency': np.round(deal_amounts, 2),
        'closed_deal_amount': [np.round(deal_amounts[i], 2) if is_closed_flags[i] else 0 for i in range(N_DEALS)],
        'forecast_amount': np.round([deal_amounts[i] * stage_probabilities[stage_indices[i]] for i in range(N_DEALS)], 2),
        'hs_projected_amount': np.round([deal_amounts[i] * stage_probabilities[stage_indices[i]] for i in range(N_DEALS)], 2),
        'hs_projected_amount_in_home_currency': np.round([deal_amounts[i] * stage_probabilities[stage_indices[i]] for i in range(N_DEALS)], 2),
        'hs_closed_amount_in_home_currency': [np.round(deal_amounts[i], 2) if is_closed_flags[i] else 0 for i in range(N_DEALS)],
        'is_deal_closed': is_closed_flags,
        'is_closed_won': is_won_flags,
        'deal_probability': [stage_probabilities[idx] for idx in stage_indices],
        'closed_lost_reason': closed_lost_reason_list,
        'closed_won_reason': closed_won_reason_list,
        'create_date': create_dt,
        'close_date': close_dates,
        'last_modified_date': create_dt + pd.to_timedelta(rng.integers(0, 30, N_DEALS), unit='D'),
        'hs_createdate': create_dt,
        'days_to_close': days_to_close_list,
        'last_contacted': create_dt + pd.to_timedelta(rng.integers(1, 10, N_DEALS), unit='D'),
        'number_of_associated_contacts': contact_counts,
        'num_notes': note_counts,
        'meeting_count': meeting_counts,
        'email_count': email_counts,
        'call_count': call_counts,
        'note_count': note_counts,
        'task_count': task_counts,
        'total_engagement_count': [note_counts[i] + meeting_counts[i] + email_counts[i] + call_counts[i] + task_counts[i] for i in range(N_DEALS)],
        'date_of_first_sale': [close_dates[i] if is_won_flags[i] else None for i in range(N_DEALS)],
        'enrollment_rep': [owners[idx]['email'] for idx in owner_indices],
        'enrollment_type': enrollment_types,
        'hours_purchased': rng.integers(10, 200, N_DEALS),
        'delivery_method': delivery_methods,
        'discount_used': discount_used_flags,
        'discount_amount': np.round(discount_amounts, 2),
        'discount_percent': np.round(discount_percents, 2),
        'discount_code_used': [f'DISC{rng.integers(100, 999)}' if discount_used_flags[i] else None for i in range(N_DEALS)],
        'items_purchased': rng.integers(1, 10, N_DEALS),
        'membership_purchased': membership_purchased_flags,
        'package_purchased': package_purchased_flags,
        'package_purchase_name': [f'Package_{rng.choice(["Basic", "Pro", "Premium"])}' if package_purchased_flags[i] else None for i in range(N_DEALS)],
        'membership_expiration_date': [create_dt[i] + pd.Timedelta(days=365) if membership_purchased_flags[i] else None for i in range(N_DEALS)],
        'membership_purchase_name': [rng.choice(['Gold', 'Silver', 'Bronze']) if membership_purchased_flags[i] else None for i in range(N_DEALS)],
        'membership_purchase_date': [create_dt[i] if membership_purchased_flags[i] else None for i in range(N_DEALS)],
        'purchased_items': [f'Item_{rng.integers(1, 50)}' for _ in range(N_DEALS)],
        'first_name': contact_first_names,
        'last_name': contact_last_names,
        'email': contact_emails,
        'phone_number': contact_phones,
        'contact_name': [f"{contact_first_names[i]} {contact_last_names[i]}" for i in range(N_DEALS)],
        'profession': purchase_professions,
        'username': [f'user_{rng.integers(1000, 9999)}' for _ in range(N_DEALS)],
        'purchase_subsidiary': [rng.choice(['Sub_A', 'Sub_B', 'Sub_C']) for _ in range(N_DEALS)],
        'purchase_education_type': education_types,
        'purchase_state': purchase_states,
        'purchase_profession': purchase_professions,
        'hs_analytics_latest_source': latest_sources,
        'hs_analytics_latest_source_data_1': [f'campaign_{rng.integers(100, 999)}' for _ in range(N_DEALS)],
        'hs_analytics_latest_source_data_2': [f'medium_{rng.choice(["cpc", "organic", "referral", "email"])}' for _ in range(N_DEALS)],
        'hs_analytics_latest_source_contact': contact_emails,
        'hs_analytics_latest_source_company': [f'Company_{rng.integers(100, 999)}' for _ in range(N_DEALS)],
        'hs_analytics_latest_source_timestamp': create_dt - pd.to_timedelta(rng.integers(1, 90, N_DEALS), unit='D'),
        'hs_analytics_source': original_sources,
        'hs_analytics_source_data_1': [f'campaign_{rng.integers(100, 999)}' for _ in range(N_DEALS)],
        'hs_analytics_source_data_2': [f'medium_{rng.choice(["cpc", "organic", "referral", "email"])}' for _ in range(N_DEALS)],
        'hs_object_id': [f'OBJ_{i:010d}' for i in range(N_DEALS)],
        'hs_created_by_user_id': [owners[idx]['user_id'] for idx in owner_indices],
        'hs_updated_by_user_id': [owners[idx]['user_id'] for idx in owner_indices],
        'hs_all_owner_ids': [owners[idx]['user_id'] for idx in owner_indices],
        'hs_all_team_ids': [owners[idx]['team'] for idx in owner_indices],
        'hs_user_ids_of_all_owners': [owners[idx]['user_id'] for idx in owner_indices],
        'hs_time_in_appointmentscheduled': [rng.integers(1, 72) if stage_indices[i] >= 0 else 0 for i in range(N_DEALS)],
        'hs_time_in_qualifiedtobuy': [rng.integers(1, 168) if stage_indices[i] >= 1 else 0 for i in range(N_DEALS)],
        'hs_time_in_presentationscheduled': [rng.integers(1, 240) if stage_indices[i] >= 2 else 0 for i in range(N_DEALS)],
        'hs_time_in_decisionmakerboughtin': [rng.integers(1, 192) if stage_indices[i] >= 3 else 0 for i in range(N_DEALS)],
        'hs_time_in_contractsent': [rng.integers(1, 168) if stage_indices[i] >= 4 else 0 for i in range(N_DEALS)],
        'hs_time_in_closedwon': [rng.integers(1, 48) if stage_indices[i] == 5 else 0 for i in range(N_DEALS)],
        'hs_time_in_closedlost': [rng.integers(1, 24) if stage_indices[i] == 6 else 0 for i in range(N_DEALS)],
        'total_days_to_close': days_to_close_list,
        'days_appointment_to_qualified': [rng.integers(1, 10) if stage_indices[i] >= 1 else None for i in range(N_DEALS)],
        'days_qualified_to_presentation': [rng.integers(1, 15) if stage_indices[i] >= 2 else None for i in range(N_DEALS)],
        'days_presentation_to_decision': [rng.integers(1, 20) if stage_indices[i] >= 3 else None for i in range(N_DEALS)],
        'days_decision_to_contract': [rng.integers(1, 12) if stage_indices[i] >= 4 else None for i in range(N_DEALS)],
        'days_contract_to_closed_won': [rng.integers(1, 15) if stage_indices[i] == 5 else None for i in range(N_DEALS)],
        'appointment_scheduled': appointment_dates,
        'qualified_to_buy': qualified_dates,
        'presentation_scheduled': presentation_dates,
        'decision_maker_bought_in': decision_dates,
        'contract_sent': contract_dates,
        'closed_won_stage': [close_dates[i] if is_won_flags[i] else None for i in range(N_DEALS)],
        'closed_lost_stage': [close_dates[i] if (is_closed_flags[i] and not is_won_flags[i]) else None for i in range(N_DEALS)],
        '_fivetran_synced_ts': datetime.now()
    })
    
    return df

# Generate dataset
df = generate()

# Filter for records before today
df = df[pd.to_datetime(df['create_date']) < pd.to_datetime('today')]

# Summary statistics
print(f"\nGenerated {len(df)} deals")
print(f"\nDeals by Stage:")
print(df['stage_name'].value_counts().sort_index())
print(f"\nDeals by Brand:")
print(df['brand'].value_counts())
print(f"\nTotal Deal Value: ${df['deal_amount'].sum():,.2f}")
print(f"Total Closed Won Value: ${df[df['is_closed_won']]['deal_amount'].sum():,.2f}")
print(f"Win Rate: {df['is_closed_won'].sum() / df['is_deal_closed'].sum() * 100:.1f}%")

# Save dataset
output_path = os.path.join(output_dir, f'hubspot_deals_{datetime.now().strftime("%m-%d")}.csv')
df.to_csv(output_path, index=False)
print(f"\nSaved dataset: {output_path}")