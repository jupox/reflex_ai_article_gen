import reflex as rx


def _badge(text: str, color_scheme: str):
    return rx.badge(
        text, color_scheme=color_scheme, radius="full", variant="soft", size="3"
    )


def gender_badge(gender: str):
    badge_mapping = {
        "Male": ("♂️ Masculino", "blue"),
        "Female": ("♀️ Femenino", "pink"),
        "Other": ("Otro", "gray"),
    }
    return _badge(*badge_mapping.get(gender, ("Otro", "gray")))
