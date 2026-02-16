# OpenProficiency - Python Library

This library provides class objects for managing proficiency across knowledge domains.

## Features

- **Topic Class**: A defined unique area of knowledge composed of subtopics and built upon pretopics (prerequisite topics).
- **TopicList Class**: A collection of related topics covering one knowledge domain.

## Installation

```bash
pip install openproficiency
```

## Quick Start

### Create a Topic

A **Topic** is an area of knowledge that a person gains proficiency in. If it has subtopics, the person can alternately gain proficiency in the parent topic by gaining proficiency in the subtopics.

```python
from openproficiency import Topic

# Create a simple topic and what composes it
topic_arithmetic = Topic(
    id="arithmetic",
    description="Basic operations for numeric calculations",
    subtopics=["addition", "subtraction"],
    pretopics=["numbers"]
)
```

### Add a subtopic to an existing topic

```python
# Specific other topics that compose the parent topic
topic_arithmetic.add_subtopic("multiplication")
topic_arithmetic.add_subtopic("division")
```

### Add a pretopic to an existing topic

A **Pretopic** (prerequisite topic) is a topic that must be understood before a person can begin understanding the parent topic.

```python
# Specify prerequisites to understand first
topic_arithmetic.add_pretopic("integers")
topic_arithmetic.add_pretopic("decimals")
topic_arithmetic.add_pretopic("fractions")
```

### Create a Topic List

A topic list is a collection of topics that describe a specific knowledge domain.

```python
from openproficiency import Topic, TopicList

# Create an empty topic list
topic_list = TopicList(
    owner="core-fundamentals",
    name="math",
    description="Math topics through basic calculus"
)

# Add topics to the list
t_arithmetic = Topic(
    id="arithmetic",
    description="Basic operations for numeric calculations",
    subtopics=[
        "addition",
        "subtraction",
        "multiplication",
        "division"
    ]
)
topic_list.add_topic(t_arithmetic)

t_algebra = Topic(
    id="algebra",
    description="Basic operations for numeric calculations",
    subtopics=[
        "variables",
        "constants",
        "single-variable-equations",
        "multiple-variable-equations"
    ],
    pretopics=["arithmetic"]
)
```

### Create a Proficiency Score, by name

A **Proficiency Score** represents a person's level of proficiency in a specific topic.

```python
from openproficiency import ProficiencyScore, ProficiencyScoreName

proficiency_score = ProficiencyScore(
    topic_id="addition",
    score=ProficiencyScoreName.PROFICIENT
)
```

### Create a Proficiency Score, numerically

All score are internally numeric from 0.0 to 1.0, even if set using the score name (above).

```python
from openproficiency import ProficiencyScore

proficiency_score = ProficiencyScore(
    topic_id="arithmetic",
    score=0.8 # Same as 'ProficiencyScoreName.PROFICIENT'
)
```

### Issue a Transcript Entry

A **Transcript Entry** associates a proficiency score to a user and is claimed by an issuer.

```python
from openproficiency import TranscriptEntry

# Create a transcript entry
entry = TranscriptEntry(
    user_id="first.last@my-email.com",
    topic_id="arithmetic",
    score=0.9,
    issuer="example.com"
)

# Access the transcript entry information
print(entry.user_id)  # john-doe
print(entry.proficiency_score.score)  # 0.9
print(entry.issuer)  # university-of-example
print(entry.timestamp)  # datetime object

# Convert to JSON for storage or transmission
entry_json = entry.to_json()
```

## How to Develop

This project is open to pull requests.

Please see the [contribution guide](CONTRIBUTE.md) to get started.
