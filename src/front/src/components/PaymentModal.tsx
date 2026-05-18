import { useState } from 'react'
import type { PaymentMethod } from '../types/api'
import styles from './PaymentModal.module.css'

interface PaymentOption {
  value: PaymentMethod
  label: string
  emoji: string
}

const METHODS: PaymentOption[] = [
  { value: 'pix',  label: 'PIX',      emoji: '📱' },
  { value: 'cash', label: 'Dinheiro', emoji: '💵' },
  { value: 'credit_card', label: 'Cartão de Crédito',   emoji: '💳' },
  { value: 'debit_card', label: 'Cartão de Débito',   emoji: '💳' },
  { value: 'vr_card', label: 'VR',   emoji: '💳' },
]

interface Props {
  total: () => number
  onConfirm: (method: PaymentMethod) => void
  onClose: () => void
  isLoading: boolean
}

export function PaymentModal({ total, onConfirm, onClose, isLoading }: Props) {
  const [selected, setSelected] = useState<PaymentMethod | null>(null)

  return (
    <div className={styles.overlay}>
      <div className={styles.modal}>
        <div className={styles.header}>
          <div>
            <h2 className={styles.title}>Forma de pagamento</h2>
            <p className={styles.subtitle}>
              Total:{' '}
              <strong className={styles.totalAmount}>
                R$ {total().toFixed(2).replace('.', ',')}
              </strong>
            </p>
          </div>
          <button className={styles.closeBtn} onClick={onClose} aria-label="Fechar">
            ✕
          </button>
        </div>

        <div className={styles.methods}>
          {METHODS.map((method) => (
            <button
              key={method.value}
              className={`${styles.methodOption} ${selected === method.value ? styles.methodOptionSelected : ''}`}
              onClick={() => setSelected(method.value)}
            >
              <span className={styles.methodEmoji}>{method.emoji}</span>
              <span className={styles.methodLabel}>{method.label}</span>
              {selected === method.value && (
                <span className={styles.methodCheck}>✓</span>
              )}
            </button>
          ))}
        </div>

        <div className={styles.actions}>
          <button className={styles.cancelBtn} onClick={onClose}>
            Cancelar
          </button>
          <button
            className={styles.confirmBtn}
            disabled={!selected || isLoading}
            onClick={() => selected && onConfirm(selected)}
          >
            {isLoading ? 'Salvando...' : 'Confirmar'}
          </button>
        </div>
      </div>
    </div>
  )
}