---
状态: 已发布
置信度: H（内部约定）
最后核验: 2026-09-27
下次复核: 2026-12-27
来源登记: 无需
---

# 01 · 文件夹与文件命名规范（含对 v1 的复盘）

## 0. 先复盘：v1（docs/ 时代）做对了什么、做错了什么

v1 的命名是 `docs/01-怎么卖-二手工程机械出海打法.md`、`docs/data/品类-市场矩阵.csv`。

**做对的**：
- 用两位数字前缀控制阅读顺序；
- 文件名直接写"回答什么问题"（怎么卖 / 匹配矩阵 / 风险速查），扫一眼就懂；
- 数据单独放 `data/`，与叙述分离。

**做错的**：
1. `docs/` 这个文件夹名是**技术词不是业务词**，无法扩展第二个行业；
2. 文件名太长、把"行业 + 动作 + 对象"全塞进去（`01-怎么卖-二手工程机械出海打法`），换行业后前缀含义失效；
3. 状态（草稿/已核实）和日期没进文件，只能靠 frontmatter 补，**名字和元数据脱节**；
4. CSV 文件名（`品类-市场矩阵.csv`）和它的 md（`02-…矩阵.md`）**没有用同一个序号绑定**，靠人记；
5. 来源清单是 md 表格，没有机器可读的登记册，ID 无法被脚本校验；
6. **v2 新教训：文件名用了中文**。Workspace 查看器对中文文件名全部显示 "Unknown file"（6→17 个），
   人无法在文件树里分辨任何文档。**文件名必须纯 ASCII**；中文只进正文，不进文件名/文件夹名。

→ 本规范就是针对以上各点的修正。

## 1. 顶层文件夹（业务分层，非技术分层）

```
00-system/                 方法论与约定（命名、truth、调研、GTM、模板、来源登记册）
10-industry-<industry>/    行业级结论（如 10-industry-used-machinery/）
20-project-<product>-<market>/ 落地项目（如 20-project-rotary-rig-sea/）
90-archive/                被推翻/过期的版本，只移入不删除
```

规则：
- 顶层用 `NN-` 两位数字表达**层的稳定性**：00 最稳、90 是终点；
- 行业层、项目层名字里必须带**业务对象**（行业名 / 品类-市场），让人不看内容也知道范围；
- 每个行业/项目文件夹内部，用同一套 `01-05` 语义槽位（见下），跨项目对齐。

## 2. 文件夹内语义槽位（跨行业统一的 01–05）

| 序号 | 语义 | 行业层示例 | 项目层示例 |
|---|---|---|---|
| 00 | 概览/对象画像 | — | `00-equipment-analysis-inventory-profile.md` |
| 01 | 打法/调研 | `01-how-to-sell-playbook.md` | `01-market-research-sea-rotary-rig.md` |
| 02 | 矩阵/匹配 | `02-product-market-customer-matrix.md` | `02-gtm-playbook-lead-to-delivery.md` |
| 03 | 合规/风险 或 团队/组织 | `03-compliance-risk-cheatsheet.md` | `03-team-org-to-subsidiary.md` |
| 04 | 调研实录 | `04-research-log-used-machinery.md` | `04-…`（按需） |
| 05 | 来源清单 | `05-source-list.md` | `05-…`（按需） |

不强制全有，但**序号的语义要对齐**，这样任何人打开一个新项目都知道 02 是打法/匹配。

## 3. 文件命名规则

1. 格式：`NN-topic[-subtopic].md`，`NN` 两位数字，分隔符**只用连字符 `-`**；
2. **文件名/文件夹名纯 ASCII**（小写英文关键词）：workspace 查看器对中文文件名显示 Unknown file；
   中文只写进正文与 frontmatter，不写进名字；
3. 不用空格、下划线、emoji、全角符号（避免跨平台与 URL 编码问题）；主题要写"回答什么问题"而非文件类型；
4. **日期、状态、版本号一律不进文件名**，放 frontmatter（见 `02-truth-anti-hallucination`）；时间序列型产物（周报/快照）才用 `主题-YYYYMMDD.md`；
5. 数据文件放同目录 `data/` 子夹，**与父文档共用序号**：`02-product-market-customer-matrix.md` ↔ `data/02-product-market-matrix.csv`；
6. 一个文件只回答一个问题；超过 300 行就拆。

## 4. 校验

命名规范由仓库根的 `verify.py` 兜底：每次提交前跑验证脚本，检查
（a）顶层目录是否符合 `00/10/20/90` 前缀；（b）md 是否带 frontmatter；（c）引用 ID 是否存在于登记册；
（d）**文件名/目录名是否纯 ASCII**（中文即失败）。见 `02-truth-anti-hallucination.md` §6。
