import type { Product } from '../types/api'
import styles from './ProductCard.module.css'

const CATEGORY_LABEL: Record<string, string> = {
  FOOD: 'Salgado',
  SWEET: 'Doce',
  DRINK: 'Bebida',
  OTHERS: 'Outro',
}

interface Props {
  product: Product
  quantity: number
  onAdd: (product: Product) => void
  onRemove: (productId: number) => void
}

export function ProductCard({ product, quantity, onAdd, onRemove }: Props) {
  return (
    <div className={styles.card}>
      <div className={styles.body}>
        <span className={styles.category}>
          {CATEGORY_LABEL[product.category] ?? product.category}
        </span>
        <h3 className={styles.name}>{product.name}</h3>
        <p className={styles.price}>
          R$ {product.price.toFixed(2).replace('.', ',')}
        </p>
      </div>

      {quantity === 0 ? (
        <button className={styles.addBtn} onClick={() => onAdd(product)}>
          Adicionar
        </button>
      ) : (
        <div className={styles.counter}>
          <button className={styles.counterBtn} onClick={() => onRemove(product.id)}>
            −
          </button>
          <span className={styles.counterQty}>{quantity}</span>
          <button className={`${styles.counterBtn} ${styles.counterBtnPrimary}`} onClick={() => onAdd(product)}>
            +
          </button>
        </div>
      )}
    </div>
  )
}