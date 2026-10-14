# 原图字段与核查记录

核查日期：2026-10-14。共 22 个模型，均定位到对应论文或作者官方发布来源。“定位”仅确认模型身份与引用来源，技术字段只做选定核查，应用证据标签没有逐项重新审计。

## 核查方法与边界

从原图转录名称、年份、三类任务、应用证据、模态、架构、预训练数据与方法；以模型名搜索出版商、arXiv、官方会议档案与作者发布页。论文正文的 code/data availability 或作者项目说明用于关联代码。

原图没有参考文献表，不能将其中上标编号直接映射到文献。表内数字采用原图口径；确有差异时只在备注中澄清，不覆盖转录。k=千，M=百万，B=十亿；需要区分语料规模、训练子集、增强样本与独立聚合物。

部分出版商/会议页面访问受限，采用已检索到的官方摘要、arXiv 或作者机构稿交叉定位。404/访问失败只描述本次访问，不能据此断言项目不存在。未下载或重跑第三方项目，未验证其许可、完整性、checkpoint 或指标复现。

## 原图技术字段

| 模型 | 年份 | 应用 [证据] | 模态 | 架构 | 预训练语料 | 预训练方法 |
| --- | --- | --- | --- | --- | --- | --- |
| polyBERT | 2023 | Multidomain prediction [B] | Sequence | DeBERTa | Augmented from 13k real polymers (100M) | GL |
| TransPolymer | 2023 | Multidomain prediction [B] | Sequence | RoBERTa | PI1M (1M) | GL |
| SML-MT | 2023 | Electronic and optical prediction [B] | Sequence | BERT | Enamine (1M) | GL |
| SPG-TED289M | 2024 | Thermal, optical, membrane, and electrolyte prediction [B] | Sequence | BERT | Polymers from open literature (1M) | GL |
| PolyCL | 2025 | Electronic and optical prediction [B] | Sequence | DeBERTa | PI1M (1M) | CL |
| Trinity | 2025 | Flammability prediction [B] | Sequence | MoLFormer | — | — |
| MHG-GNN | 2023 | Multidomain prediction [B] | Graph | GIN, MHG | PubChem (1.3M) | GL |
| Polymer-JEPA | 2026 | Electron-affinity and phase prediction [B] | Graph | JEPA | Copolymer dataset (43k) | PL |
| MMPolymer | 2024 | Multidomain prediction [B] | Sequence, 3D | RoBERTa, SE(3)-Transformer | PI1M (1M) | GL, CL, denoising |
| PolyNC | 2024 | Property prediction [B]; Tg validation [E] | Sequence, Text | Text+Chem T5 | — | — |
| MIPS | 2025 | Multidomain prediction [B] | Graph, 3D | Graphormer | PI1M (1M) | GL, multimodal learning |
| PolyLLMem | 2025 | Multidomain prediction [B] | Sequence, Text, 3D | Llama, Uni-Mol | — | — |
| STR-Bamba | 2025 | Multidomain prediction [B] | Sequence, Text | Bamba | PubChem (117M); polymers from open literature (2M) | GL, PL |
| Uni-Poly | 2025 | Thermal, density, and resistivity prediction [B] | Sequence, Text, Graph, 3D | ChemBERTa, GIN, Text+Chem T5, SchNet | PolyInfo (15k) | Multimodal learning |
| PolyRL | 2026 | Gas-separation design [S, Sim] | Sequence | GPT-2, Llama-2 | Hypothetical polymers (1M) | GL |
| PolyTAO | 2024 | Property-conditioned generation [S] | Sequence, Text | Text+Chem T5 | PI1M (1M) | GL (structure-property) |
| DemoDiff | 2025 | In-context design [S] | Graph | GraphDiT | PolyInfo, MSA | GL (task-context) |
| CoMole | 2026 | Property-conditioned generation [S] | Graph | GraphDiT | Real polymers (13k) | Denoising |
| polyBART | 2025 | Property prediction [B]; inverse design [S, E] | Sequence | SELFIES-TED | Genome, SMiPoly (200M), real polymers (13k) | Denoising |
| POLYT5 | 2026 | Property prediction [B]; dielectric design [S, Sim, E] | Sequence | T5 | Hypothetical polymers (100M), real polymers (13k) | GL |
| PolyConFM | 2025 | Property prediction [B]; conformation generation [B]; polymer design [S] | Sequence, 3D | MolCLR, Uni-Mol, GraphDiT | 50k polymers with conformations | GL |
| Llamole | 2025 | Molecular design [S]; retrosynthesis [B] | Text, Graph | GraphDiT, GNN | Graph-text pairs (600k) | Denoising, CL, reaction-template supervision |


## 差异、资源状态与依据

