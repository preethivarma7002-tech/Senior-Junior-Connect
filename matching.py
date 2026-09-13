def calculate_match(
    junior_skills,
    junior_requirement,
    senior_skills,
    senior_projects,
    senior_hackathon,
    senior_guidance,
    senior_experience_rating=0
):

    junior_text = (
        str(junior_skills) + " " +
        str(junior_requirement)
    ).lower()

    senior_skill_text = str(senior_skills).lower()
    senior_project_text = str(senior_projects).lower()
    senior_hackathon_text = str(senior_hackathon).lower()
    senior_guidance_text = str(senior_guidance).lower()

    # --------------------------------
    # Important matching words
    # --------------------------------

    keywords = [
        "python",
        "java",
        "c",
        "c++",
        "dsa",
        "ai",
        "machine learning",
        "web development",
        "html",
        "css",
        "javascript",
        "react",
        "hackathon",
        "project",
        "placement",
        "coding",
        "sih",
        "data science",
        "database",
        "sql",
        "cloud",
        "iot"
    ]

    matched = []

    for word in keywords:

        if word in junior_text:

            if (
                word in senior_skill_text
                or
                word in senior_project_text
                or
                word in senior_hackathon_text
                or
                word in senior_guidance_text
            ):
                matched.append(word)

    # --------------------------------
    # Score calculation
    # --------------------------------

    # Skill / requirement match = 60
    if len(matched) == 0:
        skill_score = 0
    else:
        skill_score = min(60, len(matched) * 10)

    # Experience match = 20
    experience_words = 0

    if "project" in junior_text and senior_project_text.strip():
        experience_words += 1

    if "hackathon" in junior_text and senior_hackathon_text.strip():
        experience_words += 1

    if "placement" in junior_text and "placement" in senior_guidance_text:
        experience_words += 1

    experience_score = min(20, experience_words * 10)

    # Guidance area match = 10
    guidance_score = 0

    for word in matched:
        if word in senior_guidance_text:
            guidance_score += 2

    guidance_score = min(10, guidance_score)

    # Feedback score = maximum 10
    feedback_score = min(
        10,
        round(float(senior_experience_rating) * 2)
    )

    final_score = min(
        100,
        skill_score +
        experience_score +
        guidance_score +
        feedback_score
    )

    breakdown = {
        "skill": skill_score,
        "experience": experience_score,
        "guidance": guidance_score,
        "feedback": feedback_score
    }

    return final_score, matched, breakdown