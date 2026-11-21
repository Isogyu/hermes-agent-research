# E008 Foundry 版のテストを Azure なしで実行（2026-11-20）

- **目的**: Hermes Foundry のどこまでをローカルで検証できるかを実行で確かめる（H7）。
- **方法**: `uv venv --python 3.14 lab/foundry-venv`、`requirements-test.txt` を導入、`repos/hermes-foundry` で `python scripts/run-python-tests.py`。出力は `lab/runs/foundry-tests.txt`。commit 8367c97。
- **結果**: 372件を27秒で実行。失敗2件、スキップ3件、残り367件は成功。終了コードは1。
  - 失敗2件（`test_build_context`、`test_new_version_resume`）はどちらも `…/bin/az: /Users/user/Nous: bad interpreter`。テストが作る偽の `az` スクリプトの shebang に、空白を含む venv のパス（`Nous Research`）が入るため。**こちらの環境が原因で、製品の欠陥ではない。**
  - スキップ3件は PowerShell が必要なテスト。テスト実行スクリプトはスキップを失敗として扱う。
- **解釈**: Foundry 版のロジック（権限の grant、状態同期、ルーティング、デプロイスクリプトの分岐）は、モックを相手に Azure なしで検証できる。ただしテストは Graph・Entra・az をすべて偽物に置き換えているので、「実テナントで動く」ことの証拠にはならない。
- **限界**: .NET のテスト24件は未実行（dotnet 未導入）。コンテナのビルドと起動は未実施（Docker デーモン停止中、空きディスク 12GB）。
- **次の行動**: 空白のないパスに venv を置き直して2件を再確認する。Docker を起動できるなら、コンテナをビルドしてヘルスチェックまで確かめる。
