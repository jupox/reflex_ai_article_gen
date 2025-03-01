import reflex as rx
import os
import re
import ollama

from sqlmodel import asc, desc, func, or_, select
from .models import Customer, ArticleOwner


class State(rx.State):
    """The app state."""

    current_user: Customer = Customer()
    current_articleOwner: ArticleOwner = ArticleOwner()
    users: list[Customer] = []
    articleOwners: list[ArticleOwner] = []
    email_content_data: str = (
        "Clic en 'Generar Artículo' para generar un nuevo articulo sobre el tema deseado."
    )
    gen_response = False
    tone: str = "😊 Formal"
    length: int = 100
    search_value: str = ""
    sort_value: str = ""
    sort_reverse: bool = False

    @rx.event
    def set_length(self, value: list[int | float]):
        self.length = int(value[0])

    def load_entries(self) -> list[ArticleOwner]:
        """Get all articles profiles from the database."""
        with rx.session() as session:
            query = select(ArticleOwner)
            if self.search_value:
                search_value = f"%{str(self.search_value).lower()}%"
                query = query.where(
                    or_(
                        *[
                            getattr(ArticleOwner, field).ilike(search_value)
                            for field in ArticleOwner.get_fields()
                        ],
                    )
                )

            if self.sort_value:
                sort_column = getattr(ArticleOwner, self.sort_value)
                if self.sort_value == "topic":
                    order = desc(sort_column) if self.sort_reverse else asc(sort_column)
                else:
                    order = (
                        desc(func.lower(sort_column))
                        if self.sort_reverse
                        else asc(func.lower(sort_column))
                    )
                query = query.order_by(order)

            self.articleOwners = session.exec(query).all()

    def sort_values(self, sort_value: str):
        print("sort_values, sort_value: ", sort_value)
        values = {
            "Nombre":"author_name",
            "Correo":"email",
            "Edad":"age",
            "Genero":"gender",
            "Ubicación":"location",
            "Tema":"topic",
            "Cargo":"position",
        }
        self.sort_value = values[sort_value]
        self.load_entries()

    def toggle_sort(self):
        self.sort_reverse = not self.sort_reverse
        self.load_entries()

    def filter_values(self, search_value):
        self.search_value = search_value
        self.load_entries()

    def get_user(self, user: ArticleOwner):
        self.current_articleOwner = user

    def add_profile_to_db(self, form_data: dict):
        self.current_articleOwner = ArticleOwner(**form_data)

        with rx.session() as session:
            if session.exec(
                select(ArticleOwner).where(ArticleOwner.email == self.current_articleOwner.email)
            ).first():
                return rx.window_alert("El usuario ya existe")
            session.add(self.current_articleOwner)
            session.commit()
            session.refresh(self.current_articleOwner)
        self.load_entries()
        return rx.toast.info(
            f"Autor: {self.current_articleOwner.author_name} creado correctamente.",
            position="bottom-right",
        )

    def update_profile_to_db(self, form_data: dict):
        with rx.session() as session:
            customer = session.exec(
                select(ArticleOwner).where(ArticleOwner.id == self.current_articleOwner.id)
            ).first()
            customer.set(**form_data)
            session.commit()
            session.refresh(customer)
            self.current_articleOwner = customer
        self.load_entries()
        return rx.toast.info(
            f"Perfil {self.current_articleOwner.author_name} actualizado.",
            position="bottom-right",
        )

    def delete_profile(self, id: int):
        """Delete a ArticleOwner from the database."""
        with rx.session() as session:
            current_articleOwner = session.exec(select(ArticleOwner).where(ArticleOwner.id == id)).first()
            session.delete(current_articleOwner)
            session.commit()
        self.load_entries()
        return rx.toast.info(
            f"Perfil {self.current_articleOwner.author_name} eliminado.", position="bottom-right"
        )

    @rx.event(background=True)
    async def call_openai(self):
        print("llamado a deepseek")        
        text_buffer = ""
        full_text = ""
        ollama_stream = ollama.chat(
            model = "deepseek-r1:7b",
            messages = [
                {
                    "role": "system",
                    "content": f"Eres un escritor y experto con muchos conocimientos en tecnologias programacion y sistemas de inteligencia artificial negocios economia inversiones salud y deporte, responde creando un articulo donde su idea principal trate sobre el tema {self.current_articleOwner.topic} detallando {self.current_articleOwner.details} de {self.length} palabras y usando un tono {self.tone}.",
                    # "content": f"You are a language model called R1 created by DeepSeek, answer in spanish with a new article for technologies trend and importants for a new company of business for the entire world being random but important in less than {self.length} words and with tone {self.tone}.",
                },
                {
                    "role": "user",
                    "content": f"hola, me llamo {self.current_articleOwner.author_name} y actualmente soy {self.current_articleOwner.position}, tengo {self.current_articleOwner.age} años y soy de genero {self.current_articleOwner.gender} me encuentro en {self.current_articleOwner.location} y me gustaria que me ayudaras a crear un articulo sobre {self.current_articleOwner.topic} detallando {self.current_articleOwner.details}.",
                },
                {
                    "role": "tool",
                    "content": f"contesta en español latinoamericano",
                },
            ],
            stream=True,
        )
        print("inicializando")
        for item in ollama_stream:
            text_buffer += item["message"]["content"]
            if text_buffer.endswith("."):
                full_text += text_buffer
                text_buffer = ""
        print("finalizado")
        if text_buffer:
            full_text += text_buffer

        full_text = re.sub(r'<think>.*?</think>', '', full_text, flags=re.DOTALL)

        async with self:
            if full_text is not None:
                self.email_content_data += full_text
        yield


        async with self:
            self.gen_response = False

    def generate_email(self, user: ArticleOwner):
        self.current_articleOwner = user
        self.gen_response = True
        self.email_content_data = ""
        return State.call_openai