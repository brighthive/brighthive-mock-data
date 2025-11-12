import pandas as pd
import numpy as np
import random
from faker import Faker
import os
from datetime import datetime

# Initialize Faker
fake = Faker()

# Define paths
script_dir = os.getcwd()  # Current working directory in this environment
output_dir = os.path.join(script_dir, "output/many_columns")

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

print("Starting generation of 15 tables with 500 columns each...")
print("5 Gene Expression datasets, 5 Trading datasets, 5 IoT datasets")

# Configuration
n_columns = 500
current_date = datetime.now()

# Function to generate gene expression data
def generate_gene_expression_data(dataset_num):
    print(f"Generating Gene Expression Dataset {dataset_num}...")
    
    n_samples = random.randint(300, 800)  # Vary sample sizes
    
    # Generate sample metadata
    sample_ids = [f"SAMPLE_{dataset_num}_{i:04d}" for i in range(1, n_samples + 1)]
    patient_ages = np.random.randint(18, 80, n_samples)
    genders = np.random.choice(['Male', 'Female'], n_samples)
    conditions = np.random.choice(['Control', 'Disease_A', 'Disease_B', 'Disease_C'], n_samples)
    
    # Generate gene expression data (log-normalized counts)
    gene_names = [f"GENE_{dataset_num}_{i:03d}" for i in range(1, n_columns + 1)]
    expression_data = np.random.lognormal(mean=2, sigma=1, size=(n_samples, n_columns))
    
    # Create DataFrame
    gene_expression_df = pd.DataFrame(expression_data, columns=gene_names)
    gene_expression_df.insert(0, 'Sample_ID', sample_ids)
    gene_expression_df.insert(1, 'Age', patient_ages)
    gene_expression_df.insert(2, 'Gender', genders)
    gene_expression_df.insert(3, 'Condition', conditions)
    
    # Save dataset
    file_name = f"gene_expression_data_{dataset_num}_{current_date.strftime('%m-%d')}.csv"
    output_path = os.path.join(output_dir, file_name)
    gene_expression_df.to_csv(output_path, index=False)
    print(f"  Saved: {file_name} (Shape: {gene_expression_df.shape})")
    return output_path

# Function to generate trading data
def generate_trading_data(dataset_num):
    print(f"Generating Trading Dataset {dataset_num}...")
    
    n_timestamps = random.randint(500, 1200)  # Vary time points
    
    # Generate timestamp data
    timestamps = pd.date_range(start='2024-01-01 09:30:00', periods=n_timestamps, freq='1min')
    
    # Generate feature names (price movements, technical indicators, etc.)
    feature_names = []
    for i in range(1, n_columns + 1):
        feature_type = random.choice(['price_change', 'volume_ratio', 'volatility', 'momentum', 'rsi', 'macd', 'bollinger'])
        feature_names.append(f"{feature_type}_{dataset_num}_{i:03d}")
    
    # Generate trading feature data
    trading_data = np.random.normal(0, 1, size=(n_timestamps, n_columns))
    
    # Create DataFrame
    trading_df = pd.DataFrame(trading_data, columns=feature_names)
    trading_df.insert(0, 'Timestamp', timestamps)
    trading_df.insert(1, 'Market_Session', np.random.choice(['Pre_Market', 'Regular', 'After_Hours'], n_timestamps))
    trading_df.insert(2, 'Trading_Volume', np.random.randint(1000000, 10000000, n_timestamps))
    
    # Save dataset
    file_name = f"trading_features_data_{dataset_num}_{current_date.strftime('%m-%d')}.csv"
    output_path = os.path.join(output_dir, file_name)
    trading_df.to_csv(output_path, index=False)
    print(f"  Saved: {file_name} (Shape: {trading_df.shape})")
    return output_path

# Function to generate IoT sensor data
def generate_iot_data(dataset_num):
    print(f"Generating IoT Dataset {dataset_num}...")
    
    n_readings = random.randint(400, 1000)  # Vary readings
    
    # Generate reading metadata
    reading_times = pd.date_range(start='2024-01-01', periods=n_readings, freq='5min')
    facility_ids = np.random.choice([f'FACILITY_{dataset_num}_{i}' for i in range(1, 6)], n_readings)
    weather_conditions = np.random.choice(['Clear', 'Cloudy', 'Rainy', 'Snowy', 'Foggy'], n_readings)
    
    # Generate sensor names
    sensor_names = []
    sensor_types = ['temperature', 'humidity', 'pressure', 'vibration', 'light', 'sound', 'air_quality', 'motion', 'co2', 'noise']
    for i in range(1, n_columns + 1):
        sensor_type = random.choice(sensor_types)
        location = random.choice(['floor_1', 'floor_2', 'floor_3', 'basement', 'roof', 'parking', 'lobby'])
        sensor_names.append(f"{sensor_type}_{location}_{dataset_num}_{i:03d}")
    
    # Generate sensor readings
    sensor_data = np.random.normal(50, 15, size=(n_readings, n_columns))
    # Add some realistic constraints
    sensor_data = np.clip(sensor_data, 0, 100)  # Keep values between 0-100
    
    # Create DataFrame
    sensor_df = pd.DataFrame(sensor_data, columns=sensor_names)
    sensor_df.insert(0, 'Reading_Time', reading_times)
    sensor_df.insert(1, 'Facility_ID', facility_ids)
    sensor_df.insert(2, 'Weather_Condition', weather_conditions)
    sensor_df.insert(3, 'System_Status', np.random.choice(['Normal', 'Warning', 'Alert', 'Maintenance'], n_readings))
    
    # Save dataset
    file_name = f"iot_sensor_data_{dataset_num}_{current_date.strftime('%m-%d')}.csv"
    output_path = os.path.join(output_dir, file_name)
    sensor_df.to_csv(output_path, index=False)
    print(f"  Saved: {file_name} (Shape: {sensor_df.shape})")
    return output_path

# Generate all datasets
created_files = []

# Generate 5 Gene Expression datasets
print("\n=== GENE EXPRESSION DATASETS ===")
for i in range(1, 6):
    file_path = generate_gene_expression_data(i)
    created_files.append(file_path)

# Generate 5 Trading datasets
print("\n=== TRADING DATASETS ===")
for i in range(1, 6):
    file_path = generate_trading_data(i)
    created_files.append(file_path)

# Generate 5 IoT datasets
print("\n=== IOT SENSOR DATASETS ===")
for i in range(1, 6):
    file_path = generate_iot_data(i)
    created_files.append(file_path)

# Summary
print(f"\n=== SUMMARY ===")
print(f"Generated 15 tables with 500 columns each:")
print(f"- 5 Gene Expression datasets")
print(f"- 5 Trading datasets") 
print(f"- 5 IoT Sensor datasets")
print(f"\nAll files saved to: {output_dir}")

# List all created files
print(f"\nCreated files:")
for file_path in created_files:
    print(f"- {os.path.basename(file_path)}")