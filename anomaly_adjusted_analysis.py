import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

# Load the complete donation data
donations_df = pd.read_csv('complete_fundraising_data.csv')

# Convert dates and ensure proper formatting
donations_df['Date'] = pd.to_datetime(donations_df['Date'], format='mixed')
donations_df = donations_df.sort_values('Date')

print("=== ANOMALY-ADJUSTED FUNDRAISING ANALYSIS ===")
print(f"Analysis Period: {donations_df['Date'].min().strftime('%Y-%m-%d')} to {donations_df['Date'].max().strftime('%Y-%m-%d')}")
print(f"Total Days: {len(donations_df)}")
print()

# Identify anomalies (large gifts)
# Define threshold for anomalies (based on the data we found: 50k and 30k+ gifts)
anomaly_threshold = 30000  # $30,000+
anomalies = donations_df[donations_df['Donations_USD'] > anomaly_threshold]

print("=== IDENTIFIED ANOMALIES ===")
for idx, row in anomalies.iterrows():
    print(f"Date: {row['Date'].strftime('%Y-%m-%d')} - Amount: ${row['Donations_USD']:,.0f} - Donors: {row['Donors']}")

print(f"\nTotal Anomaly Days: {len(anomalies)}")
print(f"Total Anomaly Amount: ${anomalies['Donations_USD'].sum():,.0f}")
print()

# Create baseline dataset (excluding anomalies)
baseline_df = donations_df[donations_df['Donations_USD'] <= anomaly_threshold].copy()

print("=== BASELINE STATISTICS (Excluding Anomalies) ===")
baseline_total = baseline_df['Donations_USD'].sum()
baseline_days = len(baseline_df)
baseline_avg_daily = baseline_total / baseline_days
baseline_avg_donors = baseline_df['Donors'].sum() / baseline_days

print(f"Baseline Total Raised: ${baseline_total:,.0f}")
print(f"Baseline Days: {baseline_days}")
print(f"Baseline Average Daily Raise: ${baseline_avg_daily:,.0f}")
print(f"Baseline Average Daily Donors: {baseline_avg_donors:.0f}")
print()

# Calculate adjusted metrics
original_total = donations_df['Donations_USD'].sum()
original_avg_daily = original_total / len(donations_df)

print("=== COMPARISON: Original vs Baseline ===")
print(f"Original Total Raised: ${original_total:,.0f}")
print(f"Original Average Daily: ${original_avg_daily:,.0f}")
print(f"Adjusted Average Daily (no anomalies): ${baseline_avg_daily:,.0f}")
print(f"Anomaly Impact on Daily Average: ${original_avg_daily - baseline_avg_daily:,.0f} (+{(original_avg_daily/baseline_avg_daily - 1)*100:.1f}%)")
print()

# Event correlation analysis with adjusted data
events_data = [
    {'event_date': '2024-12-04', 'driver_layer': 'Legal', 'event_type': 'Breaking news', 'label': 'Arrest', 'weight': 10, 'impact_window': 3},
    {'event_date': '2024-12-05', 'driver_layer': 'Media', 'event_type': 'Viral moment', 'label': 'Mugshot release', 'weight': 10, 'impact_window': 2},
    {'event_date': '2024-12-06', 'driver_layer': 'Media', 'event_type': 'Press coverage', 'label': 'National news coverage', 'weight': 8, 'impact_window': 2},
    {'event_date': '2024-12-09', 'driver_layer': 'Legal', 'event_type': 'Court hearing', 'label': 'Arraignment', 'weight': 10, 'impact_window': 2},
    {'event_date': '2024-12-10', 'driver_layer': 'Organizer', 'event_type': 'Statement', 'label': 'Free Luigi movement launch', 'weight': 9, 'impact_window': 3},
    {'event_date': '2024-12-15', 'driver_layer': 'Media', 'event_type': 'Viral moment', 'label': 'Social media trends', 'weight': 7, 'impact_window': 1},
    {'event_date': '2024-12-20', 'driver_layer': 'Legal', 'event_type': 'Court filing', 'label': 'Bail hearing', 'weight': 8, 'impact_window': 2},
    {'event_date': '2024-12-25', 'driver_layer': 'Personal', 'event_type': 'Personal milestone', 'label': 'Christmas letters from supporters', 'weight': 6, 'impact_window': 1},
    {'event_date': '2025-01-02', 'driver_layer': 'Legal', 'event_type': 'Court hearing', 'label': 'Preliminary hearing', 'weight': 9, 'impact_window': 2},
    {'event_date': '2025-01-08', 'driver_layer': 'Organizer', 'event_type': 'Statement', 'label': 'Organizer press conference', 'weight': 7, 'impact_window': 2},
    {'event_date': '2025-01-15', 'driver_layer': 'Media', 'event_type': 'Press coverage', 'label': 'Documentary announcement', 'weight': 8, 'impact_window': 3},
    {'event_date': '2025-01-20', 'driver_layer': 'Legal', 'event_type': 'Court filing', 'label': 'Motion to dismiss', 'weight': 8, 'impact_window': 2},
    {'event_date': '2025-01-25', 'driver_layer': 'Organizer', 'event_type': 'Interview', 'label': 'Organizer podcast interview', 'weight': 6, 'impact_window': 2},
    {'event_date': '2025-02-01', 'driver_layer': 'Legal', 'event_type': 'Court hearing', 'label': 'Pre-trial motion hearing', 'weight': 9, 'impact_window': 2},
    {'event_date': '2025-02-05', 'driver_layer': 'Organizer', 'event_type': 'Statement', 'label': 'Coalition statement', 'weight': 6, 'impact_window': 2},
    {'event_date': '2025-02-10', 'driver_layer': 'Media', 'event_type': 'Press coverage', 'label': 'Magazine feature', 'weight': 7, 'impact_window': 2},
    {'event_date': '2025-02-14', 'driver_layer': 'Personal', 'event_type': 'Personal milestone', 'label': "Valentine's Day campaign", 'weight': 5, 'impact_window': 1},
    {'event_date': '2025-02-20', 'driver_layer': 'Legal', 'event_type': 'Court filing', 'label': 'Discovery filing', 'weight': 7, 'impact_window': 2},
    {'event_date': '2025-02-25', 'driver_layer': 'Organizer', 'event_type': 'Statement', 'label': 'Rally announcement', 'weight': 7, 'impact_window': 3},
    {'event_date': '2025-03-01', 'driver_layer': 'Media', 'event_type': 'Viral moment', 'label': 'TikTok trend', 'weight': 6, 'impact_window': 1},
    {'event_date': '2025-03-05', 'driver_layer': 'Legal', 'event_type': 'Court hearing', 'label': 'Status conference', 'weight': 8, 'impact_window': 2},
    {'event_date': '2025-03-10', 'driver_layer': 'Organizer', 'event_type': 'Interview', 'label': 'Family interview', 'weight': 8, 'impact_window': 2},
    {'event_date': '2025-03-15', 'driver_layer': 'Media', 'event_type': 'Press coverage', 'label': 'News investigation piece', 'weight': 8, 'impact_window': 3},
]

