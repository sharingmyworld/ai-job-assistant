def ai_analysis(cv_text, job_offer):

    prompt = f"""
Jesteś ekspertem HR.

Przeanalizuj CV kandydata i ofertę pracy.

CV:
{cv_text}

Oferta:
{job_offer}

Napisz:
1. Ocena dopasowania w procentach.
2. Największe mocne strony kandydata.
3. Czego brakuje.
4. Co poprawić w CV.
"""

    return prompt
    