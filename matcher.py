import pandas as pd
from fuzzywuzzy import fuzz
import logging

# Configure logging to show process details - crucial for "Analyst" transparency
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RetailIdentityMatcher:
    def __init__(self, master_catalog: pd.DataFrame, threshold: int = 85):
        self.master_catalog = master_catalog
        self.threshold = threshold

    def find_match(self, item_name: str, upc: str):
        """
        Executes a two-stage identity resolution:
        Stage 1: Deterministic (UPC)
        Stage 2: Probabilistic (Brand-Safe Fuzzy)
        """
        
        # --- STAGE 1: THE ANCHOR (UPC MATCH) ---
        # UPC is absolute. If matched, we stop here.
        upc_match = self.master_catalog[self.master_catalog['upc'] == str(upc)]
        if not upc_match.empty:
            return {
                "matched_name": upc_match.iloc[0]['item_name'],
                "match_method": "UPC_EXACT",
                "score": 100
            }

        # --- STAGE 2: BRAND-SAFE FUZZY LOGIC ---
        best_match = None
        highest_score = 0
        
        # Standardize search string
        search_name = item_name.lower()

        for _, row in self.master_catalog.iterrows():
            brand = str(row['brand']).lower()
            target_item = str(row['item_name']).lower()

            # GUARDRAIL: Strict Brand Integrity
            # If the brand name isn't in the invoice string, we skip it entirely.
            if brand not in search_name:
                continue

            # If brand is verified, calculate similarity
            score = fuzz.token_sort_ratio(target_item, search_name)
            
            if score > highest_score and score >= self.threshold:
                highest_score = score
                best_match = row['item_name']

        if best_match:
            return {
                "matched_name": best_match,
                "match_method": "BRAND_SAFE_FUZZY",
                "score": highest_score
            }

        return {"matched_name": "MANUAL_REVIEW_REQUIRED", "match_method": "NONE", "score": 0}

    def process_invoice(self, invoice_df: pd.DataFrame):
        """Processes an entire batch (e.g., from a CSV extracted via Textract)"""
        results = []
        for _, row in invoice_df.iterrows():
            match_result = self.find_match(row['item_name'], row['upc'])
            results.append({**row.to_dict(), **match_result})
        
        return pd.DataFrame(results)

# Example Deployment Logic
if __name__ == "__main__":
    # Mock Data for testing
    master_data = pd.DataFrame({
        'upc': ['1001', '1002'],
        'brand': ['Nike', 'Adidas'],
        'item_name': ['Nike Air Max White', 'Adidas Ultraboost Black']
    })
    
    invoice_data = pd.DataFrame({
        'upc': ['1001', '9999'], # 1001 will match via UPC, 9999 will use fuzzy logic
        'item_name': ['Nike Air Max', 'Adidas Ultra 2026 Edition']
    })

    matcher = RetailIdentityMatcher(master_data)
    processed_results = matcher.process_invoice(invoice_data)
    print(processed_results)
