"""
Generate synthetic team composition and interaction dataset.

Creates realistic data for teams, members, interactions, and performance
to demonstrate network analysis and team dynamics modeling.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import itertools

np.random.seed(42)
random.seed(42)

def generate_team_data(n_employees=500, n_teams=50):
    """Generate synthetic team composition and interaction data."""

    print(f"Generating team data for {n_employees} employees across {n_teams} teams...")

    # Employee profiles
    employees = []
    personality_types = ['Analytical', 'Driver', 'Expressive', 'Amiable']
    work_styles = ['Independent', 'Collaborative', 'Structured', 'Flexible']
    seniority_levels = ['Junior', 'Mid', 'Senior', 'Lead', 'Manager']

    for emp_id in range(1, n_employees + 1):
        employees.append({
            'employee_id': f"EMP{str(emp_id).zfill(4)}",
            'personality_type': random.choice(personality_types),
            'work_style': random.choice(work_styles),
            'seniority': np.random.choice(seniority_levels, p=[0.30, 0.35, 0.20, 0.10, 0.05]),
            'technical_skill': np.round(np.random.beta(5, 3) * 100, 1),
            'communication_skill': np.round(np.random.beta(5, 3) * 100, 1),
            'leadership_skill': np.round(np.random.beta(4, 5) * 100, 1),
            'years_experience': np.round(np.random.gamma(3, 1.5), 1),
            'collaboration_score': np.round(np.random.beta(6, 3) * 100, 1)
        })

    employees_df = pd.DataFrame(employees)

    # Teams
    teams = []
    project_types = ['Product Development', 'Research', 'Operations', 'Marketing',
                    'Sales', 'Customer Success', 'Infrastructure', 'Analytics']

    for team_id in range(1, n_teams + 1):
        team_size = int(np.clip(np.random.gamma(2.5, 2), 3, 15))

        teams.append({
            'team_id': f"TEAM{str(team_id).zfill(3)}",
            'team_name': f"{random.choice(project_types)} Team {team_id}",
            'project_type': random.choice(project_types),
            'team_size': team_size,
            'formation_date': (datetime.now() - timedelta(days=random.randint(90, 730))).strftime('%Y-%m-%d'),
            'is_cross_functional': int(np.random.choice([0, 1], p=[0.4, 0.6]))
        })

    teams_df = pd.DataFrame(teams)

    # Assign employees to teams
    team_members = []
    available_employees = employees_df['employee_id'].tolist()
    random.shuffle(available_employees)

    member_id = 1
    for _, team in teams_df.iterrows():
        # Select team members
        if len(available_employees) >= team['team_size']:
            selected_members = available_employees[:team['team_size']]
            available_employees = available_employees[team['team_size']:]
        else:
            # If we run out, reassign some employees (they can be on multiple teams)
            selected_members = random.sample(employees_df['employee_id'].tolist(), team['team_size'])

        for emp_id in selected_members:
            emp_data = employees_df[employees_df['employee_id'] == emp_id].iloc[0]

            # Role in team
            if emp_data['seniority'] in ['Manager', 'Lead']:
                role = random.choice(['Team Lead', 'Technical Lead'])
            elif emp_data['seniority'] == 'Senior':
                role = random.choice(['Senior Member', 'Technical Lead'])
            else:
                role = 'Team Member'

            team_members.append({
                'member_id': f"MEM{str(member_id).zfill(5)}",
                'team_id': team['team_id'],
                'employee_id': emp_id,
                'role': role,
                'join_date': team['formation_date'],
                'is_active': int(np.random.choice([0, 1], p=[0.1, 0.9]))
            })
            member_id += 1

    team_members_df = pd.DataFrame(team_members)

    # Generate interactions between team members
    interactions = []
    interaction_types = ['Meeting', 'Code Review', 'Pair Programming', 'Discussion',
                        'Collaboration', 'Mentoring', 'Brainstorming']

    interaction_id = 1

    for _, team in teams_df.iterrows():
        team_emps = team_members_df[team_members_df['team_id'] == team['team_id']]['employee_id'].tolist()

        # Generate interactions between pairs of team members
        if len(team_emps) < 2:
            continue

        # Create interaction network (not all pairs interact equally)
        for emp1, emp2 in itertools.combinations(team_emps, 2):
            # Interaction frequency (some pairs interact more than others)
            if random.random() < 0.6:  # 60% of pairs have recorded interactions
                num_interactions = int(np.clip(np.random.poisson(5), 1, 30))

                for _ in range(num_interactions):
                    interaction_date = datetime.now() - timedelta(days=random.randint(0, 180))

                    # Duration in minutes
                    interaction_type = random.choice(interaction_types)
                    if interaction_type == 'Meeting':
                        duration = int(np.random.gamma(4, 10))
                    elif interaction_type in ['Code Review', 'Mentoring']:
                        duration = int(np.random.gamma(3, 15))
                    else:
                        duration = int(np.random.gamma(2, 8))

                    # Interaction quality (1-10)
                    quality = np.round(np.random.beta(6, 3) * 9 + 1, 1)

                    interactions.append({
                        'interaction_id': f"INT{str(interaction_id).zfill(6)}",
                        'team_id': team['team_id'],
                        'employee_1': emp1,
                        'employee_2': emp2,
                        'interaction_type': interaction_type,
                        'date': interaction_date.strftime('%Y-%m-%d'),
                        'duration_minutes': duration,
                        'quality_score': quality
                    })
                    interaction_id += 1

    interactions_df = pd.DataFrame(interactions)

    # Team performance metrics
    team_performance = []

    for _, team in teams_df.iterrows():
        # Get team members
        team_emps = team_members_df[team_members_df['team_id'] == team['team_id']]['employee_id'].tolist()
        team_emp_data = employees_df[employees_df['employee_id'].isin(team_emps)]

        # Calculate team composition metrics
        avg_technical = team_emp_data['technical_skill'].mean()
        avg_communication = team_emp_data['communication_skill'].mean()
        avg_collaboration = team_emp_data['collaboration_score'].mean()

        # Diversity scores
        personality_diversity = len(team_emp_data['personality_type'].unique()) / len(personality_types)
        seniority_diversity = len(team_emp_data['seniority'].unique()) / len(seniority_levels)

        # Team interactions
        team_interactions = interactions_df[interactions_df['team_id'] == team['team_id']]
        avg_interaction_quality = team_interactions['quality_score'].mean() if len(team_interactions) > 0 else 0

        # Calculate team performance (influenced by multiple factors)
        performance_factors = [
            avg_technical / 100 * 0.3,
            avg_communication / 100 * 0.25,
            avg_collaboration / 100 * 0.2,
            personality_diversity * 0.15,
            (avg_interaction_quality / 10) * 0.1
        ]

        team_performance_score = np.clip(sum(performance_factors) + np.random.normal(0, 0.1), 0, 1)

        # Productivity metrics
        velocity = int(team_performance_score * 50 + np.random.normal(0, 5))
        quality_score = np.round(team_performance_score * 90 + np.random.uniform(5, 10), 1)
        innovation_score = np.round(personality_diversity * 80 + np.random.uniform(10, 20), 1)

        team_performance.append({
            'team_id': team['team_id'],
            'performance_score': np.round(team_performance_score * 100, 1),
            'velocity': max(0, velocity),
            'quality_score': np.clip(quality_score, 0, 100),
            'innovation_score': np.clip(innovation_score, 0, 100),
            'avg_technical_skill': np.round(avg_technical, 1),
            'avg_communication_skill': np.round(avg_communication, 1),
            'avg_collaboration_score': np.round(avg_collaboration, 1),
            'personality_diversity': np.round(personality_diversity, 2),
            'seniority_diversity': np.round(seniority_diversity, 2),
            'avg_interaction_quality': np.round(avg_interaction_quality, 2),
            'total_interactions': len(team_interactions)
        })

    team_performance_df = pd.DataFrame(team_performance)

    return employees_df, teams_df, team_members_df, interactions_df, team_performance_df


if __name__ == "__main__":
    import os

    # Generate datasets
    employees, teams, team_members, interactions, team_performance = generate_team_data(
        n_employees=500,
        n_teams=50
    )

    # Save to CSV
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(script_dir, '../..')
    output_dir = os.path.join(project_root, 'data/raw')

    os.makedirs(output_dir, exist_ok=True)

    employees_path = os.path.join(output_dir, 'employees.csv')
    teams_path = os.path.join(output_dir, 'teams.csv')
    members_path = os.path.join(output_dir, 'team_members.csv')
    interactions_path = os.path.join(output_dir, 'interactions.csv')
    performance_path = os.path.join(output_dir, 'team_performance.csv')

    employees.to_csv(employees_path, index=False)
    teams.to_csv(teams_path, index=False)
    team_members.to_csv(members_path, index=False)
    interactions.to_csv(interactions_path, index=False)
    team_performance.to_csv(performance_path, index=False)

    print(f"\n✓ Datasets generated successfully!")

    print(f"\n👥 Employees: {employees.shape}")
    print(f"   Saved to: {employees_path}")

    print(f"\n🏆 Teams: {teams.shape}")
    print(f"   Saved to: {teams_path}")

    print(f"\n👤 Team Members: {team_members.shape}")
    print(f"   Saved to: {members_path}")

    print(f"\n🤝 Interactions: {interactions.shape}")
    print(f"   Saved to: {interactions_path}")

    print(f"\n📊 Team Performance: {team_performance.shape}")
    print(f"   Saved to: {performance_path}")

    print(f"\n📈 Personality Distribution:")
    print(employees['personality_type'].value_counts())

    print(f"\n🎯 Average Team Performance:")
    print(f"Performance Score: {team_performance['performance_score'].mean():.1f}/100")
    print(f"Quality Score: {team_performance['quality_score'].mean():.1f}/100")
    print(f"Innovation Score: {team_performance['innovation_score'].mean():.1f}/100")

    print(f"\n🔢 Team Size Distribution:")
    print(teams['team_size'].describe())

    print(f"\n💬 Interaction Types:")
    print(interactions['interaction_type'].value_counts())

    print(f"\n🌟 Top Performing Teams:")
    top_teams = team_performance.nlargest(5, 'performance_score')[['team_id', 'performance_score', 'velocity', 'quality_score']]
    print(top_teams.to_string(index=False))
