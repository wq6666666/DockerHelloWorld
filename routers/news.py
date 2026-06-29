from fastapi import APIRouter,Depends,Query,HTTPException
from configs.db_config import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from enum import Enum
from typing import Annotated
from crud import news_cache
from utils.response import success_response

router = APIRouter(prefix="/news",tags=["news"])

@router.get("/list")
async def get_news_list(
        # category_id:Annotated[int,Query(alias="categoryId")] ,和下面Query(...,)等价
        category_id: int = Query(..., alias="categoryId"),
        page:int = 1,
        page_size:int = Query(10,le=100,alias="pageSize"),
        db: AsyncSession = Depends(get_db)
):
    skip = (page - 1)* page_size
    news_list = await news_cache.get_news_list(db, category_id, skip, page_size)
    total = await news_cache.get_news_count(db,category_id)
    return {
        "code": 200,
        "message":"success",
        "data":{
            "list":news_list,
            "total":total,
            "hasMore": total > len(news_list) + skip
        }
    }

@router.get("/detail")
async def read_news_detail(news_id: int=Query(...,alias="id"),db: AsyncSession = Depends(get_db)):
    detail = await news_cache.get_news_detail(db,news_id)
    if not detail:
        raise HTTPException(
            status_code=404,
            detail="新闻不存在"
        )
    if not await news_cache.increase_news_views(db, news_id):
        raise HTTPException(
            status_code=404,
            detail="新闻不存在"
        )
    related_list = await news_cache.get_related_news(db,news_id,detail.category_id)
    return {
        "code":200,
        "message":"successful",
        "data":{
            "id": detail.id,
            "title": detail.title,
            "content": detail.content,
            "image": detail.image,
            "author": detail.author,
            "publishTime": detail.publish_time,
            "categoryId": detail.category_id,
            "views": detail.views,
            "relatedNews": related_list

        }
    }

@router.get("/rank")
async def get_rang_new(rank:int,category_id:int,db: AsyncSession = Depends(get_db)):
    rank_news = await news_cache.get_rank_news(db,rank,category_id)
    return success_response("success",data=rank_news)