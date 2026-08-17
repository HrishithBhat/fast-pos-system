import { useEffect, useState } from 'react';
import axios from 'axios';

const API = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';

export default function Admin() {
  const [token, setToken] = useState<string | null>(null);
  const [name, setName] = useState('Coffee');
  const [sku, setSku] = useState('COF-001');
  const [price, setPrice] = useState(3.5);
  const [taxRate, setTaxRate] = useState<number | undefined>(0.0);
  const [msg, setMsg] = useState<string | null>(null);

  useEffect(() => {
    (async () => {
      try {
        await axios.post(`${API}/api/auth/register`, { email: 'admin@example.com', password: 'pass', role: 'admin' });
      } catch {}
      const res = await axios.post(`${API}/api/auth/login`, { email: 'admin@example.com', password: 'pass' });
      setToken(res.data.access_token);
    })();
  }, []);

  const createProduct = async () => {
    if (!token) return;
    setMsg(null);
    try {
      const res = await axios.post(
        `${API}/api/products`,
        { name, sku, price, tax_rate: taxRate },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setMsg(`Product created: ${res.data.id}`);
    } catch (e: any) {
      setMsg(e?.response?.data?.detail || 'Create failed');
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold">Admin Dashboard</h1>
      <p>Manage products, categories, and tenant settings.</p>

      {!token && <p className="mt-2 text-gray-600">Logging in as admin...</p>}

      <div className="mt-6 border-t pt-4">
        <h2 className="text-xl font-semibold">Create Product</h2>
        <div className="mt-3 grid grid-cols-2 gap-3 max-w-xl">
          <label className="flex flex-col">
            <span>Name</span>
            <input className="border p-2 rounded" value={name} onChange={(e) => setName(e.target.value)} />
          </label>
          <label className="flex flex-col">
            <span>SKU</span>
            <input className="border p-2 rounded" value={sku} onChange={(e) => setSku(e.target.value)} />
          </label>
          <label className="flex flex-col">
            <span>Price</span>
            <input
              type="number"
              className="border p-2 rounded"
              value={price}
              onChange={(e) => setPrice(parseFloat(e.target.value))}
            />
          </label>
          <label className="flex flex-col">
            <span>Tax Rate</span>
            <input
              type="number"
              className="border p-2 rounded"
              value={taxRate ?? 0}
              onChange={(e) => setTaxRate(parseFloat(e.target.value))}
            />
          </label>
        </div>
        <button
          disabled={!token}
          className="mt-4 px-4 py-2 bg-blue-600 text-white rounded disabled:bg-gray-400"
          onClick={createProduct}
        >
          Create Product
        </button>
        {msg && <p className="mt-2 text-sm text-gray-700">{msg}</p>}
      </div>
    </div>
  );
}
