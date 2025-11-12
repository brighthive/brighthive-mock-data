"""
GRECO & SONS MOCK DATA - INJECTED TRENDS
========================================
Product Trends (YoY): Frozen Foods +25-45%, Disposables -5-15%, Italian Specialties +12-22%
Customer Trends: Top 5 "whales" = ~40-50% of margin, Country Clubs = premium pricing, Schools = high volume/low margin
Regional Trends: IL/WI = +10-30% volume & lower freight, AZ/NV/CA = +20-50% freight costs
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def create_foodservice_datasets(num_records=5000):
    """Create Greco & Sons style synthetic datasets with realistic business trends"""
    
    # Current date for filenames
    current_date = datetime.now().strftime("%m-%d")
    output_dir = os.path.join("output", f"food_distribution_{current_date}")
    os.makedirs(output_dir, exist_ok=True)
    
    # ===== Master Data Setup =====
    regions = ["IL", "WI", "OH", "AZ", "NV", "MI", "IN", "IA", "MO", "NM", "TX", "CA", "MN"]
    customer_segments = ["Pizzeria", "School", "Hotel", "Country Club", "Grocery", "Bar", "QSR"]
    product_categories = {
        'Italian Sausage': ['Mild Italian Sausage', 'Hot Italian Sausage', 'Fennel Sausage'],
        'Cheese': ['Mozzarella', 'Provolone', 'Parmigiano Reggiano', 'Imported Pecorino'],
        'Tomatoes': ['San Marzano Tomatoes', 'Crushed Tomatoes', 'Diced Tomatoes'],
        'Pasta': ['Dry Spaghetti', 'Frozen Ravioli', 'Lasagna Sheets'],
        'Frozen Foods': ['Garlic Bread', 'Mozzarella Sticks', 'Frozen Meatballs', 'Breadsticks'],
        'Desserts': ['Tiramisu', 'Cannoli', 'Gelato', 'Italian Cookies'],
        'Disposables': ['Pizza Boxes', 'Napkins', 'Plastic Cups', 'Food Containers']
    }

    # Generate base customer IDs with weighted segments (more pizzerias, fewer country clubs)
    segment_weights = [0.3, 0.25, 0.15, 0.08, 0.12, 0.05, 0.05]  # Pizzeria heavy
    base_customers = [f'CUST{str(i).zfill(4)}' for i in range(1000, 1000 + int(num_records * 0.15))]
    
    # ===== Customer Master with Trend Injection =====
    def create_customers():
        num_customers = len(base_customers)
        
        # Create customer segments with realistic distribution
        segments = np.random.choice(customer_segments, num_customers, p=segment_weights)
        
        # Create regions with IL/WI bias (Greco's home markets)
        region_weights = [0.25, 0.15, 0.12, 0.08, 0.06, 0.08, 0.08, 0.06, 0.06, 0.03, 0.03]
        regions_selected = np.random.choice(regions[:11], num_customers, p=region_weights)
        
        # Create "whale customers" - mark top customers for special treatment
        whale_flags = [1 if i < 5 else 0 for i in range(num_customers)]  # Top 5 are whales
        np.random.shuffle(whale_flags)
        
        data = {
            'customer_id': base_customers,
            'customer_name': [f"{segments[i]} Chain {base_customers[i][-3:]}" if whale_flags[i] else f"{segments[i]} {base_customers[i][-3:]}" 
                             for i in range(num_customers)],
            'segment': segments,
            'region': regions_selected,
            'account_start_date': [(datetime(2019,1,1) + timedelta(days=np.random.randint(0, 1800))).strftime('%Y-%m-%d') 
                                  for _ in range(num_customers)],
            'status': np.random.choice(['Active','Inactive'], num_customers, p=[0.9,0.1]),
            'whale_customer': whale_flags,  # Internal flag for trend injection
            'customer_tier': ['Premium' if whale_flags[i] else 'Standard' for i in range(num_customers)]
        }
        return pd.DataFrame(data)
    
    # ===== Product Master =====
    def create_products():
        product_list = []
        for cat, subs in product_categories.items():
            for sub in subs:
                product_list.append((f'PROD{len(product_list)+1000:04d}', sub, cat))
        
        df = pd.DataFrame(product_list, columns=['product_id','product_name','product_category'])
        df['supplier'] = np.where(df['product_category']=='Italian Sausage','Greco & Sons (USDA)', 'Imported')
        
        # Set realistic unit costs by category
        cost_ranges = {
            'Italian Sausage': (3.5, 6.0),
            'Cheese': (4.0, 12.0),
            'Tomatoes': (2.0, 8.0),
            'Pasta': (1.5, 4.0),
            'Frozen Foods': (2.5, 7.0),
            'Desserts': (3.0, 15.0),
            'Disposables': (0.5, 3.0)
        }
        
        df['unit_cost'] = [np.random.uniform(*cost_ranges[cat]) for cat in df['product_category']]
        df['unit_cost'] = df['unit_cost'].round(2)
        
        return df
    
    # ===== Sales Transactions with TREND INJECTION =====
    def create_sales(customers, products):
        data = {}
        
        # Generate order dates with more recent bias
        order_dates = []
        for _ in range(num_records):
            # 60% of orders in 2024, 40% in 2023 for YoY comparison
            if np.random.random() < 0.6:
                date = datetime(2024,1,1) + timedelta(days=np.random.randint(0, 300))
            else:
                date = datetime(2023,1,1) + timedelta(days=np.random.randint(0, 365))
            order_dates.append(date)
        
        data['order_id'] = [f'ORD{i+100000:06d}' for i in range(num_records)]
        data['order_date'] = [d.strftime('%Y-%m-%d') for d in order_dates]
        
        # Customer selection with whale bias (whales get more orders)
        customer_weights = [3.0 if row['whale_customer'] else 1.0 for _, row in customers.iterrows()]
        customer_weights = np.array(customer_weights) / sum(customer_weights)
        selected_customers = np.random.choice(customers['customer_id'], num_records, p=customer_weights)
        data['customer_id'] = selected_customers
        
        # Merge customer info for trend calculations
        customer_lookup = customers.set_index('customer_id').to_dict('index')
        data['customer_segment'] = [customer_lookup[cid]['segment'] for cid in selected_customers]
        data['customer_region'] = [customer_lookup[cid]['region'] for cid in selected_customers]
        data['is_whale'] = [customer_lookup[cid]['whale_customer'] for cid in selected_customers]
        
        # Product selection
        selected_products = products.sample(num_records, replace=True).reset_index(drop=True)
        data['product_id'] = selected_products['product_id']
        data['product_category'] = selected_products['product_category']
        
        # TREND INJECTION: Quantity based on year, category, and customer type
        base_quantities = np.random.randint(5, 50, num_records)
        
        for i in range(num_records):
            year = order_dates[i].year
            category = data['product_category'][i]
            segment = data['customer_segment'][i]
            is_whale = data['is_whale'][i]
            region = data['customer_region'][i]
            
            quantity_multiplier = 1.0
            
            # PRODUCT TRENDS (YoY growth/decline)
            if year == 2024:
                if category == 'Frozen Foods':
                    quantity_multiplier *= np.random.uniform(1.25, 1.45)  # 25-45% growth
                elif category == 'Disposables':
                    quantity_multiplier *= np.random.uniform(0.85, 0.95)  # 5-15% decline
                elif category in ['Italian Sausage', 'Cheese', 'Tomatoes']:
                    quantity_multiplier *= np.random.uniform(1.12, 1.22)  # 12-22% growth
            
            # CUSTOMER TRENDS
            if is_whale:
                quantity_multiplier *= np.random.uniform(2.0, 4.0)  # Whales order 2-4x more
            
            if segment == 'Country Club':
                quantity_multiplier *= np.random.uniform(0.7, 0.9)  # Lower volume, higher margin
            elif segment == 'School':
                quantity_multiplier *= np.random.uniform(1.3, 1.8)  # High volume, lower margin
            
            if region in ['IL', 'WI']:  # Home markets
                quantity_multiplier *= np.random.uniform(1.1, 1.3)  # 10-30% boost
            
            base_quantities[i] = max(1, int(base_quantities[i] * quantity_multiplier))
        
        data['quantity'] = base_quantities
        
        # Pricing with segment-based margins
        base_prices = selected_products['unit_cost'] * np.random.uniform(1.3, 2.0, num_records)
        
        # Premium pricing for premium segments
        for i in range(num_records):
            if data['customer_segment'][i] in ['Country Club', 'Hotel']:
                base_prices[i] *= np.random.uniform(1.2, 1.4)  # 20-40% premium
            elif data['customer_segment'][i] == 'School':
                base_prices[i] *= np.random.uniform(0.9, 1.0)  # 0-10% discount
        
        data['unit_price'] = base_prices.round(2)
        
        # Discounts (whales get better deals)
        discount_probs = [[0.4, 0.3, 0.2, 0.1] if is_whale else [0.7, 0.2, 0.08, 0.02] for is_whale in data['is_whale']]
        data['discount_rate'] = [np.random.choice([0, 0.05, 0.10, 0.15], p=prob) for prob in discount_probs]
        
        # Freight costs (regional variation)
        base_freight = np.random.uniform(15, 75, num_records)
        for i in range(num_records):
            if data['customer_region'][i] in ['IL', 'WI', 'OH']:  # Close to warehouses
                base_freight[i] *= np.random.uniform(0.7, 0.9)
            elif data['customer_region'][i] in ['AZ', 'NV', 'CA']:  # Far markets
                base_freight[i] *= np.random.uniform(1.2, 1.5)
        
        data['freight_cost'] = base_freight.round(2)
        
        # Calculate financials
        data['sales_revenue'] = (data['quantity'] * data['unit_price'] * (1 - np.array(data['discount_rate']))).round(2)
        data['cogs'] = (data['quantity'] * selected_products['unit_cost']).round(2)
        data['gross_margin'] = (data['sales_revenue'] - data['cogs'] - data['freight_cost']).round(2)
        
        # Clean up internal columns
        del data['is_whale']
        
        return pd.DataFrame(data)
    
    # Build all datasets
    print("Creating customers with whale customer trends...")
    customers_df = create_customers()
    
    print("Creating products with category-specific pricing...")
    products_df = create_products()
    
    print("Creating sales with YoY trends and customer behavior patterns...")
    sales_df = create_sales(customers_df, products_df)
    
    # Save files
    cust_file = os.path.join(output_dir, f"food_distribution_customers_{current_date}.csv")
    prod_file = os.path.join(output_dir, f"food_distribution_products_{current_date}.csv")
    sales_file = os.path.join(output_dir, f"food_distribution_sales_{current_date}.csv")
    
    customers_df.to_csv(cust_file, index=False)
    products_df.to_csv(prod_file, index=False)
    sales_df.to_csv(sales_file, index=False)
    
    # Analysis preview
    whale_customers = customers_df[customers_df['whale_customer'] == 1]['customer_id'].tolist()
    whale_margin = sales_df[sales_df['customer_id'].isin(whale_customers)]['gross_margin'].sum()
    total_margin = sales_df['gross_margin'].sum()
    whale_percentage = (whale_margin / total_margin * 100) if total_margin > 0 else 0
    
    print(f"\n=== GRECO DATASETS CREATED ===")
    print(f"Output directory: {output_dir}")
    print(f"Customers: {len(customers_df)} records | Products: {len(products_df)} | Sales: {len(sales_df)}")
    print(f"\n=== INJECTED TRENDS PREVIEW ===")
    print(f"🐋 Whale customers (top 5): {whale_percentage:.1f}% of total gross margin")
    print(f"📈 Frozen Foods: +25-45% growth in 2024")
    print(f"📉 Disposables: -5-15% decline in 2024") 
    print(f"🍕 Italian Specialties: +12-22% growth in 2024")
    print(f"🏢 Country Clubs: Premium pricing, lower volume")
    print(f"🏫 Schools: Bulk pricing, higher volume")
    print(f"📍 IL/WI regions: 10-30% volume boost (home market advantage)")
    
    print(f"\n=== DEMO QUESTIONS SUPPORTED ===")
    print(f"✅ Top 10 customers by gross margin (with whale concentration)")
    print(f"✅ YoY category growth trends (3 distinct patterns)")
    print(f"✅ Margin leakage by region/segment")
    print(f"✅ Customer LTV by segment analysis")

    return {
        'customers': customers_df,
        'products': products_df, 
        'sales': sales_df,
        'files': [cust_file, prod_file, sales_file]
    }

# Execute
if __name__ == "__main__":
    datasets = create_foodservice_datasets(5000)
    
    print("\n=== SAMPLE DATA ===")
    print("\nTop 5 Customers by Total Margin:")
    customer_margins = datasets['sales'].groupby('customer_id')['gross_margin'].sum().sort_values(ascending=False).head()
    print(customer_margins)
    
    print("\nSales by Category (2024 vs 2023):")
    sales_by_year_cat = datasets['sales'].copy()
    sales_by_year_cat['year'] = pd.to_datetime(sales_by_year_cat['order_date']).dt.year
    category_trends = sales_by_year_cat.groupby(['year', 'product_category'])['sales_revenue'].sum().unstack(level=0)
    if 2023 in category_trends.columns and 2024 in category_trends.columns:
        category_trends['YoY_Growth'] = ((category_trends[2024] / category_trends[2023] - 1) * 100).round(1)
        print(category_trends[['YoY_Growth']].sort_values('YoY_Growth', ascending=False))