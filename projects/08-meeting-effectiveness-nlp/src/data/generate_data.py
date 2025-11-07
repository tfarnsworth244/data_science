"""
Generate synthetic meeting effectiveness dataset.

Creates realistic meeting transcripts, sentiment data, and effectiveness metrics
to demonstrate NLP and sentiment analysis for meeting quality assessment.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

def generate_meeting_data(n_meetings=1000):
    """Generate synthetic meeting transcript and effectiveness data."""

    print(f"Generating meeting data for {n_meetings} meetings...")

    meeting_types = ['Planning', 'Retrospective', 'Standup', 'Review', 'Brainstorming',
                    'Decision-Making', 'Status Update', 'One-on-One', 'All-Hands']

    # Sample utterance templates for different meeting qualities
    positive_utterances = [
        "Great idea! Let's explore that further.",
        "I agree with this approach. It makes sense.",
        "This is exactly what we need. Well done.",
        "Excellent point. I hadn't considered that.",
        "I'm excited about this direction. Let's move forward.",
        "This solution addresses our concerns perfectly.",
        "I appreciate everyone's input today.",
        "We're making great progress on this.",
        "That's a really innovative approach.",
        "I think we've reached a good decision here."
    ]

    neutral_utterances = [
        "Let me share my screen to show the data.",
        "We have three items on the agenda today.",
        "The deadline for this is next Friday.",
        "I'll take the action item to follow up.",
        "Can everyone see the presentation?",
        "Let's move to the next topic.",
        "I'll send out the meeting notes later.",
        "We should schedule a follow-up meeting.",
        "The project timeline is on track.",
        "Here are the key metrics from last week."
    ]

    negative_utterances = [
        "I'm not sure this is the right approach.",
        "We've discussed this several times already.",
        "This doesn't align with our objectives.",
        "I'm concerned about the timeline here.",
        "We're going in circles on this topic.",
        "I don't think we have enough information to decide.",
        "This seems like a waste of time honestly.",
        "We should have resolved this weeks ago.",
        "I disagree with this direction completely.",
        "This meeting could have been an email."
    ]

    meetings = []

    for meeting_id in range(1, n_meetings + 1):
        meeting_type = random.choice(meeting_types)

        # Meeting metadata
        duration_minutes = {
            'Standup': int(np.random.gamma(2, 5)),
            'One-on-One': int(np.random.gamma(4, 7)),
            'Planning': int(np.random.gamma(6, 10)),
            'Review': int(np.random.gamma(5, 8)),
            'Brainstorming': int(np.random.gamma(5, 10)),
            'Decision-Making': int(np.random.gamma(5, 9)),
            'Status Update': int(np.random.gamma(3, 8)),
            'Retrospective': int(np.random.gamma(5, 10)),
            'All-Hands': int(np.random.gamma(7, 8))
        }[meeting_type]

        num_participants = {
            'Standup': int(np.clip(np.random.gamma(2, 2), 3, 12)),
            'One-on-One': 2,
            'Planning': int(np.clip(np.random.gamma(2.5, 2), 4, 15)),
            'Review': int(np.clip(np.random.gamma(2, 2.5), 3, 12)),
            'Brainstorming': int(np.clip(np.random.gamma(2.5, 2), 5, 20)),
            'Decision-Making': int(np.clip(np.random.gamma(2, 2), 4, 10)),
            'Status Update': int(np.clip(np.random.gamma(2, 3), 5, 20)),
            'Retrospective': int(np.clip(np.random.gamma(2, 2), 3, 12)),
            'All-Hands': int(np.clip(np.random.gamma(5, 10), 20, 100))
        }[meeting_type]

        meeting_date = datetime.now() - timedelta(days=random.randint(0, 180))

        # Generate transcript with mixed sentiment
        num_utterances = int(duration_minutes / 3) + random.randint(5, 15)

        # Meeting effectiveness factors
        agenda_clear = int(np.random.choice([0, 1], p=[0.25, 0.75]))
        on_time_start = int(np.random.choice([0, 1], p=[0.30, 0.70]))
        stayed_on_topic = np.random.beta(6, 3)

        # Generate sentiment distribution (varies by meeting quality)
        if stayed_on_topic > 0.7 and agenda_clear:
            # Effective meeting - more positive sentiment
            sentiment_dist = [0.15, 0.35, 0.50]  # negative, neutral, positive
        elif stayed_on_topic > 0.4:
            # Moderately effective
            sentiment_dist = [0.25, 0.50, 0.25]
        else:
            # Ineffective meeting - more negative sentiment
            sentiment_dist = [0.45, 0.40, 0.15]

        # Generate transcript
        transcript_parts = []
        sentiment_scores = []

        for _ in range(num_utterances):
            sentiment_category = np.random.choice(['negative', 'neutral', 'positive'], p=sentiment_dist)

            if sentiment_category == 'positive':
                utterance = random.choice(positive_utterances)
                sentiment = np.random.beta(7, 3)  # Skewed positive
            elif sentiment_category == 'neutral':
                utterance = random.choice(neutral_utterances)
                sentiment = np.random.beta(4, 4)  # Centered
            else:
                utterance = random.choice(negative_utterances)
                sentiment = np.random.beta(3, 7)  # Skewed negative

            transcript_parts.append(utterance)
            sentiment_scores.append(sentiment)

        full_transcript = " ".join(transcript_parts)

        # Aggregate sentiment
        avg_sentiment = np.mean(sentiment_scores)
        sentiment_std = np.std(sentiment_scores)

        # Participation metrics
        avg_speaking_time = duration_minutes / num_participants
        participation_balance = 1 - min(sentiment_std * 0.5, 0.8)  # More balanced = higher score

        # Engagement metrics
        questions_asked = int(np.clip(np.random.poisson(num_participants * 0.3), 0, 50))
        action_items = int(np.clip(np.random.poisson(3), 0, 15))
        decisions_made = int(np.clip(np.random.poisson(2), 0, 10))

        # Calculate effectiveness score
        effectiveness_factors = [
            agenda_clear * 0.2,
            on_time_start * 0.1,
            stayed_on_topic * 0.25,
            avg_sentiment * 0.2,
            participation_balance * 0.15,
            min(action_items / 5, 1.0) * 0.1
        ]

        effectiveness_score = np.clip(sum(effectiveness_factors), 0, 1)

        # Post-meeting survey (1-5 scale)
        usefulness_rating = np.round(effectiveness_score * 4 + 1 + np.random.normal(0, 0.3), 1)
        usefulness_rating = np.clip(usefulness_rating, 1, 5)

        # Follow-up metrics
        action_completion_rate = effectiveness_score * np.random.uniform(0.7, 1.0) if action_items > 0 else None

        meetings.append({
            'meeting_id': f"MTG{str(meeting_id).zfill(5)}",
            'meeting_type': meeting_type,
            'date': meeting_date.strftime('%Y-%m-%d'),
            'duration_minutes': duration_minutes,
            'num_participants': num_participants,
            'transcript': full_transcript[:500] + "...",  # Truncate for CSV
            'transcript_length': len(full_transcript),
            'num_utterances': num_utterances,
            'avg_sentiment': np.round(avg_sentiment, 3),
            'sentiment_std': np.round(sentiment_std, 3),
            'agenda_clear': agenda_clear,
            'on_time_start': on_time_start,
            'stayed_on_topic': np.round(stayed_on_topic, 3),
            'avg_speaking_time': np.round(avg_speaking_time, 2),
            'participation_balance': np.round(participation_balance, 3),
            'questions_asked': questions_asked,
            'action_items': action_items,
            'decisions_made': decisions_made,
            'usefulness_rating': usefulness_rating,
            'action_completion_rate': np.round(action_completion_rate, 3) if action_completion_rate else None,
            'effectiveness_score': np.round(effectiveness_score * 100, 1)
        })

    df = pd.DataFrame(meetings)
    return df


if __name__ == "__main__":
    import os

    # Generate dataset
    meetings_df = generate_meeting_data(n_meetings=1000)

    # Save to CSV
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(script_dir, '../..')
    output_dir = os.path.join(project_root, 'data/raw')

    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, 'meetings.csv')
    meetings_df.to_csv(output_path, index=False)

    print(f"\n✓ Dataset generated successfully!")
    print(f"\nDataset Shape: {meetings_df.shape}")
    print(f"Saved to: {output_path}")

    print(f"\n📊 Meeting Type Distribution:")
    print(meetings_df['meeting_type'].value_counts())

    print(f"\n⏱️ Duration Statistics:")
    print(f"Average duration: {meetings_df['duration_minutes'].mean():.1f} minutes")
    print(f"Median duration: {meetings_df['duration_minutes'].median():.1f} minutes")

    print(f"\n👥 Participation:")
    print(f"Average participants: {meetings_df['num_participants'].mean():.1f}")

    print(f"\n💬 Sentiment Analysis:")
    print(f"Average sentiment: {meetings_df['avg_sentiment'].mean():.3f} (0=negative, 1=positive)")

    print(f"\n✅ Effectiveness Metrics:")
    print(f"Average effectiveness: {meetings_df['effectiveness_score'].mean():.1f}/100")
    print(f"Average usefulness rating: {meetings_df['usefulness_rating'].mean():.2f}/5.0")

    print(f"\n📝 Action Items:")
    print(f"Average action items per meeting: {meetings_df['action_items'].mean():.1f}")
    print(f"Average decisions made: {meetings_df['decisions_made'].mean():.1f}")

    print(f"\n🎯 Highly Effective Meetings (>80 score):")
    high_effective = len(meetings_df[meetings_df['effectiveness_score'] > 80])
    print(f"Count: {high_effective} ({high_effective/len(meetings_df)*100:.1f}%)")

    print(f"\n⚠️ Low Effectiveness Meetings (<40 score):")
    low_effective = len(meetings_df[meetings_df['effectiveness_score'] < 40])
    print(f"Count: {low_effective} ({low_effective/len(meetings_df)*100:.1f}%)")
