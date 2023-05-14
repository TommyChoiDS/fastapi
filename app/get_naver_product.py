
from pydantic import BaseModel
from typing import Optional
import asyncio
import aiohttp


# fastapi는 post를 받을 때 반드시 pydantic을 통해서만 받을 수 있다.
class Body(BaseModel):
    keyword: Optional[str] = '고양이'


class NaverShoppingScraper:

    querystring = {"eq": "",
                    "frm": "NVSHCHK",
                    "iq": "",
                    "origQuery": "",
                    "pagingIndex": "1",
                    "pagingSize": "80",
                    "productSet": "checkout",
                    "query": "",
                    "sort": "rel",
                    "viewType": "list",
                    "xq": ""}

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/112.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://search.shopping.naver.com/search/all?frm=NVSHCHK&origQuery=%EA%B3%A0%EC%96%91%EC%9D%B4&pagingIndex=1&pagingSize=40&productSet=checkout&query=%EA%B3%A0%EC%96%91%EC%9D%B4&sort=rel&timestamp=&viewType=list",
        "logic": "PART",
        "sbth": "bbceef35e6bc4b1921a6feade64c9c9e38ee02aa775f1702d9d1d07e6db4f5a5bb5d50ca93b5b0aa2949ddd31af18f11",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin"
    }

    @staticmethod
    async def fetch(session, url, headers, querystring):
        async with session.get(url, headers=headers, params=querystring) as response:
            if response.status == 200:
                result = await response.json()
                return result

    def unit_url(self, keyword, paging_index):

        headers = self.headers
        querystring = self.querystring
        querystring['query'] = keyword
        querystring['pagingIndex'] = paging_index
        return {
            "url": "https://search.shopping.naver.com/api/search/all",
            "headers" : headers,
            "querystring" : querystring
        }

    async def main(self, keyword, total_page):
        async with aiohttp.ClientSession() as session:
            apis = [self.unit_url(keyword, paging_index) for paging_index in range(total_page)]
            all_data = await asyncio.gather(
                *[NaverShoppingScraper.fetch(session, api["url"], api["headers"], api["querystring"]) for api in apis]
            )
        return all_data





# ---
# def main(keywords):
#     result = dict()
#     category = dict()
#     productList = list()
#     pageProductList = list()
#     NAVER_PRODUCT_PAGE = 2
#     relatedKeywordList = [dict()]
#     pageList = [dict()] * NAVER_PRODUCT_PAGE
#     g.task.append(requestInfo.NAVER_SHOPPING_PRODUCT_HTML(keywords, relatedKeywordList, 0))
#     for index in range(NAVER_PRODUCT_PAGE):
#         g.task.append(requestInfo.NAVER_SHOPPING_PRODUCT_API(index, keywords, pageList))

#     function.runUntilComplete()

#     try:
#         pageList[0]["shoppingResult"]["products"]
#     except KeyError:
#         return function.returnError(502, "empty product")

#     try:
#         pageList[1]["shoppingResult"]["products"] = pageList[1]["shoppingResult"]["products"][:20]
#         pageList[1]["searchAdResult"]["products"] = pageList[1]["searchAdResult"]["products"][:3]
#     except Exception:
#         pass
#     relatedKeyword = relatedKeywordList[0]["props"]["pageProps"]["initialState"]["relatedTags"]
#     for i in range(len(pageList)):
#         try:
#             for j in range(len(pageList[i]["shoppingResult"]["products"])):
#                 try:
#                     pageProductList.append(pageList[i]["shoppingResult"]["products"][j])
#                     pageProductList[i]["rank"] = j + 1
#                     function.getCategory(pageList[i]["shoppingResult"]["products"][j], category)
#                 except KeyError:
#                     pass
#             if pageList[i].get("searchAdResult") != None:
#                 for k in range(len(pageList[i]["searchAdResult"]["products"])):
#                     try:
#                         pageProductList.append(pageList[i]["searchAdResult"]["products"][k])
#                         pageProductList[k]["rank"] = k + 1
#                         function.getCategory(pageList[i]["searchAdResult"]["products"][k], category)
#                     except KeyError:
#                         pass
#         except KeyError:
#             pass
#     functionList.setProductList(pageProductList, productList)
#     function.runUntilComplete()
#     result["smartStoreRelatedKeyWords"] = relatedKeyword
#     result["shoppingList"] = productList
#     result["productCount"] = pageList[0]["productSetFilter"]["filterValues"][2]["productCount"]
#     result["categoryName"] = category
#     return result
