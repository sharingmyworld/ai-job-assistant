import os

import streamlit as st

from i18n import get_language


def _show_privacy_pl():
    operator_name = os.environ.get(
        "PRIVACY_OPERATOR_NAME",
        "Operator aplikacji AI Job Assistant",
    )
    contact_email = os.environ.get(
        "PRIVACY_CONTACT_EMAIL",
        "uzupełnij-adres-email",
    )

    st.header("🔐 Polityka prywatności")
    st.caption("Ostatnia aktualizacja: lipiec 2026")

    if contact_email == "uzupełnij-adres-email":
        st.warning(
            "Administrator aplikacji nie uzupełnił jeszcze "
            "adresu kontaktowego."
        )

    st.markdown(
        f"""
### 1. Administrator danych

Administratorem danych przetwarzanych w aplikacji jest
**{operator_name}**.

Kontakt w sprawach prywatności:
**{contact_email}**.

### 2. Jakie dane są przetwarzane

Aplikacja może przetwarzać:

- login i zaszyfrowany skrót hasła,
- treść przesłanego CV podczas analizy,
- informacje o ofertach pracy i aplikacjach,
- wyniki analiz dopasowania i ATS,
- plan nauki oraz postęp roadmap,
- notatki, odpowiedzi i feedback związany z rozmowami,
- techniczne tokeny potrzebne do funkcji „Nie wylogowuj mnie”.

Plik CV jest przetwarzany tymczasowo podczas analizy i nie jest
zapisywany jako trwały plik w bazie danych przez tę aplikację.

### 3. Cele przetwarzania

Dane są używane wyłącznie do udostępnienia funkcji aplikacji,
w szczególności do analizy CV, prowadzenia historii, śledzenia
aplikacji, przygotowania do rozmów i tworzenia statystyk użytkownika.

### 4. Podstawa i dobrowolność

Podanie danych jest dobrowolne, ale niektóre dane są niezbędne
do utworzenia konta i korzystania z funkcji aplikacji.

### 5. Przechowywanie danych

Dane są przechowywane do czasu usunięcia ich przez użytkownika
lub usunięcia konta. W Profilu dostępne są funkcje eksportu danych
oraz trwałego usunięcia konta i danych.

### 6. Dostawcy infrastruktury

Aplikacja korzysta z usług podmiotów zapewniających infrastrukturę:

- Streamlit Community Cloud — hosting aplikacji,
- Supabase — baza danych PostgreSQL,
- GitHub — przechowywanie kodu źródłowego; sekrety i dane
  użytkowników nie powinny znajdować się w repozytorium.

Dostawcy mogą przetwarzać dane techniczne zgodnie ze swoimi
warunkami i politykami prywatności.

### 7. Prawa użytkownika

Użytkownik może w szczególności:

- uzyskać dostęp do swoich danych poprzez eksport JSON,
- poprawiać dane w dostępnych formularzach,
- usunąć swoje konto i wszystkie przypisane dane,
- skontaktować się z administratorem w sprawach dotyczących danych,
- złożyć skargę do właściwego organu ochrony danych.

### 8. Bezpieczeństwo

Hasła są przechowywane jako skróty bcrypt. Sekrety połączeń
i szyfrowania są przechowywane poza kodem źródłowym. Połączenie
z bazą odbywa się przy użyciu danych dostępowych zapisanych
w konfiguracji środowiska.

### 9. Automatyczne decyzje

Wyniki dopasowania CV, ATS i Mock Interview mają charakter
pomocniczy. Nie stanowią decyzji rekrutacyjnej ani profesjonalnej
porady i nie wywołują skutków prawnych wobec użytkownika.

### 10. Zmiany polityki

Polityka może być aktualizowana wraz z rozwojem aplikacji.
Data ostatniej aktualizacji jest widoczna na początku dokumentu.
"""
    )



def show_privacy():
    if get_language() != "en":
        return _show_privacy_pl()

    operator_name = os.environ.get("PRIVACY_OPERATOR_NAME", "AI Job Assistant operator")
    contact_email = os.environ.get("PRIVACY_CONTACT_EMAIL", "contact-email-not-configured")

    st.header("🔐 Privacy Policy")
    st.caption("Last updated: July 2026")
    st.markdown(f"""
### 1. Data controller
The controller of data processed in the application is **{operator_name}**.

Privacy contact: **{contact_email}**.

### 2. Data processed
The application may process a username and bcrypt password hash, CV content during analysis, job application information, analysis and ATS results, learning progress, interview notes and feedback, and technical tokens required for persistent login.

CV files are processed temporarily during analysis and are not stored as permanent files in the application database.

### 3. Purpose of processing
Data is used to provide the application's features, including CV analysis, history, application tracking, learning planning, interview preparation, and user statistics.

### 4. Voluntary provision of data
Providing data is voluntary, although some information is required to create an account and use selected features.

### 5. Data retention
Data is stored until deleted by the user or until the account is deleted. The Profile view provides JSON export and permanent account deletion.

### 6. Infrastructure providers
The application uses Streamlit Community Cloud for hosting, Supabase for PostgreSQL storage, and GitHub for source-code hosting. Secrets and user data should not be stored in the source-code repository.

### 7. User rights
Users can access their data through JSON export, update data through available forms, delete their account and associated data, contact the controller regarding privacy, and submit a complaint to the competent data-protection authority.

### 8. Security
Passwords are stored as bcrypt hashes. Connection credentials and secrets are stored outside the source code in environment configuration.

### 9. Automated decisions
CV match, ATS, and Mock Interview results are assistive only. They do not constitute recruitment decisions or professional advice and do not produce legal effects for the user.

### 10. Policy changes
This policy may be updated as the application evolves. The latest update date is shown at the top of this document.
""")
