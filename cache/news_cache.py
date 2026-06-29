from typing import Dict, Any, Optional

from configs.cache_config import get_json_cache,set_cache

CATEGORIES_KEY = "news:categories"
NEWS_LIST_PREFIX = "news_list:"
NEWS_DETAIL_PREFIX = "news:detail:"
RELATED_NEWS_PREFIX = "news:related:"
RANK_NEWS_PREFIX = "news:category:int:ranks:"

#获取新闻分类缓存
async def get_cached_categories():
    return await get_json_cache(CATEGORIES_KEY)

#写入新闻分类缓存
#分类，配置 7200：列表：600；详情：1800；验证码：120 -- 数据越稳定，缓存越持久
# 避免所有key同时过期 引起缓存雪崩
async def set_cache_categories(data: list[Dict[str,Any]],expire:int=7200):
    return await set_cache(CATEGORIES_KEY,data,expire)


#写入缓存：新闻列表 key = news_list:分类ID：页码，每页数量 + value + 过期时间
async def set_cache_news_list(
        category_id:Optional[int],
        page:int,
        size:int,
        news_list:list[Dict[str,Any]],
        expire:int=1800
):
    key = f"{NEWS_LIST_PREFIX}{category_id if category_id is not None else "all"}:{page}:{size}"
    return await set_cache(key,news_list,expire)

#读取缓存-新闻列表
async def get_cache_news_list(
        category_id:Optional[int],
        page:int,
        size:int,
):
    key = f"{NEWS_LIST_PREFIX}{category_id if category_id is not None else "all"}:{page}:{size}"
    return await get_json_cache(key)


#获取缓存新闻详情
async def get_cache_news_detail(news_id:int):
    return await get_json_cache(f"{NEWS_DETAIL_PREFIX}{news_id}")

#缓存欣慰详情
async def set_cache_news_detail(news_id:int,news_detail:Dict[str,Any],expire:int=300):
    key = f"{NEWS_DETAIL_PREFIX}{news_id}"
    return await set_cache(key,news_detail,expire)


#相关新闻列表

async def cache_related_news(news_id:int,category_id:int,related_list:list[Dict[str,Any]],expire:int=1800):
    key = f"{RELATED_NEWS_PREFIX}{news_id}:{category_id}"
    return await set_cache(key,related_list,expire)

async def get_cache_related_news(news_id:int,category_id:int):
    key = f"{RELATED_NEWS_PREFIX}{news_id}:{category_id}"
    return await get_json_cache(key)

async def get_cache_rank_news(rank:int,category_id:int):
    key = f"{RANK_NEWS_PREFIX}:{category_id}:{rank}"
    return await get_json_cache(key)

async def set_cache_rank_news(rank:int,category_id,rank_list:list[dict[str,Any]],expire:int=1800):
    key = f"{RANK_NEWS_PREFIX}:{category_id}:{rank}"
    return await set_cache(key,rank_list,expire)