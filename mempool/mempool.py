class Mempool:
    """
    Quản lý các giao dịch vé đang chờ được xác nhận.

    Chức năng:
    - Thêm giao dịch hợp lệ vào Mempool.
    - Kiểm tra vé trùng.
    - Kiểm tra vé đã sử dụng.
    - Kiểm tra quyền sở hữu khi chuyển vé.
    - Lấy danh sách giao dịch đang chờ.
    - Xóa giao dịch đã được xử lý.
    """

    def __init__(self):
        self.pending_transactions = []

    def add_transaction(self, tx):
        """
        Thêm giao dịch vào Mempool.

        Args:
            tx (dict): Thông tin giao dịch vé.

        Returns:
            bool: True nếu giao dịch hợp lệ.

        Raises:
            ValueError: Nếu giao dịch không hợp lệ.
        """

        # 1. Kiểm tra dữ liệu đầu vào
        if not isinstance(tx, dict):
            raise ValueError("Transaction phải là dictionary.")

        required_fields = ["ticket_id", "status"]

        for field in required_fields:
            if field not in tx:
                raise ValueError(
                    f"Transaction thiếu trường: {field}"
                )

        ticket_id = tx["ticket_id"]
        status = tx["status"]

        # 2. Kiểm tra vé đã tồn tại trong Mempool
        for pending_tx in self.pending_transactions:
            if pending_tx["ticket_id"] == ticket_id:
                raise ValueError(
                    f"Vé {ticket_id} đã tồn tại trong Mempool."
                )

        # 3. Kiểm tra trạng thái vé
        if status == "used":
            raise ValueError(
                f"Vé {ticket_id} đã được sử dụng."
            )

        if status != "unused":
            raise ValueError(
                f"Trạng thái vé không hợp lệ: {status}"
            )

        # 4. Kiểm tra quyền sở hữu khi chuyển vé
        sender = tx.get("from")
        owner = tx.get("owner")

        if sender is not None and owner is not None:
            if sender != owner:
                raise ValueError(
                    "Người gửi không phải chủ sở hữu vé."
                )

        # 5. Thêm giao dịch hợp lệ vào Mempool
        self.pending_transactions.append(tx)

        return True

    def get_pending(self):
        """
        Lấy danh sách giao dịch đang chờ.

        Returns:
            list: Danh sách giao dịch trong Mempool.
        """

        return self.pending_transactions.copy()

    def remove_transactions(self, tx_list):
        """
        Xóa các giao dịch đã được xử lý.

        Args:
            tx_list (list): Danh sách giao dịch cần xóa.

        Returns:
            int: Số lượng giao dịch đã xóa.
        """

        if not isinstance(tx_list, list):
            raise ValueError(
                "tx_list phải là danh sách."
            )

        ticket_ids = set()

        for tx in tx_list:
            if isinstance(tx, dict):
                ticket_ids.add(tx.get("ticket_id"))
            else:
                ticket_ids.add(tx)

        original_length = len(self.pending_transactions)

        self.pending_transactions = [
            tx for tx in self.pending_transactions
            if tx.get("ticket_id") not in ticket_ids
        ]

        removed_count = (
            original_length - len(self.pending_transactions)
        )

        return removed_count

    def contains_ticket(self, ticket_id):
        """
        Kiểm tra vé đã tồn tại trong Mempool chưa.

        Args:
            ticket_id (str): Mã vé.

        Returns:
            bool: True nếu vé đã tồn tại.
        """

        return any(
            tx["ticket_id"] == ticket_id
            for tx in self.pending_transactions
        )

    def clear(self):
        """
        Xóa toàn bộ giao dịch trong Mempool.
        """

        self.pending_transactions.clear()
