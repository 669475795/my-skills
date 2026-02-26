#!/usr/bin/env python3
"""
Opportunity Hunter - 趋势数据抓取器

功能：
  - 从多个公开数据源抓取趋势信息
  - 聚合创投融资数据
  - 抓取行业报告摘要
  - 获取平台热搜/热榜数据
  - 获取宏观经济指标

用法：
  python trend_fetcher.py trends          # 综合趋势扫描
  python trend_fetcher.py hot-search      # 各平台热搜聚合
  python trend_fetcher.py funding         # 近期融资事件
  python trend_fetcher.py macro           # 宏观经济指标
  python trend_fetcher.py industry <行业>  # 特定行业数据

依赖：
  pip install requests beautifulsoup4
"""

import json
import sys
import argparse
from datetime import datetime, timedelta
from urllib.parse import quote

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False


def check_dependencies():
    """检查依赖是否安装"""
    missing = []
    if not HAS_REQUESTS:
        missing.append("requests")
    if not HAS_BS4:
        missing.append("beautifulsoup4")
    if missing:
        print(json.dumps({
            "status": "error",
            "message": f"缺少依赖包: {', '.join(missing)}",
            "fix": f"pip install {' '.join(missing)}"
        }, ensure_ascii=False, indent=2))
        return False
    return True


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def fetch_weibo_hot():
    """获取微博热搜"""
    try:
        url = "https://weibo.com/ajax/side/hotSearch"
        resp = requests.get(url, headers=HEADERS, timeout=10)
        data = resp.json()
        items = []
        for item in data.get("data", {}).get("realtime", [])[:20]:
            items.append({
                "rank": item.get("rank", 0),
                "title": item.get("note", ""),
                "hot_value": item.get("num", 0),
                "category": item.get("category", ""),
                "label": item.get("label_name", "")
            })
        return {"source": "微博热搜", "items": items, "status": "ok"}
    except Exception as e:
        return {"source": "微博热搜", "status": "error", "message": str(e)}


def fetch_zhihu_hot():
    """获取知乎热榜"""
    try:
        url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total"
        resp = requests.get(url, headers={**HEADERS, "Accept": "application/json"}, timeout=10)
        data = resp.json()
        items = []
        for item in data.get("data", [])[:20]:
            target = item.get("target", {})
            items.append({
                "title": target.get("title", ""),
                "excerpt": target.get("excerpt", "")[:100],
                "hot_value": item.get("detail_text", "")
            })
        return {"source": "知乎热榜", "items": items, "status": "ok"}
    except Exception as e:
        return {"source": "知乎热榜", "status": "error", "message": str(e)}


def fetch_baidu_hot():
    """获取百度热搜"""
    try:
        url = "https://top.baidu.com/api/board?platform=wise&tab=realtime"
        resp = requests.get(url, headers=HEADERS, timeout=10)
        data = resp.json()
        items = []
        for item in data.get("data", {}).get("cards", [{}])[0].get("content", [])[:20]:
            items.append({
                "title": item.get("word", ""),
                "desc": item.get("desc", ""),
                "hot_value": item.get("hotScore", 0)
            })
        return {"source": "百度热搜", "items": items, "status": "ok"}
    except Exception as e:
        return {"source": "百度热搜", "status": "error", "message": str(e)}


def fetch_36kr_newsflash():
    """获取36氪快讯（创投动态）"""
    try:
        url = "https://gateway.36kr.com/api/mis/nav/newsflash/flow"
        payload = {
            "partner_id": "wap",
            "param": {
                "pageSize": 20,
                "pageEvent": 0,
                "siteId": 1,
                "platformId": 2
            },
            "timestamp": int(datetime.now().timestamp())
        }
        resp = requests.post(url, json=payload, headers=HEADERS, timeout=10)
        data = resp.json()
        items = []
        for item in data.get("data", {}).get("itemList", [])[:20]:
            template = item.get("templateMaterial", {})
            items.append({
                "title": template.get("widgetTitle", ""),
                "summary": template.get("widgetContent", "")[:150],
                "time": template.get("publishTime", "")
            })
        return {"source": "36氪快讯", "items": items, "status": "ok"}
    except Exception as e:
        return {"source": "36氪快讯", "status": "error", "message": str(e)}


def fetch_hn_top():
    """获取 Hacker News Top Stories（全球科技趋势）"""
    try:
        ids_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        resp = requests.get(ids_url, timeout=10)
        top_ids = resp.json()[:15]

        items = []
        for sid in top_ids:
            item_url = f"https://hacker-news.firebaseio.com/v0/item/{sid}.json"
            item_resp = requests.get(item_url, timeout=5)
            item = item_resp.json()
            if item:
                items.append({
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "score": item.get("score", 0),
                    "comments": item.get("descendants", 0)
                })

        return {"source": "Hacker News Top", "items": items, "status": "ok"}
    except Exception as e:
        return {"source": "Hacker News Top", "status": "error", "message": str(e)}


