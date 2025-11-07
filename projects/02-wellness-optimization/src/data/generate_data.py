"""
Generate synthetic wellness optimization dataset.

Creates realistic data for fitness tracking, surveys, and engagement metrics
to demonstrate clustering and personalized recommendation systems.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

def generate_wellness_data(n_users=2000, n_days=90):
    """Generate synthetic wellness data for multiple users over time."""

    print(f"Generating wellness data for {n_users} users over {n_days} days...")

    # User profiles (one-time data)
    user_ids = [f"USER{str(i).zfill(4)}" for i in range(1, n_users + 1)]
    ages = np.random.normal(32, 10, n_users).clip(18, 70).astype(int)
    genders = np.random.choice(['Male', 'Female', 'Other'], n_users, p=[0.48, 0.48, 0.04])

    # Baseline fitness levels (determines daily activity patterns)
    fitness_levels = np.random.choice(['Sedentary', 'Lightly Active', 'Moderately Active', 'Very Active'],
                                      n_users, p=[0.25, 0.35, 0.30, 0.10])

    # Health goals
    goals = np.random.choice(['Weight Loss', 'Build Muscle', 'General Fitness', 'Stress Management', 'Better Sleep'],
                            n_users, p=[0.30, 0.20, 0.25, 0.15, 0.10])

    # BMI
    bmis = np.random.normal(26, 4, n_users).clip(18, 40)

    # Survey data (lifestyle factors)
    diet_preferences = np.random.choice(['Balanced', 'Low Carb', 'Vegetarian', 'Vegan', 'High Protein'],
                                        n_users, p=[0.50, 0.20, 0.15, 0.08, 0.07])

    # Stress levels (1-10)
    baseline_stress = np.random.beta(3, 5, n_users) * 9 + 1

    # Exercise habits (times per week)
    exercise_frequency = {
        'Sedentary': np.random.poisson(1, n_users),
        'Lightly Active': np.random.poisson(2, n_users),
        'Moderately Active': np.random.poisson(4, n_users),
        'Very Active': np.random.poisson(6, n_users)
    }

    # Create user profile DataFrame
    users_df = pd.DataFrame({
        'user_id': user_ids,
        'age': ages,
        'gender': genders,
        'fitness_level': fitness_levels,
        'health_goal': goals,
        'bmi': np.round(bmis, 1),
        'diet_preference': diet_preferences,
        'baseline_stress': np.round(baseline_stress, 2)
    })

    # Generate daily tracking data
    daily_data = []

    for user_idx, user_id in enumerate(user_ids):
        fitness_level = fitness_levels[user_idx]

        # Base parameters based on fitness level
        if fitness_level == 'Sedentary':
            base_steps = 3000
            base_active_min = 10
            base_sleep_hrs = 6.5
        elif fitness_level == 'Lightly Active':
            base_steps = 6000
            base_active_min = 30
            base_sleep_hrs = 7.0
        elif fitness_level == 'Moderately Active':
            base_steps = 9000
            base_active_min = 50
            base_sleep_hrs = 7.5
        else:  # Very Active
            base_steps = 12000
            base_active_min = 80
            base_sleep_hrs = 8.0

        for day in range(n_days):
            date = datetime.now() - timedelta(days=n_days - day)

            # Add weekly variation (weekend effect)
            is_weekend = date.weekday() >= 5
            weekend_factor = 0.7 if is_weekend else 1.0

            # Daily metrics with variation
            steps = int(np.random.normal(base_steps * weekend_factor, base_steps * 0.3))
            active_minutes = int(np.clip(np.random.normal(base_active_min * weekend_factor, base_active_min * 0.4), 0, 200))
            sleep_hours = np.clip(np.random.normal(base_sleep_hrs, 0.8), 4, 12)

            # Heart rate (resting)
            resting_hr = int(np.clip(np.random.normal(70, 10), 50, 100))

            # Calories burned (based on activity)
            calories_burned = int(1500 + steps * 0.04 + active_minutes * 5 + np.random.normal(0, 100))

            # Subjective wellness score (1-10)
            wellness_score = np.random.beta(6, 3) * 9 + 1

            daily_data.append({
                'user_id': user_id,
                'date': date.strftime('%Y-%m-%d'),
                'steps': max(0, steps),
                'active_minutes': max(0, active_minutes),
                'sleep_hours': np.round(sleep_hours, 2),
                'resting_heart_rate': resting_hr,
                'calories_burned': calories_burned,
                'wellness_score': np.round(wellness_score, 2)
            })

    daily_df = pd.DataFrame(daily_data)

    # Aggregate metrics per user (for clustering)
    aggregated = daily_df.groupby('user_id').agg({
        'steps': 'mean',
        'active_minutes': 'mean',
        'sleep_hours': 'mean',
        'resting_heart_rate': 'mean',
        'calories_burned': 'mean',
        'wellness_score': 'mean'
    }).reset_index()

    # Calculate consistency (coefficient of variation - lower is more consistent)
    consistency = daily_df.groupby('user_id').agg({
        'steps': lambda x: np.std(x) / (np.mean(x) + 1),
        'active_minutes': lambda x: np.std(x) / (np.mean(x) + 1)
    }).reset_index()
    consistency.columns = ['user_id', 'steps_consistency', 'activity_consistency']

    # Merge everything
    final_df = users_df.merge(aggregated, on='user_id').merge(consistency, on='user_id')

    # Rename columns for clarity
    final_df.columns = ['user_id', 'age', 'gender', 'fitness_level', 'health_goal', 'bmi',
                        'diet_preference', 'baseline_stress', 'avg_steps', 'avg_active_minutes',
                        'avg_sleep_hours', 'avg_resting_hr', 'avg_calories_burned',
                        'avg_wellness_score', 'steps_consistency', 'activity_consistency']

    return final_df, daily_df


if __name__ == "__main__":
    import os

    # Generate datasets
    user_profiles, daily_tracking = generate_wellness_data(n_users=2000, n_days=90)

    # Save to CSV
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(script_dir, '../..')
    output_dir = os.path.join(project_root, 'data/raw')

    profiles_path = os.path.join(output_dir, 'user_profiles.csv')
    daily_path = os.path.join(output_dir, 'daily_tracking.csv')

    user_profiles.to_csv(profiles_path, index=False)
    daily_tracking.to_csv(daily_path, index=False)

    print(f"\n✓ Datasets generated successfully!")
    print(f"\n📊 User Profiles:")
    print(f"  - Shape: {user_profiles.shape}")
    print(f"  - Saved to: {profiles_path}")

    print(f"\n📈 Daily Tracking Data:")
    print(f"  - Shape: {daily_tracking.shape}")
    print(f"  - Date range: {daily_tracking['date'].min()} to {daily_tracking['date'].max()}")
    print(f"  - Saved to: {daily_path}")

    print(f"\n🏋️ Fitness Level Distribution:")
    print(user_profiles['fitness_level'].value_counts())

    print(f"\n🎯 Health Goals Distribution:")
    print(user_profiles['health_goal'].value_counts())

    print(f"\nSample user profile:")
    print(user_profiles.head(3))
