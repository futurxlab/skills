#!/usr/bin/env python3
"""
arXiv 论文抓取与解析脚本

用法:
  # 方法一：使用预定义分类
  python3 fetch_arxiv.py --category all [--max N] [--days N]
  python3 fetch_arxiv.py --category agent [--max N] [--days N]

  # 方法二：自定义查询
  python3 fetch_arxiv.py --query <查询词> --label <标签> [--max N] [--days N]

参数说明:
  --category  预定义类别，可选值: all, general, agent, rag, persona
  --query     arXiv API search_query 字符串（URL 编码格式）
  --label     该主题在报告中显示的名称，如 "AI Agent"
  --max       最多获取论文数，默认 8
  --days      时间过滤范围（天数），只返回该时间段内更新的论文，默认 7

示例:
  python3 fetch_arxiv.py --category all --days 7

  python3 fetch_arxiv.py \
    --query "cat:cs.AI+AND+all:%22machine+learning%22" \
    --label "机器学习" --max 5 --days 14
"""

import os
import time
import argparse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

# ── 不再使用本地临时文件存储，全程内存解析 ──────────────────────────

NS = {"atom": "http://www.w3.org/2005/Atom"}

# 预定义类别
PREDEFINED_CATEGORIES = {
    "general": {"query": "cat:cs.AI+OR+cat:cs.CL+OR+cat:cs.LG", "label": "通用 AI 进展"},
    "agent": {"query": "cat:cs.AI+AND+all:%22agent%22", "label": "AI Agent"},
    "rag": {"query": "(cat:cs.CL+OR+cat:cs.AI)+AND+(all:%22RAG%22+OR+all:%22knowledge+graph%22)", "label": "RAG / 知识图谱"},
    "persona": {"query": "cat:cs.AI+AND+(all:%22persona%22+OR+all:%22role-playing%22)", "label": "AI 数字分身 / 人格建模"},
}

def fetch(query: str, label: str, max_results: int, days: int) -> list:
    """下载并解析 arXiv 论文，返回时间范围内的条目列表"""
    url = (
        f"https://export.arxiv.org/api/query"
        f"?search_query={query}"
        f"&sortBy=lastUpdatedDate"
        f"&max_results={max_results}"
    )
    try:
        print(f"[arXiv] 正在抓取 [{label}] ...")
        with urllib.request.urlopen(url, timeout=15) as response:
            xml_data = response.read()
    except Exception as e:
        print(f"[错误] [{label}] 下载失败: {e}")
        return []

    # 解析 XML（直接在内存中解析）
    cutoff = datetime.now(tz=timezone.utc) - timedelta(days=days)
    papers = []

    try:
        root = ET.fromstring(xml_data)

        for entry in root.findall("atom:entry", NS):
            # 时间过滤
            updated_str = entry.findtext("atom:updated", default="", namespaces=NS)
            if updated_str:
                try:
                    updated = datetime.fromisoformat(updated_str.replace("Z", "+00:00"))
                    if updated < cutoff:
                        continue
                except ValueError:
                    pass

            title = (
                entry.findtext("atom:title", default="", namespaces=NS)
                .strip().replace("\n", " ")
            )
            summary = (
                entry.findtext("atom:summary", default="", namespaces=NS)
                .strip().replace("\n", " ")
            )[:400]
            published = (
                entry.findtext("atom:published", default="", namespaces=NS) or ""
            )[:10]
            link = entry.findtext("atom:id", default="", namespaces=NS)

            # 作者
            authors = [
                a.findtext("atom:name", default="", namespaces=NS)
                for a in entry.findall("atom:author", NS)
            ]
            author_str = "、".join(authors[:3]) + ("等" if len(authors) > 3 else "")

            papers.append({
                "title": title,
                "summary": summary,
                "published": published,
                "link": link,
                "authors": author_str,
            })

    except ET.ParseError as e:
        print(f"[错误] [{label}] XML 解析失败: {e}")

    return papers


def print_papers(label: str, papers: list):
    """格式化输出论文列表"""
    print(f"\n### {label}（{len(papers)} 篇）")
    if not papers:
        print("  暂无近期论文。")
        return
    for p in papers:
        print(f"\n**{p['title']}**")
        print(f"  - 更新时间：{p['published']}　作者：{p['authors']}")
        print(f"  - 摘要：{p['summary']}...")
        print(f"  - 链接：{p['link']}")


def main():
    parser = argparse.ArgumentParser(description="抓取 arXiv 论文")
    parser.add_argument(
        "--category",
        type=str,
        help="预定义类别: all, general, agent, rag, persona",
    )
    parser.add_argument(
        "--query",
        type=str,
        help="arXiv API search_query 字符串（自定义查询格式）",
    )
    parser.add_argument(
        "--label",
        type=str,
        help="该主题在报告中的显示名称（结合--query使用）",
    )
    parser.add_argument(
        "--max",
        type=int,
        default=8,
        help="最多获取论文数，默认 8",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="时间范围（天数），默认 7",
    )
    args = parser.parse_args()

    # 处理预定义类别模式
    if args.category:
        if args.category == "all":
            cats = list(PREDEFINED_CATEGORIES.keys())
        elif args.category in PREDEFINED_CATEGORIES:
            cats = [args.category]
        else:
            print(f"[错误] 未知类别: {args.category}。可选类别为: all, {', '.join(PREDEFINED_CATEGORIES.keys())}")
            return
            
        print(f"\n=== arXiv 论文精选（最近 {args.days} 天 | 类别: {args.category}）===\n")
        for cat in cats:
            info = PREDEFINED_CATEGORIES[cat]
            papers = fetch(info["query"], info["label"], args.max, args.days)
            print_papers(info["label"], papers)

    # 处理自定义查询模式
    elif args.query and args.label:
        print(f"\n=== arXiv 论文精选（最近 {args.days} 天 | 自定义: {args.label}）===\n")
        papers = fetch(args.query, args.label, args.max, args.days)
        print_papers(args.label, papers)

    else:
        print("[错误] 必须提供 --category (如 all) 或同时提供 --query 和 --label。")
        parser.print_help()

    print("\n--- 抓取完毕 ---")


if __name__ == "__main__":
    main()
