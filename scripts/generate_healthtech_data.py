import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from faker import Faker
import os

# Set up Faker and random seeds
fake = Faker()
np.random.seed(42)
random.seed(42)

# Get current date for directory naming
current_date = datetime.now()
date_suffix = current_date.strftime("%m-%d")

# Create output directory
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, f"../output/healthtech_{date_suffix}")
os.makedirs(output_dir, exist_ok=True)

def generate_patients(n_patients=500):
    """Generate patients table for healthtech"""
    diagnoses = ['Multiple Sclerosis', 'Rheumatoid Arthritis', 'Oncology', 'Hepatitis C', 'HIV', 'Psoriasis', 'Crohns Disease']
    insurance_types = ['Commercial', 'Medicare', 'Medicaid', 'Cash Pay', 'Patient Assistance']
    program_statuses = ['Active', 'Enrolled', 'Dropped', 'Completed', 'Pending']
    
    patients = []
    for i in range(n_patients):
        enrollment_date = fake.date_between(start_date='-2y', end_date='today')
        patients.append({
            'patient_id': f'PAT{i+1:05d}',
            'name': fake.name(),
            'date_of_birth': fake.date_of_birth(minimum_age=18, maximum_age=85),
            'gender': random.choice(['M', 'F', 'Other']),
            'phone': fake.phone_number(),
            'email': fake.email(),
            'address': fake.address().replace('\n', ', '),
            'zip_code': fake.zipcode(),
            'primary_diagnosis': random.choice(diagnoses),
            'insurance_type': random.choice(insurance_types),
            'insurance_id': fake.bothify(text='INS-####-????'),
            'enrollment_date': enrollment_date,
            'program_status': random.choice(program_statuses),
            'preferred_contact': random.choice(['Phone', 'Email', 'SMS', 'Mail'])
        })
    return pd.DataFrame(patients)

def generate_prescriptions(n_prescriptions=1200, patient_df=None):
    """Generate prescriptions table"""
    specialty_drugs = [
        'Humira', 'Enbrel', 'Remicade', 'Copaxone', 'Tecfidera', 
        'Harvoni', 'Sovaldi', 'Keytruda', 'Opdivo', 'Rituxan'
    ]
    statuses = ['Written', 'Sent to Pharmacy', 'Filled', 'Abandoned', 'Denied', 'Pending PA']
    
    prescriptions = []
    for i in range(n_prescriptions):
        date_written = fake.date_between(start_date='-18m', end_date='today')
        date_filled = None
        status = random.choice(statuses)
        
        if status == 'Filled':
            date_filled = fake.date_between(start_date=date_written, end_date='today')
        
        prescriptions.append({
            'prescription_id': f'RX{i+1:06d}',
            'patient_id': f'PAT{random.randint(1,500):05d}',
            'prescriber_id': f'PRV{random.randint(1,200):03d}',
            'drug_name': random.choice(specialty_drugs),
            'ndc_number': fake.bothify(text='#####-####-##'),
            'quantity': random.randint(1, 90),
            'days_supply': random.choice([30, 60, 90]),
            'date_written': date_written,
            'date_sent_to_pharmacy': fake.date_between(start_date=date_written, end_date='today') if status != 'Written' else None,
            'date_filled': date_filled,
            'status': status,
            'pharmacy_id': f'PHM{random.randint(1,150):03d}' if status in ['Sent to Pharmacy', 'Filled'] else None,
            'copay_amount': round(random.uniform(0, 500), 2),
            'insurance_covered_amount': round(random.uniform(1000, 15000), 2)
        })
    return pd.DataFrame(prescriptions)

def generate_providers(n_providers=200):
    """Generate healthcare providers table"""
    specialties = [
        'Rheumatology', 'Neurology', 'Oncology', 'Gastroenterology', 
        'Infectious Disease', 'Dermatology', 'Internal Medicine'
    ]
    
    providers = []
    for i in range(n_providers):
        providers.append({
            'provider_id': f'PRV{i+1:03d}',
            'name': f'Dr. {fake.name()}',
            'specialty': random.choice(specialties),
            'npi_number': fake.bothify(text='##########'),
            'practice_name': fake.company() + ' Medical Center',
            'address': fake.address().replace('\n', ', '),
            'city': fake.city(),
            'state': fake.state_abbr(),
            'zip_code': fake.zipcode(),
            'phone': fake.phone_number(),
            'email': fake.email(),
            'years_in_practice': random.randint(1, 35),
            'affiliated_hospitals': random.randint(1, 3)
        })
    return pd.DataFrame(providers)

def generate_pharmacies(n_pharmacies=150):
    """Generate pharmacies table"""
    pharmacy_types = ['Specialty', 'Retail', 'Hospital', 'Mail Order']
    chains = ['CVS Specialty', 'Walgreens Specialty', 'Accredo', 'BioPlus', 'Independent', 'Kroger', 'Rite Aid']
    
    pharmacies = []
    for i in range(n_pharmacies):
        pharmacy_type = random.choice(pharmacy_types)
        pharmacies.append({
            'pharmacy_id': f'PHM{i+1:03d}',
            'name': random.choice(chains) + (f' #{random.randint(1000,9999)}' if pharmacy_type == 'Retail' else ''),
            'type': pharmacy_type,
            'chain': random.choice(chains),
            'address': fake.address().replace('\n', ', '),
            'city': fake.city(),
            'state': fake.state_abbr(),
            'zip_code': fake.zipcode(),
            'phone': fake.phone_number(),
            'network_status': random.choice(['In Network', 'Out of Network', 'Preferred']),
            'average_fill_time_days': random.randint(1, 14),
            'patient_satisfaction_score': round(random.uniform(3.0, 5.0), 1),
            'specialty_certified': pharmacy_type == 'Specialty'
        })
    return pd.DataFrame(pharmacies)

