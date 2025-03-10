import reflex as rx

from ..backend.backend import ArticleOwner, State
from ..components.form_field import form_field
from ..components.gender_badges import gender_badge


def _header_cell(text: str, icon: str):
    return rx.table.column_header_cell(
        rx.hstack(
            rx.icon(icon, size=18),
            rx.text(text),
            align="center",
            spacing="2",
        ),
    )


def _show_profile(user: ArticleOwner):
    """Show a customer in a table row."""
    return rx.table.row(
        rx.table.row_header_cell(user.author_name),
        rx.table.cell(user.email),
        rx.table.cell(user.age),
        rx.table.cell(
            rx.match(
                user.gender,
                ("Masculino", gender_badge("Male")),
                ("Femenino", gender_badge("Female")),
                ("Otro", gender_badge("Other")),
                gender_badge("Other"),
            )
        ),
        rx.table.cell(user.location),
        rx.table.cell(user.position),
        rx.table.cell(user.topic),
        rx.table.cell(
            rx.hstack(
                rx.cond(
                    (State.current_articleOwner.id == user.id),
                    rx.button(
                        rx.icon("play", size=22),
                        color_scheme="blue",
                        on_click=State.generate_email(user),
                        loading=State.gen_response,
                    ),
                    rx.button(
                        rx.icon("play", size=22),
                        color_scheme="blue",
                        on_click=State.generate_email(user),
                        disabled=State.gen_response,
                    ),
                ),
                _update_profile_dialog(user),
                rx.icon_button(
                    rx.icon("trash-2", size=22),
                    on_click=lambda: State.delete_profile(user.id),
                    size="2",
                    variant="solid",
                    color_scheme="red",
                    disabled=State.gen_response,
                ),
                min_width="max-content",
            )
        ),
        style={"_hover": {"bg": rx.color("accent", 2)}},
        align="center",
    )


def _add_article_button() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("plus", size=26),
                rx.text("Crear perfil", size="4", display=["none", "none", "block"]),
                size="3",
            ),
        ),
        rx.dialog.content(
            rx.hstack(
                rx.badge(
                    rx.icon(tag="users", size=34),
                    color_scheme="blue",
                    radius="full",
                    padding="0.65rem",
                ),
                rx.vstack(
                    rx.dialog.title(
                        "Autor - Artículo",
                        weight="bold",
                        margin="0",
                    ),
                    rx.dialog.description(
                        "Complete la información para perfilar el autor del artículo.",
                    ),
                    spacing="1",
                    height="100%",
                    align_items="start",
                ),
                height="100%",
                spacing="4",
                margin_bottom="1.5em",
                align_items="center",
                width="100%",
            ),
            rx.flex(
                rx.form.root(
                    rx.flex(
                        rx.hstack(
                            # Name
                            form_field(
                                "Name",
                                "Author Name",
                                "text",
                                "author_name",
                                "user",
                            ),
                            # Location
                            form_field(
                                "Location",
                                "Customer Location",
                                "text",
                                "location",
                                "map-pinned",
                            ),
                            spacing="3",
                            width="100%",
                        ),
                        rx.hstack(
                            # Email
                            form_field(
                                "Email", "usuario@ejemplo.cc", "email", "email", "mail"
                            ),
                            # topic
                            form_field(
                                "Topic", "Topic", "text", "topic", "info"
                            ),
                            spacing="3",
                            width="100%",
                        ),
                        # Gender
                        rx.vstack(
                            rx.hstack(
                                rx.icon("user-round", size=16, stroke_width=1.5),
                                rx.text("Gender"),
                                align="center",
                                spacing="2",
                            ),
                            rx.select(
                                ["Másculino", "Fémenino", "Otro"],
                                placeholder="Seleccione el genero",
                                name="gender",
                                direction="row",
                                as_child=True,
                                required=True,
                                width="100%",
                            ),
                            width="100%",
                        ),
                        rx.hstack(
                            # Age
                            form_field(
                                "Age",
                                "Customer Age",
                                "number",
                                "age",
                                "person-standing",
                            ),
                            # Position
                            form_field(
                                "Position",
                                "Position",
                                "text",
                                "position",
                                "briefcase",
                            ),
                            spacing="3",
                            width="100%",
                        ),
                        form_field(
                            "Detalle",
                            "Detalle corto",
                            "text",
                            "details",
                            "info",
                        ),                        
                        width="100%",
                        direction="column",
                        spacing="3",
                    ),
                    rx.flex(
                        rx.dialog.close(
                            rx.button(
                                "Cancel",
                                variant="soft",
                                color_scheme="gray",
                            ),
                        ),
                        rx.form.submit(
                            rx.dialog.close(
                                rx.button("Crear"),
                            ),
                            as_child=True,
                        ),
                        padding_top="2em",
                        spacing="3",
                        mt="4",
                        justify="end",
                    ),
                    on_submit=State.add_profile_to_db,
                    reset_on_submit=False,
                ),
                width="100%",
                direction="column",
                spacing="4",
            ),
            width="100%",
            max_width="450px",
            justify=["end", "end", "start"],
            padding="1.5em",
            border=f"2.5px solid {rx.color('accent', 7)}",
            border_radius="25px",
        ),
    )


