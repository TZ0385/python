# 任务契约：发布证据构建器（ship check）

只修改 `starter/ship_check.py`。仅用标准库。绝不直接修改场景项目，只能
使用其副本。

- `run_checks(command, cwd) -> dict`：在 *cwd* 中运行
  `[sys.executable, *command]`，捕获输出，返回
  `{"command": " ".join(command), "exit_code": int, "ran": int, "result": str}`：
  - `ran` 是从 `Ran N tests in ...` 解析出的测试数。
  - `ran == 0` 时 `result` 为 `"no-tests"`（无论退出码——新版 Python 对
    "NO TESTS RAN" 返回非零）；退出码非零为 `"failed"`；否则 `"ok"`。
- `build_record(checks, *, verified_on, unverified=None) -> dict`：
  `{"verified_on", "checks", "all_passed", "unverified"}`，其中
  `all_passed` 仅当每个检查退出码为 0 且 result 为 `"ok"` 时为真
  （零测试项目永远不通过）；`unverified` 缺省为空列表。
- `write_record(record, destination)`：原子地写 JSON（UTF-8、缩进 2、
  末尾换行）——先写同名临时文件再 `os.replace`；创建缺失的父目录；
  成功后不留 `.tmp` 文件。
- `run_project(project_dir, *, verified_on) -> dict`：读取 `ship.json`
  （`command`、可选 `unverified`），在项目目录中运行检查、构建记录、
  写出 `SHIP-RECORD.json` 并返回它。
- `main(argv=None) -> int`：
  - `ship_check.py <project-dir> [--verified-on YYYY-MM-DD]`；否则向
    stderr 打印用法并返回 2。未提供 `--verified-on` 时使用当天日期。
  - 向 stdout 打印 `all_passed=... checks=...`；`all_passed` 时返回 0，
    否则 1。

完成的标准是 `python verify.py starter` 以 0 退出且全部十个测试通过。
