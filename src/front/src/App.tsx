import { useState } from 'react'
import { useQuery, useMutation } from '@tanstack/react-query'
import { api } from './api/client'
import { useCartStore } from './store/cartStore'
import { ProductCard } from './components/ProductCard'
import { CartSidebar } from './components/CartSidebar'
import { PaymentModal } from './components/PaymentModal'
import type { PaymentMethod, ProductCategory } from './types/api'

type CategoryFilter = ProductCategory | 'Todos'

const CATEGORIES: { value: CategoryFilter; label: string }[] = [
  { value: 'Todos',  label: 'Todos'    },
  { value: 'FOOD',   label: 'Salgados' },
  { value: 'SWEET',  label: 'Doces'    },
  { value: 'DRINK',  label: 'Bebidas'  },
  { value: 'OTHERS', label: 'Outros'   },
]

export default function App() {
  const [activeCategory, setActiveCategory] = useState<CategoryFilter>('Todos')
  const [showPayment, setShowPayment] = useState(false)

  const { items, addItem, removeItem, clearCart, total, itemCount } = useCartStore()

  const { data: products = [], isLoading, isError } = useQuery({
    queryKey: ['products'],
    queryFn: api.getProducts,
  })

  const { mutate: createOrder, isPending } = useMutation({
    mutationFn: api.createOrder,
    onSuccess: () => {
      clearCart()
      setShowPayment(false)
      alert('Pedido criado com sucesso!')
    },
    onError: (err: Error) => {
      alert(`Erro: ${err.message}`)
    },
  })

  const filtered = activeCategory === 'Todos'
    ? products
    : products.filter(p => p.category === activeCategory)

  const getQuantity = (productId: number): number =>
    items.find(i => i.product.id === productId)?.quantity ?? 0

  const handleConfirmOrder = (paymentMethod: PaymentMethod) => {
    createOrder({
      payment_method: paymentMethod,
      items: items.map(i => ({
        product_id: i.product.id,
        quantity: i.quantity,
      })),
    })
  }

  return (
    <div className="flex h-screen bg-gray-50 font-sans">
      <main className="flex-1 flex flex-col overflow-hidden">
        <header className="bg-white border-b border-gray-100 px-6 py-4 flex items-center justify-between shrink-0">
          <h1 className="text-xl font-bold text-gray-900">🍡 Dricas Doces e Salgados</h1>
          <span className="text-sm text-gray-500">{products.length} produtos no cardápio</span>
        </header>

        <div className="px-6 py-3 flex gap-2 overflow-x-auto shrink-0 bg-white border-b border-gray-100">
          {CATEGORIES.map(cat => (
            <button
              key={cat.value}
              onClick={() => setActiveCategory(cat.value)}
              className={`px-4 py-2 rounded-full text-sm font-medium whitespace-nowrap transition-colors touch-manipulation
                ${activeCategory === cat.value
                  ? 'bg-orange-500 text-white'
                  : 'bg-gray-100 text-gray-600 active:bg-gray-200'
                }`}
            >
              {cat.label}
            </button>
          ))}
        </div>

        <div className="flex-1 overflow-y-auto p-6">
          {isLoading && (
            <p className="text-center text-gray-400 mt-16">Carregando cardápio...</p>
          )}
          {isError && (
            <p className="text-center text-red-400 mt-16">Erro ao carregar produtos.</p>
          )}
          <div className="grid grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {filtered.map(product => (
              <ProductCard
                key={product.id}
                product={product}
                quantity={getQuantity(product.id)}
                onAdd={addItem}
                onRemove={removeItem}
              />
            ))}
          </div>
        </div>
      </main>

      <CartSidebar
        items={items}
        total={total}
        onAdd={addItem}
        onRemove={removeItem}
        onOpenPayment={() => setShowPayment(true)}
      />

      {showPayment && (
        <PaymentModal
          total={total}
          onConfirm={handleConfirmOrder}
          onClose={() => setShowPayment(false)}
          isLoading={isPending}
        />
      )}
    </div>
  )
}