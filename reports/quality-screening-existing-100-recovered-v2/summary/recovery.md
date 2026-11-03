# 本地模型筛选恢复版

该实验保留原有 100 条数据组、冻结相关性、模型 digest、分流策略与完整质量校验。已通过校验的旧标注从父实验导入；未通过的旧标注重新进行本地评估。父实验没有被覆盖。

恢复版使用精简传输：模型输出精确引用和语义字段，程序仅在指定原文单元内唯一匹配引用后生成绝对位置。所有覆盖、重叠、范围、信息类型和字面名称校验继续由原 evidence_quality.py 执行。找不到或不唯一的引用不能自动修复，也不能放行。

新提示词和传输格式与原实验不同，属于明确记录的恢复协议，不应当作逐位重现原模型输出。原引用、模型判断和校验错误均保存在 requests/quality/；有效输出另有 expanded-annotation.json。manifest.json 记录协议、提示词、代码 hash、父实验、模型及策略。

本地运行方式为 CPU、单请求串行。英文使用 Llama 3.1，中文使用 Qwen 2.5 7B。

再次中断时，先确认没有本任务的残留进程，然后运行：

```sh
PYTHONHASHSEED=2 python3 scripts/run_quality_screening_recovery.py --out reports/quality-screening-existing-100-recovered-v2
```

完整响应按内容缓存；中断的部分输出独立保留。最终完成前，progress.json 与 screening-progress.json 仅为阶段性结果；最终结果以 summary.json 和 retained/excluded/review-comments 文件为准。

启动日志：../quality-screening-existing-100-recovery-v2.log。验证日志：../quality-screening-recovery-tests.log。

恢复协议 v2 在输出结构中要求每个 E 单元都是必填键，且至少包含一个片段；模型不能只返回它认为相关的单元。仍须通过原有非空白字符完整覆盖校验。
