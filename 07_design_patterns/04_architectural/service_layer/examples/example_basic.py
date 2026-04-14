class TaxService:
    def calculate(self, amount: float) -> float:
        return round(amount * 0.21, 2)


class BillingService:
    def __init__(self, tax_service: TaxService) -> None:
        self.tax_service = tax_service

    def invoice_total(self, subtotal: float) -> float:
        return subtotal + self.tax_service.calculate(subtotal)


def main() -> None:
    print(BillingService(TaxService()).invoice_total(100))


if __name__ == '__main__':
    main()
