"""振り返りプロンプトに1段落を足してからゲートウェイを起動する実験用ラッパー。
Hermes のソースは書き換えない。足す文は環境変数 REVIEW_APPEND で渡す。"""
import os, sys
import agent.background_review as br
extra = os.environ.get("REVIEW_APPEND", "")
if extra:
    for name in ("_SKILL_REVIEW_PROMPT", "_COMBINED_REVIEW_PROMPT"):
        setattr(br, name, getattr(br, name) + "\n\n" + extra)
    import run_agent
    for name in ("_SKILL_REVIEW_PROMPT", "_COMBINED_REVIEW_PROMPT"):
        if hasattr(run_agent.AIAgent, name):
            setattr(run_agent.AIAgent, name, getattr(br, name))
sys.argv = ["hermes", "gateway", "run", "--quiet"]
from hermes_cli.main import main
main()
