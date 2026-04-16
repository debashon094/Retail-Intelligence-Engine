import fuzzywuzzy.fuzz as fuzz
import pandas as pd

def smart_inventory_match(master_df, invoice_df, threshold=90):
    """
    Matches inventory using a strict hierarchy:
    1. Exact UPC Match (Anchor)
    2. Brand-Safe Fuzzy Match (Logic)
    """
    results = []

    for index, row in invoice_df.iterrows():
        # STEP 1: THE ANCHOR (UPC Matching)
        # Always check UPC first for 100% accuracy
        match = master_df[master_df['upc'] == row['upc']]
        
        if not match.empty:
            results.append({
                'invoice_item': row['item_name'],
                'matched_name': match.iloc[0]['item_name'],
                'match_type': 'UPC_EXACT',
                'score': 100
            })
            continue

        # STEP 2: BRAND-SAFE FUZZY MATCHING
        # If UPC fails, we look at the name, but PROTECT THE BRAND.
        best_score = 0
        best_match = None
        
        for m_index, m_row in master_df.iterrows():
            # Check if Brand Name is even in the string before fuzzy matching
            # This prevents "Brand A" matching "Brand B" just because they are both 'Soda'
            if m_row['brand'].lower() in row['item_name'].lower():
                score = fuzz.token_sort_ratio(m_row['item_name'], row['item_name'])
                
                if score > best_score and score >= threshold:
                    best_score = score
                    best_match = m_row['item_name']

        results.append({
            'invoice_item': row['item_name'],
            'matched_name': best_match if best_match else "NO_MATCH",
            'match_type': 'BRAND_FUZZY' if best_match else 'FAILED',
            'score': best_score
        })

    return pd.DataFrame(results)

# Example Usage
# master_data = pd.DataFrame({'upc': ['123', '456'], 'brand': ['Nike', 'Adidas'], 'item_name': ['Nike Air Max', 'Adidas Runner']})
# invoice_data = pd.DataFrame({'upc': ['123', '999'], 'item_name': ['Nike Air Max 2024', 'Adidas Runner']})
