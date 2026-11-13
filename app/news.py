import asyncio
import feedparser
import httpx
from app.config import settings

async def _fetch(client,url):
    try:
        r=await client.get(url); r.raise_for_status()
        parsed=feedparser.parse(r.content)
        title=parsed.feed.get("title",url)
        return [{"title":str(e.get("title", ""))[:500],"link":str(e.get("link", ""))[:1000],"published":str(e.get("published", ""))[:100],"source":str(title)[:200]} for e in parsed.entries[:settings.news_limit] if e.get("title")]
    except Exception as exc:
        return [{"title":f"News feed unavailable: {type(exc).__name__}","source":url,"link":"","published":"","error":True}]

async def recent_news(limit=None):
    urls=settings.feed_urls
    if not urls: return []
    async with httpx.AsyncClient(timeout=settings.news_timeout_seconds,follow_redirects=True,headers={"User-Agent":"AIQuantTraderMVP/1.0"}) as client:
        batches=await asyncio.gather(*[_fetch(client,u) for u in urls],return_exceptions=True)
    result=[]
    for batch in batches:
        if isinstance(batch,list): result.extend(batch)
    return result[:min(limit or settings.news_limit,50)]
