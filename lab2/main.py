from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Lab 2 API")

class Comment(BaseModel):
    id: int
    article_id: int
    text: str

class Article(BaseModel):
    id: int
    author_id: int
    title: str
    content: str

class Author(BaseModel):
    id: int
    name: str

authors_db = [
    {"id": 1, "name": "Ivan"}
]
articles_db = [
    {"id": 1, "author_id": 1, "title": "API Guide", "content": "REST API concepts"}
]
comments_db = [
    {"id": 1, "article_id": 1, "text": "Useful"}
]

@app.get("/authors", response_model=List[Author])
def get_authors():
    return authors_db

@app.post("/authors", response_model=Author, status_code=201)
def create_author(author: Author):
    authors_db.append(author.dict())
    return author

@app.get("/articles")
def get_articles(
    author_id: Optional[int] = None,
    sort_by: str = Query("id"),
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0)
):
    result = articles_db

    if author_id is not None:
        result = [a for a in result if a["author_id"] == author_id]

    try:
        result = sorted(result, key=lambda x: x[sort_by])
    except KeyError:
        pass

    paginated_result = result[offset : offset + limit]

    for article in paginated_result:
        article["comments"] = [c for c in comments_db if c["article_id"] == article["id"]]

    return paginated_result

@app.post("/articles", status_code=201)
def create_article(article: Article):
    articles_db.append(article.dict())
    return article

@app.put("/articles/{article_id}")
def update_article(article_id: int, updated_article: Article):
    for i, a in enumerate(articles_db):
        if a["id"] == article_id:
            articles_db[i] = updated_article.dict()
            return articles_db[i]
    raise HTTPException(status_code=404, detail="Article not found")

@app.delete("/articles/{article_id}", status_code=204)
def delete_article(article_id: int):
    for i, a in enumerate(articles_db):
        if a["id"] == article_id:
            del articles_db[i]
            return
    raise HTTPException(status_code=404, detail="Article not found")

@app.post("/comments", status_code=201)
def create_comment(comment: Comment):
    comments_db.append(comment.dict())
    return comment
