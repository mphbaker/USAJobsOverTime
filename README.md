USAJobsOverTime: 18-Month Federal Hiring Analysis
An open-source Python pipeline and analytical framework for processing, normalizing, and evaluating federal job posting trends from the USAJOBS API.This repository analyzes an 18-month dataset comparing a 9-month pre-2025 baseline against post-2025 hiring activity to track structural reallocations, public accessibility, and agency-level recruitment shifts.
Repository StructureUSAJobsOverTime/
├── monthlyjobs_full.py          # Script to fetch/aggregate raw USAJOBS API postings
├── usajobs_analysis.py          # Data analysis, monthly normalization, and plotting script
├── usajobs_18months_analysis.csv# Raw aggregated dataset (18-month observation period)
├── overall_agency_changes.png   # Generated visualization comparing top growth & decline agencies
├── LICENSE                      # License file
└── README.md                    # Project documentation
Getting StartedPrerequisitesMake sure you have Python 3 installed along with the required libraries:pip install pandas matplotlib seaborn

Running the AnalysisTo run the data analysis pipeline and display the top agency growth/decline metrics in your terminal:python3 usajobs_analysis.py

This will output:Printed summary tables in your console detailing monthly baseline vs. post-period averages.An updated overall_agency_changes.png chart comparing top expanding and contracting agencies.📈 Methodology & Data NormalizationBecause observation windows differ between time periods, raw listing counts are normalized on a Monthly Average basis:Pre-2025 Baseline: 9 months of historical data ($\text{Monthly Avg} = \frac{\text{Total Pre Listings}}{9}$).Post-2025 Window: 18 months of post-baseline data ($\text{Monthly Avg} = \frac{\text{Total Post Listings}}{18}$).Net Change: $\text{Post Monthly Avg} - \text{Pre Monthly Avg}$.Agencies with fewer than 15 total postings across the entire 27-month combined window were filtered out to eliminate low-sample noise.📄 LicenseThis project is open source and available under the terms of the LICENSE.

ContributingContributions, issues, and feature requests are welcome! Feel free to fork the repository and submit a pull request for custom OPM series queries or additional visualizations.