| 模型 | 代码状态 | 核查说明 | 原始依据 |
| --- | --- | --- | --- |
| polyBERT | 作者代码 | 原图 100M 指假想结构语料；论文从 13,766 个已知聚合物的片段重组生成 100M PSMILES。方法实际为掩码语言建模（MLM）。 | [来源 1](https://www.nature.com/articles/s41467-023-39868-6) · [来源 2](https://github.com/Ramprasad-Group/polyBERT) · [来源 3](https://huggingface.co/kuelumbus/polyBERT) |
| TransPolymer | 作者代码 | 作者仓库注明 PI1M 原始约 1M，五倍增强后约 5M 序列；不要将这两个规模混用。 | [来源 1](https://arxiv.org/abs/2209.01307) · [来源 2](https://github.com/ChangwenXu98/TransPolymer) · [来源 3](https://huggingface.co/ChangwenXu/TransPolymer) |
| SML-MT | 代码未定位 | 规模存在实质差异：原图 Enamine 1M；作者稿明确为约 1 billion（1B，10亿）Enamine REAL 小分子。代码未定位。 | [来源 1](https://arxiv.org/abs/2310.16958) · [来源 2](https://www.osti.gov/servlets/purl/2282951) · [来源 3](https://doi.org/10.1021/acs.jcim.3c01650) |
| SPG-TED289M | 代码未定位 | IBM 官方摘要称其为 encoder-decoder，约 1M SPG 样本；原图 BERT 是简化架构标签。未定位专属代码/权重，不能用 SMI-TED 替代。 | [来源 1](https://research.ibm.com/publications/a-large-encoder-decoder-polymer-based-foundation-model) · [来源 2](https://openreview.net/pdf?id=L47GThI95d) |
| PolyCL | 作者代码 | 2025 是期刊卷期年；RSC 标示首次在线发表为 2024-11-28。代码指向聚合物 PolyCL，避免误连同名医学图像项目。 | [来源 1](https://pubs.rsc.org/en/content/articlelanding/2025/dd/d4dd00236a) · [来源 2](https://github.com/JiajunZhou96/PolyCL) |
| Trinity | 作者代码 | 作者代码项目名 TrinityLLM。原图预训练两列为空，不表示模型没有预训练；作者仓库说明使用 MoLFormer，并采用物理合成数据与实验数据两阶段训练。 | [来源 1](https://www.nature.com/articles/s43588-025-00768-y) · [来源 2](https://arxiv.org/abs/2407.02770) · [来源 3](https://github.com/ningliu-iga/TrinityLLM) |
| MHG-GNN | 相关作者实现 | 通用材料/分子表示模型。IBM 当前发布入口使用 MHG-GED 命名，列为相关实现入口，不声称与原论文版本完全相同。 | [来源 1](https://arxiv.org/abs/2309.16374) · [来源 2](https://github.com/IBM/materials) · [来源 3](https://huggingface.co/ibm-research/materials.mhg-ged) |
| Polymer-JEPA | 作者代码 | 原图采用 2026 期刊年；预印本首发于 2025。作者仓库包含 GNN 与 Transformer 编码器版本，推荐的 v2 使用 GNN。43k 规模保留原图口径。 | [来源 1](https://pubs.rsc.org/en/content/articlelanding/2026/dd/d5dd00308c) · [来源 2](https://arxiv.org/abs/2506.18194) · [来源 3](https://doi.org/10.5281/zenodo.17630815) · [来源 4](https://github.com/Intelligent-molecular-systems/Polymer-JEPA) |
| MMPolymer | 作者代码 | 论文使用 Star Substitution 构造结构信息；这里的 3D 表示应按论文定义理解，不等同于实验测得的完整聚合物链构象。 | [来源 1](https://arxiv.org/abs/2406.04727) · [来源 2](https://github.com/FanmengWang/MMPolymer) |
| PolyNC | 作者代码 | 2024 为期刊卷期年。原图预训练数据及方法为空；不据此推断从零训练。 | [来源 1](https://pubs.rsc.org/en/content/articlelanding/2024/sc/d3sc05079c) · [来源 2](https://pmc.ncbi.nlm.nih.gov/articles/PMC10763023/) · [来源 3](https://github.com/HKQiu/Unified_ML4Polymers) · [来源 4](https://huggingface.co/hkqiu/PolyNC) |
| MIPS | 作者代码 | Graphormer 为原图架构标签；论文重点是局部图注意力、主链嵌入与跨模态融合。 | [来源 1](https://arxiv.org/abs/2507.20326) · [来源 2](https://github.com/wjxts/MIPS) |
| PolyLLMem | 作者链接（内容待核实） | 原图预训练为空；论文使用已有 Llama 3 与 Uni-Mol 表示，不等于没有预训练。作者代码链接存在，但本次访问只看到仓库入口，未确认完整实现可用。 | [来源 1](https://arxiv.org/abs/2503.22962) · [来源 2](https://github.com/zhangtr10/PolyLLMem) |
| STR-Bamba | 作者代码 | 原图 PubChem 117M；作者模型卡写约 118M 小分子、2M 聚合物及 258 个配方，另有 588M 多表示样本口径。GL/PL 标签保留原图，实际目标以原文为准。 | [来源 1](https://openreview.net/pdf?id=0uWNuJ1xtz) · [来源 2](https://github.com/IBM/materials/tree/main/models/str_bamba) · [来源 3](https://huggingface.co/ibm-research/materials.str-bamba) |
| Uni-Poly | 作者链接（访问失败） | 论文给出作者仓库 huang-qi/Uni-Poly，但本次网页访问返回 404；保留作者声明链接并标记访问失败。PolyInfo 数据需遵循 NIMS 使用条件。 | [来源 1](https://www.nature.com/articles/s41524-025-01652-z) · [来源 2](https://d-nb.info/1372505911/34) · [来源 3](https://github.com/huang-qi/Uni-Poly) |
| PolyRL | 作者代码 | 2026 是期刊卷期年，作者稿首次在线发表于 2025-11-25。作者仓库引用作者名单与出版页面不一致，引用请以出版商为准。 | [来源 1](https://pubs.rsc.org/en/content/articlelanding/2026/dd/d5dd00272a) · [来源 2](https://doi.org/10.5281/zenodo.17498383) · [来源 3](https://doi.org/10.5281/zenodo.17498407) · [来源 4](https://github.com/Knitua/PolyRL) |
| PolyTAO | 作者代码 | 作者论文说明基于 PolyNC 初始权重训练；条件预训练使用约 1M 结构-性质对。原图 S 为代理性质评估。 | [来源 1](https://www.nature.com/articles/s41524-024-01466-5) · [来源 2](https://d-nb.info/1356348556/34) · [来源 3](https://github.com/hkqiu/PolymerGenerationPretrainedModel) · [来源 4](https://huggingface.co/hkqiu/PolymerGenerationPretrainedModel) |
| DemoDiff | 作者代码 | 通用分子模型，包含聚合物设计任务。原图只列 PolyInfo/MSA，论文语料覆盖药物与材料多来源；不能视为仅用聚合物预训练。 | [来源 1](https://arxiv.org/abs/2510.08744) · [来源 2](https://github.com/liugangcode/DemoDiff) · [来源 3](https://huggingface.co/liuganghuggingface/DemoDiff-0.7B) |
| CoMole | 代码未定位 | 论文说明材料部分用约 13k 真实聚合物预训练，同时还有药物相关任务。架构及 Denoising 标签为原图概括；未定位官方代码链接。 | [来源 1](https://arxiv.org/abs/2605.15354) · [来源 2](https://arxiv.org/html/2605.15354v2) |
| polyBART | 代码未定位 | 原图约 200M 是语料概括。正式论文附录列总语料 210,645,750；small 使用约 200M，large 使用 25M，规模取决于变体。未定位官方代码。 | [来源 1](https://aclanthology.org/2025.findings-emnlp.647/) · [来源 2](https://arxiv.org/abs/2506.04233) |
| POLYT5 | 代码未定位 | 预印本首发于 2025，正式期刊年为 2026。作者稿说明超过 100M 假想结构；Data availability 明确数据因机构考虑 IP 保护而未公开。未定位官方代码。 | [来源 1](https://www.nature.com/articles/s44387-026-00087-1) · [来源 2](https://arxiv.org/abs/2510.18860) · [来源 3](https://ramprasad.mse.gatech.edu/wp-content/uploads/2026/03/polyT5-Sahu_et_al-2026-npj_Artificial_Intelligence.pdf) |
| PolyConFM | 作者代码 | 论文介绍掩码自回归局部构象重建与方向变换。原图架构为组件概括；作者仓库标题采用 A Conformation-Centric Generative Foundation Model for Linear Polymer Modeling and Design。50k 规模为原图口径。 | [来源 1](https://arxiv.org/abs/2510.16023) · [来源 2](https://github.com/FanmengWang/PolyConFM) |
| Llamole | 作者代码 | 属于通用分子设计与逆合成模型，不能据原图归类声称其已经验证聚合物专属逆合成。预印本为 2024，会议年为 2025；原图架构省略了基础 LLM。 | [来源 1](https://arxiv.org/abs/2410.04223) · [来源 2](https://github.com/liugangcode/Llamole) |


## 数据格式

- `source_table`：图片转录；`null` 对应原图破折号。
- `paper`：独立定位的论文题名、来源 URL、发表入口与年份。期刊采用卷期年，预印本采用首发年。
- `resources`：作者关联的代码/模型链接及代码状态；`not_located` 表示本次未定位。
- `curation`：中文说明、差异备注、身份定位状态、技术核查范围与日期。
- `scope`：聚合物模型、小分子迁移模型、包含聚合物任务的通用分子模型，或相关通用分子模型。

本目录是图片限定范围的资源汇编，并非穷尽式系统综述。原图的 E/Sim/S/B 是不同验证路径，不能直接用于模型间性能排名或证明所有生成候选均可实验合成。
