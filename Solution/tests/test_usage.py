"""Token logging: per-call usage from the SDK result and the per-stage summary in report.json (no LLM)."""
import asyncio
import os
import unittest
from types import SimpleNamespace

from pipeline.engine import llm


class TestUsage(unittest.TestCase):
    def test_tokens_from_result(self):
        r = SimpleNamespace(usage={"input_tokens": 10, "output_tokens": 5, "cache_read_input_tokens": 100,
                                   "cache_creation_input_tokens": 7, "server_tool_use": {}})
        self.assertEqual(llm.tokens(r), {"input_tokens": 10, "output_tokens": 5,
                                         "cache_read_input_tokens": 100, "cache_creation_input_tokens": 7})
        self.assertEqual(llm.tokens(None)["input_tokens"], 0)
        self.assertEqual(llm.tokens(SimpleNamespace(usage=None))["output_tokens"], 0)

    def test_summary_per_stage(self):
        calls = [
            {"agent": "write_section/SEC-01", "cost_usd": 0.5, "seconds": 10, "turns": 1, "input_tokens": 100,
             "output_tokens": 50, "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0},
            {"agent": "write_section/SEC-02", "cost_usd": 0.25, "seconds": 5, "turns": 2, "input_tokens": 10,
             "output_tokens": 5, "cache_read_input_tokens": 1000, "cache_creation_input_tokens": 3},
            {"agent": "review", "cost_usd": 0.1, "seconds": 1, "turns": 1, "input_tokens": 1,
             "output_tokens": 1, "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0},
        ]
        s = llm.usage_summary(calls)
        ws = s["by_stage"]["write_section"]
        self.assertEqual((ws["calls"], ws["turns"], ws["input_tokens"], ws["total_tokens"]), (2, 3, 110, 1168))
        self.assertAlmostEqual(ws["cost_usd"], 0.75)
        self.assertEqual(list(s["by_stage"]), ["write_section", "review"])   # most expensive first
        self.assertEqual(s["total"]["calls"], 3)
        self.assertEqual(s["total"]["total_tokens"], 1168 + 2)

    def test_no_agents_guard(self):
        os.environ["PIPELINE_NO_AGENTS"] = "1"
        try:
            with self.assertRaises(llm.AgentError):
                asyncio.run(llm.run_agent("x", "s", "p", {"type": "object"}, model="m"))
        finally:
            del os.environ["PIPELINE_NO_AGENTS"]


if __name__ == "__main__":
    unittest.main()
