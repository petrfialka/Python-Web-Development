"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
import httpx

from rxconfig import config


class State(rx.State):
    """The app state."""
    data_url = "http://localhost:8000/api"
    tags: list = []
    articles: list = []
    
    
    async def get_index_data(self):
        async with httpx.AsyncClient() as client:
            res = await client.get(f"{self.data_url}/tags")
            res.raise_for_status()
            self.tags = res.json()
            res = await client.get(f"{self.data_url}/articles")
            res.raise_for_status()
            self.articles = res.json()
            
    async def get_article_by_id(self):
        article_id = self.router.page.params.get("id")
        
            
def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.hstack(
            rx.link(rx.text("Tag1"), href="https://google.com"),
            rx.link(rx.text("Tag2"), href="https://google.com"),
            rx.link(rx.text("Tag3"), href="https://google.com"),
        ),
        rx.divider(margin_top="20px", margin_bottom="20px"),
        rx.vstack(
            rx.link(rx.text("Article1"), href="https://google.com"),
            rx.link(rx.text("Article2"), href="https://google.com"),
            rx.link(rx.text("Article3"), href="https://google.com"),
        )
    )

def article() -> rx.Component:
    return rx.container(
        rx.heading(rx.State.id),
        rx.heading("Title"),
    )

app = rx.App()
app.add_page(index, on_load=State.get_index_data)
app.add_page(article, "/article/[id]", on_load=State.get_article_by_id)
