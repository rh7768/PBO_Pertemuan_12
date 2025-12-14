from abc import ABC, abstractmethod
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)

LOGGER = logging.getLogger('Checkout')


# --- ABSTRAKSI (Kontrak untuk OCP/DIP) ---
class IPaymentProcessor(ABC):
    """Interface untuk semua prosesor pembayaran."""

    @abstractmethod
    def process(self, order) -> bool:
        """Memproses pembayaran.

        Args:
            order (Order): Objek pesanan.

        Returns:
            bool: True jika pembayaran berhasil, False jika gagal.
        """
        pass


class INotificationService(ABC):
    """Interface untuk semua layanan notifikasi."""

    @abstractmethod
    def send(self, order):
        """Mengirim notifikasi.

        Args:
            order (Order): Objek pesanan.
        """
        pass


# --- IMPLEMENTASI KONKRIT (Plug-in) ---
class CreditCardProcessor(IPaymentProcessor):
    """Prosesor pembayaran menggunakan kartu kredit."""

    def process(self, order) -> bool:
        LOGGER.info("Memproses pembayaran menggunakan Kartu Kredit.")
        return True


class EmailNotifier(INotificationService):
    """Layanan notifikasi melalui email."""

    def send(self, order):
        LOGGER.info(f"Mengirim email konfirmasi ke {order.customer}.")


# --- KELAS KOORDINATOR (SRP & DIP) ---
class CheckoutService:
    """
    Kelas high-level untuk mengkoordinasi proses transaksi pembayaran.

    Kelas ini memisahkan logika pembayaran dan notifikasi (memenuhi SRP).
    """

    def __init__(self, payment_processor: IPaymentProcessor,
                 notifier: INotificationService):
        """
        Menginisialisasi CheckoutService dengan dependensi yang diperlukan.

        Args:
            payment_processor (IPaymentProcessor): Implementasi interface pembayaran.
            notifier (INotificationService): Implementasi interface notifikasi.
        """
        self.payment_processor = payment_processor
        self.notifier = notifier

    def run_checkout(self, order) -> bool:
        """
        Menjalankan proses checkout dan memvalidasi pembayaran.

        Args:
            order (Order): Objek pesanan yang akan diproses.

        Returns:
            bool: True jika checkout sukses, False jika gagal.
        """
        LOGGER.info(
            f"Memulai checkout untuk {order.customer}. Total: {order.amount}"
        )

        payment_success = self.payment_processor.process(order)

        if payment_success:
            order.status = "paid"
            self.notifier.send(order)
            LOGGER.info("Checkout sukses. Status pesanan: PAID.")
            return True
        else:
            LOGGER.error("Pembayaran gagal. Transaksi dibatalkan.")
            return False


# --- PROGRAM UTAMA ---
class Order:
    """Representasi data pesanan."""

    def __init__(self, customer, amount):
        """
        Membuat objek Order.

        Args:
            customer (str): Nama pelanggan.
            amount (int): Total harga pesanan.
        """
        self.customer = customer
        self.amount = amount
        self.status = "unpaid"

    def __repr__(self):
        return f"Order({self.customer}, {self.amount})"


class EmailNotifier:
    """Implementasi sederhana notifikasi email."""

    def notify(self, order):
        LOGGER.info(f"Mengirim email ke {order.customer}")

    # Tambahan agar konsisten dengan interface
    def send(self, order):
        self.notify(order)


class IPaymentProcessor:
    """Interface pembayaran (versi implied)."""

    def process(self, order) -> bool:
        raise NotImplementedError


class CheckoutService:
    """Service checkout versi implied."""

    def __init__(self, payment_processor: IPaymentProcessor,
                 notifier: EmailNotifier):
        self.payment_processor = payment_processor
        self.notifier = notifier

    def run_checkout(self, order) -> bool:
        LOGGER.info(f"Checkout untuk pesanan: {order}")

        if self.payment_processor.process(order):
            LOGGER.info("Pembayaran berhasil.")
            self.notifier.send(order)
            return True
        else:
            LOGGER.warning("Pembayaran gagal.")
            return False


class CreditCardProcessor(IPaymentProcessor):
    """Prosesor pembayaran kartu kredit (versi implied)."""

    def process(self, order) -> bool:
        LOGGER.info("Memproses pembayaran Credit Card.")
        return True


# --- Kode dari Gambar ---
andi_order = Order("Andi", 500000)
email_service = EmailNotifier()

cc_processor = CreditCardProcessor()
checkout_cc = CheckoutService(
    payment_processor=cc_processor,
    notifier=email_service
)

print("--- Skenario 1: Credit Card ---")
checkout_cc.run_checkout(andi_order)


class QrisProcessor(IPaymentProcessor):
    """Prosesor pembayaran QRIS."""

    def process(self, order) -> bool:
        LOGGER.info("Memproses pembayaran QRIS.")
        return True


budi_order = Order("Budi", 100000)
qris_processor = QrisProcessor()

checkout_qris = CheckoutService(
    payment_processor=qris_processor,
    notifier=email_service
)

print("\n--- Skenario 2: Pembuktian OCP (QRIS) ---")
checkout_qris.run_checkout(budi_order)
