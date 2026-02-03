import { useEffect, useState } from "react";

type Cell = {
  pos: number;
  token: string;
  image: string;
  is_blank: boolean;
};

export default function App() {
  const [layout, setLayout] = useState<Cell[]>([]);
  const [sessionId, setSessionId] = useState("");
  const [error, setError] = useState("");

  const initKeypad = async () => {
    setError("");
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
    console.log("클릭된 토큰:", cell.token);
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>E2E Keypad Demo</h1>

      {error && <div style={{ color: "red" }}>{error}</div>}

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(3, 100px)",
          gap: 10,
        }}
      >
        {layout.map((cell) => (
          <button
            key={cell.pos}
            onClick={() => handleClick(cell)}
            disabled={cell.is_blank}
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

      <div style={{ marginTop: 10, fontSize: 12 }}>
        Session: {sessionId}
      </div>
    </div>
  );
}
