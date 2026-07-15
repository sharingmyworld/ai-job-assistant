import os

import streamlit as st


def show_privacy():
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

