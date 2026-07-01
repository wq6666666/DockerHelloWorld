from typing import Any
import redis.asyncio as redis
import json
from settings import settings

redis_client = redis.Redis(**settings.redis_client)
#设置和读取（字符串和列表或字典）"[{}]"
#读取字符串
async def get_cache(key:str):
    # return await redis_client.get(key)
    try:
        return await redis_client.get(key)
    except Exception as e:
        print(f"获取缓存失败:{e}")
        return None

#读取列表或字典
async def get_json_cache(key:str):
    try:
        data = await redis_client.get(key)
        if data:
             return json.loads(data)
        return None
    except Exception as e:
        print(f"获取json格式缓存失败:{e}")
        return None


#设置缓存
async def set_cache(key:str,value:Any,expire:int=3600):
    try:
        if isinstance(value,(list,dict)):  #判断类型
            value = json.dumps(value,ensure_ascii=False) #中文正常保存
        await redis_client.setex(key,expire,value)
        return True
    except Exception as e:
        print(f"设置缓存失败:{e}")
        return False