def _update_profile_dialog(user):
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.icon_button(
                rx.icon("square-pen", size=22),
                color_scheme="green",
                size="2",
                variant="solid",
                on_click=lambda: State.get_user(user),
                disabled=State.gen_response,
            ),
        ),
        rx.dialog.content(
            rx.hstack(
                rx.badge(
                    rx.icon(tag="square-pen", size=34),
                    color_scheme="blue",
                    radius="full",
                    padding="0.65rem",
                ),
                rx.vstack(
                    rx.dialog.title(
                        "Actualizar",
                        weight="bold",
                        margin="0",
                    ),
                    rx.dialog.description(
                        "Edita la información para perfilar el autor del artículo.",
                    ),
                    spacing="1",
                    height="100%",
                    align_items="start",
                ),
                height="100%",
                spacing="4",
                margin_bottom="1.5em",
                align_items="center",
                width="100%",
            ),
            rx.flex(
                rx.form.root(
                    rx.flex(
                        rx.hstack(
                            # Name
                            form_field(
                                "Nombre",
                                "Nombre",
                                "text",
                                "author_name",
                                "user",
                                user.author_name,
                            ),
                            # Location
                            form_field(
                                "Ubicación",
                                "Ubicación",
                                "text",
                                "location",
                                "map-pinned",
                                user.location,
                            ),
                            spacing="3",
                            width="100%",
                        ),
                        rx.hstack(
                            # Email
                            form_field(
                                "Correo",
                                "user@reflex.dev",
                                "email",
                                "email",
                                "mail",
                                user.email,
                            ),
                            # Job
                            form_field(
                                "Tema",
                                "Tema",
                                "text",
                                "topic",
                                "info",
                                user.topic,
                            ),
                            spacing="3",
                            width="100%",
                        ),
                        # Gender
                        rx.vstack(
                            rx.hstack(
                                rx.icon("user-round", size=16, stroke_width=1.5),
                                rx.text("Genero"),
                                align="center",
                                spacing="2",
                            ),
                            rx.select(
                                ["Masculino", "Femenino", "Otro"],
                                default_value=user.gender,
                                name="gender",
                                direction="row",
                                as_child=True,
                                required=True,
                                width="100%",
                            ),
                            width="100%",
                        ),
                        rx.hstack(
                            # Age
                            form_field(
                                "Edad",
                                "Edad",
                                "number",
                                "age",
                                "person-standing",
                                user.age.to(str),
                            ),
                            # Position
                            form_field(
                                "Cargo",
                                "Cargo",
                                "text",
                                "position",
                                "briefcase",
                                user.position,
                            ),
                            spacing="3",
                            width="100%",
                        ),
                        direction="column",
                        spacing="3",
                    ),
                    rx.flex(
                        rx.dialog.close(
                            rx.button(
                                "Cancel",
                                variant="soft",
                                color_scheme="gray",
                            ),
                        ),
                        rx.form.submit(
                            rx.dialog.close(
                                rx.button("Actualizar"),
                            ),
                            as_child=True,
                        ),
                        padding_top="2em",
                        spacing="3",
                        mt="4",
                        justify="end",
                    ),
                    on_submit=State.update_profile_to_db,
                    reset_on_submit=False,
                ),
                width="100%",
                direction="column",
                spacing="4",
            ),
            max_width="450px",
            padding="1.5em",
            border=f"2px solid {rx.color('accent', 7)}",
            border_radius="25px",
        ),
    )


def main_table():
    return rx.fragment(
        rx.flex(
            _add_article_button(),
            rx.spacer(),
            rx.cond(
                State.sort_reverse,
                rx.icon(
                    "arrow-down-z-a",
                    size=28,
                    stroke_width=1.5,
                    cursor="pointer",
                    on_click=State.toggle_sort,
                ),
                rx.icon(
                    "arrow-down-a-z",
                    size=28,
                    stroke_width=1.5,
                    cursor="pointer",
                    on_click=State.toggle_sort,
                ),
            ),
            rx.select(
                [
                    "Nombre",
                    "Correo",
                    "Edad",
                    "Genero",
                    "Ubicación",
                    "Tema",
                    "Cargo"
                ],
                placeholder="Ordenar por...",
                size="3",
                on_change=lambda sort_value: State.sort_values(sort_value),
            ),
            rx.input(
                rx.input.slot(rx.icon("search")),
                placeholder="Buscar...",
                size="3",
                max_width="225px",
                width="100%",
                variant="surface",
                on_change=lambda value: State.filter_values(value),
            ),
            justify="end",
            align="center",
            spacing="3",
            wrap="wrap",
            width="100%",
            padding_bottom="1em",
        ),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    _header_cell("Nombre", "square-user-round"),
                    _header_cell("Correo", "mail"),
                    _header_cell("Edad", "person-standing"),
                    _header_cell("Genero", "user-round"),
                    _header_cell("Ubicación", "map-pinned"),
                    _header_cell("Cargo", "briefcase"),
                    _header_cell("Tema", "info"),
                    _header_cell("", "cog"),
                ),
            ),
            rx.table.body(rx.foreach(State.articleOwners, _show_profile)),
            variant="surface",
            size="3",
            width="100%",
        ),
    )
