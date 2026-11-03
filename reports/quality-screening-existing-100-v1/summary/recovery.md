# 意外关机后的保护性恢复

恢复日期：2026-10-26（America/Los_Angeles）。

恢复前核对：

- 现有 100 条真实评论组的文件 hash 未变。
- 实验 manifest 中代码、配置、策略、词表 hash 全部匹配。
- 本地 Qwen / Llama 模型 digest 与原实验一致。
- 没有残留筛选进程，避免两个进程同时写入。
- 5 份 response.json 可解析；进度汇总当时仅记录 2 条，完整响应缓存比汇总更完整。
- 保护性备份：`../quality-screening-existing-100-v1-checkpoint-20261026/`，内含 `checkpoint-inventory.json` 文件校验清单。

恢复命令（仓库根目录）：

```sh
PYTHONHASHSEED=2 python3 scripts/resume_quality_screening_local.py --out reports/quality-screening-existing-100-v1 --workers 1
```

保持代码、策略、提示词、原始输入和模型 digest 不变，使用同一命令及输出目录。
程序从内容寻址的请求缓存重建结果，而不是把旧计数再累加。失败请求保留两次独立尝试，耗尽后进入待复核；未完成内容不能记为剔除。

本次恢复日志：`resume-20261026.log`。
最终完成前，`progress.json` 和 `screening-progress.json` 仅代表阶段性状态；完成后才输出 retained/excluded/review 清单及 summary.json。

若再次中断，先确认没有同名筛选进程，再使用同一恢复命令。不要删除缓存、修改 manifest 或修改冻结标签。

本次继续核对发现，Python 随机 hash seed 会改变模型字典在请求文本中的字段顺序，造成语义相同但缓存身份不同。恢复命令固定 PYTHONHASHSEED=2，以匹配首次实验的字段顺序；原有请求历史全部保留，不覆盖。此次继续日志为 `resume-final.log`。

## 本次续跑方式

本次使用本地模型的 CPU 串行方式。实测 Llama 短输出生成速度：CPU 8.46 token/s，GPU 2.85 token/s，详见 local-speed-diagnostic.json。原请求、模型 digest、提示词、随机种子、上下文长度、质量策略与数据组不变；运行时通过独立适配器设置 num_gpu=0。

新发请求的实际参数记录在每个请求目录的 effective-runtime-request.json 中；runtime-recovery.json 记录适配器 hash 与设置。运行硬件改变可能带来浮点执行差异，不承诺逐位可复现。有效的原缓存继续复用，关机/暂停留下的部分输出保留为 interrupted-partial-*.txt。

本次 CPU 续跑日志：resume-cpu-serial-20261026.log。运行前应确认没有同一任务的旧进程。输出文件仍采用临时文件原子替换；再次中断后使用上面的固定 seed、单请求命令恢复。
