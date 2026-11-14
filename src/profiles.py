"""Only this country is enabled; no foreign profile is imported."""

import json
from dataclasses import dataclass
from pathlib import Path

FESTIVAL_SOURCES = json.loads(
    Path(__file__).with_name("festival_sources.json").read_text(encoding="utf-8")
)


@dataclass(frozen=True)
class Profile:
    code: str
    name: str
    timezone: str
    engine: str
    languages: tuple[str, ...]
    native: str
    tradition: str
    first_year: int
    last_year: int
    sources: tuple[str, ...]
    leap_festivals: bool = False


PROFILES = {
    "TW": Profile(
        code="TW",
        name="Taiwan",
        timezone="Asia/Taipei",
        engine="chinese",
        languages=("zh-Hant", "en"),
        native="zh-Hant",
        tradition="chinese",
        first_year=1901,
        last_year=2099,
        sources=("https://www.hko.gov.hk/en/gts/time/conversion.htm", "https://www.dgpa.gov.tw/"),
        leap_festivals=False,
    )
}
RULES = {
    "TW": (
        (1, 1, "lunar_new_year"),
        (1, 15, "lantern"),
        (5, 5, "dragon_boat"),
        (8, 15, "mid_autumn"),
        (1, 2, "cny_day_2"),
        (3, 23, "mazu"),
        (7, 7, "qixi"),
        (7, 15, "ghost"),
        (9, 9, "double_ninth"),
        (12, 24, "kitchen_gods"),
    )
}
SOLAR_RULES = {"TW": ()}
SOLAR_TERMS = {"TW": {"清明": "qingming"}}
RESIDENCES = {}
ROADMAP = {}
GLOBAL_ROADMAP = {}


def get_profile(code):
    if not isinstance(code, str) or code.upper() not in PROFILES:
        raise ValueError(f"Unsupported lunar profile: {code}. Use --list-countries.")
    return PROFILES[code.upper()]


def resolve_language(profile, language, residence=None):
    language = ("en" if residence else profile.native) if language in (None, "native") else language
    supported = residence_languages(residence, profile) if residence else profile.languages
    if language not in supported:
        raise ValueError(
            f"{residence or profile.code} / {profile.tradition} supports languages: {', '.join(supported)}"
        )
    return language


def get_residence(code):
    if not isinstance(code, str) or code.upper() not in RESIDENCES:
        raise ValueError(f"Unsupported residence: {code}. Use --list-countries.")
    return RESIDENCES[code.upper()]


def residence_languages(residence, profile):
    host = get_residence(residence)
    if profile.code not in dict(host.traditions).values():
        raise ValueError(f"{host.code} does not support the {profile.code} profile")
    if profile.tradition == "chinese":
        return ("en", "zh-Hans", "zh-Hant")
    return ("en",) + tuple(lang for lang in profile.languages if lang != "en")
