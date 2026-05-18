from enum import Enum


class ProductCategory(str, Enum):
    OTHERS = "others"
    DRINK = "drink"
    FOOD = "food"
    SWEET = "doce"

class OrderStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class PaymentMethod(str, Enum):
    CASH = "cash"
    DEBIT_CARD = "debit_card"
    CREDIT_CARD = "credit_card"
    VR_CARD = "vr_card"
    PIX = "pix"
