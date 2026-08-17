import { useEffect, useState } from 'react';
import axios from 'axios';

const API = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';

type Product = { id: string; name: string; price: number };
type CartItem = { product_id: string; name: string; price: number; quantity: number };

export default function POSPage() {
  const [token, setToken] = useState<string | null>(null);
  const [products, setProducts] = useState<Product[]>([]);
  const [cart, setCart] = useState<CartItem[]>([]);
  const [message, setMessage] = useState<string | null>(null);

  useEffect(() => {
    // demo: register then login to get a token
    (async () => {
      try {
        await axios.post(`${API}/api/auth/register`, { email: 'cashier@example.com', password: 'pass', role: 'cashier' });
      } catch {}
      const res = await axios.post(`${API}/api/auth/login`, { email: 'cashier@example.com', password: 'pass' });
      setToken(res.data.access_token);
    })();
  }, []);

  useEffect(() => {
    (async () => {
      if (!token) return;
      const res = await axios.get(`${API}/api/products`, { headers: { Authorization: `Bearer ${token}` } });
      setProducts(res.data);
    })();
  }, [token]);

  const addToCart = (p: Product) => {
    setCart((prev) => {
      const idx = prev.findIndex((ci) => ci.product_id === p.id);
      if (idx >= 0) {
        const next = [...prev];
        next[idx] = { ...next[idx], quantity: next[idx].quantity + 1 };
        return next;
      }
      return [...prev, { product_id: p.id, name: p.name, price: p.price, quantity: 1 }];
    });
  };

  const removeFromCart = (product_id: string) => {
    setCart((prev) => prev.filter((ci) => ci.product_id !== product_id));
  };

  const checkout = async () => {
    if (!token || cart.length === 0) return;
    setMessage(null);
    try {
      const items = cart.map((ci) => ({ product_id: ci.product_id, quantity: ci.quantity }));
      const res = await axios.post(
        `${API}/api/orders`,
        { items, source: 'pos', payment_method: 'cash' },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setCart([]);
      setMessage(`Order ${res.data.order_id} placed. Status: ${res.data.status}`);
    } catch (e: any) {
      setMessage(e?.response?.data?.detail || 'Checkout failed');
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold">POS</h1>
      {!token && <p>Logging in...</p>}

      <div className="grid grid-cols-2 gap-4 mt-4">
        {products.map((p) => (
          <div key={p.id} className="border p-3 rounded">
            <div className="font-semibold">{p.name}</div>
            <div>${p.price.toFixed(2)}</div>
            <button className="mt-2 px-3 py-1 bg-blue-600 text-white rounded" onClick={() => addToCart(p)}>
              Add to cart
            </button>
          </div>
        ))}
      </div>

      <div className="mt-6 border-t pt-4">
        <h2 className="text-xl font-semibold">Cart</h2>
        {cart.length === 0 && <p className="text-gray-600">No items</p>}
        {cart.map((ci) => (
          <div key={ci.product_id} className="flex items-center justify-between py-2">
            <div>
              {ci.name} x {ci.quantity}
            </div>
            <div className="flex items-center gap-2">
              <span>${(ci.price * ci.quantity).toFixed(2)}</span>
              <button className="px-2 py-1 bg-red-600 text-white rounded" onClick={() => removeFromCart(ci.product_id)}>
                Remove
              </button>
            </div>
          </div>
        ))}

        <div className="mt-4">
          <button
            disabled={!token || cart.length === 0}
            className="px-4 py-2 bg-green-600 text-white rounded disabled:bg-gray-400"
            onClick={checkout}
          >
            Checkout (cash)
          </button>
        </div>
        {message && <p className="mt-2 text-sm text-gray-700">{message}</p>}
      </div>
    </div>
  );
}
