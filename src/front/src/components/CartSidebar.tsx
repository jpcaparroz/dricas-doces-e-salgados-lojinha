import type { CartItem } from '../store/cartStore'
import type { Product } from '../types/api'
import styles from './CartSidebar.module.css'

interface Props {
  items: CartItem[]
  total: () => number
  onAdd: (product: Product) => void
  onRemove: (productId: number) => void
  onOpenPayment: () => void
}

export function CartSidebar({ items, total, onAdd, onRemove, onOpenPayment }: Props) {
  const isEmpty = items.length === 0

  return (
    <aside className={styles.sidebar}>
      <div className={styles.header}>
        <h2 className={styles.title}>Pedido atual</h2>
        {!isEmpty && (
          <span className={styles.badge}>{items.length}</span>
        )}
      </div>

      <div className={styles.itemList}>
        {isEmpty ? (
          <div className={styles.empty}>
            <span className={styles.emptyIcon}>🛒</span>
            <p className={styles.emptyText}>Nenhum item adicionado</p>
          </div>
        ) : (
          items.map(({ product, quantity }) => (
            <div key={product.id} className={styles.item}>
              <div className={styles.itemInfo}>
                <p className={styles.itemName}>{product.name}</p>
                <p className={styles.itemSubtotal}>
                  R$ {(product.price * quantity).toFixed(2).replace('.', ',')}
                </p>
              </div>
              <div className={styles.itemCounter}>
                <button
                  className={styles.itemBtn}
                  onClick={() => onRemove(product.id)}
                >
                  −
                </button>
                <span className={styles.itemQty}>{quantity}</span>
                <button
                  className={`${styles.itemBtn} ${styles.itemBtnPrimary}`}
                  onClick={() => onAdd(product)}
                >
                  +
                </button>
              </div>
            </div>
          ))
        )}
      </div>

      <div className={styles.footer}>
        <div className={styles.totalRow}>
          <span className={styles.totalLabel}>Total</span>
          <span className={styles.totalValue}>
            R$ {total().toFixed(2).replace('.', ',')}
          </span>
        </div>
        <button
          className={styles.checkoutBtn}
          disabled={isEmpty}
          onClick={onOpenPayment}
        >
          Finalizar pedido
        </button>
      </div>
    </aside>
  )
}