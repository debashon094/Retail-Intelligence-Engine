# Retail-Intelligence-Engine 📦🤖

An automated, serverless data pipeline designed to bridge the gap between messy retail invoices and clean Master Catalog data. This project was developed to solve real-world inventory discrepancies in industrial logistics.

## 🚀 Key Features
* **UPC-Anchor Logic:** Prioritizes deterministic matching for 100% accuracy on standard products.
* **Brand-Safe Fuzzy Matching:** A custom algorithm that prevents cross-brand misidentification (e.g., won't match Brand A 'Soda' to Brand B 'Soda').
* **Cloud-Native Architecture:** Designed to trigger via **AWS S3** and execute in **AWS Lambda**.
* **Scalable Data Extraction:** Integrated with **AWS Textract** for high-volume PDF-to-CSV processing.

## 🏗️ Architecture
The pipeline follows an Event-Driven Architecture:
1. **Ingestion:** Raw invoice upload to **S3**.
2. **Extraction:** **Lambda** + **Textract** converts document images to structured data.
3. **Resolution:** **Python** matcher executes the UPC-Anchor and Brand-Safety logic.
4. **Storage:** Final matched inventory is pushed to **Redshift** for analytics.

## 🔬 Research Context (PhD Focus)
This project serves as a prototype for **Cyber-Physical Systems (CPS)** in Industrial Engineering. It addresses the "Identity Resolution" bottleneck in supply chain management, ensuring data integrity across disparate vendor systems—a critical requirement for Industry 4.0 automation.

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **Libraries:** Pandas, FuzzyWuzzy, Levenshtein
* **Cloud Infrastructure:** AWS (Lambda, S3, Textract, Redshift)

## 📖 How to Use
1. Clone the repo: `git clone https://github.com/[YourUsername]/Retail-Intelligence-Engine`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the matcher: `python matcher.py`
