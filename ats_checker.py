def check_ats(cv_text, job_text):

    cv_text = cv_text.lower()
    job_text = job_text.lower()


    result = {
        "score": 0,
        "found_keywords": [],
        "missing_keywords": [],
        "sections_found": [],
        "sections_missing": []
    }


    # Sprawdzanie słów kluczowych

    keywords = [
        "warehouse",
        "magazyn",
        "excel",
        "python",
        "customer service",
        "obsługa klienta",
        "english",
        "angielski",
        "ai",
        "machine learning"
    ]


    found = 0


    for keyword in keywords:

        if keyword in job_text:

            if keyword in cv_text:

                result["found_keywords"].append(keyword)
                found += 1

            else:

                result["missing_keywords"].append(keyword)



    # Wynik słów kluczowych

    total = len(
        result["found_keywords"]
    ) + len(
        result["missing_keywords"]
    )


    if total > 0:

        keyword_score = (
            len(result["found_keywords"])
            /
            total
            *
            100
        )

    else:

        keyword_score = 0



    # Sprawdzanie sekcji CV

    sections = {

        "doświadczenie": [
            "experience",
            "doświadczenie",
            "work history"
        ],

        "umiejętności": [
            "skills",
            "umiejętności"
        ],

        "wykształcenie": [
            "education",
            "wykształcenie"
        ],

        "języki": [
            "languages",
            "języki",
            "english"
        ]

    }



    for section, words in sections.items():

        found_section = False


        for word in words:

            if word in cv_text:

                found_section = True



        if found_section:

            result["sections_found"].append(section)

        else:

            result["sections_missing"].append(section)



    # Wynik końcowy ATS

    section_score = (

        len(result["sections_found"])
        /
        len(sections)
        *
        100

    )


    result["score"] = round(

        keyword_score * 0.7
        +
        section_score * 0.3

    )



    return result