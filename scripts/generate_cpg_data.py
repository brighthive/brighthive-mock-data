"""
CPG RETAIL - COVID IMPACT SYNTHETIC DATASET GENERATOR
======================================================
Generates realistic CPG sales data with COVID-19 business trends (2019-2025)

INJECTED TRENDS:
1. Channel Whiplash: eCommerce surge, Convenience collapse, then stabilization
2. Premiumization Ratchet: Organic/natural products grow 15% → 33%
3. Out-of-Stock Crisis: Supply chain disruption causes market share shift

Dataset follows minimal star schema:
- sales_fact (transactions)
- stores (dimension)
- products (dimension)

Data Coverage: 2019-2025 (through December 2025)
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def create_cpg_covid_dataset(num_weekly_records=100000):
    """
    Generate CPG retail dataset with COVID trends
    
    Args:
        num_weekly_records: Number of weekly sales records to generate
    """
    
    np.random.seed(42)
    current_date = datetime.now().strftime("%Y-%m-%d")
    output_dir = os.path.join("output", f"cpg_{current_date}")
    os.makedirs(output_dir, exist_ok=True)
    
    # ===== TREND PARAMETERS =====
    
    # Trend 1: Channel distribution by year
    channel_trends = {
        2019: {'eCommerce': 0.03, 'MULO': 0.52, 'Natural': 0.15, 'Convenience': 0.18, 'Club': 0.12},
        2020: {'eCommerce': 0.15, 'MULO': 0.60, 'Natural': 0.08, 'Convenience': 0.07, 'Club': 0.10},
        2021: {'eCommerce': 0.14, 'MULO': 0.54, 'Natural': 0.12, 'Convenience': 0.10, 'Club': 0.10},
        2022: {'eCommerce': 0.13, 'MULO': 0.52, 'Natural': 0.13, 'Convenience': 0.12, 'Club': 0.10},
        2023: {'eCommerce': 0.12, 'MULO': 0.51, 'Natural': 0.14, 'Convenience': 0.13, 'Club': 0.10},
        2024: {'eCommerce': 0.11, 'MULO': 0.50, 'Natural': 0.15, 'Convenience': 0.14, 'Club': 0.10},
        2025: {'eCommerce': 0.11, 'MULO': 0.50, 'Natural': 0.15, 'Convenience': 0.14, 'Club': 0.10}
    }
    
    # Trend 2: Premiumization metrics by year
    premium_trends = {
        2019: {'organic_pct': 0.15, 'avg_price': 5.20, 'premium_volume_pct': 0.22},
        2020: {'organic_pct': 0.23, 'avg_price': 5.50, 'premium_volume_pct': 0.31},
        2021: {'organic_pct': 0.23, 'avg_price': 5.80, 'premium_volume_pct': 0.33},
        2022: {'organic_pct': 0.26, 'avg_price': 6.20, 'premium_volume_pct': 0.35},
        2023: {'organic_pct': 0.29, 'avg_price': 6.40, 'premium_volume_pct': 0.36},
        2024: {'organic_pct': 0.31, 'avg_price': 6.60, 'premium_volume_pct': 0.37},
        2025: {'organic_pct': 0.33, 'avg_price': 6.80, 'premium_volume_pct': 0.38}
    }
    
    # Trend 3: Out-of-stock rates by year
    oos_trends = {
        2019: 0.02,
        2020: 0.05,
        2021: 0.18,  # Peak crisis
        2022: 0.08,
        2023: 0.03,
        2024: 0.02,
        2025: 0.02
    }
    
    # Brand market share evolution (Top 3 vs Challengers)
    brand_share_trends = {
        2019: {'top3': 0.72, 'challengers': 0.28},
        2020: {'top3': 0.68, 'challengers': 0.32},
        2021: {'top3': 0.63, 'challengers': 0.37},
        2022: {'top3': 0.64, 'challengers': 0.36},
        2023: {'top3': 0.63, 'challengers': 0.37},
        2024: {'top3': 0.62, 'challengers': 0.38},
        2025: {'top3': 0.62, 'challengers': 0.38}
    }
    
    # ===== STORE MASTER DATA =====
    
    print("Creating store master data...")
    
    retailers = {
        'Whole Foods': {'channel': 'Natural', 'count': 500, 'avg_velocity': 420},
        'Kroger': {'channel': 'MULO', 'count': 2800, 'avg_velocity': 280},
        'Walmart': {'channel': 'MULO', 'count': 4700, 'avg_velocity': 350},
        'Target': {'channel': 'MULO', 'count': 1900, 'avg_velocity': 310},
        'Costco': {'channel': 'Club', 'count': 580, 'avg_velocity': 850},
        "Sam's Club": {'channel': 'Club', 'count': 600, 'avg_velocity': 720},
        'Sprouts': {'channel': 'Natural', 'count': 380, 'avg_velocity': 320},
        '7-Eleven': {'channel': 'Convenience', 'count': 9500, 'avg_velocity': 85},
        'Circle K': {'channel': 'Convenience', 'count': 7200, 'avg_velocity': 75},
        'Amazon Fresh': {'channel': 'eCommerce', 'count': 1, 'avg_velocity': 12000},
        'Instacart': {'channel': 'eCommerce', 'count': 1, 'avg_velocity': 15000}
    }
    
    states = ['CA', 'TX', 'FL', 'NY', 'PA', 'IL', 'OH', 'GA', 'NC', 'MI', 
              'WA', 'AZ', 'MA', 'TN', 'IN', 'MO', 'WI', 'CO', 'OR', 'VA']
    
    stores = []
    store_id = 1
    
    for retailer_name, config in retailers.items():
        for i in range(config['count']):
            stores.append({
                'store_id': f'STR{store_id:06d}',
                'retailer_name': retailer_name,
                'channel': config['channel'],
                'state': np.random.choice(states),
                'dma': f"DMA_{np.random.randint(1, 210)}",
                'region': np.random.choice(['Northeast', 'Southeast', 'Midwest', 'West', 'Southwest']),
                'zip_code': f"{np.random.randint(10000, 99999)}",
                'base_velocity': config['avg_velocity']
            })
            store_id += 1
    
    stores_df = pd.DataFrame(stores)
    
    # ===== PRODUCT MASTER DATA =====
    
    print("Creating product master data...")
    
    # Define product attributes and their characteristics
    product_types = [
        # Category, Base Price Range, Has Organic Option, Package Sizes
        ('Yogurt', (3.5, 7.5), True, ['6oz', '32oz', '5.3oz 4-pack']),
        ('Granola', (4.0, 9.0), True, ['12oz', '16oz', '24oz']),
        ('Protein Bars', (8.0, 18.0), True, ['Box of 5', 'Box of 12', 'Single']),
        ('Kombucha', (3.0, 5.5), True, ['16oz', '32oz', '12oz 4-pack']),
        ('Nut Butter', (6.0, 14.0), True, ['16oz', '28oz', '12oz']),
        ('Plant-Based Milk', (3.5, 6.5), True, ['32oz', '64oz', 'Half Gallon']),
        ('Energy Drinks', (2.5, 4.5), False, ['12oz', '16oz', '8oz 4-pack']),
        ('Chips', (2.5, 6.0), True, ['5oz', '10oz', '1oz Single-serve']),
        ('Frozen Meals', (4.0, 8.5), True, ['10oz', '16oz', '24oz Family']),
        ('Hummus', (3.5, 7.0), True, ['8oz', '16oz', '32oz']),
    ]
    
    brands = {
        'top3': ['BrandLeader', 'MegaBrand', 'MarketKing'],
        'challengers': ['RisingStar', 'HealthFirst', 'EcoChoice', 'PureNature', 
                       'GreenValley', 'OrganicPro', 'FreshStart']
    }
    
    products = []
    item_id = 1000
    
    for category, price_range, has_organic, package_sizes in product_types:
        # Create conventional products
        for brand_tier in ['top3', 'challengers']:
            for brand in brands[brand_tier]:
                for package in package_sizes:
                    # Conventional version
                    base_price = np.random.uniform(*price_range)
                    
                    products.append({
                        'item_id': f'ITM{item_id:06d}',
                        'upc': f"{np.random.randint(100000000000, 999999999999)}",
                        'product_name': f'{brand} {category} {package}',
                        'brand_name': brand,
                        'brand_tier': brand_tier,
                        'category_name': category,
                        'package_size': package,
                        'attributes': '',
                        'is_organic': False,
                        'is_premium': base_price > 8.0,
                        'base_price_2019': base_price,
                        'launch_date': f"20{np.random.randint(15, 20)}-{np.random.randint(1, 13):02d}-01"
                    })
                    item_id += 1
                    
                    # Organic version if applicable
                    if has_organic and np.random.random() < 0.6:  # 60% of products have organic variant
                        organic_price = base_price * 1.35  # Organic premium
                        
                        products.append({
                            'item_id': f'ITM{item_id:06d}',
                            'upc': f"{np.random.randint(100000000000, 999999999999)}",
                            'product_name': f'{brand} Organic {category} {package}',
                            'brand_name': brand,
                            'brand_tier': brand_tier,
                            'category_name': category,
                            'package_size': package,
                            'attributes': 'Organic',
                            'is_organic': True,
                            'is_premium': True,
                            'base_price_2019': organic_price,
                            'launch_date': f"20{np.random.randint(17, 21)}-{np.random.randint(1, 13):02d}-01"
                        })
                        item_id += 1
    
    products_df = pd.DataFrame(products)
    
    # ===== GENERATE SALES FACT TABLE =====
    
    print(f"Generating {num_weekly_records:,} weekly sales records with COVID trends...")
    
    sales_records = []
    
    # Distribute records across years (more weight on recent years)
    year_weights = {
        2019: 0.14,
        2020: 0.16,
        2021: 0.18,
        2022: 0.20,
        2023: 0.22,
        2024: 0.10  # Partial year
    }
    
    for _ in range(num_weekly_records):
        # Select year with weights
        year = np.random.choice(list(year_weights.keys()), p=list(year_weights.values()))
        
        # Generate week
        if year == 2024:
            week = np.random.randint(1, 48)  # Up to week 47 (late Nov)
        else:
            week = np.random.randint(1, 53)
        
        week_date = datetime(year, 1, 1) + timedelta(weeks=week)
        
        # Get year-specific trends
        channel_dist = channel_trends[year]
        premium_params = premium_trends[year]
        oos_rate = oos_trends[year]
        brand_shares = brand_share_trends[year]
        
        # Select channel based on year-specific distribution
        channel = np.random.choice(
            list(channel_dist.keys()), 
            p=list(channel_dist.values())
        )
        
        # Select store from that channel
        channel_stores = stores_df[stores_df['channel'] == channel]
        store = channel_stores.sample(1).iloc[0]
        
        # Select brand tier based on market share trends
        brand_tier = np.random.choice(
            ['top3', 'challengers'],
            p=[brand_shares['top3'], brand_shares['challengers']]
        )
        
        # Select product (bias toward organic based on year)
        if np.random.random() < premium_params['organic_pct']:
            # Select organic product
            eligible_products = products_df[
                (products_df['is_organic'] == True) & 
                (products_df['brand_tier'] == brand_tier)
            ]
        else:
            # Select conventional product
            eligible_products = products_df[
                (products_df['is_organic'] == False) & 
                (products_df['brand_tier'] == brand_tier)
            ]
        
        if len(eligible_products) == 0:
            eligible_products = products_df[products_df['brand_tier'] == brand_tier]
        
        product = eligible_products.sample(1).iloc[0]
        
        # Check if out of stock (Trend 3)
        in_distribution = np.random.random() > oos_rate
        
        if not in_distribution:
            # Out of stock - record zero sales
            dollar_sales = 0
            unit_sales = 0
            base_dollar_sales = 0
            promo_dollar_sales = 0
            avg_retail_price = 0
            on_promotion = False
        else:
            # Calculate price with year inflation
            price_multiplier = premium_params['avg_price'] / 5.20  # vs 2019 baseline
            avg_retail_price = product['base_price_2019'] * price_multiplier
            
            # Add price variance
            avg_retail_price *= np.random.uniform(0.95, 1.05)
            avg_retail_price = round(avg_retail_price, 2)
            
            # Determine if on promotion (varies by channel)
            promo_rates = {
                'MULO': 0.35,
                'Natural': 0.18,
                'Convenience': 0.28,
                'Club': 0.12,
                'eCommerce': 0.25
            }
            on_promotion = np.random.random() < promo_rates.get(channel, 0.25)
            
            # Calculate unit sales based on velocity
            base_velocity = store['base_velocity']
            
            # Apply channel-specific modifiers
            if channel == 'eCommerce':
                base_velocity *= np.random.uniform(0.8, 1.5)  # High variance online
            elif channel == 'Club':
                base_velocity *= np.random.uniform(1.2, 1.8)  # Bulk purchases
            
            # COVID volume adjustment by year
            year_volume_multipliers = {
                2019: 1.00,
                2020: 1.35,  # Panic buying
                2021: 1.18,  # Sustained
                2022: 1.04,  # Correction
                2023: 1.08,
                2024: 1.10
            }
            
            unit_sales = int(base_velocity * year_volume_multipliers[year] * np.random.uniform(0.3, 2.0))
            unit_sales = max(1, unit_sales)
            
            # Calculate dollar sales
            if on_promotion:
                promo_discount = np.random.uniform(0.15, 0.30)
                promo_price = avg_retail_price * (1 - promo_discount)
                promo_lift = np.random.uniform(1.3, 2.0)  # Promo increases units
                
                promo_units = int(unit_sales * 0.7 * promo_lift)  # 70% of sales on promo
                base_units = unit_sales - promo_units
                
                base_dollar_sales = base_units * avg_retail_price
                promo_dollar_sales = promo_units * promo_price
                dollar_sales = base_dollar_sales + promo_dollar_sales
            else:
                base_dollar_sales = unit_sales * avg_retail_price
                promo_dollar_sales = 0
                dollar_sales = base_dollar_sales
            
            dollar_sales = round(dollar_sales, 2)
            base_dollar_sales = round(base_dollar_sales, 2)
            promo_dollar_sales = round(promo_dollar_sales, 2)
        
        sales_records.append({
            'store_id': store['store_id'],
            'item_id': product['item_id'],
            'week_ending_date': week_date.strftime('%Y-%m-%d'),
            'dollar_sales': dollar_sales,
            'unit_sales': unit_sales,
            'base_dollar_sales': base_dollar_sales,
            'promo_dollar_sales': promo_dollar_sales,
            'average_retail_price': avg_retail_price,
            'in_distribution': in_distribution,
            'on_promotion': on_promotion
        })
    
    sales_df = pd.DataFrame(sales_records)
    
    # ===== SAVE FILES =====
    
    print("\nSaving tables...")
    
    prefix = f"cpg__"
    stores_file = os.path.join(output_dir, f"{prefix}stores.csv")
    products_file = os.path.join(output_dir, f"{prefix}products.csv")
    sales_file = os.path.join(output_dir, f"{prefix}sales.csv")
    
    stores_df.to_csv(stores_file, index=False)
    products_df.to_csv(products_file, index=False)
    sales_df.to_csv(sales_file, index=False)
    
    # ===== VALIDATION & ANALYSIS =====
    
    print(f"\n{'='*70}")
    print(f"  CPG COVID TRENDS DATASET GENERATED")
    print(f"{'='*70}")
    print(f"Output Directory: {output_dir}")
    print(f"\n📊 TABLES CREATED:")
    print(f"  1. sales_fact.csv  : {len(sales_df):,} rows × {len(sales_df.columns)} columns (FACT TABLE)")
    print(f"  2. stores.csv      : {len(stores_df):,} rows × {len(stores_df.columns)} columns")
    print(f"  3. products.csv    : {len(products_df):,} rows × {len(products_df.columns)} columns")
    
    # Add year column for analysis
    sales_df['year'] = pd.to_datetime(sales_df['week_ending_date']).dt.year
    
    # Merge with store and product data for analysis
    analysis_df = sales_df.merge(stores_df, on='store_id').merge(products_df, on='item_id')
    
    print(f"\n{'='*70}")
    print(f"  TREND VALIDATION")
    print(f"{'='*70}")
    
    # TREND 1: Channel distribution by year
    print("\n📊 TREND 1: Channel Whiplash (Sales % by Channel)")
    channel_by_year = analysis_df.groupby(['year', 'channel'])['dollar_sales'].sum().unstack(fill_value=0)
    channel_pct = channel_by_year.div(channel_by_year.sum(axis=1), axis=0) * 100
    print(channel_pct.round(1).to_string())
    
    # TREND 2: Premiumization
    print("\n🌿 TREND 2: Premiumization Ratchet")
    organic_sales = analysis_df.groupby(['year', 'is_organic'])['dollar_sales'].sum().unstack(fill_value=0)
    organic_pct = organic_sales[True] / (organic_sales[True] + organic_sales[False]) * 100
    avg_price_by_year = analysis_df[analysis_df['dollar_sales'] > 0].groupby('year')['average_retail_price'].mean()
    
    premium_summary = pd.DataFrame({
        'Organic % of Sales': organic_pct,
        'Avg Retail Price': avg_price_by_year
    })
    print(premium_summary.round(2).to_string())
    
    # TREND 3: Out-of-stock rates
    print("\n📦 TREND 3: Out-of-Stock Crisis")
    oos_by_year = analysis_df.groupby('year')['in_distribution'].apply(lambda x: (1 - x.mean()) * 100)
    print("Distribution Voids % by Year:")
    print(oos_by_year.round(1).to_string())
    
    # Brand share evolution
    print("\n🏆 Brand Market Share Evolution")
    brand_sales = analysis_df.groupby(['year', 'brand_tier'])['dollar_sales'].sum().unstack(fill_value=0)
    brand_share = brand_sales.div(brand_sales.sum(axis=1), axis=0) * 100
    print(brand_share.round(1).to_string())
    
    print(f"\n{'='*70}")
    print(f"  ✅ DATASET READY FOR PIPELINE TESTING")
    print(f"{'='*70}")
    
    print("\n🎯 Key Questions Your Agent Should Answer:")
    print("1. Which channel grew most during COVID? (Answer: eCommerce 3% → 15%)")
    print("2. When did out-of-stocks peak? (Answer: 2021 at 18%)")
    print("3. Did organic products maintain COVID gains? (Answer: Yes, 15% → 31%)")
    print("4. Which brands gained share? (Answer: Challengers 28% → 37%)")
    print("5. What happened to pricing? (Answer: +25% from 2019 to 2024)")
    
    return {
        'sales_fact': sales_df,
        'stores': stores_df,
        'products': products_df
    }


# Execute
if __name__ == "__main__":
    # MODIFY THIS NUMBER to change dataset size
    NUM_RECORDS = 100000  # 100K weekly sales records
    
    tables = create_cpg_covid_dataset(NUM_RECORDS)
    
    print("\n\n" + "="*70)
    print("  SAMPLE DATA FROM EACH TABLE")
    print("="*70)
    
    print("\n🏪 STORES (first 5 rows):")
    print(tables['stores'].head(5).to_string(index=False))
    
    print("\n\n📦 PRODUCTS (first 5 rows):")
    print(tables['products'].head(5).to_string(index=False))
    
    print("\n\n💰 SALES FACT TABLE (first 5 rows):")
    print(tables['sales_fact'].head(5).to_string(index=False))