events_df = pd.DataFrame(events_data)
events_df['event_date'] = pd.to_datetime(events_df['event_date'])

# Analyze event impact on baseline data
print("=== EVENT IMPACT ANALYSIS (Baseline Data) ===")
event_impacts = []

for _, event in events_df.iterrows():
    event_date = event['event_date']
    impact_start = event_date - timedelta(days=1)
    impact_end = event_date + timedelta(days=event['impact_window'])
    
    # Get baseline performance during impact window
    impact_period = baseline_df[
        (baseline_df['Date'] >= impact_start) & 
        (baseline_df['Date'] <= impact_end)
    ]
    
    if len(impact_period) > 0:
        avg_impact = impact_period['Donations_USD'].mean()
        baseline_comparison = baseline_df['Donations_USD'].mean()
        lift_percentage = ((avg_impact - baseline_comparison) / baseline_comparison) * 100
        
        event_impacts.append({
            'event': event['label'],
            'driver_layer': event['driver_layer'],
            'event_type': event['event_type'],
            'avg_impact': avg_impact,
            'lift_percentage': lift_percentage,
            'sample_size': len(impact_period)
        })

# Sort by impact
event_impacts_sorted = sorted(event_impacts, key=lambda x: x['lift_percentage'], reverse=True)

print("Top 10 Events by Performance Lift (Baseline Data):")
for i, impact in enumerate(event_impacts_sorted[:10]):
    print(f"{i+1:2d}. {impact['event']:<25} ({impact['driver_layer']:<8}) - "
          f"Lift: {impact['lift_percentage']:+.1f}% (${impact['avg_impact']:,.0f})")

print()

# Revised forecasting without anomaly bias
print("=== REVISED FORECASTING (Anomaly-Adjusted) ===")
monthly_baseline = baseline_df.groupby(baseline_df['Date'].dt.to_period('M'))['Donations_USD'].mean()
projected_monthly = monthly_baseline.mean() * 30  # Average month

print(f"Projected Monthly Raise (Baseline): ${projected_monthly:,.0f}")
print(f"Projected Annual Raise (Baseline): ${projected_monthly * 12:,.0f}")

# Conservative forecast (80% of baseline projection)
conservative_monthly = projected_monthly * 0.8
print(f"Conservative Monthly Target: ${conservative_monthly:,.0f}")
print(f"Conservative Annual Target: ${conservative_monthly * 12:,.0f}")
print()

# Save adjusted analysis
with open('anomaly_adjusted_analysis.txt', 'w') as f:
    f.write("ANOMALY-ADJUSTED FUNDRAISING ANALYSIS REPORT\n")
    f.write("=" * 50 + "\n\n")
    f.write(f"Analysis Period: {donations_df['Date'].min().strftime('%Y-%m-%d')} to {donations_df['Date'].max().strftime('%Y-%m-%d')}\n")
    f.write(f"Anomaly Threshold: ${anomaly_threshold:,}\n")
    f.write(f"Anomalies Identified: {len(anomalies)} days\n\n")
    
    f.write("KEY FINDINGS:\n")
    f.write("-" * 20 + "\n")
    f.write(f"Baseline Daily Performance: ${baseline_avg_daily:,.0f}\n")
    f.write(f"Anomaly Impact: +${original_avg_daily - baseline_avg_daily:,.0f}/day\n")
    f.write(f"Conservative Monthly Projection: ${conservative_monthly:,.0f}\n")

print("\nAnomaly-adjusted analysis saved to 'anomaly_adjusted_analysis.txt'")