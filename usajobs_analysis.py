import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

def analyze_and_plot(csv_file='usajobs_18months_analysis.csv'):
    df = pd.read_csv(csv_file)
    
    def extract_series(text):
        match = re.search(r'\(Series:\s*(\d+)\)', str(text))
        return match.group(1) if match else 'Unknown'
        
    df['Series_Code'] = df['Job_Title_Series'].apply(extract_series)
    
    agency_totals = df.groupby(['Agency', 'Period_Type'])['Total_Listings'].sum().unstack(fill_value=0)
    agency_totals['Pre_Monthly_Avg'] = agency_totals.get('Pre-Trump Baseline', 0) / 9.0
    agency_totals['Post_Monthly_Avg'] = agency_totals.get('Post-2025 Period', 0) / 18.0
    agency_totals['Monthly_Change'] = agency_totals['Post_Monthly_Avg'] - agency_totals['Pre_Monthly_Avg']
    
    filtered = agency_totals[(agency_totals.get('Pre-Trump Baseline', 0) + agency_totals.get('Post-2025 Period', 0)) >= 15]
    top_growth = filtered.sort_values(by='Monthly_Change', ascending=False).head(10).reset_index()
    top_decline = filtered.sort_values(by='Monthly_Change', ascending=True).head(10).reset_index()
    
    fig, axes = plt.subplots(2, 1, figsize=(11, 9))
    sns.barplot(data=top_growth, y='Agency', x='Monthly_Change', ax=axes[0], palette='Greens_r')
    axes[0].set_title('Top 10 Agencies with Largest Increase in Monthly Avg Postings', fontweight='bold')
    axes[0].set_xlabel('Change in Monthly Listings')
    
    sns.barplot(data=top_decline, y='Agency', x='Monthly_Change', ax=axes[1], palette='Reds')
    axes[1].set_title('Top 10 Agencies with Largest Decrease in Monthly Avg Postings', fontweight='bold')
    axes[1].set_xlabel('Change in Monthly Listings')
    
    plt.tight_layout()
    plt.savefig('overall_agency_changes.png')
    plt.close()

if __name__ == '__main__':
    analyze_and_plot()
