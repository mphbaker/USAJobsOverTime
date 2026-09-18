# USAJobsOverTime: 18-Month Federal Hiring Analysis

An open-source Python pipeline and analytical framework for processing, normalizing, and evaluating federal job posting trends from the **USAJOBS API**.

This repository analyzes an 18-month dataset comparing a 9-month pre-2025 baseline against post-2025 hiring activity to track structural reallocations, public accessibility, and agency-level recruitment shifts.

## 📊 Overview & Key Findings

Rather than showing a uniform trend across the executive branch, empirical USAJOBS data demonstrates major sector-specific reallocations between frontline/operational mandates and administrative/scientific bodies.

### **1. Operational & Frontline Surge**
* **Veterans Health Administration (VHA):** Experienced a **+474.1%** increase (+195.9 listings/month), driven primarily by bedside healthcare and clinical series.
* **Customs and Border Protection (CBP):** Expanded by **+82.3%** (+48.8 listings/month).
* **Occupational Series Growth:** Registered Nurses (Series 0610) increased by **+138%**, while Police Officers (Series 0083) saw a **+222%** spike in monthly postings.

### **2. Absolute Volume Leaders (Post-2025)**
High absolute posting volume is heavily concentrated in agencies with statutorily mandated 24/7 operations:
1. **Veterans Health Administration (VHA):** 237.2 listings/mo
2. **Customs and Border Protection (CBP):** 108.1 listings/mo
3. **Federal Bureau of Prisons (BOP):** 51.6 listings/mo
4. **Veterans Benefits Administration (VBA):** 39.4 listings/mo
5. **Federal Aviation Administration (FAA):** 38.1 listings/mo

### **3. Scientific, Regulatory & Administrative Contraction**
* **U.S. Geological Survey (USGS):** Postings dropped by **-95.0%** (-21.0 listings/month).
* **National Institutes of Health (NIH):** Postings fell by **-70.4%** (-30.9 listings/month).
* **Series Reductions:** Biologist (Series 0401) listings fell **-71.3%**, and Program Analysts (Series 0343) dropped **-32.2%**.
* **Posting Pauses:** Select sub-entities—including the Consumer Financial Protection Bureau (CFPB) and U.S. Army Contracting Command—recorded **zero new postings** in the post-2025 observation window.

### **4. Public vs. Internal Accessibility**
* **Aggregate Access:** Aggregate listings designated as "Open to the Public" remained flat at **~46%**.
* **Agency-Level Divergence:** Specific agencies implemented internal restriction policies; for instance, the FAA routed **>90%** of its postings through restricted or internal candidate pools.

## 🛠️ Repository Structure

* `monthlyjobs_full.py`: Script to fetch/aggregate raw USAJOBS API postings
* `usajobs_analysis.py`: Data analysis, monthly normalization, and plotting script
* `usajobs_18months_analysis.csv`: Raw aggregated dataset (18-month observation period)
* `overall_agency_changes.png`: Generated visualization comparing top growth & decline agencies
* `LICENSE`: License file
* `README.md`: Project documentation

## 🚀 Getting Started

### **Prerequisites**
Make sure you have Python 3 installed along with the required libraries:
```bash
pip install pandas matplotlib seaborn
```

### **Running the Analysis**
To run the data analysis pipeline and display the top agency growth/decline metrics in your terminal:
```bash
python3 usajobs_analysis.py
```

This will output:
1. Printed summary tables in your console detailing monthly baseline vs. post-period averages.
2. An updated **`overall_agency_changes.png`** chart comparing top expanding and contracting agencies.

## 📈 Methodology & Data Normalization

Because observation windows differ between time periods, raw listing counts are normalized on a **Monthly Average** basis:

* **Pre-2025 Baseline:** 9 months of historical data (Monthly Avg = Total Pre Listings / 9).
* **Post-2025 Window:** 18 months of post-baseline data (Monthly Avg = Total Post Listings / 18).
* **Net Change:** Post Monthly Avg - Pre Monthly Avg.

Agencies with fewer than 15 total postings across the entire 27-month combined window were filtered out to eliminate low-sample noise.

## 📄 License
This project is open source and available under the terms of the [LICENSE](LICENSE) file.

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to fork the repository and submit a pull request for custom OPM series queries or additional visualizations.
