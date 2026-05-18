import type { Product, Order, OrderCreate } from '../types/api'

const BASE_URL = import.meta.env.VITE_API_URL ?? '/api'

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  if (!res.ok) {
    const error = await res.json().catch(() => ({}))
    throw new Error((error as { detail?: string }).detail ?? 'Erro na requisição')
  }
  return res.json() as Promise<T>
}

export const api = {
  getProducts: () => request<Product[]>('/products/'),
  createOrder:  (data: OrderCreate) => request<Order>('/orders/', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
}