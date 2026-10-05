# Senior–Junior Connect

## Project Description

Senior–Junior Connect is a web-based AI-assisted platform that helps college juniors find suitable seniors based on their skills, experience and guidance requirements.

The system analyses the junior's requirement, matches it with senior profiles and ranks suitable seniors.

## Key Features

- Senior registration
- Junior registration
- User login
- Senior profile management
- AI-assisted senior matching
- Senior ranking
- Guidance requests
- Accept / Decline requests
- Junior–Senior discussion
- Feedback and rating
- Online deployment

## Technology Stack

- Python
- Flask
- HTML
- CSS
- SQLite
- GitHub
- Render

## AI Matching

The current prototype uses rule-based, NLP-inspired weighted keyword and skill matching.

The matching considers:

- Junior skills
- Junior requirement
- Senior skills
- Senior projects
- Hackathon experience
- Guidance areas
- Feedback rating

The system calculates a matching score and ranks suitable seniors.

## Application Routes

| Route | Method | Purpose |
|---|---|---|
| `/login` | GET | Display login page |
| `/login-check` | POST | Validate user login |
| `/logout` | GET | Logout user |
| `/senior-register` | GET | Display senior registration |
| `/register` | POST | Register senior |
| `/junior` | GET | Display junior registration |
| `/junior-register` | POST | Register junior |
| `/matches` | GET/POST | Generate senior matches |
| `/profile/<senior_id>` | GET | View senior profile |
| `/send-request/<senior_id>` | GET | Send guidance request |
| `/senior-dashboard` | GET | View senior requests |
| `/accept-request/<request_id>` | GET | Accept request |
| `/decline-request/<request_id>` | GET | Decline request |
| `/my-requests` | GET | View junior requests |
| `/discussion/<request_id>` | GET | Open discussion |
| `/send-message/<request_id>` | POST | Send message |
| `/feedback/<request_id>` | GET | Display feedback |
| `/submit-feedback/<request_id>` | POST | Submit feedback |
| `/manage-profile` | GET/POST | Manage senior profile |

## Database Schema

### seniors

Stores senior profile and experience information.

Important fields:
- id
- name
- department
- year
- skills
- projects
- hackathon
- internship
- guidance
- location
- mode
- availability

### juniors

Stores junior profile and requirement information.

Important fields:
- id
- name
- department
- year
- skills
- requirement
- location
- mode

### requests

Stores guidance requests between juniors and seniors.

Important fields:
- id
- junior_id
- senior_id
- status

### messages

Stores messages exchanged during guidance discussions.

Important fields:
- id
- request_id
- sender
- message

### feedback

Stores ratings and feedback after guidance.

Important fields:
- id
- request_id
- junior_id
- senior_id
- rating
- comment

## Testing

The major application workflow has been manually tested.

| Test Case | Expected Result | Status |
|---|---|---|
| Senior Registration | Senior profile created | PASS |
| Junior Registration | Junior profile created | PASS |
| Login | User login successful | PASS |
| Requirement Input | Requirement accepted | PASS |
| AI Matching | Suitable seniors displayed | PASS |
| Profile View | Senior details displayed | PASS |
| Guidance Request | Request sent successfully | PASS |
| Accept Request | Request accepted | PASS |
| Discussion | Messages sent and displayed | PASS |
| Feedback | Rating and feedback submitted | PASS |

## End-to-End Workflow

Senior Registration
→ Junior Registration
→ Login
→ Requirement Input
→ AI Matching
→ Senior Ranking
→ Profile View
→ Guidance Request
→ Senior Accepts
→ Discussion
→ Feedback

## Deployment

The prototype is deployed using Render.

Live Prototype:
https://senior-junior-connect-2mxs.onrender.com

GitHub Repository:
https://github.com/preethivarma7002-tech/Senior-Junior-Connect

## Current Limitations

- Current matching is rule-based.
- Advanced machine-learning models are not yet implemented.
- SQLite is currently used.
- Large-scale user testing is pending.
- Advanced notification features are pending.
- Admin management features are pending.

## Future Improvements

- Advanced NLP-based matching
- Semantic similarity matching
- Better error handling
- Unit testing
- Improved security
- Production database
- Notifications
- Admin dashboard
- Larger real-user validation