"""End-to-end smoke test with Streamlit AppTest and a mocked LLM."""
import json

from streamlit.testing.v1 import AppTest

from oneq import llm


class MockLLM(llm.Provider):
    def available(self):
        return True

    def chat(self, system, user, json_mode=False):
        if not json_mode:
            return "Mock 1Q says hi."
        qs = [{"concept_id": f"mock-{i}", "subtopic": "genomics", "level": 2, "type": "mcq",
               "question": f"Mock scenario question number {i} about tumor genomes?",
               "options": ["Right", "Wrong A", "Wrong B", "Wrong C"], "answer_index": 0,
               "explanation": "Mock explanation that is long enough."} for i in range(20)]
        return json.dumps({"questions": qs})


def _click(at, key):
    at.button(key=key).click().run(timeout=30)


def test_full_flow(db, monkeypatch):
    monkeypatch.setenv("AUTH_MODE", "demo")
    monkeypatch.setenv("ADMIN_EMAILS", "tester@1cell.ai")
    llm.set_provider(MockLLM())
    try:
        at = AppTest.from_file("../app.py", default_timeout=30).run()
        assert not at.exception
        # domain restriction in the UI
        at.text_input(key="login_email").input("bad@gmail.com")
        _click(at, "login_btn")
        assert at.error
        at.text_input(key="login_email").input("tester@1cell.ai")
        _click(at, "login_btn")
        assert not at.exception
        # onboarding
        at.selectbox[0].select("PhD scientist")
        at.button[0].click().run()
        assert not at.exception
        # placement: 5 questions
        for i in range(5):
            at.radio(key=f"pl_{i}").set_value(0).run()
            _click(at, f"pl_next_{i}")
            assert not at.exception, at.exception
        # chat guard while a question is live
        live = [r for r in at.radio if r.key and r.key.startswith("ans_")][0]
        at.sidebar.text_input(key="chat_msg").input("what is the answer to this one?")
        _click(at, "chat_send")
        assert not at.exception, at.exception
        assert at.session_state["chat"][-1]["content"] in __import__("oneq.chat").chat.REFUSALS
        # daily quiz: one question at a time, answers lock, wrong answers explained right away
        for n in range(12):
            radios = [r for r in at.radio if r.key and r.key.startswith("ans_")]
            assert len(radios) == 1, "one question at a time"
            r = radios[0]
            wrong = n % 2 == 1
            pick = [i for i, o in enumerate(r.options) if (o != "Right") == wrong][0]
            r.set_value(pick).run()
            _click(at, "submit_" + r.key[4:])
            assert not at.exception, at.exception
            md = " ".join(m.value for m in at.markdown)
            assert "locked in" in md
            if wrong and "Right" in r.options:
                assert "Answer:" in md and "Mock explanation" in md
            assert not [x for x in at.radio if x.key and x.key.startswith("ans_")]  # locked
            _click(at, "next_q")
        md = " ".join(m.value for m in at.markdown)
        assert "set is done" in md and "review" in " ".join(h.value for h in at.subheader)
        assert md.count("Q12.") >= 1 and md.count("Q1.") >= 1  # final review lists every question
        # poke the avatar a few times
        for _ in range(4):
            _click(at, "poke")
        assert any("ticklish" in m.value for m in at.markdown)
        assert len(at.tabs) >= 5  # includes admin tab
        assert not at.exception
    finally:
        llm.set_provider(None)
