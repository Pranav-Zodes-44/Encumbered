from services import embed_service, dto

def get_transaction_icon(method: str):
	if (method == "set"):
		return ":pencil2:"
	
	if (method == "add"):
		return ":inbox_tray:"
	
	if (method == "remove"):
		return ":outbox_tray:"


def get_transaction_strings(transactions: list[dto.TransactionDto]):
	data = []

	for transaction in transactions:
		pp_str = f"{embed_service.icons['platinum']} {transaction.gold_change.pp}"
		gp_str = f"{embed_service.icons['gold']} {transaction.gold_change.gp}"
		sp_str = f"{embed_service.icons['silver']} {transaction.gold_change.sp}"
		cp_str = f"{embed_service.icons['copper']} {transaction.gold_change.cp}"

		data.append(f"`{transaction.id}` - {get_transaction_icon(transaction.method)} - {pp_str}, {gp_str}, {sp_str}, {cp_str}")

	return data