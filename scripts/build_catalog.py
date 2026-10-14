#!/usr/bin/env python3
"""Render the curated model index from data/models.json (standard library only)."""
import csv
import io
import json
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = {
    "property_prediction": ("性质预测 · Property Prediction", "property-prediction"),
    "inverse_design": ("逆向设计 · Inverse Design", "inverse-design"),
    "unified_prediction_design": ("预测与设计统一 · Unified Prediction and Design", "unified-prediction-design"),
}
CODE_STATUS = {
    "author_linked": "作者代码",
    "related_author_release": "相关作者实现",
    "author_linked_contents_unconfirmed": "作者链接（内容待核实）",
    "author_linked_access_failed": "作者链接（访问失败）",
    "not_located": "代码未定位",
}


def cell(value):
    if value is None:
        return "—"
    if isinstance(value, list):
        value = ", ".join(value)
    return str(value).replace("|", "\\|").replace("\n", " ")


def resources(model):
    links = [f"[论文]({model['paper']['url']})"]
    r = model["resources"]
    label = CODE_STATUS[r["code_status"]]
    links.append(f"[{label}]({r['code_url']})" if r["code_url"] else label)
    if r["model_url"]:
        links.append(f"[模型]({r['model_url']})")
    return " · ".join(links)


def render():
    data = json.loads((ROOT / "data/models.json").read_text())
    models = data["models"]
    ids = [m["id"] for m in models]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate model ids")
    for m in models:
        if m["category"] not in CATEGORIES:
            raise ValueError(f"Unknown category: {m['category']}")
        if m["resources"]["code_status"] not in CODE_STATUS:
            raise ValueError(f"Unknown code status: {m['id']}")
        urls = [m["paper"]["url"], m["resources"]["code_url"], m["resources"]["model_url"], *m["resources"]["additional_urls"]]
        for url in filter(None, urls):
            if urlparse(url).scheme != "https" or not urlparse(url).netloc:
                raise ValueError(f"Invalid URL in {m['id']}: {url}")
    counts = Counter(m["category"] for m in models)
    readme = [
        "# Awesome-AI4Polymer-Models\n",
        "> Representative AI models for polymer property prediction, inverse design, and unified modeling.\n",
        "聚合物领域代表性 AI 模型索引：以用户提供的 Table 1 图片为初始范围，补充论文、作者代码与模型发布入口。"
        "本版收录 **%d 个模型**，按原图的主要下游能力分组。\n" % len(models),
        f"**最近核查：{data['checked_on']}** · [JSON](data/models.json) · [CSV](data/models.csv) · "
        "[原图字段与核查记录](docs/verification.md) · [贡献指南](CONTRIBUTING.md)\n",
        "覆盖：性质预测 **%d** 个，逆向设计 **%d** 个，预测与设计统一 **%d** 个。\n" % tuple(counts[k] for k in CATEGORIES),
        "## 导航\n",
        "- [性质预测](#property-prediction)\n- [逆向设计](#inverse-design)\n- [预测与设计统一](#unified-prediction-design)\n"
        "- [逐项文献与备注](#model-notes)\n- [读表说明](#reading-guide)\n",
        '<a id="reading-guide"></a>\n\n## 读表说明\n',
        "**年份、应用证据、模态、架构与预训练方法沿用原图**；它们不是本仓库对每篇全文的独立审计结论。"
        "已核查的差异和补充信息放在条目备注与 [核查记录](docs/verification.md)，原始值另存于 JSON 的 `source_table`。\n",
        "- **B**：留出基准评估；**S**：代理模型/性质 oracle 评估；**Sim**：物理计算验证；**E**：前瞻合成或实验测量。\n"
        "- **CL**：对比学习；**PL**：预测学习；**GL**：原图的生成学习标签。GL 也覆盖 MLM 等训练目标，并不意味着模型能直接进行聚合物生成。\n"
        "- **—**：原图未给出；不是“没有预训练”。**多领域预测**表示多个性质类别，不代表所有性质都被验证。\n"
        "- **作者代码/模型**表示定位到作者关联的入口；未运行第三方代码或验证权重与结果。**代码未定位**不等于未开源。\n"
        "- 通用分子模型及从小分子迁移的模型也按原图保留，具体范围见条目备注；本列表不对 foundation model 的定义作统一背书。\n",
    ]
    for category, (title, anchor) in CATEGORIES.items():
        readme += [f'<a id="{anchor}"></a>\n\n## {title}\n',
                   "| 模型 | 年份 | 应用 [证据] | 模态 | 架构（原图） | 方法（原图） | 资源 |\n",
                   "| --- | --- | --- | --- | --- | --- | --- |\n"]
        for m in models:
            if m["category"] != category:
                continue
            t = m["source_table"]
            values = [f"[{m['name']}](#{m['id']})", t["year"], t["application"], t["modality"], t["architecture"], t["pretraining_method"], resources(m)]
            readme.append("| " + " | ".join(cell(v) for v in values) + " |\n")
        readme.append("\n")
    readme += ['<a id="model-notes"></a>\n\n## 逐项文献与备注\n']
    for m in models:
        p, t, r = m["paper"], m["source_table"], m["resources"]
        readme += [f'<a id="{m["id"]}"></a>\n\n### {m["name"]}\n',
                   f"**[{p['title']}]({p['url']})** · {p['venue']} · {p['year']}\n",
                   m["curation"]["summary_zh"] + "\n",
                   f"**预训练语料（原图）：** {cell(t['pretraining_data'])}。\n",
                   f"**核查备注：** {m['curation']['notes_zh']}\n"]
        if r["additional_urls"]:
            readme.append("补充来源：" + " · ".join(f"[来源 {i}]({url})" for i, url in enumerate(r["additional_urls"], 1)) + "\n")
    readme += ["## 来源与维护\n",
               "初始范围来自用户提供的代表性聚合物基础模型 Table 1 截图。截图没有附原文题名、DOI 或参考文献表，"
               "因此不能还原其中的上标引用编号；本仓库根据模型名独立定位原始论文及作者发布资源。\n",
               "主要来源为出版商、arXiv、会议官方档案和作者仓库。未找到的资源留空，访问失败单独标注。"
               "没有使用其他 Awesome 列表或自动生成摘要作为事实依据，也未对各论文做统一重跑或性能排名。\n",
               "修改 `data/models.json` 后运行 `python3 scripts/build_catalog.py`，可更新本页、CSV 与核查记录。"
               "欢迎通过 Issue/PR 补充官方资源、修复链接或澄清原图差异。\n"]
    (ROOT / "README.md").write_text("\n".join(readme).replace("|\n\n|", "|\n|"))

    fields = ["id", "name", "category", "scope", "table_year", "paper_year", "paper_venue", "paper_title", "application", "modality", "architecture", "pretraining_data", "pretraining_method", "paper_url", "code_url", "code_status", "model_url", "additional_urls", "summary_zh", "notes_zh", "checked_on"]
    out = io.StringIO(newline="")
    writer = csv.DictWriter(out, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    for m in models:
        t, p, r, c = m["source_table"], m["paper"], m["resources"], m["curation"]
        writer.writerow(dict(id=m["id"], name=m["name"], category=m["category"], scope=m["scope"], table_year=t["year"], paper_year=p["year"], paper_venue=p["venue"], paper_title=p["title"], application=t["application"], modality="; ".join(t["modality"]), architecture=t["architecture"], pretraining_data=t["pretraining_data"] or "", pretraining_method=t["pretraining_method"] or "", paper_url=p["url"], code_url=r["code_url"] or "", code_status=r["code_status"], model_url=r["model_url"] or "", additional_urls="; ".join(r["additional_urls"]), summary_zh=c["summary_zh"], notes_zh=c["notes_zh"], checked_on=c["checked_on"]))
    (ROOT / "data/models.csv").write_text(out.getvalue(), encoding="utf-8")

    audit = ["# 原图字段与核查记录\n",
             f"核查日期：{data['checked_on']}。共 {len(models)} 个模型，均定位到对应论文或作者官方发布来源。"
             "“定位”仅确认模型身份与引用来源，技术字段只做选定核查，应用证据标签没有逐项重新审计。\n",
             "## 核查方法与边界\n",
             "从原图转录名称、年份、三类任务、应用证据、模态、架构、预训练数据与方法；"
             "以模型名搜索出版商、arXiv、官方会议档案与作者发布页。论文正文的 code/data availability 或作者项目说明用于关联代码。\n",
             "原图没有参考文献表，不能将其中上标编号直接映射到文献。表内数字采用原图口径；"
             "确有差异时只在备注中澄清，不覆盖转录。k=千，M=百万，B=十亿；需要区分语料规模、训练子集、增强样本与独立聚合物。\n",
             "部分出版商/会议页面访问受限，采用已检索到的官方摘要、arXiv 或作者机构稿交叉定位。"
             "404/访问失败只描述本次访问，不能据此断言项目不存在。未下载或重跑第三方项目，未验证其许可、完整性、checkpoint 或指标复现。\n",
             "## 原图技术字段\n",
             "| 模型 | 年份 | 应用 [证据] | 模态 | 架构 | 预训练语料 | 预训练方法 |\n",
             "| --- | --- | --- | --- | --- | --- | --- |\n"]
    for m in models:
        t = m["source_table"]
        audit.append("| " + " | ".join(cell(v) for v in [m["name"], t["year"], t["application"], t["modality"], t["architecture"], t["pretraining_data"], t["pretraining_method"]]) + " |\n")
    audit += ["\n## 差异、资源状态与依据\n", "| 模型 | 代码状态 | 核查说明 | 原始依据 |\n", "| --- | --- | --- | --- |\n"]
    for m in models:
        r = m["resources"]
        urls = [m["paper"]["url"], *r["additional_urls"]]
        if r["code_url"]:
            urls.append(r["code_url"])
        if r["model_url"]:
            urls.append(r["model_url"])
        sources = " · ".join(f"[来源 {i}]({url})" for i, url in enumerate(urls, 1))
        audit.append("| " + " | ".join(cell(v) for v in [m["name"], CODE_STATUS[r["code_status"]], m["curation"]["notes_zh"], sources]) + " |\n")
    audit += ["\n## 数据格式\n",
              "- `source_table`：图片转录；`null` 对应原图破折号。\n"
              "- `paper`：独立定位的论文题名、来源 URL、发表入口与年份。期刊采用卷期年，预印本采用首发年。\n"
              "- `resources`：作者关联的代码/模型链接及代码状态；`not_located` 表示本次未定位。\n"
              "- `curation`：中文说明、差异备注、身份定位状态、技术核查范围与日期。\n"
              "- `scope`：聚合物模型、小分子迁移模型、包含聚合物任务的通用分子模型，或相关通用分子模型。\n",
              "本目录是图片限定范围的资源汇编，并非穷尽式系统综述。原图的 E/Sim/S/B 是不同验证路径，"
              "不能直接用于模型间性能排名或证明所有生成候选均可实验合成。\n"]
    (ROOT / "docs/verification.md").write_text("\n".join(audit).replace("|\n\n|", "|\n|"))
    print(f"Rendered {len(models)} models: {dict(counts)}")


if __name__ == "__main__":
    render()
