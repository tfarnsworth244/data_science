"""
Generate synthetic employee engagement dataset with multi-modal features.

Creates realistic data for employee surveys, feedback patterns, and engagement metrics
to demonstrate CNN/deep learning models for engagement prediction.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

def generate_engagement_data(n_employees=2000, n_surveys=8):
    """Generate synthetic engagement data with multi-dimensional features."""

    print(f"Generating engagement data for {n_employees} employees across {n_surveys} survey periods...")

    # Survey categories (12 dimensions for engagement)
    survey_dimensions = [
        'job_satisfaction',
        'work_life_balance',
        'career_development',
        'manager_relationship',
        'team_collaboration',
        'company_culture',
        'recognition',
        'compensation_fairness',
        'work_meaningfulness',
        'autonomy',
        'resources_support',
        'innovation_encouraged'
    ]

    # Employee baseline profiles
    employees = []
    departments = ['Engineering', 'Product', 'Sales', 'Marketing', 'Operations',
                  'Customer Success', 'Finance', 'HR', 'Legal', 'Data']

    for emp_id in range(1, n_employees + 1):
        # Demographics
        age = int(np.clip(np.random.normal(32, 8), 22, 65))
        tenure_months = int(np.clip(np.random.gamma(3, 8), 1, 240))
        department = random.choice(departments)
        seniority = np.random.choice(['IC1', 'IC2', 'IC3', 'IC4', 'Manager', 'Senior Manager', 'Director'],
                                    p=[0.25, 0.25, 0.20, 0.12, 0.10, 0.05, 0.03])

        # Personality/work factors
        intrinsic_motivation = np.random.beta(5, 3)
        learning_orientation = np.random.beta(5, 3)
        social_connection = np.random.beta(5, 4)

        employees.append({
            'employee_id': f"EMP{str(emp_id).zfill(5)}",
            'age': age,
            'tenure_months': tenure_months,
            'department': department,
            'seniority': seniority,
            'intrinsic_motivation': np.round(intrinsic_motivation, 3),
            'learning_orientation': np.round(learning_orientation, 3),
            'social_connection': np.round(social_connection, 3)
        })

    employees_df = pd.DataFrame(employees)

    # Generate survey responses over time
    survey_responses = []
    response_id = 1

    for survey_num in range(1, n_surveys + 1):
        survey_date = datetime.now() - timedelta(days=(n_surveys - survey_num) * 45)  # Quarterly

        for _, emp in employees_df.iterrows():
            # Response rate (some employees skip surveys)
            if random.random() < 0.15:  # 15% skip rate
                continue

            # Calculate engagement trajectory
            # Newer employees often more engaged, then it dips, then stabilizes
            tenure_effect = 0.8 if emp['tenure_months'] < 6 else \
                          0.6 if emp['tenure_months'] < 24 else \
                          0.7

            # Base engagement from personality
            base_engagement = (
                emp['intrinsic_motivation'] * 0.4 +
                emp['learning_orientation'] * 0.3 +
                emp['social_connection'] * 0.3
            )

            # Temporal effects (engagement can change over surveys)
            time_variance = np.random.normal(0, 0.1)

            # Calculate overall engagement
            overall_engagement = np.clip(
                base_engagement * tenure_effect + time_variance,
                0, 1
            )

            # Generate scores for each dimension (1-10 scale)
            dimension_scores = {}

            for dim in survey_dimensions:
                # Each dimension correlates with overall engagement but has variance
                base_score = overall_engagement * 9 + 1

                # Dimension-specific factors
                if dim == 'manager_relationship':
                    # Managers often rate this higher
                    if 'Manager' in emp['seniority'] or 'Director' in emp['seniority']:
                        base_score += np.random.uniform(0, 1)

                elif dim == 'career_development':
                    # Learning-oriented people care more about this
                    base_score += emp['learning_orientation'] * 2 - 1

                elif dim == 'team_collaboration':
                    # Social connection matters here
                    base_score += emp['social_connection'] * 2 - 1

                elif dim == 'compensation_fairness':
                    # Tenure affects perception
                    if emp['tenure_months'] > 36:
                        base_score -= np.random.uniform(0, 1.5)

                # Add noise and clip
                score = np.clip(base_score + np.random.normal(0, 0.8), 1, 10)
                dimension_scores[dim] = np.round(score, 1)

            # Additional metrics
            would_recommend = int(overall_engagement > 0.7)
            likelihood_to_stay = np.round(overall_engagement * 9 + 1, 1)
            satisfaction_change = np.round(np.random.normal(0, 1), 1)  # vs previous survey

            # Free text sentiment (simulated as score)
            feedback_sentiment = np.round(overall_engagement, 3)
            feedback_length_words = int(np.clip(np.random.gamma(3, 15), 5, 200))

            # Behavioral indicators
            participated_in_events = int(np.random.choice([0, 1], p=[1-overall_engagement, overall_engagement]))
            training_hours_completed = int(np.clip(overall_engagement * 20 + np.random.normal(0, 5), 0, 100))

            # Create response record
            response_record = {
                'response_id': f"RESP{str(response_id).zfill(6)}",
                'employee_id': emp['employee_id'],
                'survey_number': survey_num,
                'survey_date': survey_date.strftime('%Y-%m-%d'),
                'overall_engagement_score': np.round(overall_engagement * 100, 1),
                **dimension_scores,
                'would_recommend': would_recommend,
                'likelihood_to_stay': likelihood_to_stay,
                'satisfaction_change': satisfaction_change,
                'feedback_sentiment': feedback_sentiment,
                'feedback_length_words': feedback_length_words,
                'participated_in_events': participated_in_events,
                'training_hours_completed': training_hours_completed
            }

            survey_responses.append(response_record)
            response_id += 1

    survey_df = pd.DataFrame(survey_responses)

    # Generate engagement outcomes (attrition risk)
    outcomes = []

    for _, emp in employees_df.iterrows():
        emp_surveys = survey_df[survey_df['employee_id'] == emp['employee_id']]

        if len(emp_surveys) == 0:
            continue

        # Calculate attrition risk based on engagement trend
        recent_engagement = emp_surveys['overall_engagement_score'].tail(3).mean()
        engagement_trend = emp_surveys['overall_engagement_score'].diff().mean()

        # Low engagement = high risk
        attrition_risk = 1 - (recent_engagement / 100)

        # Declining trend increases risk
        if engagement_trend < -5:
            attrition_risk += 0.2
        elif engagement_trend > 5:
            attrition_risk -= 0.1

        attrition_risk = np.clip(attrition_risk, 0, 1)

        # Actual attrition (binary outcome)
        did_leave = int(np.random.random() < attrition_risk)

        outcomes.append({
            'employee_id': emp['employee_id'],
            'num_surveys_completed': len(emp_surveys),
            'avg_engagement': np.round(emp_surveys['overall_engagement_score'].mean(), 1),
            'latest_engagement': np.round(recent_engagement, 1),
            'engagement_trend': np.round(engagement_trend, 2),
            'attrition_risk': np.round(attrition_risk, 3),
            'did_leave': did_leave
        })

    outcomes_df = pd.DataFrame(outcomes)

    return employees_df, survey_df, outcomes_df


if __name__ == "__main__":
    import os

    # Generate datasets
    employees, surveys, outcomes = generate_engagement_data(n_employees=2000, n_surveys=8)

    # Save to CSV
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(script_dir, '../..')
    output_dir = os.path.join(project_root, 'data/raw')

    os.makedirs(output_dir, exist_ok=True)

    employees_path = os.path.join(output_dir, 'employees.csv')
    surveys_path = os.path.join(output_dir, 'survey_responses.csv')
    outcomes_path = os.path.join(output_dir, 'engagement_outcomes.csv')

    employees.to_csv(employees_path, index=False)
    surveys.to_csv(surveys_path, index=False)
    outcomes.to_csv(outcomes_path, index=False)

    print(f"\n✓ Datasets generated successfully!")

    print(f"\n👥 Employees:")
    print(f"  Shape: {employees.shape}")
    print(f"  Saved to: {employees_path}")

    print(f"\n📋 Survey Responses:")
    print(f"  Shape: {surveys.shape}")
    print(f"  Total responses: {len(surveys)}")
    print(f"  Saved to: {surveys_path}")

    print(f"\n📊 Engagement Outcomes:")
    print(f"  Shape: {outcomes.shape}")
    print(f"  Saved to: {outcomes_path}")

    print(f"\n🏢 Department Distribution:")
    print(employees['department'].value_counts())

    print(f"\n📈 Engagement Metrics:")
    print(f"Average engagement score: {surveys['overall_engagement_score'].mean():.1f}/100")
    print(f"Median engagement: {surveys['overall_engagement_score'].median():.1f}/100")

    print(f"\n💬 Survey Participation:")
    response_rate = len(surveys) / (len(employees) * 8) * 100
    print(f"Overall response rate: {response_rate:.1f}%")

    print(f"\n👍 Recommendation Rate:")
    recommend_rate = surveys['would_recommend'].mean() * 100
    print(f"{recommend_rate:.1f}% would recommend the company")

    print(f"\n📉 Attrition Analysis:")
    attrition_rate = outcomes['did_leave'].mean() * 100
    print(f"Overall attrition rate: {attrition_rate:.1f}%")
    print(f"Average attrition risk: {outcomes['attrition_risk'].mean():.3f}")

    print(f"\n🎯 Engagement Levels:")
    high_engagement = len(surveys[surveys['overall_engagement_score'] > 70])
    low_engagement = len(surveys[surveys['overall_engagement_score'] < 40])
    print(f"High engagement (>70): {high_engagement} ({high_engagement/len(surveys)*100:.1f}%)")
    print(f"Low engagement (<40): {low_engagement} ({low_engagement/len(surveys)*100:.1f}%)")

    print(f"\n📊 Top Engagement Dimensions:")
    dimension_cols = ['job_satisfaction', 'work_life_balance', 'career_development',
                     'manager_relationship', 'team_collaboration', 'company_culture']
    dim_means = surveys[dimension_cols].mean().sort_values(ascending=False)
    print(dim_means.head().to_string())

    print(f"\n⚠️ Lowest Rated Dimensions:")
    print(dim_means.tail().to_string())
