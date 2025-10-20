from typing import Optional
from ninja import NinjaAPI
from ninja import Schema


class AuthorSchema(Schema):
    id: int
    first_name: str
    second_name: str


class TagSchema(Schema):
    id: int
    title: str


class ArticleSchema(Schema):
    id: int
    title: str
    author: AuthorSchema
    tags: list[TagSchema]


api = NinjaAPI()


class DB:
    articles = [
        {
            "id": 1,
            "title": "Koráli se blíží bodu zvratu, varuje zpráva. A s nimi všechno, co dávají lidstvu",
            "author": 1,
            "tags": [1, 3],
        },
        {
            "id": 2,
            "title": "Slabé místo magnetického pole Země se výrazně zvětšuje",
            "author": 2,
            "tags": [1, 2, 4],
        },
        {
            "id": 3,
            "title": "Vědci z Cambridge hlásí průlom. Vytvořili v laboratoři lidskou krev",
            "author": 2,
            "tags": [1, 4],
        },
    ]
    authors = {
        1: {"id": 1, "first_name": "Pavel", "second_name": "Beneš"},
        2: {"id": 2, "first_name": "Tomáš", "second_name": "Karlík"},
    }
    tags = {
        1: {"id": 1, "title": "Věda"},
        2: {"id": 2, "title": "Země"},
        3: {"id": 3, "title": "Koráli"},
        4: {"id": 4, "title": "Výběr redakce"},
    }

    def article_dict_to_schema(self, article: dict):
        return ArticleSchema(
            id=article.get("id"),
            title=article.get("title"),
            author=AuthorSchema(**self.authors.get(article["author"])),
            tags=[TagSchema(**self.tags.get(tag)) for tag in article.get("tags")],
        )

    def get_articles(self):
        return [self.article_dict_to_schema(article) for article in self.articles]

    def get_articles_by_tag(self, tag_id: int):
        return [self.article_dict_to_schema(article) for article in self.articles if tag_id in article.get("tags")]

    def get_tags(self):
        return [TagSchema(id=tag.get("id"), title=tag.get("title")) for tag in self.tags.values()]


db = DB()

@api.get("/articles", response=list[ArticleSchema])
def get_articles(request, by_tag_id:Optional[int]=None):
    if by_tag_id is not None:
        return db.get_articles_by_tag(by_tag_id)
    return db.get_articles()


@api.get("/tags", response=list[TagSchema])
def get_tags(request):
    return db.get_tags()
