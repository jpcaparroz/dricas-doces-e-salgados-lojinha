import { create } from 'zustand'
import type { Product } from '../types/api'

export interface CartItem {
  product: Product
  quantity: number
}

interface CartStore {
  items: CartItem[]
  addItem:    (product: Product) => void
  removeItem: (productId: number) => void
  clearCart:  () => void
  total:      () => number
  itemCount:  () => number
}

export const useCartStore = create<CartStore>((set, get) => ({
  items: [],

  addItem: (product) => {
    const items = get().items
    const existing = items.find(i => i.product.id === product.id)
    if (existing) {
      set({
        items: items.map(i =>
          i.product.id === product.id ? { ...i, quantity: i.quantity + 1 } : i
        ),
      })
    } else {
      set({ items: [...items, { product, quantity: 1 }] })
    }
  },

  removeItem: (productId) => {
    const items = get().items
    const existing = items.find(i => i.product.id === productId)
    if (!existing) return
    if (existing.quantity === 1) {
      set({ items: items.filter(i => i.product.id !== productId) })
    } else {
      set({
        items: items.map(i =>
          i.product.id === productId ? { ...i, quantity: i.quantity - 1 } : i
        ),
      })
    }
  },

  clearCart: () => set({ items: [] }),

  total: () =>
    get().items.reduce((sum, i) => sum + i.product.price * i.quantity, 0),

  itemCount: () =>
    get().items.reduce((sum, i) => sum + i.quantity, 0),
}))