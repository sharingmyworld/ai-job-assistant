from datetime import date, timedelta

from answer_evaluator import evaluate_answer
from followup_assistant import (
    generate_followup_message,
    should_suggest_followup,
)
from job_title_detector import detect_job_title
from learning_roadmaps import (
    DEFAULT_ROADMAP,
    get_skill_roadmap,
)


def test_empty_answer_scores_zero():
    score, feedback = evaluate_answer(
        "Czym różni się lista od krotki?",
        "",
    )
    assert score == 0
    assert feedback == "Brak odpowiedzi."


def test_strong_known_answer_scores_high():
    answer = (
        "Lista w Pythonie jest mutowalna, a tuple jest "
        "niemutowalna. W projekcie użyłem listy do danych, "
        "które zmieniały się podczas działania programu. "
        "Krotkę zastosowałem dla stałych wartości. "
        "Dzięki temu kod był czytelniejszy i lepiej "
        "odzwierciedlał przeznaczenie danych."
    )
    score, _ = evaluate_answer(
        "Czym różni się lista a krotka?",
        answer,
    )
    assert score >= 4


def test_detect_job_title_from_explicit_position():
    offer = """
    Stanowisko: Junior Python Developer
    Wymagania:
    Python
    SQL
    """
    assert detect_job_title(offer) == "Junior Python Developer"


def test_detect_job_title_returns_empty_for_empty_offer():
    assert detect_job_title("") == ""


def test_followup_after_seven_days_for_sent_application():
    sent = date.today() - timedelta(days=7)
    assert should_suggest_followup(
        sent.isoformat(),
        "Wysłana",
    ) is True


def test_no_followup_for_other_status():
    sent = date.today() - timedelta(days=30)
    assert should_suggest_followup(
        sent.isoformat(),
        "Rozmowa",
    ) is False


def test_invalid_application_date_is_safe():
    assert should_suggest_followup(
        "niepoprawna-data",
        "Wysłana",
    ) is False


def test_english_followup_contains_company_and_position():
    message = generate_followup_message(
        "OpenAI",
        "Python Developer",
        language="English",
    )
    assert "OpenAI" in message
    assert "Python Developer" in message
    assert "following up" in message


def test_python_roadmap_is_specific():
    roadmap = get_skill_roadmap(" Python ")
    assert "Testy jednostkowe" in roadmap
    assert roadmap is not DEFAULT_ROADMAP


def test_unknown_skill_uses_default_roadmap():
    assert get_skill_roadmap(
        "Nieznana technologia"
    ) == DEFAULT_ROADMAP
