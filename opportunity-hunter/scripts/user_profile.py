#!/usr/bin/env python3
"""
Opportunity Hunter - 用户画像持久化管理

功能：
  - 保存用户画像到本地 JSON 文件
  - 加载已有用户画像
  - 更新用户画像字段
  - 记录用户关注过的机会和复盘历史

用法：
  python user_profile.py save --name "用户名" --data '{"key": "value"}'
  python user_profile.py load --name "用户名"
  python user_profile.py update --name "用户名" --field "risk_preference" --value "moderate"
  python user_profile.py add-opportunity --name "用户名" --opportunity '{"name": "AI工具开发", "score": "A", "status": "tracking"}'
  python user_profile.py list
"""

import json
import os
import sys
import argparse
from datetime import datetime
from pathlib import Path

# 用户画像存储目录
PROFILE_DIR = Path.home() / ".claude" / "opportunity-hunter-profiles"


def ensure_dir():
    """确保存储目录存在"""
    PROFILE_DIR.mkdir(parents=True, exist_ok=True)


def get_profile_path(name: str) -> Path:
    """获取用户画像文件路径"""
    safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in name)
    return PROFILE_DIR / f"{safe_name}.json"


def save_profile(name: str, data: dict):
    """保存完整用户画像"""
    ensure_dir()
    profile = {
        "name": name,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "profile": data,
        "opportunities": [],
        "reviews": []
    }

    # 如果已存在，保留历史数据
    path = get_profile_path(name)
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            existing = json.load(f)
        profile["created_at"] = existing.get("created_at", profile["created_at"])
        profile["opportunities"] = existing.get("opportunities", [])
        profile["reviews"] = existing.get("reviews", [])

    profile["updated_at"] = datetime.now().isoformat()

    with open(path, "w", encoding="utf-8") as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)

    print(json.dumps({"status": "saved", "path": str(path), "profile": profile}, ensure_ascii=False, indent=2))


def load_profile(name: str):
    """加载用户画像"""
    path = get_profile_path(name)
    if not path.exists():
        print(json.dumps({"status": "not_found", "message": f"未找到用户 '{name}' 的画像"}, ensure_ascii=False))
        return

    with open(path, "r", encoding="utf-8") as f:
        profile = json.load(f)

    print(json.dumps({"status": "loaded", "data": profile}, ensure_ascii=False, indent=2))


def update_field(name: str, field: str, value: str):
    """更新用户画像的特定字段"""
    path = get_profile_path(name)
    if not path.exists():
        print(json.dumps({"status": "error", "message": f"未找到用户 '{name}' 的画像，请先创建"}, ensure_ascii=False))
        return

    with open(path, "r", encoding="utf-8") as f:
        profile = json.load(f)

    # 尝试解析 JSON 值
    try:
        parsed_value = json.loads(value)
    except (json.JSONDecodeError, TypeError):
        parsed_value = value

    profile["profile"][field] = parsed_value
    profile["updated_at"] = datetime.now().isoformat()

    with open(path, "w", encoding="utf-8") as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)

    print(json.dumps({"status": "updated", "field": field, "value": parsed_value}, ensure_ascii=False, indent=2))


def add_opportunity(name: str, opportunity: dict):
    """添加关注的机会记录"""
    path = get_profile_path(name)
    if not path.exists():
        print(json.dumps({"status": "error", "message": f"未找到用户 '{name}' 的画像"}, ensure_ascii=False))
        return

    with open(path, "r", encoding="utf-8") as f:
        profile = json.load(f)

    opportunity["added_at"] = datetime.now().isoformat()
    opportunity.setdefault("status", "tracking")  # tracking / executing / paused / completed / abandoned
    profile["opportunities"].append(opportunity)
    profile["updated_at"] = datetime.now().isoformat()

    with open(path, "w", encoding="utf-8") as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)

    print(json.dumps({"status": "added", "opportunity": opportunity}, ensure_ascii=False, indent=2))


def add_review(name: str, review: dict):
    """添加复盘记录"""
    path = get_profile_path(name)
    if not path.exists():
        print(json.dumps({"status": "error", "message": f"未找到用户 '{name}' 的画像"}, ensure_ascii=False))
        return

    with open(path, "r", encoding="utf-8") as f:
        profile = json.load(f)

    review["reviewed_at"] = datetime.now().isoformat()
    profile["reviews"].append(review)
    profile["updated_at"] = datetime.now().isoformat()

    with open(path, "w", encoding="utf-8") as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)

    print(json.dumps({"status": "added", "review": review}, ensure_ascii=False, indent=2))


def list_profiles():
    """列出所有已保存的用户画像"""
    ensure_dir()
    profiles = []
    for f in PROFILE_DIR.glob("*.json"):
        with open(f, "r", encoding="utf-8") as fp:
            data = json.load(fp)
        profiles.append({
            "name": data.get("name", f.stem),
            "created_at": data.get("created_at", "unknown"),
            "updated_at": data.get("updated_at", "unknown"),
            "opportunities_count": len(data.get("opportunities", [])),
            "reviews_count": len(data.get("reviews", []))
        })

    print(json.dumps({"status": "ok", "profiles": profiles, "count": len(profiles)}, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Opportunity Hunter 用户画像管理")
    subparsers = parser.add_subparsers(dest="command", help="操作类型")

    # save
    p_save = subparsers.add_parser("save", help="保存用户画像")
    p_save.add_argument("--name", required=True, help="用户名称")
    p_save.add_argument("--data", required=True, help="画像数据 (JSON)")

    # load
    p_load = subparsers.add_parser("load", help="加载用户画像")
    p_load.add_argument("--name", required=True, help="用户名称")

    # update
    p_update = subparsers.add_parser("update", help="更新画像字段")
    p_update.add_argument("--name", required=True, help="用户名称")
    p_update.add_argument("--field", required=True, help="字段名")
    p_update.add_argument("--value", required=True, help="字段值")

    # add-opportunity
    p_opp = subparsers.add_parser("add-opportunity", help="添加关注机会")
    p_opp.add_argument("--name", required=True, help="用户名称")
    p_opp.add_argument("--opportunity", required=True, help="机会数据 (JSON)")

    # add-review
    p_rev = subparsers.add_parser("add-review", help="添加复盘记录")
    p_rev.add_argument("--name", required=True, help="用户名称")
    p_rev.add_argument("--review", required=True, help="复盘数据 (JSON)")

    # list
    subparsers.add_parser("list", help="列出所有画像")

    args = parser.parse_args()

    if args.command == "save":
        data = json.loads(args.data)
        save_profile(args.name, data)
    elif args.command == "load":
        load_profile(args.name)
    elif args.command == "update":
        update_field(args.name, args.field, args.value)
    elif args.command == "add-opportunity":
        opp = json.loads(args.opportunity)
        add_opportunity(args.name, opp)
    elif args.command == "add-review":
        rev = json.loads(args.review)
        add_review(args.name, rev)
    elif args.command == "list":
        list_profiles()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
