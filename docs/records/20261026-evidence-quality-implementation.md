# 评论证据质量模块：实现与验证

日期：2026-10-26（America/Los_Angeles）。工程规格见 `docs/design/evidence-quality.md`。
本次交付 CLI 工程能力；尚未获得独立人工效果验证，推荐先运行 shadow。

## 实现文件

- `scripts/evidence_quality.py`：严格 schema、覆盖与原文校验、Unicode LNMS 篇幅比例、逐信息点路由、claim 资格绑定、独立意见统计。
- `configs/evidence-quality-policy.json`：v1 策略，比例算法 `unicode-LNMS-codepoint-v1`；0.70 只作未校准告警，不能作删除阈值。每评论一次标注请求，8192 输出预算、16384 上下文，失败最多两次独立请求。
- `prompts/evidence-quality.{en,zh}.txt`：双语标注；不输出最终路由、可信度或工程建议。
- `prompts/quality-extract.{en,zh}.txt`、`prompts/quality-verify.{en,zh}.txt`：只在 enforce 追加到当前主流程提示词，保留 off/shadow 原提示词。
- `scripts/run_balance_analysis.py`：相关性放行后进入质量阶段；独立解析与 schema；三种模式、quality-only、缓存、快照、覆盖、报告出口。
- `scripts/review_balance_sources.py`：来源复核保留并重新校验资格；提案指纹包括资格。修改过的主张不能沿用修改前的自动语义审查。
- `scripts/experiments/prepare_balance_design.py`：新版输入还需机制资格、选定片段引用、语义审查和官方身份；继续要求来源 accept、明确目标、数值意图和匹配的版本数据。
- `scripts/experiments/demo_evidence_quality.py`：合成标注重放及三种模式 mock 端到端示例，不连接模型、不产生真实准确率。
- `scripts/experiments/diagnose_evidence_quality_live.py`：显式选定冻结 admission 中的评论，在新目录做真实 quality 与 shadow/enforce 提取、审查对照；不重跑检索。
- `scripts/evaluate_evidence_quality.py`：新建待标注集与效果计分，分来源、语言、开发/测试及固定 admission 条件；不自动把模型输出当标签。
- `tests/test_evidence_quality.py`、`tests/test_evidence_quality_evaluation.py`：双语纯逻辑、mock 全流程、失败/恢复与评估边界测试。

## 行为与兼容

默认 `--evidence-quality off` 不增加质量模型调用；旧 extraction、计数与报告主体语义保留，但新代码必须用新目录。默认输出改为 `runs/balance-quality-v1`，避免沿用历史实验目录。

shadow 标注与路由产物均为观察，原 extraction/aggregation 照旧；正式报告不混入这些观察结果。enforce 只有明确的角色机制信息点进入 extraction。完整原始 units 仍作上下文，原 E-ID 和 `[start,end)` 不改变，不用模型改写替代证据。

每条 claim 必须引用**一个**本评论合格 `quality_point_ids`，对应 evidence IDs 必须完整匹配所选点；角色、方向、目标与数值必须通过局部绑定检查。一个点涉及多个片段时，全部片段的来源保留。独立语义审查看完整原文作解释上下文，但只允许所选片段支撑主张，且保留请求/观察区别；不把资格标签、情绪占比或情绪强度当证据。局部数值检查不替代原有数值意图、身份、来源及版本规则。

程序不能证明模型提出的语义分段、主体、去重或具体性正确。当前 v1 对原文中出现的具体目标做保守字面约束，跨语言改写可能增加复核量。不要以复核为成功提取。缺少上下文、反讽、被引用的辱骂、结构错误或请求失败均可复核；确定的其他点仍可独立保留。

`balance-report-v3` 的 enforce 出口包括：

- `opinion_summary`：一般意见，保留方向和 explicit_request / strength_assessment / observation 的分别来源数；不生成具体设计。
- `character_adjustments`：仅后续审查支持的机制证据，按角色、字面主题、方向计数，保留 buff/nerf/keep/unclear。
- `system_feedback`：系统反馈与一般/具体等级，独立保存；v1 无系统建议生成器。
- `quality_review_queue` / `quality_exclusions`：片段、来源、原因、运行状态及可追溯请求。

