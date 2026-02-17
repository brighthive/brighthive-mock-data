"""
BRIGHT CHEESE MANUFACTURING - COMPREHENSIVE BUSINESS TRENDS DATASET
=====================================================================
Company: Bright Cheese Manufacturing (2020-2025)
Records: ~75,000 orders across 5+ years

INJECTED TRENDS:
================
PRIMARY TRENDS:
1. 2021 COVID Crisis: -35% revenue drop, supply chain disruption
2. 2024 Recovery Surge: +40% above 2020 baseline, record performance
3. Product Category Shift: Fresh cheeses +45% (2020-2024), Aged cheeses -15%

OPERATIONAL TRENDS:
- Production times: Fresh (2d), Soft/Semi-soft (4-5d), Hard/Aged (8d)
- Rush orders: 3.6% expedited with same/next-day production start
- Payment behavior: Distributors 33d, Restaurants 38d (18 chronic late payers), Manufacturers 37d
- Seasonal effects: Summer +1-2d production time, Nov-Dec holiday delays
- Premium customer concentration: Top tier generates 40-50% of margin
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def create_cheese_manufacturing_dataset(num_records=75000):
    """Generate Bright Cheese Manufacturing dataset with business trends"""
    
    np.random.seed(42)
    current_date = datetime.now().strftime("%m-%d")
    output_dir = os.path.join("output", f"bright_cheese_manufacturing_{current_date}")
    os.makedirs(output_dir, exist_ok=True)
    
    # ===== MASTER DATA SETUP =====
    
    # Cheese categories with production characteristics
    cheese_data = {
        'Fresh': {
            'products': ['Fresh Mozzarella', 'Ricotta', 'Fresh Goat Cheese', 'Cottage Cheese', 'Cream Cheese'],
            'production_days': 2,
            'shelf_life_days': 21,
            'base_price_range': (4.50, 8.00),
            'growth_multiplier_2024': 1.60  # +60% growth (stronger trend)
        },
        'Soft/Semi-Soft': {
            'products': ['Gorgonzola', 'Feta', 'Aged Goat Cheese', 'Brie', 'Camembert'],
            'production_days': 4.5,
            'shelf_life_days': 45,
            'base_price_range': (6.00, 12.00),
            'growth_multiplier_2024': 1.08  # Slight growth
        },
        'Hard/Aged': {
            'products': ['Parmesan', 'Aged Cheddar', 'Swiss', 'Aged Provolone', 'Romano'],
            'production_days': 8,
            'shelf_life_days': 180,
            'base_price_range': (8.00, 18.00),
            'growth_multiplier_2024': 0.70  # -30% decline (stronger trend)
        },
        'Blue': {
            'products': ['Blue Cheese', 'Stilton', 'Roquefort'],
            'production_days': 5,
            'shelf_life_days': 60,
            'base_price_range': (9.00, 15.00),
            'growth_multiplier_2024': 0.95  # Slight decline
        },
        'Specialty': {
            'products': ['Burrata', 'Mascarpone', 'Gouda', 'Gruyere'],
            'production_days': 6,
            'shelf_life_days': 90,
            'base_price_range': (10.00, 22.00),
            'growth_multiplier_2024': 1.15  # Premium growth
        }
    }
    
    # Build product master
    products = []
    for category, data in cheese_data.items():
        for product in data['products']:
            products.append({
                'category': category,
                'product_name': product,
                'production_days': data['production_days'],
                'shelf_life_days': data['shelf_life_days'],
                'base_price_range': data['base_price_range'],
                'growth_multiplier': data['growth_multiplier_2024']
            })
    
    # Package sizes and formats
    package_sizes = ['5 LB', '10 LB', '20 LB', '40 LB', '2.5 LB']
    package_weights = [0.25, 0.35, 0.25, 0.10, 0.05]
    
    cheese_formats = ['Block', 'Wheel', 'Shredded', 'Sliced', 'Crumbled']
    
    # Customer types with payment behavior
    customer_types = {
        'Distributor': {
            'count': 100,
            'payment_terms': 'Net 30',
            'avg_days_to_pay': 33,
            'late_probability': 0.05,
            'order_frequency': 'high',
            'tier_distribution': [0.10, 0.25, 0.40, 0.25]  # Platinum, Gold, Silver, Bronze
        },
        'Restaurant': {
            'count': 180,
            'payment_terms': 'Net 45',
            'avg_days_to_pay': 38,
            'late_probability': 0.25,  # 25% are chronic late payers
            'order_frequency': 'medium',
            'tier_distribution': [0.05, 0.15, 0.35, 0.45]
        },
        'Manufacturer': {
            'count': 70,
            'payment_terms': 'Net 30',
            'avg_days_to_pay': 37,
            'late_probability': 0.08,
            'order_frequency': 'high',
            'tier_distribution': [0.15, 0.30, 0.35, 0.20]
        }
    }
    
    # US States (focus on Midwest/Great Lakes but national reach)
    states = ['IL', 'WI', 'MI', 'OH', 'IN', 'MN', 'IA', 'MO', 'NY', 'PA', 'CA', 'TX', 'FL', 'NC', 'GA']
    state_weights = [0.18, 0.15, 0.12, 0.10, 0.08, 0.06, 0.05, 0.04, 0.05, 0.04, 0.05, 0.03, 0.02, 0.02, 0.01]
    
    # Production facilities
    facilities = [
        {'code': 'BCM-01', 'name': 'Bright Cheese - Green Bay, WI'},
        {'code': 'BCM-02', 'name': 'Bright Cheese - Madison, WI'},
        {'code': 'BCM-03', 'name': 'Bright Cheese - Chicago, IL'},
        {'code': 'BCM-04', 'name': 'Bright Cheese - Milwaukee, WI'}
    ]
    
    # Sales channels
    sales_channels = ['Direct Sales', 'Broker', 'Online Portal', 'Trade Show', 'Sales Rep']
    channel_weights = [0.45, 0.25, 0.15, 0.05, 0.10]
    
    # Freight methods
    freight_methods = ['Refrigerated LTL', 'Refrigerated FTL', 'Express Refrigerated', 'Standard LTL']
    freight_weights = [0.45, 0.35, 0.15, 0.05]
    
    # ===== GENERATE CUSTOMER MASTER =====
    customers = []
    customer_id = 1000
    chronic_late_payers = []
    
    for cust_type, config in customer_types.items():
        for i in range(config['count']):
            tier = np.random.choice(['Platinum', 'Gold', 'Silver', 'Bronze'], p=config['tier_distribution'])
            
            # Assign chronic late payer status (mostly Restaurants)
            is_late_payer = False
            if cust_type == 'Restaurant' and len(chronic_late_payers) < 18 and np.random.random() < 0.10:
                is_late_payer = True
                chronic_late_payers.append(f'CUST{customer_id:05d}')
            
            customers.append({
                'customer_no': f'CUST{customer_id:05d}',
                'customer_name': f'{cust_type} {customer_id}',
                'customer_type': cust_type,
                'state': np.random.choice(states, p=state_weights),
                'payment_terms': config['payment_terms'],
                'avg_days_to_pay': config['avg_days_to_pay'],
                'tier': tier,
                'is_chronic_late_payer': is_late_payer
            })
            customer_id += 1
    
    customers_df = pd.DataFrame(customers)
    
    # ===== GENERATE ORDERS WITH TRENDS =====
    print("Generating orders with year-based and product trends...")
    
    orders = []
    order_id = 100000
    
    # Year-based revenue multipliers (TREND A: 2021 COVID dip, 2024 surge)
    year_revenue_multipliers = {
        2020: 1.00,   # Baseline
        2021: 0.65,   # -35% COVID crash
        2022: 0.85,   # Recovery begins
        2023: 1.10,   # Exceeded baseline
        2024: 1.40,   # +40% record year
        2025: 1.42    # Continued growth
    }
    
    # Distribute orders across years with 2024-2025 bias
    year_weights = {
        2020: 0.15,
        2021: 0.12,  # Fewer orders during COVID
        2022: 0.16,
        2023: 0.20,
        2024: 0.25,  # Peak year
        2025: 0.12   # YTD
    }
    
    for _ in range(num_records):
        # Select year with weights
        year = np.random.choice(list(year_weights.keys()), p=list(year_weights.values()))
        year_multiplier = year_revenue_multipliers[year]
        
        # Generate order date
        if year == 2025:
            # YTD only (Jan-Nov)
            month = np.random.randint(1, 12)
        else:
            month = np.random.randint(1, 13)
        
        day = np.random.randint(1, 29)  # Safe day range
        order_date = datetime(year, month, day)
        
        # Skip future dates
        if order_date > datetime.now():
            continue
        
        # Select customer with tier bias (Platinum customers order more frequently)
        customer = customers_df.sample(1, weights=customers_df['tier'].map(
            {'Platinum': 4.0, 'Gold': 2.5, 'Silver': 1.5, 'Bronze': 1.0}
        )).iloc[0]
        
        # Select product
        product = np.random.choice(products)
        category = product['category']
        
        # TREND D: Apply product category growth/decline
        category_multiplier = 1.0
        if year >= 2022:  # Trend starts post-COVID
            years_since_2020 = year - 2020
            trend_factor = (product['growth_multiplier'] - 1.0) / 4  # Spread over 4 years
            category_multiplier = 1.0 + (trend_factor * years_since_2020)
        
        # Quantity calculation with all multipliers
        base_quantity = np.random.randint(20, 200)
        
        # Apply tier multiplier
        tier_multipliers = {'Platinum': 3.0, 'Gold': 2.0, 'Silver': 1.2, 'Bronze': 1.0}
        quantity = int(base_quantity * year_multiplier * category_multiplier * tier_multipliers[customer['tier']])
        quantity = max(5, quantity)  # Minimum order
        
        # Package details
        package_size = np.random.choice(package_sizes, p=package_weights)
        cheese_format = np.random.choice(cheese_formats)
        variant_code = f"{cheese_format[0]}{package_size.split()[0]}"
        
        # Pricing
        base_price = np.random.uniform(*product['base_price_range'])
        
        # 2024 premium pricing power
        if year == 2024:
            base_price *= 1.08
        elif year == 2021:
            base_price *= 0.95  # Discounts during COVID
        
        # Tier-based pricing
        tier_price_multipliers = {'Platinum': 0.92, 'Gold': 0.96, 'Silver': 1.00, 'Bronze': 1.04}
        unit_price = base_price * tier_price_multipliers[customer['tier']]
        
        # Discounts
        discount_pct = 0.0
        if np.random.random() < 0.20:  # 20% of orders have discounts
            discount_pct = np.random.choice([5, 10, 15, 20])
        
        line_amount = quantity * unit_price * (1 - discount_pct/100)
        
        # Rush order flag (3.6% of orders)
        is_rush = np.random.random() < 0.036
        
        # Production timing
        base_production_days = product['production_days']
        
        # Seasonal adjustment
        if month in [6, 7, 8]:  # Summer
            base_production_days += np.random.uniform(1, 2)
        elif month in [11, 12]:  # Holiday
            base_production_days += np.random.uniform(0.5, 1.5)
        
        # Rush order adjustment
        if is_rush:
            production_start = order_date + timedelta(days=int(np.random.randint(0, 2)))
        else:
            production_start = order_date + timedelta(days=int(np.random.randint(1, 4)))
        
        production_end = production_start + timedelta(days=int(base_production_days))
        
        # Shipment timing (1-3 days after production)
        shipment_date = production_end + timedelta(days=int(np.random.randint(1, 4)))
        
        # Invoice timing (same day or next day after shipment)
        invoice_date = shipment_date + timedelta(days=int(np.random.randint(0, 2)))
        
        # Payment timing with late payer logic
        expected_days = customer['avg_days_to_pay']
        if customer['is_chronic_late_payer']:
            days_overdue = int(np.random.randint(10, 21))
            actual_payment_days = expected_days + days_overdue
        else:
            actual_payment_days = int(np.random.normal(expected_days, 5))
            actual_payment_days = max(15, min(actual_payment_days, 90))  # Realistic range
        
        payment_date = invoice_date + timedelta(days=int(actual_payment_days))
        
        # Only include payment date if it's in the past
        if payment_date > datetime.now():
            payment_date = None
            order_status = 'Shipped'
        else:
            order_status = 'Completed'
        
        # Expiration date
        expiration_date = production_end + timedelta(days=int(product['shelf_life_days']))
        
        # Generate lot number
        lot_no = f"LOT{year}{month:02d}{np.random.randint(1000, 9999)}"
        
        # Facility assignment
        facility = np.random.choice(facilities)
        
        # Item number
        item_no = f"BCM-{category[:3].upper()}-{np.random.randint(1000, 9999)}"
        
        # PO number
        po_no = f"PO{year}{np.random.randint(10000, 99999)}"
        
        # Salesperson
        salesperson_code = f"SP{np.random.randint(100, 150)}"
        
        # Sales channel
        sales_channel = np.random.choice(sales_channels, p=channel_weights)
        
        # Freight method
        freight_method = np.random.choice(freight_methods, p=freight_weights)
        
        # Document type (mostly sales orders)
        doc_type = np.random.choice(['Sales Order', 'Rush Order', 'Standing Order'], p=[0.85, 0.10, 0.05])
        if is_rush:
            doc_type = 'Rush Order'
        
        orders.append({
            'document_type': doc_type,
            'document_no': f'SO{order_id}',
            'order_date': order_date.strftime('%Y-%m-%d'),
            'production_start_date': production_start.strftime('%Y-%m-%d'),
            'production_end_date': production_end.strftime('%Y-%m-%d'),
            'shipment_date': shipment_date.strftime('%Y-%m-%d'),
            'invoice_date': invoice_date.strftime('%Y-%m-%d'),
            'payment_date': payment_date.strftime('%Y-%m-%d') if payment_date else None,
            'sell_to_customer_no': customer['customer_no'],
            'sell_to_customer_name': customer['customer_name'],
            'customer_type': customer['customer_type'],
            'sell_to_state': customer['state'],
            'payment_terms_code': customer['payment_terms'],
            'sales_channel': sales_channel,
            'location_code': facility['code'],
            'location_name': facility['name'],
            'item_no': item_no,
            'item_description': product['product_name'],
            'cheese_category': category,
            'cheese_style_format': cheese_format,
            'variant_code': variant_code,
            'package_size': package_size,
            'unit_of_measure_code': 'LB',
            'quantity': quantity,
            'unit_price_usd': round(unit_price, 2),
            'line_discount_pct': discount_pct,
            'line_amount_usd': round(line_amount, 2),
            'currency_code': 'USD',
            'freight_method': freight_method,
            'lot_no': lot_no,
            'expiration_date': expiration_date.strftime('%Y-%m-%d'),
            'order_status': order_status,
            'po_no': po_no,
            'salesperson_code': salesperson_code,
            'customer_tier': customer['tier'],
            'is_rush_order': is_rush,
            'year': year,
            'month': month
        })
        
        order_id += 1
    
    orders_df = pd.DataFrame(orders)
    
    # ===== CREATE DIMENSION TABLES =====
    
    # 1. CUSTOMERS TABLE
    customers_unique = customers_df.copy()
    customers_unique['customer_id'] = range(1, len(customers_unique) + 1)
    customers_table = customers_unique[[
        'customer_id', 'customer_no', 'customer_name', 'customer_type', 
        'state', 'payment_terms', 'tier', 'is_chronic_late_payer'
    ]].rename(columns={
        'state': 'customer_state',
        'payment_terms': 'payment_terms_code',
        'tier': 'customer_tier'
    })
    
    # 2. PRODUCTS TABLE
    # Extract unique products from orders
    product_info = orders_df[[
        'item_no', 'item_description', 'cheese_category', 
        'cheese_style_format', 'variant_code', 'package_size', 'unit_of_measure_code'
    ]].drop_duplicates(subset=['item_no'])
    
    # Add production characteristics based on category
    category_specs = {
        'Fresh': {'production_days': 2, 'shelf_life_days': 21},
        'Soft/Semi-Soft': {'production_days': 4.5, 'shelf_life_days': 45},
        'Hard/Aged': {'production_days': 8, 'shelf_life_days': 180},
        'Blue': {'production_days': 5, 'shelf_life_days': 60},
        'Specialty': {'production_days': 6, 'shelf_life_days': 90}
    }
    
    product_info['standard_production_days'] = product_info['cheese_category'].map(
        lambda x: category_specs.get(x, {}).get('production_days', 5)
    )
    product_info['shelf_life_days'] = product_info['cheese_category'].map(
        lambda x: category_specs.get(x, {}).get('shelf_life_days', 60)
    )
    
    product_info.insert(0, 'product_id', range(1, len(product_info) + 1))
    products_table = product_info
    
    # 3. LOCATIONS TABLE
    locations_data = []
    for i, facility in enumerate(facilities, 1):
        city_state = facility['name'].split(' - ')[1]  # "Green Bay, WI"
        city = city_state.split(', ')[0]
        state = city_state.split(', ')[1]
        locations_data.append({
            'location_id': i,
            'location_code': facility['code'],
            'location_name': facility['name'],
            'facility_city': city,
            'facility_state': state
        })
    locations_table = pd.DataFrame(locations_data)
    
    # 4. SALESPEOPLE TABLE
    salesperson_codes = orders_df['salesperson_code'].unique()
    salespeople_data = []
    first_names = ['Alex', 'Jordan', 'Taylor', 'Morgan', 'Casey', 'Riley', 'Avery', 'Quinn', 'Dakota', 'Skyler']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']
    
    for code in sorted(salesperson_codes):
        sp_id = int(code.replace('SP', ''))
        fname = np.random.choice(first_names)
        lname = np.random.choice(last_names)
        salespeople_data.append({
            'salesperson_id': sp_id,
            'salesperson_code': code,
            'first_name': fname,
            'last_name': lname,
            'full_name': f'{fname} {lname}',
            'email': f'{fname.lower()}.{lname.lower()}@brightcheese.com'
        })
    salespeople_table = pd.DataFrame(salespeople_data).sort_values('salesperson_id').reset_index(drop=True)
    
    # 5. ORDERS (FACT) TABLE
    # Create lookup dictionaries for IDs
    customer_lookup = dict(zip(customers_unique['customer_no'], customers_unique['customer_id']))
    product_lookup = dict(zip(products_table['item_no'], products_table['product_id']))
    location_lookup = dict(zip(locations_table['location_code'], locations_table['location_id']))
    salesperson_lookup = dict(zip(salespeople_table['salesperson_code'], salespeople_table['salesperson_id']))
    
    # Build fact table with foreign keys
    orders_table = orders_df.copy()
    orders_table.insert(0, 'order_id', range(1, len(orders_table) + 1))
    orders_table['customer_id'] = orders_table['sell_to_customer_no'].map(customer_lookup)
    orders_table['product_id'] = orders_table['item_no'].map(product_lookup)
    orders_table['location_id'] = orders_table['location_code'].map(location_lookup)
    orders_table['salesperson_id'] = orders_table['salesperson_code'].map(salesperson_lookup)
    
    # Keep only fact table columns (remove dimension attributes)
    orders_fact_table = orders_table[[
        'order_id', 'document_type', 'document_no', 'customer_id', 'product_id', 
        'location_id', 'salesperson_id', 'order_date', 'production_start_date',
        'production_end_date', 'shipment_date', 'invoice_date', 'payment_date',
        'quantity', 'unit_price_usd', 'line_discount_pct', 'line_amount_usd',
        'currency_code', 'sales_channel', 'freight_method', 'lot_no', 
        'expiration_date', 'order_status', 'po_no', 'is_rush_order'
    ]]
    
    # ===== SAVE ALL TABLES =====
    customers_file = os.path.join(output_dir, "bright_cheese_manufacturing__customers.csv")
    products_file = os.path.join(output_dir, "bright_cheese_manufacturing__products.csv")
    locations_file = os.path.join(output_dir, "bright_cheese_manufacturing__locations.csv")
    salespeople_file = os.path.join(output_dir, "bright_cheese_manufacturing__salespeople.csv")
    orders_file = os.path.join(output_dir, "bright_cheese_manufacturing__orders.csv")
    
    customers_table.to_csv(customers_file, index=False)
    products_table.to_csv(products_file, index=False)
    locations_table.to_csv(locations_file, index=False)
    salespeople_table.to_csv(salespeople_file, index=False)
    orders_fact_table.to_csv(orders_file, index=False)
    
    # ===== ANALYSIS & VALIDATION =====
    print(f"\n{'='*60}")
    print(f"  BRIGHT CHEESE MANUFACTURING - DATASET GENERATED")
    print(f"{'='*60}")
    print(f"Output Directory: {output_dir}")
    print(f"\n📊 TABLES CREATED:")
    print(f"  1. orders.csv       : {len(orders_fact_table):,} rows × {len(orders_fact_table.columns)} columns (FACT TABLE)")
    print(f"  2. customers.csv    : {len(customers_table):,} rows × {len(customers_table.columns)} columns")
    print(f"  3. products.csv     : {len(products_table):,} rows × {len(products_table.columns)} columns")
    print(f"  4. locations.csv    : {len(locations_table):,} rows × {len(locations_table.columns)} columns")
    print(f"  5. salespeople.csv  : {len(salespeople_table):,} rows × {len(salespeople_table.columns)} columns")
    print(f"\nDate Range: {orders_df['order_date'].min()} to {orders_df['order_date'].max()}")
    
    print(f"\n{'='*60}")
    print(f"  TREND VALIDATION")
    print(f"{'='*60}")
    
    # TREND A: Year-over-year revenue
    print("\n📊 TREND A: Year-over-Year Revenue (2021 COVID Crash → 2024 Surge)")
    yearly_revenue = orders_df.groupby('year')['line_amount_usd'].sum()
    print(yearly_revenue.to_string())
    
    baseline_2020 = yearly_revenue.get(2020, 1)
    for year in [2021, 2022, 2023, 2024]:
        if year in yearly_revenue.index:
            pct_change = ((yearly_revenue[year] / baseline_2020) - 1) * 100
            print(f"  {year} vs 2020: {pct_change:+.1f}%")
    
    # TREND D: Product category trends
    print("\n🧀 TREND D: Product Category Trends (Fresh +45%, Aged -15%)")
    category_trends = orders_df[orders_df['year'].isin([2020, 2024])].groupby(['year', 'cheese_category'])['quantity'].sum().unstack(level=0)
    
    if 2020 in category_trends.columns and 2024 in category_trends.columns:
        category_trends['Growth_2020_to_2024'] = ((category_trends[2024] / category_trends[2020]) - 1) * 100
        print(category_trends[['Growth_2020_to_2024']].sort_values('Growth_2020_to_2024', ascending=False).to_string())
    
    # Payment behavior
    print("\n💳 Payment Behavior by Customer Type")
    payment_analysis = orders_df[orders_df['payment_date'].notna()].copy()
    payment_analysis['days_to_pay'] = (
        pd.to_datetime(payment_analysis['payment_date']) - 
        pd.to_datetime(payment_analysis['invoice_date'])
    ).dt.days
    
    avg_payment = payment_analysis.groupby('customer_type')['days_to_pay'].agg(['mean', 'median', 'std'])
    print(avg_payment.to_string())
    
    # Late payers
    late_payer_orders = orders_df[orders_df['sell_to_customer_no'].isin(chronic_late_payers)]
    print(f"\n⏰ Chronic Late Payers: {len(chronic_late_payers)} customers, {len(late_payer_orders)} orders")
    
    # Rush orders
    rush_count = orders_df['is_rush_order'].sum()
    rush_pct = (rush_count / len(orders_df)) * 100
    print(f"\n⚡ Rush Orders: {rush_count} ({rush_pct:.2f}% of total)")
    
    # Customer tier analysis
    print("\n🏆 Customer Tier Revenue Distribution")
    tier_revenue = orders_df.groupby('customer_tier')['line_amount_usd'].sum().sort_values(ascending=False)
    tier_pct = (tier_revenue / tier_revenue.sum() * 100)
    for tier, pct in tier_pct.items():
        print(f"  {tier}: {pct:.1f}%")
    
    print(f"\n{'='*60}")
    print(f"  ✅ DATASET READY FOR AGENT TESTING")
    print(f"{'='*60}")
    print("\nKey Questions Your Agent Should Answer:")
    print("1. Which year had the worst sales performance? (Answer: 2021)")
    print("2. Which cheese category is growing fastest? (Answer: Fresh)")
    print("3. Which customer type pays slowest? (Answer: Restaurants)")
    print("4. What percent of customers drive most revenue? (Answer: Platinum tier ~40-50%)")
    print("5. When are production times longest? (Answer: Summer & Holiday months)")
    
    print(f"\n🔗 DATA MODEL (Star Schema):")
    print(f"  orders (FACT)")
    print(f"    ├─ customer_id → customers.customer_id")
    print(f"    ├─ product_id → products.product_id")
    print(f"    ├─ location_id → locations.location_id")
    print(f"    └─ salesperson_id → salespeople.salesperson_id")
    
    return {
        'orders': orders_fact_table,
        'customers': customers_table,
        'products': products_table,
        'locations': locations_table,
        'salespeople': salespeople_table
    }

# Execute
if __name__ == "__main__":
    tables = create_cheese_manufacturing_dataset(75000)
    
    print("\n\n" + "="*60)
    print("  SAMPLE DATA FROM EACH TABLE")
    print("="*60)
    
    print("\n📋 CUSTOMERS (first 3 rows):")
    print(tables['customers'].head(3).to_string(index=False))
    
    print("\n\n📦 PRODUCTS (first 3 rows):")
    print(tables['products'].head(3).to_string(index=False))
    
    print("\n\n🏭 LOCATIONS (all rows):")
    print(tables['locations'].to_string(index=False))
    
    print("\n\n👤 SALESPEOPLE (first 5 rows):")
    print(tables['salespeople'].head(5).to_string(index=False))
    
    print("\n\n📊 ORDERS/FACT TABLE (first 3 rows):")
    print(tables['orders'].head(3).to_string(index=False))
    
    print("\n\n" + "="*60)
    print("  RELATIONSHIP VALIDATION")
    print("="*60)
    
    # Verify foreign key relationships
    orders = tables['orders']
    print(f"\n✓ All customer_ids in orders exist in customers: {orders['customer_id'].isin(tables['customers']['customer_id']).all()}")
    print(f"✓ All product_ids in orders exist in products: {orders['product_id'].isin(tables['products']['product_id']).all()}")
    print(f"✓ All location_ids in orders exist in locations: {orders['location_id'].isin(tables['locations']['location_id']).all()}")
    print(f"✓ All salesperson_ids in orders exist in salespeople: {orders['salesperson_id'].isin(tables['salespeople']['salesperson_id']).all()}")
    
    print("\n" + "="*60)

