"""
Generate synthetic burnout time series dataset.

Creates realistic longitudinal data for employees with weekly measurements
to demonstrate time series forecasting and LSTM models for burnout prediction.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

def generate_time_series_data(n_employees=300, n_weeks=52):
    """Generate synthetic time series data for burnout tracking."""

    print(f"Generating time series data for {n_employees} employees over {n_weeks} weeks...")

    # Employee baseline characteristics
    employees = []

    for emp_id in range(1, n_employees + 1):
        # Baseline burnout risk (some employees more susceptible)
        baseline_risk = np.random.beta(3, 5)

        # Personal resilience factor
        resilience = np.random.beta(5, 3)

        # Work characteristics
        avg_weekly_hours = np.clip(np.random.normal(45, 8), 35, 70)
        has_flexible_schedule = int(np.random.choice([0, 1], p=[0.4, 0.6]))
        remote_work = np.random.choice(['Full Remote', 'Hybrid', 'Full Office'], p=[0.3, 0.4, 0.3])

        employees.append({
            'employee_id': f"EMP{str(emp_id).zfill(4)}",
            'baseline_burnout_risk': np.round(baseline_risk, 3),
            'resilience_score': np.round(resilience, 3),
            'avg_weekly_hours': np.round(avg_weekly_hours, 1),
            'has_flexible_schedule': has_flexible_schedule,
            'remote_work_type': remote_work,
            'department': random.choice(['Engineering', 'Sales', 'Marketing', 'Operations',
                                        'Product', 'Customer Success', 'HR', 'Finance'])
        })

    employees_df = pd.DataFrame(employees)

    # Generate weekly time series data
    time_series_data = []

    for _, emp in employees_df.iterrows():
        # Initialize burnout trajectory
        current_burnout = emp['baseline_burnout_risk'] * 0.5  # Start lower

        # Trend: some employees burnout increases, some decreases, most stable with fluctuation
        trend_type = np.random.choice(['increasing', 'stable', 'decreasing'], p=[0.35, 0.50, 0.15])

        if trend_type == 'increasing':
            weekly_trend = np.random.uniform(0.005, 0.015)  # Gradual increase
        elif trend_type == 'decreasing':
            weekly_trend = np.random.uniform(-0.010, -0.005)  # Gradual improvement
        else:
            weekly_trend = np.random.uniform(-0.002, 0.002)  # Mostly stable

        # Seasonality (vacation periods, year-end stress, etc.)
        for week in range(1, n_weeks + 1):
            week_date = datetime.now() - timedelta(weeks=n_weeks - week)

            # Seasonal factors
            month = week_date.month

            # End of quarter stress (March, June, Sept, Dec)
            if month in [3, 6, 9, 12]:
                seasonal_stress = np.random.uniform(0.05, 0.15)
            # Holiday season (Nov-Dec)
            elif month in [11, 12]:
                seasonal_stress = np.random.uniform(-0.05, 0.10)
            # Summer months (less stress)
            elif month in [7, 8]:
                seasonal_stress = np.random.uniform(-0.10, 0.05)
            else:
                seasonal_stress = np.random.uniform(-0.05, 0.05)

            # Work factors for this week
            hours_this_week = emp['avg_weekly_hours'] + np.random.normal(0, 5)
            hours_this_week = np.clip(hours_this_week, 20, 80)

            # Overtime effect
            overtime_effect = max(0, (hours_this_week - 40) * 0.01)

            # Workload (1-10)
            workload = np.clip(np.random.normal(6, 1.5), 1, 10)

            # Support factors
            manager_support = np.clip(np.random.normal(7, 1.5), 1, 10)
            peer_support = np.clip(np.random.normal(7, 1.5), 1, 10)

            # Life events (occasionally)
            has_life_stressor = int(np.random.choice([0, 1], p=[0.85, 0.15]))
            life_stressor_impact = np.random.uniform(0.1, 0.3) if has_life_stressor else 0

            # Calculate burnout change
            burnout_change = (
                weekly_trend +
                seasonal_stress +
                overtime_effect +
                (workload - 5) * 0.01 -
                (manager_support - 5) * 0.01 -
                (peer_support - 5) * 0.005 +
                life_stressor_impact -
                emp['resilience_score'] * 0.01 +
                np.random.normal(0, 0.03)  # Random noise
            )

            # Update burnout level
            current_burnout = np.clip(current_burnout + burnout_change, 0, 1)

            # Physical symptoms (correlate with burnout)
            sleep_quality = np.clip(10 - current_burnout * 10 + np.random.normal(0, 1), 1, 10)
            energy_level = np.clip(10 - current_burnout * 10 + np.random.normal(0, 1), 1, 10)

            # Emotional state
            stress_level = np.clip(current_burnout * 10 + np.random.normal(0, 1), 1, 10)
            mood_score = np.clip(10 - current_burnout * 10 + np.random.normal(0, 1.5), 1, 10)

            # Behavioral indicators
            missed_deadlines = int(np.random.poisson(current_burnout * 2))
            sick_days = int(np.random.poisson(current_burnout * 0.5))

            # Job satisfaction
            job_satisfaction = np.clip(10 - current_burnout * 12 + np.random.normal(0, 1), 1, 10)

            # Engagement metrics
            meeting_participation = np.clip(10 - current_burnout * 8 + np.random.normal(0, 1.5), 1, 10)
            collaboration_score = np.clip(10 - current_burnout * 8 + np.random.normal(0, 1), 1, 10)

            time_series_data.append({
                'employee_id': emp['employee_id'],
                'week_number': week,
                'date': week_date.strftime('%Y-%m-%d'),
                'burnout_score': np.round(current_burnout, 3),
                'hours_worked': np.round(hours_this_week, 1),
                'workload_rating': np.round(workload, 1),
                'manager_support': np.round(manager_support, 1),
                'peer_support': np.round(peer_support, 1),
                'sleep_quality': np.round(sleep_quality, 1),
                'energy_level': np.round(energy_level, 1),
                'stress_level': np.round(stress_level, 1),
                'mood_score': np.round(mood_score, 1),
                'job_satisfaction': np.round(job_satisfaction, 1),
                'meeting_participation': np.round(meeting_participation, 1),
                'collaboration_score': np.round(collaboration_score, 1),
                'missed_deadlines': missed_deadlines,
                'sick_days': sick_days,
                'has_life_stressor': has_life_stressor
            })

    time_series_df = pd.DataFrame(time_series_data)

    return employees_df, time_series_df


if __name__ == "__main__":
    import os

    # Generate datasets
    employees, time_series = generate_time_series_data(n_employees=300, n_weeks=52)

    # Save to CSV
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(script_dir, '../..')
    output_dir = os.path.join(project_root, 'data/raw')

    os.makedirs(output_dir, exist_ok=True)

    employees_path = os.path.join(output_dir, 'employees_baseline.csv')
    time_series_path = os.path.join(output_dir, 'burnout_time_series.csv')

    employees.to_csv(employees_path, index=False)
    time_series.to_csv(time_series_path, index=False)

    print(f"\n✓ Datasets generated successfully!")

    print(f"\n👥 Employees Baseline:")
    print(f"  Shape: {employees.shape}")
    print(f"  Saved to: {employees_path}")

    print(f"\n📈 Time Series Data:")
    print(f"  Shape: {time_series.shape}")
    print(f"  Total observations: {len(time_series)}")
    print(f"  Saved to: {time_series_path}")

    print(f"\n🏢 Department Distribution:")
    print(employees['department'].value_counts())

    print(f"\n📊 Burnout Trends:")
    print(f"Average burnout score: {time_series['burnout_score'].mean():.3f}")
    print(f"Min burnout: {time_series['burnout_score'].min():.3f}")
    print(f"Max burnout: {time_series['burnout_score'].max():.3f}")

    print(f"\n⏰ Work Hours:")
    print(f"Average weekly hours: {time_series['hours_worked'].mean():.1f}")
    print(f"Max weekly hours: {time_series['hours_worked'].max():.1f}")

    print(f"\n😴 Wellbeing Indicators:")
    print(f"Average sleep quality: {time_series['sleep_quality'].mean():.1f}/10")
    print(f"Average energy level: {time_series['energy_level'].mean():.1f}/10")
    print(f"Average stress level: {time_series['stress_level'].mean():.1f}/10")

    print(f"\n📅 Time Range:")
    print(f"From: {time_series['date'].min()}")
    print(f"To: {time_series['date'].max()}")

    print(f"\n🎯 High Burnout Episodes (>0.7):")
    high_burnout = len(time_series[time_series['burnout_score'] > 0.7])
    print(f"Count: {high_burnout} ({high_burnout/len(time_series)*100:.1f}% of observations)")

    print(f"\n📉 Sample Employee Trajectory:")
    sample_emp = time_series[time_series['employee_id'] == 'EMP0001'][['week_number', 'burnout_score', 'stress_level', 'job_satisfaction']].head(10)
    print(sample_emp.to_string(index=False))
