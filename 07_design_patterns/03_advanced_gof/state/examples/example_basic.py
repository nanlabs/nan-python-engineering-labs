class Order:
    def __init__(self) -> None:
        self.state = 'draft'

    def submit(self) -> None:
        if self.state == 'draft':
            self.state = 'submitted'

    def approve(self) -> None:
        if self.state == 'submitted':
            self.state = 'approved'


def main() -> None:
    order = Order()
    order.submit()
    order.approve()
    print(order.state)


if __name__ == '__main__':
    main()
