import { useEffect, useRef } from 'react';

const API = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';

export default function KDSPage() {
  const wsRef = useRef<WebSocket | null>(null);
  useEffect(() => {
    const ws = new WebSocket(API.replace('http', 'ws') + '/ws/kds/demo');
    wsRef.current = ws;
    ws.onmessage = (ev) => {
      console.log('KDS message', ev.data);
    };
    return () => ws.close();
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold">Kitchen Display</h1>
      <p>Connected to tenant demo.</p>
    </div>
  );
}
