# app/main.py
from dataclasses import dataclass, field
from typing import Any

import streamlit as st

from core.settings import Settings
from core.state import init_app_state
from services.payment_service import PaymentService
from services.security_service import SecurityService
from services.bot_service import BotService
from services.vault_service import VaultService

from ui.theme import apply_theme
from ui.home import render_home_tab
from ui.pay import render_pay_tab
from ui.auth import render_auth_tab
from ui.shield import render_shield_tab
from ui.osobot import render_osobot_tab
from ui.vault import render_vault_tab
from ui.cases import render_cases_tab
from ui.steps import render_steps_tab


@dataclass
class AppContainer:
    settings: Settings
    payment_service: PaymentService
    security_service: SecurityService
    bot_service: BotService
    vault_service: VaultService


def build_container() -> AppContainer:
    settings = Settings.from_env()

    security_service = SecurityService(
        master_key=settings.master_key
    )

    vault_service = VaultService()

    payment_service = PaymentService(
        security_service=security_service,
        min_amount=settings.min_amount,
        supported_chains=settings.supported_chains,
    )

    bot_service = BotService(
        base_url=settings.alsa_base_url,
        api_key=settings.alsa_api_key,
    )

    return AppContainer(
        settings=settings,
        payment_service=payment_service,
        security_service=security_service,
        bot_service=bot_service,
        vault_service=vault_service,
    )


def configure_page(settings: Settings) -> None:
    st.set_page_config(
        page_title=settings.app_name,
        page_icon="⭐",
        layout="wide",
        initial_sidebar_state="collapsed",
    )


def render_header(settings: Settings) -> None:
    auth = st.session_state.get("auth", False)
    auth_badge = "✅ Verified" if auth else "🔒 Unverified"

    st.markdown(
        f"""
        <div class="hero">
            <div class="title">{settings.app_name}</div>
            <div class="subtitle">{settings.slogan}</div>
            <div class="badge">{settings.app_version} · {auth_badge}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    container = build_container()
    configure_page(container.settings)
    apply_theme()
    init_app_state(container.settings)

    render_header(container.settings)

    tabs = st.tabs([
        "🏠 Home",
        "⚡ Pay",
        "🎥 Auth",
        "🛡 Shield",
        "🤖 OsoBot",
        "🔒 Vault",
        "📱 Cases",
        "⚙️ Steps",
    ])

    with tabs[0]:
        render_home_tab(
            settings=container.settings,
            payment_service=container.payment_service,
        )

    with tabs[1]:
        render_pay_tab(
            settings=container.settings,
            payment_service=container.payment_service,
            security_service=container.security_service,
            vault_service=container.vault_service,
        )

    with tabs[2]:
        render_auth_tab()

    with tabs[3]:
        render_shield_tab(
            security_service=container.security_service
        )

    with tabs[4]:
        render_osobot_tab(
            bot_service=container.bot_service
        )

    with tabs[5]:
        render_vault_tab(
            vault_service=container.vault_service
        )

    with tabs[6]:
        render_cases_tab()

    with tabs[7]:
        render_steps_tab()


if __name__ == "__main__":
    main()
