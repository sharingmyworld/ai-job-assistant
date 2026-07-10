def analyze_cv(cv_text, job_offer):

    cv_text = cv_text.lower()
    job_offer = job_offer.lower()


    skills_map = {

        "warehouse": [
            "warehouse",
            "magazyn",
            "pracownik magazynu",
            "logistyka",
            "pakowanie",
            "wysyłka"
        ],

        "customer service": [
            "customer service",
            "obsługa klienta",
            "klient",
            "sprzedaż"
        ],

        "python": [
            "python",
            "programowanie",
            "django"
        ],

        "excel": [
            "excel",
            "arkusze",
            "spreadsheet"
        ],

        "english": [
            "english",
            "angielski",
            "język angielski"
        ],

        "ai": [
            "ai",
            "sztuczna inteligencja",
            "machine learning"
        ]

    }


    found = []
    missing = []


    for skill, words in skills_map.items():

        cv_has_skill = any(
            word in cv_text
            for word in words
        )


        job_has_skill = any(
            word in job_offer
            for word in words
        )


        if job_has_skill:

            if cv_has_skill:
                found.append(skill)

            else:
                missing.append(skill)



    if len(skills_map) > 0:

        score = (
            len(found) /
            (len(found) + len(missing))
            * 100
        )

    else:
        score = 0



    return score, found, missing
