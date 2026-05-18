// Espelha os enums do back
export type PaymentMethod = 'pix' | 'cash' | 'debit_card' | 'credit_card' | 'vr_card'
export type ProductCategory = 'pending' | 'completed' | 'cancelled'
export type OrderStatus = 'pending' | 'completed' | 'cancelled'

// Espelha ProductRead
export interface Product {
  id: number
  name: string
  price: number
  category: ProductCategory
  is_active: boolean
  created_at: string
  updated_at: string | null
}

// Espelha OrderItemRead
export interface OrderItem {
  product_id: number
  quantity: number
  unit_price: number
}

export interface OrderItemRead {
  product_id: number
  quantity: number
  unit_price: number
  created_at: string
  updated_at: string | null
}

// Espelha OrderRead
export interface Order {
  id: number
  total_price: number
  payment_method: PaymentMethod
  status: OrderStatus
  items: OrderItemRead[]
  created_at: string
  updated_at: string | null
}

// Espelha OrderCreate
export interface OrderCreate {
  payment_method: PaymentMethod
  items: { product_id: number; quantity: number }[]
}