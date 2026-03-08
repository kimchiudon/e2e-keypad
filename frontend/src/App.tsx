import { useEffect, useState } from "react";
import { encryptHashArray } from "./utils/crypto";

type Cell = {
  inner_value: string;
  image: string;
  is_blank: boolean;
};

const PUBLIC_KEY_PEM: string =
  ((import.meta as any).env?.VITE_KEYPAD_PUBLIC_KEY ?? "").replace(/\\n/g, "\n");

export default function App() {
  const [layout, setLayout] = useState<Cell[]>([]);
  const [sessionId, setSessionId] = useState("");
  const [error, setError] = useState("");
  const [inputTokens, setInputTokens] = useState<string[]>([]);
  const [submitMsg, setSubmitMsg] = useState<string>("");

  const initKeypad = async () => {
    setError("");
    setSubmitMsg("");
    setInputTokens([]);

    try {
      const res = await fetch("http://127.0.0.1:8000/keypad/init");
      if (!res.ok) {
        throw new Error(`init failed: ${res.status}`);
      }

      const data = await res.json();
      setSessionId(data.session_id);
      setLayout(data.layout);
    } catch (e: any) {
      console.error("initKeypad error:", e);
      setError(`키패드 로딩 실패: ${e?.message ?? String(e)}`);
    }
  };

  useEffect(() => {
    void initKeypad();
  }, []);

  const handleClick = (cell: Cell) => {
    if (cell.is_blank) return;

    setInputTokens((prev) => {
      if (prev.length >= 4) return prev;
      return [...prev, cell.inner_value];
    });
  };

  const clearInput = () => {
    setSubmitMsg("");
    setError("");
    setInputTokens([]);
  };

  const submitInput = async () => {
    setSubmitMsg("");
    setError("");

    if (!sessionId) {
      setError("세션이 없습니다.");
      return;
    }

    if (inputTokens.length !== 4) {
      setError("입력은 정확히 4개여야 합니다.");
      return;
    }

    if (!PUBLIC_KEY_PEM || !PUBLIC_KEY_PEM.includes("BEGIN PUBLIC KEY")) {
      setError("공개키가 없습니다. .env의 VITE_KEYPAD_PUBLIC_KEY를 설정하세요.");
      return;
    }

    try {
      console.log("PUBLIC_KEY_PEM loaded:", PUBLIC_KEY_PEM);
      console.log("sessionId:", sessionId);
      console.log("inputTokens:", inputTokens);
      console.log(
        "joined tokens length:",
        inputTokens.join("|").length
      );

      const encrypted = encryptHashArray(inputTokens, PUBLIC_KEY_PEM);

      console.log("encrypted result:", encrypted);

      if (!encrypted) {
        setError("RSA 암호화 실패: 토큰 길이 초과 또는 공개키 형식 문제");
        return;
      }

      const res = await fetch("http://127.0.0.1:8000/keypad/submit", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          session_id: sessionId,
          encrypted_data: encrypted,
        }),
      });

      const rawText = await res.text();
      console.log("submit status:", res.status);
      console.log("submit raw response:", rawText);

      if (!res.ok) {
        throw new Error(`submit failed: ${res.status} ${rawText}`);
      }

      let result: any = {};
      try {
        result = JSON.parse(rawText);
      } catch {
        result = { raw: rawText };
      }

      setSubmitMsg(
        `RSA 암호화 후 전송 성공!\n\n` +
          `encrypted_data:\n${encrypted}\n\n` +
          `server response:\n${JSON.stringify(result, null, 2)}`
      );
    } catch (e: any) {
      console.error("submitInput error:", e);
      setError(`암호화 또는 전송 실패: ${e?.message ?? String(e)}`);
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>E2E Keypad Demo</h1>

      {error && <div style={{ color: "red", marginBottom: 10 }}>{error}</div>}
      {submitMsg && (
        <div style={{ color: "green", marginBottom: 10, whiteSpace: "pre-wrap" }}>
          {submitMsg}
        </div>
      )}

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

          <button onClick={submitInput} type="button" disabled={inputTokens.length !== 4}>
            입력 제출
          </button>
        </div>
      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(3, 100px)",
          gap: 10,
        }}
      >
        {layout.map((cell, idx) => (
          <button
            key={`${cell.inner_value}-${idx}`}
            onClick={() => handleClick(cell)}
            disabled={cell.is_blank || inputTokens.length >= 4}
            style={{ width: 100, height: 100 }}
            type="button"
          >
            <img
              src={cell.image}
              alt="key"
              style={{ width: "100%", height: "100%", objectFit: "contain" }}
            />
          </button>
        ))}
      </div>

      <button onClick={initKeypad} style={{ marginTop: 20 }} type="button">
        키패드 재배열(새 세션)
      </button>

      <div style={{ marginTop: 10, fontSize: 12 }}>Session: {sessionId}</div>
    </div>
  );
}