权重是同一角色/主题/方向的唯一 comment ID，不受情绪强度和重复发泄影响。意见的 stance 子计数可重叠，不能相加。`quality-summary.json` 另外提供一般意见与**审查通过机制证据**的来源集合并集和交集。分类、主题、方向之间均可重叠，不能把评论数说成独立玩家人数或总体共识。源内未验证名称继续隔离，不进入已验证角色组。

设计入口的旧 claim 列表仍走 `legacy/quality_not_assessed` 分支。新版 `balance-report-v3` 报告自动强制资格；单独传新版 claim 列表时请显式加 `--quality-mode enforce`，防止遗漏资格字段被当作 legacy。缺失字段不能默认为新版通过。人工 accept 也不能把 opinion_only 升格为机制证据。

## 运行、恢复和回滚

以下命令在仓库根目录执行，每种模式选独立新目录。依赖原有 numpy 和本地 Ollama，仍使用语言路由配置及 `qwen3-embedding:8b`；不读取 `.env`，不新增外部 API 或模型。

```sh
cd <project root>
python3 -m unittest discover -s tests -p 'test_*.py'

# 推荐：先观察，不改变旧下游流向
python3 scripts/run_balance_analysis.py --evidence-quality shadow --out reports/quality-shadow-new

# 在检索、相关性、质量之后停止
python3 scripts/run_balance_analysis.py --evidence-quality shadow --quality-only --out reports/quality-only-new

# 使用资格闸门的完整流程
python3 scripts/run_balance_analysis.py --evidence-quality enforce --out reports/quality-enforce-new

# 来源复核后的新版列表仍须显式使用 enforce 设计门槛
python3 scripts/experiments/prepare_balance_design.py --claims reports/quality-enforce-new/source-reviewed-claims.json --quality-mode enforce --out reports/quality-enforce-new/design-briefs.json

# 回滚运行行为：off + 新目录，不改写历史输出
python3 scripts/run_balance_analysis.py --evidence-quality off --out reports/quality-rollback-new

# 无模型服务也能重放合成混合路由和 mock 三模式端到端示例
python3 scripts/experiments/demo_evidence_quality.py --mock-pipeline --out reports/quality-demo-new
```

`--relevance-only` 仅允许 off；`--quality-only` 必须配 shadow/enforce，不能与 relevance-only 同用。参数错误在模型调用前报告。

恢复时重复**同一命令、同一目录**。manifest 比较模式、数据、模型 digest、代码、schema、策略、提示词、输出预算和测量版本；任一身份变化必须新目录。每个请求保存 request/response/validation 与原始流输出；quality attempt 1/2 使用独立身份，重试不是反复读取同一失败响应。两次失败持久化为 review，不算 exclude 或 generation_failed。缓存恢复不会增加信息点权重或重复计数；中断的原始流输出留作独立文件。

产物包括 `evidence-quality.json`、`quality-routing.json`、`quality-summary.json`、`quality-review-queue.json`、`quality-exclusions.json`、`opinion-summary.json`、`system-feedback.json`、`full-pipeline-coverage.json`。既有 coverage 的字段含义保留，新 coverage 对每个输入只记一行，分别记录语言未支持/未选择、相关性拒绝/待定、质量待处理/完成/失败、提取完成/失败、审查与来源待复核状态。质量判断后的正常分流不算提取失败。

## 样例与新标注集

`data/evaluation/evidence-quality-synthetic-v1/` 有 38 条 agent 编写的中英合成用例，全部 development，包含交接要求的 12 类边界及额外的历史/比较/反讽/未知身份/等义情绪变体。它们不是社区证据或人工真值。

`reports/evidence-quality-v1-delivery/examples/mixed-comment-examples.json` 展示价格+一般诉求、系统+外观、高发泄+具体机制的多路输出；`mock-pipeline/{off,shadow,enforce}/` 使用 mock 模型与检索跑完整管道，所有输入由 mock 放行，`execution-provenance.json` 明确注明模拟来源。

`data/evaluation/evidence-quality-real-v1/` 从已有**粗筛前**语料按重复簇确定性抽取 300 条：198 en、101 zh、1 und；标签全为 null/unlabeled，没有人工准确率。历史 admission 中已出现的来源强制 development；规范化重复内容不跨 split。尚需人工合并等义簇、检查语言/来源分层、冻结拆分，再做双标和裁决，不能直接将当前 provisional test 宣称为独立盲测。

