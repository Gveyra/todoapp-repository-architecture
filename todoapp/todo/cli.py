from .service import TodoApp
from .dto import AddAction, ToggleAction, PriorityAction, RemoveAction, ListMode, TodoItem


class TodoCLI:
    def __init__(self, app: TodoApp):
        self.app = app

    def _fmt(self, it: TodoItem) -> str:
        mark = "✅" if it.get("done", False) else "⬜"
        return f"{mark} [{it['id']}] (p{it['priority']}) {it['text']}"

    def render(self, result: dict) -> None:
        action = result.get("action")
        it = result.get("item")

        if action == AddAction.CREATED:
            print(f"✅ Létrehozva: {self._fmt(it)}")
            return
        if action == AddAction.MERGED:
            print(f"ℹ️ Már létezett (összevonva): {self._fmt(it)}")
            return
        if action == ToggleAction.TOGGLED:
            print(f"✅ Átváltva: {self._fmt(it)}")
            return
        if action == PriorityAction.UPDATED:
            print(f"✅ Prioritás frissítve: {self._fmt(it)}")
            return
        if action == RemoveAction.REMOVED:
            print(f"🗑️ Törölve: [{it['id']}] {it['text']}")
            return

        print(f"ℹ️ Ismeretlen eredmény: {result}")

    def show(self, mode: ListMode = ListMode.ALL) -> None:
        items = self.app.list_items(mode)
        if not items:
            print("Üres.")
            return
        for it in items:
            print(self._fmt(it))

    def run(self) -> None:
        self.app.load()
        while True:
            print(
                "\nTODO\n"
                "1) Új feladat\n"
                "2) Listázás (mind)\n"
                "3) Listázás (nyitott)\n"
                "4) Listázás (kész)\n"
                "5) Kész/nyitott váltás (toggle)\n"
                "6) Prioritás beállítás (1-3)\n"
                "7) Keresés (részszó)\n"
                "8) Törlés\n"
                "0) Kilépés\n")

            choice = input("Válasz: ").strip()
            if choice == "1":
                text = input("Feladat: ")
                raw_p = input("Prioritás (1-3, Enter=2): ").strip()
                p = 2 if raw_p == "" else raw_p
                try:
                    res = self.app.add(text, p)
                    self.render(res)
                except (ValueError, KeyError) as e:
                    print(f"❌ {e}")

            elif choice == "2":
                self.show(ListMode.ALL)

            elif choice == "3":
                self.show(ListMode.OPEN)

            elif choice == "4":
                self.show(ListMode.DONE)

            elif choice == "5":
                try:
                    item_id = int(input("ID?: ").strip())
                    res = self.app.toggle_done(item_id)

                    self.render(res)
                except (ValueError, KeyError) as e:
                    print(f"❌ {e}")

            elif choice == "6":
                try:
                    item_id = int(input("ID?: ").strip())
                    pr = input("Új prioritás (1-3): ").strip()
                    res = self.app.set_priority(item_id, pr)

                    self.render(res)
                except (ValueError, KeyError) as e:
                    print(f"❌ {e}")

            elif choice == "7":
                q = input("Keresés: ").strip()
                res = self.app.search_contains(q)
                if not res:
                    print("Nincs találat.")
                else:
                    for it in res:
                        print(self._fmt(it))

            elif choice == "8":
                try:
                    item_id = int(input("ID?: ").strip())
                    res = self.app.remove_by_id(item_id)

                    self.render(res)
                except (ValueError, KeyError) as e:
                    print(f"❌ {e}")

            elif choice == "0":
                print("Szia!")
                break

            else:
                print("Ismeretlen menüpont.")
