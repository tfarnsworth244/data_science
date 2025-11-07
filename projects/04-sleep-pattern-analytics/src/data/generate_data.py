"""
Generate synthetic sleep pattern analytics dataset.

Creates realistic data for sleep tracking, productivity logs, and cognitive tests
to demonstrate correlation analysis between sleep and performance.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

def generate_sleep_data(n_users=80, n_days=120):
    """Generate synthetic sleep and productivity data."""

    print(f"Generating sleep data for {n_users} users over {n_days} days...")

    # User profiles
    user_ids = [f"USER{str(i).zfill(3)}" for i in range(1, n_users + 1)]
    ages = np.clip(np.random.normal(35, 8, n_users), 25, 55).astype(int)

    # Chronotype (morning person vs night owl)
    chronotypes = np.random.choice(['Early Bird', 'Neutral', 'Night Owl'], n_users, p=[0.25, 0.50, 0.25])

    # Baseline sleep need (hours)
    baseline_sleep = np.clip(np.random.normal(7.5, 0.8, n_users), 6, 9)

    daily_data = []

    for user_idx, user_id in enumerate(user_ids):
        chronotype = chronotypes[user_idx]
        target_sleep = baseline_sleep[user_idx]

        # Chronotype affects sleep timing
        if chronotype == 'Early Bird':
            base_bedtime = 22.0  # 10 PM
        elif chronotype == 'Night Owl':
            base_bedtime = 1.0   # 1 AM
        else:
            base_bedtime = 23.5  # 11:30 PM

        for day in range(n_days):
            date = datetime.now() - timedelta(days=n_days - day)
            is_weekend = date.weekday() >= 5

            # Weekend sleep patterns differ
            if is_weekend:
                sleep_duration = np.clip(np.random.normal(target_sleep + 0.8, 0.9), 4, 12)
                bedtime_shift = np.random.uniform(0, 2)  # Later on weekends
            else:
                sleep_duration = np.clip(np.random.normal(target_sleep - 0.3, 1.0), 4, 12)
                bedtime_shift = np.random.uniform(-0.5, 0.5)

            # Sleep quality metrics
            deep_sleep_pct = np.random.beta(3, 5) * 40 + 10  # 10-50%
            rem_sleep_pct = np.random.beta(4, 4) * 35 + 10   # 10-45%
            wake_ups = np.clip(np.random.poisson(2), 0, 8)
            sleep_efficiency = np.random.beta(8, 2) * 30 + 70  # 70-100%

            # Productivity metrics (influenced by sleep)
            # Good sleep = better productivity
            sleep_quality_factor = (sleep_efficiency / 100) * (1 - abs(sleep_duration - target_sleep) / 3)

            focus_hours = np.clip(np.random.normal(4 + 2 * sleep_quality_factor, 1.5), 0, 10)
            tasks_completed = int(np.clip(np.random.poisson(max(0.1, 5 * sleep_quality_factor)), 0, 15))

            # Cognitive test scores (reaction time, working memory, attention)
            reaction_time_ms = int(np.clip(np.random.normal(350 - 100 * sleep_quality_factor, 50), 200, 600))
            working_memory_score = int(np.clip(np.random.normal(60 + 30 * sleep_quality_factor, 10), 0, 100))
            attention_score = int(np.clip(np.random.normal(65 + 25 * sleep_quality_factor, 12), 0, 100))

            # Context variables
            caffeine_mg = int(np.clip(np.random.gamma(2, 50), 0, 600))
            exercise_minutes = int(np.clip(np.random.exponential(20), 0, 120))
            stress_level = int(np.random.beta(3, 5) * 9 + 1)  # 1-10

            # Self-reported energy
            mental_clarity = int(np.random.beta(4 + 2 * sleep_quality_factor, 4) * 9 + 1)

            daily_data.append({
                'user_id': user_id,
                'date': date.strftime('%Y-%m-%d'),
                'sleep_duration_hrs': np.round(sleep_duration, 2),
                'deep_sleep_pct': np.round(deep_sleep_pct, 1),
                'rem_sleep_pct': np.round(rem_sleep_pct, 1),
                'wake_ups': wake_ups,
                'sleep_efficiency_pct': np.round(sleep_efficiency, 1),
                'bedtime_hr': np.round(base_bedtime + bedtime_shift, 2),
                'focus_hours': np.round(focus_hours, 2),
                'tasks_completed': tasks_completed,
                'reaction_time_ms': reaction_time_ms,
                'working_memory_score': working_memory_score,
                'attention_score': attention_score,
                'caffeine_mg': caffeine_mg,
                'exercise_minutes': exercise_minutes,
                'stress_level': stress_level,
                'mental_clarity': mental_clarity
            })

    df = pd.DataFrame(daily_data)

    # Add user profiles
    users_df = pd.DataFrame({
        'user_id': user_ids,
        'age': ages,
        'chronotype': chronotypes,
        'target_sleep_hrs': np.round(baseline_sleep, 2)
    })

    return df, users_df


if __name__ == "__main__":
    import os

    daily_df, users_df = generate_sleep_data(n_users=80, n_days=120)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(script_dir, '../..')
    output_dir = os.path.join(project_root, 'data/raw')

    daily_path = os.path.join(output_dir, 'sleep_daily.csv')
    users_path = os.path.join(output_dir, 'users.csv')

    daily_df.to_csv(daily_path, index=False)
    users_df.to_csv(users_path, index=False)

    print(f"\n✓ Datasets generated!")
    print(f"Daily sleep data: {daily_df.shape} -> {daily_path}")
    print(f"User profiles: {users_df.shape} -> {users_path}")
    print(f"\nSleep Statistics:")
    print(f"  Avg sleep duration: {daily_df['sleep_duration_hrs'].mean():.2f} hrs")
    print(f"  Avg focus hours: {daily_df['focus_hours'].mean():.2f} hrs")
    print(f"  Correlation (sleep × focus): {daily_df['sleep_duration_hrs'].corr(daily_df['focus_hours']):.3f}")
