import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def create_insurance_datasets(num_records=500):
    """Create comprehensive insurance datasets for property claims, auto claims, and underwriting"""
    
    # Get current date for file naming
    current_date = datetime.now().strftime("%m-%d")
    
    # Create output directory
    output_dir = os.path.join("output", f"insurance_{current_date}")
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate base policyholder IDs to ensure consistency across datasets
    base_policyholders = [f'PH{np.random.randint(10000, 99999)}' for _ in range(int(num_records * 0.7))]
    
    # ===== ENHANCED PROPERTY CLAIMS DATASET =====
    def create_enhanced_property_claims():
        # Original property claims data structure
        loss_categories = ['Water Damage', 'Fire', 'Theft', 'Wind Damage', 'Hail Damage', 'Lightning Damage', 'Mold']
        loss_subcategories = {
            'Water Damage': ['Pipe Burst', 'Plumbing Leak', 'Appliance Leak', 'Sewer Backup', 'Roof Leak'],
            'Fire': ['Electrical Fire', 'Kitchen Fire', 'Heating Equipment', 'Wildfire', 'Arson'],
            'Theft': ['Burglary', 'Home Invasion', 'Package Theft', 'Vehicle Break-in'],
            'Wind Damage': ['Hurricane', 'Tornado', 'Severe Storm', 'Fallen Tree'],
            'Hail Damage': ['Roof Damage', 'Siding Damage', 'Window Damage', 'Vehicle Damage'],
            'Lightning Damage': ['Direct Strike', 'Power Surge', 'Fire from Strike'],
            'Mold': ['Water Intrusion', 'HVAC Related', 'Poor Ventilation']
        }
        
        # New additions for business questions
        property_types = ['Single Family Home', 'Condo', 'Townhouse', 'Commercial Building', 'Industrial', 'Apartment Complex']
        construction_types = ['Frame', 'Masonry', 'Steel', 'Concrete', 'Mixed']
        states = ['TX', 'FL', 'CA', 'NY', 'IL', 'GA', 'CO', 'WA', 'MA', 'NC']
        catastrophe_codes = ['', 'CAT2024001', 'CAT2024002', 'CAT2024003', 'CAT2025001']  # Empty for non-cat claims
        weather_perils = ['Clear', 'Rain', 'Wind', 'Hail', 'Snow', 'Hurricane', 'Tornado']
        
        data = {}
        
        # Original columns
        data['claim_id'] = [f'CLM{np.random.randint(100000, 999999)}' for _ in range(num_records)]
        data['policyholder_id'] = np.random.choice(base_policyholders + [f'PH{np.random.randint(10000, 99999)}' for _ in range(int(num_records * 0.3))], num_records)
        data['date_of_loss'] = [(datetime(2024, 1, 1) + timedelta(days=np.random.randint(0, 365))).strftime('%Y-%m-%d') for _ in range(num_records)]
        
        # Enhanced location data
        cities = ['Houston', 'Miami', 'Los Angeles', 'New York', 'Chicago', 'Atlanta', 'Denver', 'Seattle', 'Boston', 'Charlotte']
        selected_states = np.random.choice(states, num_records)
        selected_cities = np.random.choice(cities, num_records)
        zip_codes = [f'{np.random.randint(10000, 99999)}' for _ in range(num_records)]
        
        data['location_of_loss'] = [f'{np.random.randint(100, 999)} {np.random.choice(["Main", "Oak", "Elm", "Maple", "Pine"])} St, {selected_cities[i]}, {selected_states[i]}' for i in range(num_records)]
        data['location_state'] = selected_states
        data['location_zip'] = zip_codes
        
        # New property and construction data
        data['property_type'] = np.random.choice(property_types, num_records)
        data['construction_type'] = np.random.choice(construction_types, num_records)
        
        # Original loss categorization
        loss_category_list = np.random.choice(loss_categories, num_records)
        data['loss_category'] = loss_category_list
        data['loss_subcategory'] = [np.random.choice(loss_subcategories[category]) for category in loss_category_list]
        
        # Original failure analysis
        loss_mechanisms = ['Freezing', 'Overheating', 'Impact', 'Wear and Tear', 'Corrosion', 'Forced Entry', 'Electrical Surge', 'Mechanical Failure', 'Human Error']
        origins_of_failure = ['Faulty Installation', 'Aging Infrastructure', 'Manufacturer Defect', 'Poor Maintenance', 'Weather Event', 'Weak Security', 'Design Flaw']
        components = ['Pipe', 'Wiring', 'Roof', 'Appliance', 'HVAC System', 'Door/Window', 'Sprinkler System', 'Foundation', 'Siding', 'Plumbing Fixture']
        
        data['loss_mechanism'] = np.random.choice(loss_mechanisms, num_records)
        data['origin_of_failure'] = np.random.choice(origins_of_failure, num_records)
        data['component_of_failure'] = np.random.choice(components, num_records)
        data['sub_component_of_failure'] = [f'{comp} Component' for comp in data['component_of_failure']]
        data['manufacturer_brand'] = [f'Brand{np.random.randint(1, 10)}' for _ in range(num_records)]
        data['model_serial_number'] = [f'{brand[:2].upper()}-{np.random.randint(10000, 99999)}' for brand in data['manufacturer_brand']]
        
        # Enhanced financial data
        base_loss_amounts = np.random.lognormal(8, 1, num_records)  # More realistic distribution
        data['estimated_loss_amount'] = [max(1000, int(amount)) for amount in base_loss_amounts]
        data['policy_premium'] = [max(500, int(loss * np.random.uniform(0.02, 0.08))) for loss in data['estimated_loss_amount']]
        
        # Catastrophe and weather data
        data['catastrophe_code'] = np.random.choice(catastrophe_codes, num_records, p=[0.7, 0.075, 0.075, 0.075, 0.075])
        data['weather_peril'] = np.random.choice(weather_perils, num_records)
        
        # Original operational data
        data['adjuster_notes'] = [f'Property damage assessment for {cat}' for cat in data['loss_category']]
        data['subrogation_potential'] = np.random.choice(['Yes', 'No', 'Pending Review'], num_records, p=[0.3, 0.5, 0.2])
        data['subrogation_notes'] = ['Investigating potential recovery' if pot == 'Yes' else 'No recovery potential' for pot in data['subrogation_potential']]
        data['preventable_loss'] = np.random.choice(['Yes', 'No'], num_records)
        data['preventive_action'] = ['Regular maintenance recommended' for _ in range(num_records)]
        data['claim_status'] = np.random.choice(['Open', 'Closed', 'Pending', 'Under Investigation'], num_records)
        data['recovery_amount'] = [int(loss * np.random.uniform(0, 0.3)) if pot == 'Yes' else 0 for loss, pot in zip(data['estimated_loss_amount'], data['subrogation_potential'])]
        data['underwriting_impact'] = np.random.choice(['Yes', 'No'], num_records)
        
        return pd.DataFrame(data)
    
    # ===== AUTO CLAIMS DATASET =====
    def create_auto_claims():
        # Use subset of policyholders for multi-line customers
        auto_policyholders = np.random.choice(base_policyholders + [f'PH{np.random.randint(10000, 99999)}' for _ in range(int(num_records * 0.4))], num_records)
        
        # Generate driver ages first
        driver_ages = np.random.randint(16, 80, num_records)
        
        data = {
            'claim_id': [f'AUTO{np.random.randint(100000, 999999)}' for _ in range(num_records)],
            'policy_number': [f'AUTO-{np.random.randint(1000000, 9999999)}' for _ in range(num_records)],
            'policyholder_id': auto_policyholders,
            'date_of_loss': [(datetime(2024, 1, 1) + timedelta(days=np.random.randint(0, 365))).strftime('%Y-%m-%d') for _ in range(num_records)],
            'location_state': np.random.choice(['TX', 'FL', 'CA', 'NY', 'IL', 'GA', 'CO', 'WA', 'MA', 'NC'], num_records),
            'location_zip': [f'{np.random.randint(10000, 99999)}' for _ in range(num_records)],
            'driver_age': driver_ages,
            'driver_experience_years': [min(age - 16, np.random.randint(0, age - 15)) if age > 16 else 0 for age in driver_ages],
            'vehicle_year': np.random.randint(2010, 2025, num_records),
            'vehicle_make': np.random.choice(['Toyota', 'Honda', 'Ford', 'Chevrolet', 'BMW', 'Mercedes', 'Audi', 'Nissan'], num_records),
            'vehicle_model': np.random.choice(['Sedan', 'SUV', 'Truck', 'Coupe', 'Hatchback'], num_records),
            'vehicle_type': np.random.choice(['Personal', 'Commercial', 'Fleet'], num_records),
            'fault_percentage': np.random.choice([0, 25, 50, 75, 100], num_records, p=[0.3, 0.1, 0.2, 0.1, 0.3]),
            'coverage_type': np.random.choice(['Collision', 'Comprehensive', 'Liability', 'Uninsured Motorist'], num_records),
            'policy_premium': np.random.randint(800, 3000, num_records),
            'policy_limit': np.random.choice([25000, 50000, 100000, 250000, 500000], num_records),
            'estimated_loss_amount': np.random.randint(500, 25000, num_records),
            'total_paid': [int(est * np.random.uniform(0.8, 1.0)) for est in np.random.randint(500, 25000, num_records)],
            'claim_status': np.random.choice(['Open', 'Closed', 'Pending', 'Under Investigation'], num_records),
            'recovery_amount': [int(paid * np.random.uniform(0, 0.4)) if fault < 50 else 0 for paid, fault in zip(np.random.randint(500, 25000, num_records), np.random.choice([0, 25, 50, 75, 100], num_records))],
            'accident_type': np.random.choice(['Rear End', 'Side Impact', 'Head On', 'Single Vehicle', 'Parking Lot'], num_records),
            'injury_severity': np.random.choice(['None', 'Minor', 'Moderate', 'Severe'], num_records, p=[0.6, 0.25, 0.1, 0.05]),
            'litigation_flag': np.random.choice([0, 1], num_records, p=[0.85, 0.15])
        }
        
        return pd.DataFrame(data)
    
    # ===== UNDERWRITING DATASET =====
    def create_underwriting():
        # Use base policyholders to ensure overlap
        underwriting_policyholders = base_policyholders + [f'PH{np.random.randint(10000, 99999)}' for _ in range(int(num_records * 0.5))]
        
        data = {
            'policy_number': [f'POL-{np.random.randint(1000000, 9999999)}' for _ in range(num_records)],
            'policyholder_id': np.random.choice(underwriting_policyholders, num_records),
            'effective_date': [(datetime(2024, 1, 1) + timedelta(days=np.random.randint(0, 365))).strftime('%Y-%m-%d') for _ in range(num_records)],
            'expiration_date': [(datetime(2024, 1, 1) + timedelta(days=np.random.randint(365, 730))).strftime('%Y-%m-%d') for _ in range(num_records)],
            'line_of_business': np.random.choice(['Property', 'Auto', 'Multi-Line'], num_records, p=[0.4, 0.4, 0.2]),
            'property_type': np.random.choice(['Single Family Home', 'Condo', 'Townhouse', 'Commercial Building', 'Industrial'], num_records),
            'construction_type': np.random.choice(['Frame', 'Masonry', 'Steel', 'Concrete', 'Mixed'], num_records),
            'location_state': np.random.choice(['TX', 'FL', 'CA', 'NY', 'IL', 'GA', 'CO', 'WA', 'MA', 'NC'], num_records),
            'location_zip': [f'{np.random.randint(10000, 99999)}' for _ in range(num_records)],
            'territory_code': [f'T{np.random.randint(100, 999)}' for _ in range(num_records)],
            'industry_code': np.random.choice(['NAICS334', 'NAICS541', 'NAICS722', 'NAICS236', 'NAICS441'], num_records),
            'underwriting_tier': np.random.choice(['Preferred', 'Standard', 'Non-Standard'], num_records, p=[0.3, 0.5, 0.2]),
            'risk_score': np.random.randint(300, 850, num_records),
            'policy_premium': np.random.randint(500, 5000, num_records),
            'total_insured_value': np.random.randint(100000, 1000000, num_records),
            'prior_claims_count': np.random.choice([0, 1, 2, 3, 4, 5], num_records, p=[0.4, 0.25, 0.15, 0.1, 0.05, 0.05]),
            'years_with_prior_carrier': np.random.randint(0, 10, num_records),
            'distribution_channel': np.random.choice(['Agent', 'Broker', 'Direct', 'Online'], num_records),
            'broker_id': [f'BRK{np.random.randint(1000, 9999)}' for _ in range(num_records)],
            'renewal_flag': np.random.choice([0, 1], num_records, p=[0.3, 0.7]),
            'retention_flag': np.random.choice([0, 1], num_records, p=[0.2, 0.8]),
            'rate_change_percent': np.random.uniform(-0.15, 0.25, num_records),
            'premium_change_percent': np.random.uniform(-0.20, 0.30, num_records)
        }
        
        return pd.DataFrame(data)
    
    # Create all datasets
    print("Creating enhanced property claims dataset...")
    property_df = create_enhanced_property_claims()
    property_file = os.path.join(output_dir, f"insurance__property_claims_{current_date}.csv")
    property_df.to_csv(property_file, index=False)
    
    print("Creating auto claims dataset...")
    auto_df = create_auto_claims()
    auto_file = os.path.join(output_dir, f"insurance__auto_claims_{current_date}.csv")
    auto_df.to_csv(auto_file, index=False)
    
    print("Creating underwriting dataset...")
    underwriting_df = create_underwriting()
    underwriting_file = os.path.join(output_dir, f"insurance__underwriting_{current_date}.csv")
    underwriting_df.to_csv(underwriting_file, index=False)
    
    # Create summary report
    summary = {
        'Dataset': ['Property Claims', 'Auto Claims', 'Underwriting'],
        'Records': [len(property_df), len(auto_df), len(underwriting_df)],
        'Columns': [len(property_df.columns), len(auto_df.columns), len(underwriting_df.columns)],
        'File': [property_file, auto_file, underwriting_file]
    }
    
    # summary_df = pd.DataFrame(summary)
    # summary_file = os.path.join(output_dir, f"dataset_summary_{current_date}.csv")
    # summary_df.to_csv(summary_file, index=False)
    
    print(f"\n=== INSURANCE DATASETS CREATED ===")
    print(f"Output directory: {output_dir}")
    print(f"Property Claims: {len(property_df)} records, {len(property_df.columns)} columns")
    print(f"Auto Claims: {len(auto_df)} records, {len(auto_df.columns)} columns") 
    print(f"Underwriting: {len(underwriting_df)} records, {len(underwriting_df.columns)} columns")
    print(f"\nOverlapping policyholders: {len(set(property_df['policyholder_id']) & set(auto_df['policyholder_id']) & set(underwriting_df['policyholder_id']))}")
    
    print("\n=== KEY BUSINESS QUESTIONS SUPPORTED ===")
    print("✅ Property: Loss ratios by property type and construction")
    print("✅ Property: Claims frequency/severity by catastrophe zone")
    print("✅ Auto: Claim costs by driver age/experience and vehicle type")
    print("✅ Auto: Fault percentage vs total claim costs by coverage")
    print("✅ Underwriting: Tier/risk score correlation with loss performance")
    print("✅ Underwriting: Retention and premium growth by segment/channel")
    
    return {
        'property_claims': property_df,
        'auto_claims': auto_df, 
        'underwriting': underwriting_df,
        'files': [property_file, auto_file, underwriting_file] # summary_file
    }

# Execute the function
if __name__ == "__main__":
    datasets = create_insurance_datasets(500)
    
    # Display sample data
    print("\n=== SAMPLE DATA ===")
    print("\nProperty Claims Sample:")
    print(datasets['property_claims'].head(3))
    print(f"\nProperty Claims Columns: {list(datasets['property_claims'].columns)}")
    
    print("\nAuto Claims Sample:")
    print(datasets['auto_claims'].head(3))
    
    print("\nUnderwriting Sample:")
    print(datasets['underwriting'].head(3))