def fetch_producthunt():
    """获取 Product Hunt 热门产品"""
    try:
        url = "https://www.producthunt.com"
        resp = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")

        items = []
        # 尝试提取产品信息
        for tag in soup.find_all("a", {"data-test": True})[:10]:
            title = tag.get_text(strip=True)
            if title:
                items.append({"title": title, "url": url + tag.get("href", "")})

        if not items:
            return {"source": "Product Hunt", "status": "ok", "items": [], "note": "需要通过 WebFetch 获取更详细的内容"}

        return {"source": "Product Hunt", "items": items, "status": "ok"}
    except Exception as e:
        return {"source": "Product Hunt", "status": "error", "message": str(e)}


def fetch_github_trending():
    """获取 GitHub Trending（技术趋势）"""
    try:
        url = "https://api.github.com/search/repositories?q=created:>{}&sort=stars&order=desc&per_page=10".format(
            (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        )
        resp = requests.get(url, headers={**HEADERS, "Accept": "application/vnd.github.v3+json"}, timeout=10)
        data = resp.json()
        items = []
        for repo in data.get("items", [])[:10]:
            items.append({
                "name": repo.get("full_name", ""),
                "description": (repo.get("description", "") or "")[:100],
                "stars": repo.get("stargazers_count", 0),
                "language": repo.get("language", ""),
                "url": repo.get("html_url", "")
            })
        return {"source": "GitHub Trending (本周)", "items": items, "status": "ok"}
    except Exception as e:
        return {"source": "GitHub Trending", "status": "error", "message": str(e)}


def scan_trends():
    """综合趋势扫描"""
    print(json.dumps({"status": "scanning", "message": "正在扫描多个数据源..."}, ensure_ascii=False))

    results = {
        "scan_time": datetime.now().isoformat(),
        "sources": []
    }

    # 国内热搜
    results["sources"].append(fetch_baidu_hot())
    results["sources"].append(fetch_weibo_hot())
    results["sources"].append(fetch_zhihu_hot())

    # 创投动态
    results["sources"].append(fetch_36kr_newsflash())

    # 全球科技趋势
    results["sources"].append(fetch_hn_top())
    results["sources"].append(fetch_github_trending())

    print(json.dumps(results, ensure_ascii=False, indent=2))


def scan_hot_search():
    """各平台热搜聚合"""
    results = {
        "scan_time": datetime.now().isoformat(),
        "sources": [
            fetch_baidu_hot(),
            fetch_weibo_hot(),
            fetch_zhihu_hot()
        ]
    }
    print(json.dumps(results, ensure_ascii=False, indent=2))


def scan_funding():
    """近期融资事件扫描"""
    results = {
        "scan_time": datetime.now().isoformat(),
        "sources": [
            fetch_36kr_newsflash()
        ],
        "note": "如需更详细的融资数据，建议配合 WebSearch 搜索 'IT桔子 融资' 或 '投资界 融资'"
    }
    print(json.dumps(results, ensure_ascii=False, indent=2))


def scan_macro():
    """宏观经济指标概览"""
    # 使用公开可用的数据接口
    results = {
        "scan_time": datetime.now().isoformat(),
        "note": "宏观数据建议配合 WebSearch 搜索最新 CPI、PMI、GDP 等数据",
        "suggested_searches": [
            "中国 CPI PPI 最新数据",
            "PMI 制造业 非制造业 最新",
            "社会融资规模 最新",
            "美联储利率决议 最新",
            "中国 GDP 增速 季度",
            "居民消费 趋势 数据"
        ]
    }
    print(json.dumps(results, ensure_ascii=False, indent=2))


def scan_industry(industry: str):
    """特定行业数据扫描"""
    results = {
        "scan_time": datetime.now().isoformat(),
        "industry": industry,
        "suggested_searches": [
            f"{industry} 行业报告 {datetime.now().year}",
            f"{industry} 市场规模 增速",
            f"{industry} 融资 投资 最新",
            f"{industry} 头部企业 竞争格局",
            f"{industry} 政策 监管 最新",
            f"{industry} 创业 机会 趋势",
            f"{industry} industry report {datetime.now().year}",
            f"{industry} market size growth"
        ],
        "note": "请将以上关键词通过 WebSearch 搜索获取最新行业数据"
    }

    # 同时尝试抓取相关热搜
    hot_results = fetch_baidu_hot()
    if hot_results["status"] == "ok":
        related = [
            item for item in hot_results.get("items", [])
            if industry in item.get("title", "") or industry in item.get("desc", "")
        ]
        if related:
            results["related_hot_topics"] = related

    print(json.dumps(results, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Opportunity Hunter 趋势数据抓取器")
    subparsers = parser.add_subparsers(dest="command", help="操作类型")

    subparsers.add_parser("trends", help="综合趋势扫描")
    subparsers.add_parser("hot-search", help="各平台热搜聚合")
    subparsers.add_parser("funding", help="近期融资事件")
    subparsers.add_parser("macro", help="宏观经济指标")

    p_industry = subparsers.add_parser("industry", help="特定行业数据")
    p_industry.add_argument("name", help="行业名称")

    args = parser.parse_args()

    if not check_dependencies():
        sys.exit(1)

    if args.command == "trends":
        scan_trends()
    elif args.command == "hot-search":
        scan_hot_search()
    elif args.command == "funding":
        scan_funding()
    elif args.command == "macro":
        scan_macro()
    elif args.command == "industry":
        scan_industry(args.name)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
