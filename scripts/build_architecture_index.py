#!/usr/bin/env python3
"""Validate architecture assets and rebuild the source-linked gallery."""
import hashlib
import json
import re
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "figures"


def build():
    catalog = json.loads((ROOT / "data/models.json").read_text())["models"]
    specs = json.loads((FIGURES / "architecture_specs.json").read_text())["models"]
    manifest = json.loads((FIGURES / "generation_manifest.json").read_text())["models"]
    assets = {row["id"]: row for row in manifest}
    by_id = {row["id"]: row for row in specs}
    assert len(by_id) == len(specs) == len(catalog), "Duplicate or missing diagrams"
    assert set(by_id) == {row["id"] for row in catalog}
    assert set(assets) == set(by_id) and len(assets) == len(manifest)
    reused = sum(row["status"] == "reused_existing" for row in specs)
    lines = ["# 聚合物模型架构图", "",
             f"覆盖原始表中的 {len(specs)} 个模型：新生成 {len(specs)-reused} 张，复用 {reused} 张。",
             "沿用 PolymerGeneration 项目的白底、深蓝标题、青色编码模块和橙色生成/预测模块风格。",
             "新图使用内置 ImageGen，根据论文或作者公开资料重绘；这些图是架构示意，不是论文原图。", "",
             "PolyTAO、POLYT5 从原项目直接复制，文件哈希保持一致，没有重复生成。",
             "其余图已人工检查文字、分支和关键连线；图中省略的实现细节应以论文及作者代码为准。", "",
             "SPG-TED289M、STR-Bamba、PolyRL 暂无可获取的本地全文，使用作者公开来源绘制概要，图内及下表单独标注。",
             "来源页码按本地 PDF 的物理页序号（从 1 开始），不同版本可能不同。", "",
             "[结构规格与来源](architecture_specs.json) · [可用提示词与文件校验](generation_manifest.json) · [模型资源索引](../README.md)", "",
             "| 模型 | 图像 | 制作方式 | 依据 |", "| --- | --- | --- | --- |"]
    files = set()
    for model in catalog:
        row = by_id[model["id"]]
        path = FIGURES / row["image"]
        assert path.name == row["image"] and path.is_file(), path
        assert row["image"] not in files, path
        files.add(row["image"])
        raw = path.read_bytes()
        assert raw[:8] == b"\x89PNG\r\n\x1a\n" and raw[12:16] == b"IHDR", path
        width, height = struct.unpack(">II", raw[16:24])
        assert width >= 1000 and height >= 600, path
        asset = assets[row["id"]]
        assert asset["sha256"] == hashlib.sha256(raw).hexdigest(), path
        assert asset["image"] == row["image"] and asset["size_bytes"] == len(raw), path
        assert asset["width"] == width and asset["height"] == height, path
        assert row["visual_review_status"] == "reviewed", model["id"]
        method = "复用原图" if row["status"] == "reused_existing" else "新生成"
        source = row["source"]
        evidence = "全文" if source["evidence_level"] == "local_primary_paper" else "作者公开资料概要"
        lines.append(f"| {model['name']} | [PNG]({row['image']}) | {method} | {evidence} |")
    for model in catalog:
        row = by_id[model["id"]]
        source = row["source"]
        lines.extend(["", f"## {model['name']}", "", f"![{model['name']} architecture]({row['image']})", "",
                      f"论文：[{source['paper_title']}]({source['paper_url']})", ""])
        if source["local_pdf_filename"]:
            pages = ", ".join(map(str, source["pdf_page_numbers"]))
            lines.append(f"依据：本地 `{source['local_pdf_filename']}`，PDF 第 {pages} 页。")
        else:
            lines.append("依据：作者公开资料概要；本地全文缺失，未确认的层数、参数和细节没有加入图中。")
        for url in dict.fromkeys(source.get("additional_urls", [])):
            lines.extend(["", f"补充依据：[作者来源]({url})"])
        notes = re.sub(r"<[A-Za-z]+>", lambda match: "`" + match.group() + "`", row["architecture_review_zh"])
        lines.extend(["", notes, ""])
    lines.extend(["## 维护", "",
                  "新增或修改图前，先按模型 ID 检查结构规格、生成清单和现有 PNG，避免重复生成。",
                  "确认修改后更新来源、检查记录和 SHA-256，再运行：", "",
                  "```sh", "python3 scripts/build_architecture_index.py", "python3 scripts/build_catalog.py", "```", ""])
    (FIGURES / "README.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Validated {len(specs)} diagrams ({len(specs)-reused} new, {reused} reused); rendered gallery")


if __name__ == "__main__":
    build()
