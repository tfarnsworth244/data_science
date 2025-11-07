"""
Exploratory Data Analysis: Employee Burnout Prediction
=======================================================

This notebook explores the employee burnout dataset to understand:
- Data quality and distributions
- Relationships between features and burnout
- Key risk factors
- Insights for modeling
"""

# %% Imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# %% Load Data
import os
script_dir = Path(__file__).parent if '__file__' in globals() else Path.cwd() / 'notebooks'
project_root = script_dir.parent
data_path = project_root / 'data' / 'raw' / 'employee_data.csv'
df = pd.read_csv(data_path)

print("Dataset loaded successfully!")
print(f"Shape: {df.shape}")
print(f"\nFirst few rows:")
print(df.head())

# %% Data Overview
print("\n" + "="*80)
print("DATA OVERVIEW")
print("="*80)

print(f"\nDataset Info:")
print(df.info())

print(f"\nMissing Values:")
print(df.isnull().sum())

print(f"\nData Types:")
print(df.dtypes.value_counts())

# %% Target Variable Analysis
print("\n" + "="*80)
print("TARGET VARIABLE: BURNOUT")
print("="*80)

print(f"\nBurnout Score Statistics:")
print(df['burnout_score'].describe())

print(f"\nBurnout High Risk Distribution:")
print(df['burnout_high_risk'].value_counts())
print(f"\nPercentage at high risk: {df['burnout_high_risk'].mean()*100:.2f}%")

# Visualize burnout distribution
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Histogram
axes[0].hist(df['burnout_score'], bins=50, edgecolor='black', alpha=0.7)
axes[0].axvline(0.7, color='red', linestyle='--', linewidth=2, label='High Risk Threshold')
axes[0].set_xlabel('Burnout Score')
axes[0].set_ylabel('Frequency')
axes[0].set_title('Distribution of Burnout Scores')
axes[0].legend()

# Box plot by risk level
df['risk_category'] = df['burnout_high_risk'].map({0: 'Low Risk', 1: 'High Risk'})
sns.boxplot(data=df, x='risk_category', y='burnout_score', ax=axes[1])
axes[1].set_title('Burnout Score by Risk Category')
axes[1].set_ylabel('Burnout Score')

plt.tight_layout()
fig_path = project_root / 'reports' / 'figures' / 'burnout_distribution.png'
fig_path.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(fig_path, dpi=300, bbox_inches='tight')
print("\n✓ Saved: burnout_distribution.png")

# %% Demographic Analysis
print("\n" + "="*80)
print("DEMOGRAPHIC FACTORS")
print("="*80)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Age distribution
axes[0, 0].hist(df['age'], bins=30, edgecolor='black', alpha=0.7)
axes[0, 0].set_xlabel('Age')
axes[0, 0].set_ylabel('Frequency')
axes[0, 0].set_title('Age Distribution')

# Age vs Burnout
axes[0, 1].scatter(df['age'], df['burnout_score'], alpha=0.3)
axes[0, 1].set_xlabel('Age')
axes[0, 1].set_ylabel('Burnout Score')
axes[0, 1].set_title('Age vs Burnout Score')

# Gender distribution
gender_burnout = df.groupby('gender')['burnout_score'].mean().sort_values(ascending=False)
axes[1, 0].bar(gender_burnout.index, gender_burnout.values)
axes[1, 0].set_xlabel('Gender')
axes[1, 0].set_ylabel('Average Burnout Score')
axes[1, 0].set_title('Average Burnout by Gender')
axes[1, 0].tick_params(axis='x', rotation=45)

# Department distribution
dept_burnout = df.groupby('department')['burnout_score'].mean().sort_values(ascending=False)
axes[1, 1].barh(dept_burnout.index, dept_burnout.values)
axes[1, 1].set_xlabel('Average Burnout Score')
axes[1, 1].set_title('Average Burnout by Department')

