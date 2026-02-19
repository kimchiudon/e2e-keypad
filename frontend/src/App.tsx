import { useEffect, useState } from "react";

type Cell = {
  inner_value: string;
  image: string;
  is_blank: boolean;
};

export default function App() {
  const [layout, setLayout] = useState<Cell[]>([]);
  const [sessionId, setSessionId] = useState("");
  const [error, setError] = useState("");

  // ✅ 추가: 사용자가 누른 토큰(해시값) 4개를 저장
  const [inputTokens, setInputTokens] = useState<string[]>([]);
  const [submitMsg, setSubmitMsg] = useState<string>("");

  const initKeypad = async () => {
    setError("");
    setSubmitMsg("");
    setInputTokens([]); // ✅ 새 세션이면 입력도 초기화(원하면 이 줄 빼도 됨)
    try {
      const res = await fetch("http://127.0.0.1:8000/keypad/init");
      if (!res.ok) throw new Error("init failed");

      const data = await res.json();
      setSessionId(data.session_id);
      setLayout(data.layout);
    } catch (e) {
      console.error(e);
      setError("키패드 로딩 실패. 백엔드/자산 파일을 확인하세요.");
    }
  };

  useEffect(() => {
    initKeypad();
  }, []);

  const handleClick = (cell: Cell) => {
    if (cell.is_blank) return;

    // ✅ 이미 4개면 더 받지 않기
    setInputTokens((prev) => {
      if (prev.length >= 4) return prev;
      return [...prev, cell.inner_value];
    });

    console.log("클릭된 토큰:", cell.inner_value);
  };

  // ✅ 추가: 입력 지우기
  const clearInput = () => {
    setSubmitMsg("");
    setInputTokens([]);
  };

  // ✅ 추가: 4개 토큰을 백엔드로 제출
  const submitInput = async () => {
    setSubmitMsg("");
    setError("");

    if (!sessionId) {
      setError("세션이 없습니다. 키패드를 먼저 초기화하세요.");
      return;
    }
    if (inputTokens.length !== 4) {
      setError("입력은 정확히 4개가 되어야 제출할 수 있어요.");
      return;
    }

    try {
      const res = await fetch("http://127.0.0.1:8000/keypad/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          session_id: sessionId,
          tokens: inputTokens, // ✅ 해시값(inner_value) 4개가 넘어감
        }),
      });

      if (!res.ok) {
        const text = await res.text();
        throw new Error(text || "submit failed");
      }

      const data = await res.json().catch(() => null);
      setSubmitMsg(
        data ? `제출 성공: ${JSON.stringify(data)}` : "제출 성공"
      );
    } catch (e) {
      console.error(e);
      setError("제출 실패. 백엔드 /keypad/submit 라우팅을 확인하세요.");
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>E2E Keypad Demo</h1>

      {error && <div style={{ color: "red", marginBottom: 10 }}>{error}</div>}
      {submitMsg && (
        <div style={{ color: "green", marginBottom: 10 }}>{submitMsg}</div>
      )}

      {/* ✅ 추가: 입력 상태 표시 + 제출 UI */}
      <div
        style={{
          marginBottom: 12,
          padding: 10,
          border: "1px solid #ddd",
          borderRadius: 8,
          maxWidth: 340,
        }}
      >
        <div style={{ fontWeight: 600, marginBottom: 6 }}>
          입력(4개): {inputTokens.length}/4
        </div>

        <div style={{ fontSize: 12, wordBreak: "break-all" }}>
          {inputTokens.length === 0 ? (
            <span style={{ color: "#666" }}>아직 입력 없음</span>
          ) : (
            inputTokens.map((t, idx) => (
              <div key={`${t}-${idx}`}>
                #{idx + 1}: {t}
              </div>
            ))
          )}
        </div>

        <div style={{ display: "flex", gap: 8, marginTop: 10 }}>
          <button onClick={clearInput} type="button">
            입력 지우기
          </button>

          <button
            onClick={submitInput}
            type="button"
            disabled={inputTokens.length !== 4}
          >
            입력 제출
          </button>
        </div>
      </div>

      {/* 기존 키패드 UI 그대로 */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(3, 100px)",
          gap: 10,
        }}
      >
        {layout.map((cell, idx) => (
          <button
            // key는 inner_value가 빈칸에서 중복될 수 있으니 idx 포함
            key={`${cell.inner_value}-${idx}`}
            onClick={() => handleClick(cell)}
            disabled={cell.is_blank || inputTokens.length >= 4} // ✅ 4개면 입력 막기
            style={{ width: 100, height: 100 }}
          >
            <img
              src={cell.image}
              alt="key"
              style={{ width: "100%", height: "100%", objectFit: "contain" }}
            />
          </button>
        ))}
      </div>

      <button onClick={initKeypad} style={{ marginTop: 20 }}>
        키패드 재배열(새 세션)
      </button>

      <div style={{ marginTop: 10, fontSize: 12 }}>Session: {sessionId}</div>
    </div>
  );
}
