from typing import Optional

from fastapi import FastAPI, Request
from pydantic import BaseModel

from app.book_scraper import NaverBookScraper
from app import get_naver_product

app = FastAPI(title="Sellerbox Kiwi", version="1.5.0")

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/getNaverProduct")
async def getNaverProduct(body: get_naver_product.Body):
    body_dict = body.dict()
    try:
        if body_dict is not None:
            keyword = body_dict["keyword"]

            naver_shopping_scraper = get_naver_product.NaverShoppingScraper()
            result = await naver_shopping_scraper.main(keyword, 2)
            return result
    except:
        print("except")