plt.tight_layout()
fig_path = project_root / 'reports' / 'figures' / 'demographic_analysis.png'
fig_path.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(fig_path, dpi=300, bbox_inches='tight')
print("\n✓ Saved: demographic_analysis.png")

# %% Work Patterns Analysis
print("\n" + "="*80)
print("WORK PATTERNS")
print("="*80)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Hours per week vs Burnout
axes[0, 0].scatter(df['avg_hours_per_week'], df['burnout_score'], alpha=0.3)
axes[0, 0].set_xlabel('Average Hours per Week')
axes[0, 0].set_ylabel('Burnout Score')
axes[0, 0].set_title('Work Hours vs Burnout')

# Overtime vs Burnout
axes[0, 1].scatter(df['overtime_hours_per_month'], df['burnout_score'], alpha=0.3)
axes[0, 1].set_xlabel('Overtime Hours per Month')
axes[0, 1].set_ylabel('Burnout Score')
axes[0, 1].set_title('Overtime vs Burnout')

# Remote work type
remote_burnout = df.groupby('remote_work_type')['burnout_score'].mean().sort_values(ascending=False)
axes[1, 0].bar(remote_burnout.index, remote_burnout.values)
axes[1, 0].set_xlabel('Remote Work Type')
axes[1, 0].set_ylabel('Average Burnout Score')
axes[1, 0].set_title('Burnout by Remote Work Arrangement')
axes[1, 0].tick_params(axis='x', rotation=45)

# Tenure vs Burnout
axes[1, 1].scatter(df['tenure_years'], df['burnout_score'], alpha=0.3)
axes[1, 1].set_xlabel('Tenure (Years)')
axes[1, 1].set_ylabel('Burnout Score')
axes[1, 1].set_title('Tenure vs Burnout')

plt.tight_layout()
fig_path = project_root / 'reports' / 'figures' / 'work_patterns_analysis.png'
fig_path.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(fig_path, dpi=300, bbox_inches='tight')
print("\n✓ Saved: work_patterns_analysis.png")

# %% Key Predictors Analysis
print("\n" + "="*80)
print("KEY SURVEY PREDICTORS")
print("="*80)

survey_cols = ['job_satisfaction', 'workload_stress', 'work_life_balance',
               'career_growth_satisfaction', 'manager_support_score']

fig, axes = plt.subplots(2, 3, figsize=(16, 10))
axes = axes.flatten()

for idx, col in enumerate(survey_cols):
    axes[idx].scatter(df[col], df['burnout_score'], alpha=0.3)
    axes[idx].set_xlabel(col.replace('_', ' ').title())
    axes[idx].set_ylabel('Burnout Score')
    axes[idx].set_title(f'{col.replace("_", " ").title()} vs Burnout')

    # Add correlation
    corr = df[col].corr(df['burnout_score'])
    axes[idx].text(0.05, 0.95, f'r = {corr:.3f}', transform=axes[idx].transAxes,
                  verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# Remove extra subplot
axes[-1].axis('off')

plt.tight_layout()
fig_path = project_root / 'reports' / 'figures' / 'survey_predictors.png'
fig_path.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(fig_path, dpi=300, bbox_inches='tight')
print("\n✓ Saved: survey_predictors.png")

# %% Correlation Analysis
print("\n" + "="*80)
print("CORRELATION ANALYSIS")
print("="*80)

# Select numeric columns
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
numeric_cols.remove('employee_id') if 'employee_id' in numeric_cols else None

# Calculate correlations with burnout
burnout_corr = df[numeric_cols].corr()['burnout_score'].sort_values(ascending=False)
print("\nTop 10 Positive Correlations with Burnout:")
print(burnout_corr.head(11)[1:])  # Exclude burnout_score itself

print("\nTop 10 Negative Correlations with Burnout:")
print(burnout_corr.tail(10))

# Correlation heatmap (top features)
top_features = burnout_corr.abs().nlargest(16).index.tolist()
corr_matrix = df[top_features].corr()

plt.figure(figsize=(12, 10))
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0,
            square=True, linewidths=1, cbar_kws={"shrink": 0.8})
