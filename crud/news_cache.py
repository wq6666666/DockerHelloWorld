from cache.news_cache import (
    get_cached_categories,
    set_cache_categories,
    get_cache_news_list,
    set_cache_news_list,
    get_cache_news_detail,
    set_cache_news_detail, cache_related_news, get_cache_related_news,
    set_cache_rank_news,get_cache_rank_news
)

from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from models.news import Category, News
from sqlalchemy import select, func, update, desc

async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    cache = await get_cached_categories()
    if cache:
        return cache

    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    categories = result.scalars().all()  # orm

    if categories:
        categories = jsonable_encoder(categories)
        await set_cache_categories(categories)
    return categories

async def get_news_list(db: AsyncSession, category_id: int, skip: int = 0, page_size: int = 10):
    # 读取缓存
    cache_list = await get_cache_news_list(category_id, skip // page_size + 1, page_size)
    if cache_list:
        # return [News(**item) for item in cache_list]
        return cache_list
    stmt = select(News).where(News.category_id == category_id). \
        offset(skip).limit(page_size)
    result = await db.execute(stmt)
    news_list = result.scalars().all()

    if news_list:
        # orm转换为字典   1,先转pydantic在转字典 2，jsonable_encoder
        # news_data = [NewsItemBase.model_validate(item).model_dump(mode="json",by_alias=False) for item in news_list]
        news_data = jsonable_encoder(news_list)
        await set_cache_news_list(category_id, skip // page_size + 1, page_size, news_data)
    return news_list


async def get_news_count(db: AsyncSession, category_id: int):
    stmt = select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(stmt)
    return result.scalar_one()  # 只能有一个结果，否则报错


async def get_news_detail(db: AsyncSession, news_id: int):
    cache = await get_cache_news_detail(news_id)
    if cache:
        return News(**cache)

    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    detail = result.scalar_one_or_none()

    if detail:
        detail_str = jsonable_encoder(detail)
        await set_cache_news_detail(news_id, detail_str)
    return detail



async def increase_news_views(db: AsyncSession, news_id: int):
    stmt = update(News).where(News.id == news_id).values(views=News.views + 1)
    result = await db.execute(stmt)
    await db.commit()
    # 更新检查数据库是否命中数据->命中了返回True
    return result.rowcount > 0


async def get_related_news(db: AsyncSession, news_id: int, category_id: int, limit: int = 5):
    cache = await get_cache_related_news(news_id,category_id)
    if cache:
        return cache

    stmt = select(News.id, News.title, News.content, News.image, News.author, News.publish_time.label('publishTime'),
                  News.category_id.label('categoryId'), News.views). \
        where(News.category_id == category_id, News.id != news_id). \
        order_by(News.views.desc(), News.publish_time.desc()).limit(limit)
    result = await db.execute(stmt)
    related_news = result.mappings().all()

    if related_news:
        related_data = jsonable_encoder(related_news)
        await cache_related_news(news_id, category_id, related_data)
        return related_data
    return []

#获取最受欢迎的前几名的新闻
async def get_rank_news(db:AsyncSession,rank:int,category_id:int):
    cache = await get_cache_rank_news(rank,category_id)
    if cache:
        return cache
    stmt = select(News).where(News.category_id == category_id).order_by(News.views.desc()).limit(rank)
    result = await db.execute(stmt)
    rank_news = result.scalars().all()

    if rank_news:
        rank_data = jsonable_encoder(rank_news)
        await set_cache_rank_news(rank,category_id, rank_data)
        return rank_data
    return []


