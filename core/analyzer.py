from core.skills import SKILLS_MAP


def analyze_cv(cv_text, job_offer):

    cv_text = cv_text.lower()
    job_offer = job_offer.lower()


    found = []
    missing = []


    for skill, keywords in SKILLS_MAP.items():


        cv_has_skill = any(
            word in cv_text
            for word in keywords
        )


        job_has_skill = any(
            word in job_offer
            for word in keywords
        )


        if job_has_skill:


            if cv_has_skill:

                found.append(skill)


            else:

                missing.append(skill)



    total = len(found) + len(missing)


    if total > 0:

        score = (
            len(found)
            /
            total
            *
            100
        )

    else:

        score = 0



    return (
        score,
        found,
        missing
    )
