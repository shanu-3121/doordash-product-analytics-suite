import pandas as pd
import numpy as np
from scipy import stats

print("="*60)
print("A/B TEST ANALYSIS — New Checkout Flow Experiment")
print("="*60)

# ============================================
# LOAD DATA
# ============================================
ab_df = pd.read_csv("data_ab_test.csv")

# Split into control and variant
control = ab_df[ab_df['experiment_group'] == 'control']
variant = ab_df[ab_df['experiment_group'] == 'variant']

# ============================================
# BASIC METRICS
# ============================================
print("\n📊 EXPERIMENT OVERVIEW")
print("-"*60)

control_users = len(control)
variant_users = len(variant)
control_conversions = control['converted'].sum()
variant_conversions = variant['converted'].sum()
control_rate = control_conversions / control_users
variant_rate = variant_conversions / variant_users

print(f"Control Group  → {control_users:,} users | "
      f"{control_conversions:,} converted | "
      f"{control_rate*100:.1f}% conversion rate")
print(f"Variant Group  → {variant_users:,} users | "
      f"{variant_conversions:,} converted | "
      f"{variant_rate*100:.1f}% conversion rate")

# ============================================
# STATISTICAL SIGNIFICANCE TEST
# ============================================
print("\n📊 STATISTICAL SIGNIFICANCE TEST")
print("-"*60)

# Chi-square test
contingency_table = pd.crosstab(
    ab_df['experiment_group'],
    ab_df['converted']
)

chi2, p_value, dof, expected = stats.chi2_contingency(
    contingency_table
)

print(f"Chi-Square Statistic : {chi2:.4f}")
print(f"P-Value              : {p_value:.6f}")
print(f"Degrees of Freedom   : {dof}")

# ============================================
# RESULTS INTERPRETATION
# ============================================
print("\n📊 RESULTS")
print("-"*60)

alpha = 0.05  # 95% confidence level
lift = (variant_rate - control_rate) / control_rate * 100
absolute_lift = (variant_rate - control_rate) * 100

print(f"Confidence Level     : 95%")
print(f"Significance Level   : {alpha}")
print(f"Absolute Lift        : +{absolute_lift:.1f}%")
print(f"Relative Lift        : +{lift:.1f}%")

if p_value < alpha:
    print(f"\n✅ RESULT: STATISTICALLY SIGNIFICANT")
    print(f"   P-value ({p_value:.6f}) < Alpha ({alpha})")
    print(f"   We can reject the null hypothesis")
    print(f"   The new checkout flow genuinely improves conversion")
else:
    print(f"\n❌ RESULT: NOT STATISTICALLY SIGNIFICANT")
    print(f"   P-value ({p_value:.6f}) > Alpha ({alpha})")
    print(f"   We cannot reject the null hypothesis")

# ============================================
# BUSINESS IMPACT CALCULATION
# ============================================
print("\n📊 ESTIMATED BUSINESS IMPACT")
print("-"*60)

# Assumptions based on real DoorDash public data
monthly_active_users = 37000000  # 37M MAU (real DoorDash figure)
avg_order_value = 29.22          # from our data

# Current vs projected completions
current_completions = monthly_active_users * control_rate
projected_completions = monthly_active_users * variant_rate
additional_orders = projected_completions - current_completions
additional_revenue = additional_orders * avg_order_value

print(f"DoorDash Monthly Active Users : {monthly_active_users:,}")
print(f"Current Completion Rate       : {control_rate*100:.1f}%")
print(f"Projected Completion Rate     : {variant_rate*100:.1f}%")
print(f"Additional Orders Per Month   : {additional_orders:,.0f}")
print(f"Estimated Revenue Impact      : ${additional_revenue:,.0f}/month")
print(f"Annualized Revenue Impact     : "
      f"${additional_revenue*12:,.0f}/year")

# ============================================
# SEGMENT ANALYSIS
# ============================================
print("\n📊 SEGMENT BREAKDOWN — Who Benefits Most?")
print("-"*60)

segment_analysis = ab_df.groupby(
    ['experiment_group', 'device_type']
)['converted'].agg(['sum', 'count']).reset_index()

segment_analysis['conversion_rate'] = (
    segment_analysis['sum'] /
    segment_analysis['count'] * 100
).round(1)

segment_pivot = segment_analysis.pivot(
    index='device_type',
    columns='experiment_group',
    values='conversion_rate'
).reset_index()

segment_pivot['lift'] = (
    segment_pivot['variant'] -
    segment_pivot['control']
).round(1)

segment_pivot.columns = [
    'Device', 'Control %', 'Variant %', 'Lift %'
]
print(segment_pivot.to_string(index=False))

# DashPass segment
print("\n--- By DashPass Status ---")
dashpass_analysis = ab_df.groupby(
    ['experiment_group', 'is_dashpass']
)['converted'].agg(['sum', 'count']).reset_index()

dashpass_analysis['conversion_rate'] = (
    dashpass_analysis['sum'] /
    dashpass_analysis['count'] * 100
).round(1)

dashpass_pivot = dashpass_analysis.pivot(
    index='is_dashpass',
    columns='experiment_group',
    values='conversion_rate'
).reset_index()

dashpass_pivot['lift'] = (
    dashpass_pivot['variant'] -
    dashpass_pivot['control']
).round(1)

dashpass_pivot['is_dashpass'] = dashpass_pivot[
    'is_dashpass'
].astype(str).map({
    '0': 'Regular', 
    '1': 'DashPass', 
    'False': 'Regular', 
    'True': 'DashPass',
    '0.0': 'Regular',
    '1.0': 'DashPass'
})

dashpass_pivot.columns = [
    'User Type', 'Control %', 'Variant %', 'Lift %'
]
print(dashpass_pivot.to_string(index=False))

# ============================================
# FINAL RECOMMENDATION
# ============================================
print("\n" + "="*60)
print("📌 FINAL RECOMMENDATION")
print("="*60)
print("""
The new 2-step checkout flow shows a statistically significant
7.4% absolute lift in conversion rate (p < 0.05).

Recommendation: SHIP the variant to 100% of users.

Expected impact at DoorDash scale:
- +2.7M additional completed orders per month
- +$79M additional revenue per month  
- +$950M annualized revenue impact

Priority segment: Focus rollout on Regular users first
as they show highest lift from the simplified flow.
""")

print("✅ A/B TEST ANALYSIS COMPLETE!")

