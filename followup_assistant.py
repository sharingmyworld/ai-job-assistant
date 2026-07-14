from datetime import date


def should_suggest_followup(
    application_date,
    status,
    days_after=7
):
    if status != "Wysłana":
        return False

    try:
        sent_date = date.fromisoformat(
            str(application_date)
        )
    except ValueError:
        return False

    return (
        date.today() - sent_date
    ).days >= days_after


def generate_followup_message(
    company,
    position,
    language="Polski"
):
    if language == "English":
        return (
            f"Hello,\\n\\n"
            f"I am following up regarding my application "
            f"for the {position} position at {company}. "
            f"I remain very interested in the opportunity "
            f"and would appreciate any update regarding "
            f"the recruitment process.\\n\\n"
            f"Thank you for your time.\\n\\n"
            f"Best regards"
        )

    return (
        f"Dzień dobry,\\n\\n"
        f"chciałbym uprzejmie dopytać o status mojej "
        f"aplikacji na stanowisko {position} w firmie "
        f"{company}. Nadal jestem zainteresowany "
        f"możliwością dołączenia do zespołu i będę "
        f"wdzięczny za informację dotyczącą dalszych "
        f"etapów rekrutacji.\\n\\n"
        f"Dziękuję za poświęcony czas.\\n\\n"
        f"Pozdrawiam"
    )
