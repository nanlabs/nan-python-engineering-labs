from dataclasses import dataclass


@dataclass
class Snapshot:
    value: str


class Editor:
    def __init__(self) -> None:
        self.value = ''

    def save(self) -> Snapshot:
        return Snapshot(self.value)

    def restore(self, snapshot: Snapshot) -> None:
        self.value = snapshot.value


def main() -> None:
    editor = Editor()
    editor.value = 'draft'
    snap = editor.save()
    editor.value = 'modified'
    editor.restore(snap)
    print(editor.value)


if __name__ == '__main__':
    main()
