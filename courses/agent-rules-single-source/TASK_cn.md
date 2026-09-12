# 任务契约：Agent 规则文件一致性检查器

只修改 `starter/rules_check.py`。仅用标准库。

- `load_rule_files(directory) -> dict[str, str]`：读取 `AGENTS.md`、
  `CLAUDE.md`、`.cursorrules` 中每个存在的规则文件文本。
- `is_pointer(text) -> bool`：当文件是瘦指针时为真——非空行不超过
  10 行，且至少一行引用 `AGENTS.md`。
- `check_directory(directory) -> dict` 返回
  `{"source": "AGENTS.md", "ok": bool, "files": [...]}`：
  - `AGENTS.md` 缺失或为空产生 `missing-source` 条目且 `ok=False`。
  - 存在且非空的 `AGENTS.md` 产生 `source` 条目。
  - 其余规则文件逐一分类：`pointer`（瘦指针）、`copy`（与 `AGENTS.md`
    内容完全一致）或 `diverged`（其余情况），各带 `issues` 列表；
    `diverged` 条目必须写明与 `AGENTS.md` 的差异原因。
  - 仅当所有条目都是 `source`、`pointer` 或 `copy` 时 `ok=True`。
- `main(argv=None) -> int`：
  - 恰好一个参数（目录）。否则向 stderr 打印用法并返回 2。
  - 向 stdout 打印 `ok=... files=... diverged=...`；`ok` 时返回 0，
    否则 1。

完成的标准是 `python verify.py starter` 以 0 退出且全部十一个测试通过。
