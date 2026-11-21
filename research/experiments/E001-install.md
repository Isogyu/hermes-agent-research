# E001 Hermes Agent の導入（2026-11-20）

- **目的**: 実験専用領域に Hermes Agent を入れ、既存環境を汚さずに起動できる状態を作る。
- **背景・仮説**: `pyproject.toml` は `requires-python >=3.11,<3.15` なので、手元の Python 3.13.2 で入るはず。
- **環境**: macOS 26.6.1、Apple M3（8コア）、メモリ 8GB、空きディスク 12GB。commit 2de9f51。
- **実施内容**:
  1. `python3 -m venv .venv && pip install -e repos/hermes-agent`（Python 3.13.2）
  2. `uv sync --frozen --python 3.14 --extra mcp --extra acp --extra anthropic`（uv 0.13.9、キャッシュと Python は作業フォルダ内 `.uv/`）
- **結果**:
  - 1 は pip が成功を返すが、依存が1つも入らない（venv 13MB）。`hermes --help` は `ModuleNotFoundError: No module named 'ruamel'`。
  - 原因は、基本依存がすべて `; python_version >= '3.14'` の条件つきであること（`pyproject.toml:19-` ）。
  - 2 は成功。`Hermes Agent v0.23.3+93.g2de9f51`、Python 3.14.10、venv 136MB。
- **解釈**: 実質の要件は Python 3.14。3.11〜3.13 では「導入は成功するのに動かない」状態になる。公式インストーラは 3.14 を自前で入れるので通常の利用者は踏まないが、pip で入れる利用者や企業の社内ミラー運用では罠になる。
- **限界**: 3.11〜3.13 向けの別の依存定義がどこかにある可能性は調べていない。
- **次の行動**: 3.14 の venv を使う。`env.sh` を source すれば再現できる。
