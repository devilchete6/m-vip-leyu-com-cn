from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

# 配置示例数据
SAMPLE_KEYWORD = "乐鱼体育"
SAMPLE_URL = "https://m-vip-leyu.com.cn"


@dataclass
class KeywordNote:
    """表示一条关键词笔记的数据类"""
    keyword: str
    url: str
    note: str = ""
    tags: List[str] = field(default_factory=list)
    created_at: Optional[datetime] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

    def to_dict(self) -> dict:
        return {
            "keyword": self.keyword,
            "url": self.url,
            "note": self.note,
            "tags": self.tags,
            "created_at": self.created_at.isoformat()
        }


@dataclass
class KeywordNotesCollection:
    """管理多组关键词笔记的集合类"""
    notes: List[KeywordNote] = field(default_factory=list)

    def add_note(self, keyword: str, url: str, note: str = "",
                 tags: Optional[List[str]] = None) -> KeywordNote:
        new_note = KeywordNote(
            keyword=keyword,
            url=url,
            note=note,
            tags=tags or []
        )
        self.notes.append(new_note)
        return new_note

    def find_by_keyword(self, keyword: str) -> List[KeywordNote]:
        return [n for n in self.notes if keyword.lower() in n.keyword.lower()]

    def find_by_tag(self, tag: str) -> List[KeywordNote]:
        return [n for n in self.notes if tag in n.tags]

    def format_all_notes(self) -> str:
        """将所有笔记格式化为易读的字符串"""
        if not self.notes:
            return "暂无笔记。"
        lines = []
        for idx, note in enumerate(self.notes, 1):
            lines.append(f"笔记 #{idx}")
            lines.append(f"  关键词: {note.keyword}")
            lines.append(f"  URL: {note.url}")
            if note.note:
                lines.append(f"  备注: {note.note}")
            if note.tags:
                lines.append(f"  标签: {', '.join(note.tags)}")
            lines.append(f"  创建时间: {note.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            lines.append("")
        return "\n".join(lines)

    def format_brief_list(self) -> str:
        """生成简短列表格式"""
        entries = []
        for i, note in enumerate(self.notes, 1):
            tags_str = f" [{', '.join(note.tags)}]" if note.tags else ""
            entries.append(f"{i}. {note.keyword} - {note.url}{tags_str}")
        return "\n".join(entries) if entries else "暂无笔记。"


def demonstrate():
    """演示函数，展示基本用法"""
    collection = KeywordNotesCollection()

    # 添加示例数据
    collection.add_note(
        keyword=SAMPLE_KEYWORD,
        url=SAMPLE_URL,
        note="这是一个示例关键词笔记，用于演示数据结构。",
        tags=["体育", "娱乐", "示例"]
    )
    collection.add_note(
        keyword="人工智能",
        url="https://example.com/ai",
        note="通用人工智能相关笔记。",
        tags=["科技", "AI"]
    )
    collection.add_note(
        keyword="乐鱼体育",
        url="https://m-vip-leyu.com.cn/about",
        note="关于页面链接。",
        tags=["体育", "关于"]
    )

    print("=== 完整格式输出 ===")
    print(collection.format_all_notes())

    print("=== 简短列表 ===")
    print(collection.format_brief_list())

    print("\n=== 搜索 '乐鱼体育' ===")
    found = collection.find_by_keyword("乐鱼体育")
    for note in found:
        print(f"  关键词: {note.keyword}, URL: {note.url}")

    print("\n=== 按标签 '科技' 搜索 ===")
    tagged = collection.find_by_tag("科技")
    for note in tagged:
        print(f"  关键词: {note.keyword}, 标签: {', '.join(note.tags)}")


if __name__ == "__main__":
    demonstrate()