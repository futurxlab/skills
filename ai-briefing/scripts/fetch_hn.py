#!/usr/bin/env python3
"""
Hacker News 榜单抓取脚本（Algolia 高效版 / AI 过滤版）

用法: python3 fetch_hn.py [--days N] [--limit N]
默认: 抓取最近 7 天内 Hacker News 综合排名前 N 的全部帖子（不限类别）。

设计哲学：
- 极速：利用 HN 官方提供的 Algolia API，单次请求 0.5 秒内返回完整榜单数据，彻底告别 100 次循环请求。
- 智能：脚本不再使用硬编码的正则表达式或关键词进行“死板”过滤，而是全量拉取 50 篇最火帖子，
  然后由大模型（运行该技能的 Agent）凭借世界知识自主判断、甄别并筛选出其中的前沿科技及 AI 相关重点。
"""

import argparse
import urllib.request
import urllib.parse
import json
from datetime import datetime, timedelta

def fetch_hn(days: int = 7, limit: int = 50):
    """
    通过 Algolia API 抓取 HN 上指定天数内分数最高的 N 篇帖子
    注意：不进行任何本地 AI 关键词过滤。这是为了让调用的 Agent 能看到全局，做智能筛选。
    """
    cutoff = int((datetime.now() - timedelta(days=days)).timestamp())
    
    # 我们故意不指定具体的搜索查询词，以获得该时间段内的最热门（综合）内容
    params = {
        'tags': 'story',
        'numericFilters': f'created_at_i>{cutoff}',
        'hitsPerPage': str(limit),
    }
    
    url = f'http://hn.algolia.com/api/v1/search?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 / FuturMind-Skill-Bot'})
    
    print(f"[HN] 正在极速获取最近 {days} 天的前 {limit} 项 HN 综合热点...\n")
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read())
            
            hits = data.get('hits', [])
            
            print(f"=== Hacker News 综合热点（共 {len(hits)} 条，由 Agent 稍后智能筛选其中 AI 相关内容）===")
            print("| 分数 | 评论 | 日期 | 标题 | 来源 |")
            print("|------|------|------|------|------|")
            
            for hit in hits:
                score = hit.get('points', 0)
                comments = hit.get('num_comments', 0)
                created_at = hit.get('created_at', '')[:10]
                title = hit.get('title', '').replace('\n', ' ')
                
                # Hacker News 的原始 URL 和其外部链接
                url_str = hit.get('url', '')
                source_link = f"[链接]({url_str})" if url_str else "—"
                hn_url = f"https://news.ycombinator.com/item?id={hit.get('objectID', '')}"
                
                print(f"| {score} | {comments} | {created_at} | [{title}]({hn_url}) | {source_link} |")
                
            print(f"\n[提示] 以上是全类别热门清单。请 Agent 根据技术敏感度，自主筛选出 AI、前沿硬核技术相关的精华加入最终简报。")

    except Exception as e:
        print(f"[错误] 获取 HN 数据失败: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="抓取 Hacker News 综合热点信息")
    parser.add_argument("--days", type=int, default=7, help="时间范围（天数），默认 7")
    parser.add_argument("--limit", type=int, default=50, help="获取的最大条目数，默认 50，供 AI 筛选")
    args = parser.parse_args()

    fetch_hn(days=args.days, limit=args.limit)