plt.title('Correlation Matrix: Top Features Related to Burnout', fontsize=14, pad=20)
plt.tight_layout()
fig_path = project_root / 'reports' / 'figures' / 'correlation_heatmap.png'
fig_path.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(fig_path, dpi=300, bbox_inches='tight')
print("\n✓ Saved: correlation_heatmap.png")

# %% High Risk Employees Profile
print("\n" + "="*80)
print("HIGH RISK EMPLOYEES PROFILE")
print("="*80)

high_risk = df[df['burnout_high_risk'] == 1]
low_risk = df[df['burnout_high_risk'] == 0]

print(f"\nHigh Risk Count: {len(high_risk)}")
print(f"Low Risk Count: {len(low_risk)}")

# Compare key metrics
comparison_features = ['avg_hours_per_week', 'overtime_hours_per_month',
                       'manager_support_score', 'job_satisfaction',
                       'workload_stress', 'work_life_balance']

comparison_df = pd.DataFrame({
    'High Risk': high_risk[comparison_features].mean(),
    'Low Risk': low_risk[comparison_features].mean()
})

print("\nKey Metrics Comparison:")
print(comparison_df.round(2))

# Visualize comparison
fig, ax = plt.subplots(figsize=(10, 6))
comparison_df.plot(kind='bar', ax=ax)
ax.set_ylabel('Average Value')
ax.set_title('High Risk vs Low Risk Employees: Key Metrics')
ax.legend(title='Risk Category')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
fig_path = project_root / 'reports' / 'figures' / 'risk_profile_comparison.png'
fig_path.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(fig_path, dpi=300, bbox_inches='tight')
print("\n✓ Saved: risk_profile_comparison.png")

# %% Key Insights Summary
print("\n" + "="*80)
print("KEY INSIGHTS")
print("="*80)

print("""
1. BURNOUT PREVALENCE:
   - {:.1f}% of employees are at high risk of burnout
   - Average burnout score: {:.3f}

2. STRONGEST PREDICTORS (Correlations):
   - Workload Stress: r = {:.3f} (positive)
   - Manager Support: r = {:.3f} (negative)
   - Work-Life Balance: r = {:.3f} (negative)
   - Overtime Hours: r = {:.3f} (positive)

3. HIGH-RISK PROFILE:
   - Work {:.1f} more overtime hours per month
   - Have {:.1f} points lower manager support
   - Report {:.1f} points higher workload stress
   - Show {:.1f} points lower work-life balance

4. DEPARTMENT INSIGHTS:
   - Highest burnout: {}
   - Lowest burnout: {}

5. ACTIONABLE FINDINGS:
   - Manager support is a key protective factor
   - Overtime hours strongly predict burnout risk
   - Work-life balance interventions could be highly effective
""".format(
    df['burnout_high_risk'].mean() * 100,
    df['burnout_score'].mean(),
    df['workload_stress'].corr(df['burnout_score']),
    df['manager_support_score'].corr(df['burnout_score']),
    df['work_life_balance'].corr(df['burnout_score']),
    df['overtime_hours_per_month'].corr(df['burnout_score']),
    comparison_df.loc['overtime_hours_per_month', 'High Risk'] - comparison_df.loc['overtime_hours_per_month', 'Low Risk'],
    comparison_df.loc['manager_support_score', 'Low Risk'] - comparison_df.loc['manager_support_score', 'High Risk'],
    comparison_df.loc['workload_stress', 'High Risk'] - comparison_df.loc['workload_stress', 'Low Risk'],
    comparison_df.loc['work_life_balance', 'Low Risk'] - comparison_df.loc['work_life_balance', 'High Risk'],
    dept_burnout.idxmax(),
    dept_burnout.idxmin()
))

print("\n✓ EDA Complete! All visualizations saved to reports/figures/")
