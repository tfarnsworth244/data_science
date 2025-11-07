"""
Generate synthetic employee burnout dataset.

This script creates a realistic synthetic dataset for employee burnout prediction
that mirrors real-world HR analytics data found on Kaggle.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_employee_data(n_employees=5000):
    """Generate synthetic employee data with burnout indicators."""

    print(f"Generating data for {n_employees} employees...")

    # Employee IDs
    employee_ids = [f"EMP{str(i).zfill(5)}" for i in range(1, n_employees + 1)]

    # Demographics
    ages = np.random.normal(35, 8, n_employees).clip(22, 65).astype(int)
    genders = np.random.choice(['Male', 'Female', 'Other'], n_employees, p=[0.48, 0.48, 0.04])

    # Job characteristics
    departments = np.random.choice(
        ['Engineering', 'Sales', 'Marketing', 'HR', 'Finance', 'Operations', 'Customer Support'],
        n_employees,
        p=[0.25, 0.20, 0.12, 0.08, 0.10, 0.15, 0.10]
    )

    roles = []
    for dept in departments:
        if dept == 'Engineering':
            roles.append(np.random.choice(['Junior Dev', 'Senior Dev', 'Tech Lead', 'Manager'], p=[0.3, 0.4, 0.2, 0.1]))
        elif dept in ['Sales', 'Marketing']:
            roles.append(np.random.choice(['Associate', 'Senior', 'Manager', 'Director'], p=[0.35, 0.35, 0.2, 0.1]))
        else:
            roles.append(np.random.choice(['Analyst', 'Senior Analyst', 'Manager'], p=[0.45, 0.35, 0.2]))

    # Tenure (years at company)
    tenure = np.random.exponential(scale=3, size=n_employees).clip(0.1, 20)

    # Salary (influenced by role and tenure)
    base_salary = np.random.normal(75000, 25000, n_employees).clip(40000, 200000)

    # Work characteristics
    avg_hours_per_week = np.random.normal(45, 8, n_employees).clip(35, 70)
    remote_work = np.random.choice(['Full Remote', 'Hybrid', 'On-site'], n_employees, p=[0.35, 0.40, 0.25])

    # Manager support score (1-10)
    manager_support = np.random.beta(5, 2, n_employees) * 9 + 1

    # Team size
    team_size = np.random.poisson(8, n_employees).clip(2, 30)

    # Performance metrics (last quarter)
    performance_rating = np.random.normal(3.5, 0.8, n_employees).clip(1, 5)
    goals_completed_pct = np.random.beta(7, 3, n_employees) * 100

    # Overtime patterns (hours per month)
    overtime_hours = np.random.gamma(2, 5, n_employees).clip(0, 80)

    # Leave patterns (days taken in last year)
    sick_leave_days = np.random.poisson(4, n_employees).clip(0, 30)
    vacation_days_taken = np.random.normal(12, 5, n_employees).clip(0, 30)

    # Survey responses (quarterly engagement survey, 1-10 scale)
    job_satisfaction = np.random.beta(5, 3, n_employees) * 9 + 1
    workload_stress = np.random.beta(3, 4, n_employees) * 9 + 1  # Lower is better
    work_life_balance = np.random.beta(4, 3, n_employees) * 9 + 1
    career_growth_satisfaction = np.random.beta(4, 4, n_employees) * 9 + 1

    # Engagement metrics
    last_promotion_months = np.random.exponential(24, n_employees).clip(0, 120)
    training_hours_last_year = np.random.gamma(2, 3, n_employees).clip(0, 50)

    # Generate burnout score (continuous 0-1, this is what we'll predict)
    # Burnout is influenced by multiple factors
    burnout_score = (
        -0.15 * (manager_support / 10) +  # Negative: good support reduces burnout
        0.20 * (overtime_hours / 80) +     # Positive: more overtime increases burnout
        0.15 * (avg_hours_per_week / 70) +
        -0.12 * (work_life_balance / 10) +
        -0.10 * (job_satisfaction / 10) +
        0.18 * (workload_stress / 10) +
        0.08 * (sick_leave_days / 30) +
        -0.08 * (career_growth_satisfaction / 10) +
        0.05 * np.random.normal(0, 1, n_employees)  # Random noise
    )

    # Normalize to 0-1 range
    burnout_score = (burnout_score - burnout_score.min()) / (burnout_score.max() - burnout_score.min())

    # Binary burnout indicator (high risk if score > 0.7)
    burnout_high_risk = (burnout_score > 0.7).astype(int)

    # Create DataFrame
    df = pd.DataFrame({
        'employee_id': employee_ids,
        'age': ages,
        'gender': genders,
        'department': departments,
        'role': roles,
        'tenure_years': np.round(tenure, 2),
        'salary': base_salary.astype(int),
        'avg_hours_per_week': np.round(avg_hours_per_week, 1),
        'overtime_hours_per_month': np.round(overtime_hours, 1),
        'remote_work_type': remote_work,
        'manager_support_score': np.round(manager_support, 2),
        'team_size': team_size,
        'performance_rating': np.round(performance_rating, 2),
        'goals_completed_pct': np.round(goals_completed_pct, 1),
        'sick_leave_days': sick_leave_days,
        'vacation_days_taken': np.round(vacation_days_taken, 1),
        'job_satisfaction': np.round(job_satisfaction, 2),
        'workload_stress': np.round(workload_stress, 2),
        'work_life_balance': np.round(work_life_balance, 2),
        'career_growth_satisfaction': np.round(career_growth_satisfaction, 2),
        'months_since_last_promotion': np.round(last_promotion_months, 1),
        'training_hours_last_year': np.round(training_hours_last_year, 1),
        'burnout_score': np.round(burnout_score, 4),
        'burnout_high_risk': burnout_high_risk
    })

    return df


if __name__ == "__main__":
    import os

    # Generate dataset
    df = generate_employee_data(n_employees=5000)

    # Save to CSV (use absolute path from script location)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(script_dir, '../..')
    output_dir = os.path.join(project_root, 'data/raw')
    output_path = os.path.join(output_dir, 'employee_data.csv')

    df.to_csv(output_path, index=False)

    print(f"\nDataset generated successfully!")
    print(f"Shape: {df.shape}")
    print(f"Saved to: {output_path}")
    print(f"\nBurnout Statistics:")
    print(f"  - High Risk Employees: {df['burnout_high_risk'].sum()} ({df['burnout_high_risk'].mean()*100:.1f}%)")
    print(f"  - Average Burnout Score: {df['burnout_score'].mean():.3f}")
    print(f"  - Median Burnout Score: {df['burnout_score'].median():.3f}")
    print(f"\nFirst few rows:")
    print(df.head())
    print(f"\nData types:")
    print(df.dtypes)
