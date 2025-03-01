import reflex as rx


class Customer(rx.Model, table=True):  # type: ignore
    """The customer model."""

    customer_name: str
    email: str
    age: int
    gender: str
    location: str
    job: str
    salary: int


class ArticleOwner(rx.Model, table=True):  # type: ignore
    """The article model."""

    author_name: str
    email: str
    age: int
    gender: str
    location: str
    position: str
    topic: str
    details: str
    