新建标注模板的命令（不会覆盖已有目录）：

```sh
python3 scripts/evaluate_evidence_quality.py prepare --dataset data/raw/feedback/20261015-expanded/records.jsonl --source-stage raw_pre_screen --inspected-labels data/evaluation/balance-silver-v1/labels.jsonl --limit 300 --out data/evaluation/quality-labels-new
python3 scripts/evaluate_evidence_quality.py score --labels data/evaluation/quality-labels-new/annotation-template.json --run reports/quality-shadow-new --out reports/quality-score-new.json
```

为了避免把分段 ID 相同冒充语义一致，计分要求人工/银标提供 `points`（含 point_id、route、segment_ids）和 `point_matches`（gold_point_id、predicted_point_id 的一对一裁决）。没有匹配记录的机制输出计入 precision 分母，缺失/复核计入 recall 损失。`segments` 沿用精确原文的 segment 格式；情绪 span precision/recall 和比例误差**仅**对 reviewer_type=human 且有 span 标签的记录计算。human / silver / agent_authored_synthetic 和 development/test 结果分开，不混成总准确率。所有比例保留分子分母与 Wilson 区间，零分母为 null；相关性 false acceptance 定义为已放行且有二元相关性标签中的无关占比。区间未校正评论内/字符间相关性，不能作小样本保证。

报告同时给机制 precision/recall、具体机制误排除率、一般意见升格率、系统误绑角色率、review/失败率、review 召回损失及等义资格/单位权重一致性。固定 admission 子集的结果是条件表现；只有覆盖粗筛前样本和上游放行状态的计分才可讨论端到端 recall。本模块无法找回根本没有进入它的评论。

## 验证状态

详见 `reports/evidence-quality-v1-verification/verification.json` 与 `tests.log`。
既有冻结 silver-v1、admission、原始评论和历史报告未被覆盖。新代码要求使用新目录，不直接续写旧结果。

真实诊断使用原语言模型、固定历史 admission 的两条来源，保存全部原始响应与 shadow/enforce 审查记录。英文 Drive Rush 输入被模型标为排除；中文样本的粗粒度标注和提取仍需人工核查，enforce 的语义审查曾返回 uncertain。上述都是待复核观察，不是正确性结论。最终诊断状态以 `reports/evidence-quality-v1-live-verified/diagnostic-summary.json` 为准。

当前本地模型清单缺少 `qwen3-embedding:8b`，因此未完成新鲜检索+相关性+质量+提取的完整在线运行；固定 admission 诊断没有绕过或伪造该模型的 digest。恢复原嵌入模型后才能执行上面的完整运行命令。本交付不自动下载或替换模型。

尚未验证：200–400 条双语独立双标与裁决、语义分段/去重的质量、span 标签准确性、情绪等义变体的真实推理一致性、独立测试集的各项效果指标、上游漏判后的全流程 recall，以及版本事实与实际平衡效果。规格中的 95%/5%/2%/95% 仍为候选目标，没有宣称达成。默认 off，当前推荐 shadow，完整 enforce 能力已具备。

## Moved from the root README

This section was moved from the root `README.md` on 2026-11-03 (change
record, P4-D02).

### 评论证据质量与情绪干扰控制

新增 `--evidence-quality off|shadow|enforce`（默认 off）和 `--quality-only`。
相关性放行后按原文片段与信息点分流为无关/纯发泄、一般意见、角色机制、
系统反馈和待复核；纯情绪篇幅只作诊断，不改变有信息评论的资格或权重。
一般意见不能支撑具体招式/数值设计。enforce 仍执行既有身份、原文、数值、
来源复核及版本数据门槛，off/shadow 保留旧下游语义。

运行与回滚均使用新目录，例如：
`python3 scripts/run_balance_analysis.py --evidence-quality shadow --out reports/quality-shadow-new`；
回滚改为 `--evidence-quality off --out reports/quality-rollback-new`。
无模型可运行 `python3 scripts/experiments/demo_evidence_quality.py --mock-pipeline --out reports/quality-demo-new`。
详见 [实现、命令、产物及未验证事项](20261026-evidence-quality-implementation.md)。
独立人工效果验证尚未完成，当前推荐 shadow；合成测试与小规模真实诊断不代表准确率。