def generate_program_interactions(n_interactions=2500, patient_df=None):
    """Generate patient program interactions table"""
    programs = ['Patient Access', 'Prior Authorization', 'Copay Assistance', 'Adherence Support', 'Nurse Navigation']
    channels = ['Phone', 'Email', 'SMS', 'Portal', 'Mail']
    outcomes = ['Successful Contact', 'Left Voicemail', 'No Answer', 'Email Opened', 'Email Clicked', 'Responded', 'Unsubscribed']
    
    interactions = []
    for i in range(n_interactions):
        interaction_date = fake.date_between(start_date='-12m', end_date='today')
        channel = random.choice(channels)
        
        interactions.append({
            'interaction_id': f'INT{i+1:06d}',
            'patient_id': f'PAT{random.randint(1,500):05d}',
            'program_id': f'PGM{random.randint(1,20):02d}',
            'program_type': random.choice(programs),
            'interaction_date': interaction_date,
            'interaction_time': fake.time(),
            'channel': channel,
            'direction': random.choice(['Inbound', 'Outbound']),
            'outcome': random.choice(outcomes),
            'duration_minutes': random.randint(1, 45) if channel == 'Phone' else None,
            'notes': fake.text(max_nb_chars=200),
            'follow_up_required': random.choice([True, False]),
            'follow_up_date': fake.date_between(start_date=interaction_date, end_date='today') if random.choice([True, False]) else None,
            'staff_id': f'STF{random.randint(1,50):03d}'
        })
    return pd.DataFrame(interactions)

def generate_clinical_trials(n_trials=300, patient_df=None):
    """Generate clinical trials table"""
    trial_names = [
        'Phase III MS Drug Efficacy Study', 'Oncology Immunotherapy Trial', 
        'Rheumatoid Arthritis Biologics Study', 'Hepatitis C Treatment Protocol',
        'HIV Prevention Study', 'Psoriasis Topical Treatment Trial',
        'Crohns Disease Maintenance Study', 'Phase II Neurology Drug Trial',
        'Cardiovascular Prevention Study', 'Diabetes Management Protocol'
    ]
    
    sponsors = [
        'HealthTech Pharma Inc.', 'BioMed Research Corp', 'Clinical Solutions LLC',
        'Advanced Therapeutics', 'MedTrial Partners', 'Research Innovations Inc.'
    ]
    
    phases = ['I', 'II', 'III', 'IV']
    conditions = ['Multiple Sclerosis', 'Oncology', 'Rheumatoid Arthritis', 'Hepatitis C', 'HIV', 'Psoriasis', 'Crohns Disease']
    statuses = ['Enrolled', 'Active', 'Completed', 'Withdrawn', 'Screen Failure']
    arms = ['Placebo', 'Treatment A', 'Treatment B', 'Control', 'Low Dose', 'High Dose']
    outcomes = ['Improved', 'No Change', 'Deteriorated', 'N/A']
    
    trials = []
    for i in range(n_trials):
        enrollment_date = fake.date_between(start_date='-3y', end_date='-6m')
        status = random.choice(statuses)
        completion_date = None
        
        if status in ['Completed', 'Withdrawn']:
            completion_date = fake.date_between(start_date=enrollment_date, end_date='today')
        
        trials.append({
            'trial_id': f'CT{random.randint(1,50):03d}',
            'trial_name': random.choice(trial_names),
            'sponsor': random.choice(sponsors),
            'phase': random.choice(phases),
            'condition': random.choice(conditions),
            'patient_id': f'PAT{random.randint(1,500):05d}',
            'enrollment_date': enrollment_date,
            'site_id': f'SITE{random.randint(1,20):03d}',
            'status': status,
            'arm': random.choice(arms),
            'adverse_events_reported': random.randint(0, 5),
            'primary_outcome': random.choice(outcomes) if status == 'Completed' else 'N/A',
            'completion_date': completion_date
        })
    return pd.DataFrame(trials)

# Generate all datasets
print("Generating healthtech mock datasets...")

patients_df = generate_patients()
prescriptions_df = generate_prescriptions()
providers_df = generate_providers()
pharmacies_df = generate_pharmacies()
interactions_df = generate_program_interactions()
clinical_trials_df = generate_clinical_trials()

# Save all datasets
datasets = {
    'patients': patients_df,
    'prescriptions': prescriptions_df,
    'providers': providers_df,
    'pharmacies': pharmacies_df,
    'program_interactions': interactions_df,
    'clinical_trials': clinical_trials_df
}

# Save files and print information
for name, df in datasets.items():
    filename = f'healthtech_{name}_{date_suffix}.csv'
    filepath = os.path.join(output_dir, filename)
    df.to_csv(filepath, index=False)
    print(f"\nDataset: {name}")
    print(f"Number of records: {len(df)}")
    print(f"Columns: {df.columns.tolist()}")
    print(f"Sample data:")
    print(df.head(2).to_string())
    print(f"Saved to: {filepath}")

print(f"\nAll healthtech datasets have been generated and saved to '{output_dir}' directory!")