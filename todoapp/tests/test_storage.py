import json

from todo.storage import JsonStorage


def _make_storage(tmp_path):
    """
    Létrehoz egy JsonStorage-t, de a fájl útvonalát átirányítja tmp_path alá,
    hogy a teszt ne a projekt mappájába írjon.
    """
    s = JsonStorage("test_items.json")
    # <-- átirányítás tmp= ideiglenes fájliútvonal
    s.path = tmp_path / "test_items.json"
    return s


def test_load_dict_when_file_missing_returns_empty_dict(tmp_path):
    s = _make_storage(tmp_path)

    data = s.load_dict()

    assert data == {}


def test_load_dict_when_file_empty_returns_empty_dict(tmp_path):
    s = _make_storage(tmp_path)
    s.path.write_text("", encoding="utf-8")

    data = s.load_dict()

    assert data == {}


def test_load_dict_when_invalid_json_returns_empty_dict(tmp_path):
    s = _make_storage(tmp_path)
    s.path.write_text("{not json", encoding="utf-8")

    data = s.load_dict()

    assert data == {}


def test_load_dict_when_json_is_not_dict_returns_empty_dict(tmp_path):
    s = _make_storage(tmp_path)
    s.path.write_text(json.dumps([1, 2, 3]), encoding="utf-8")

    data = s.load_dict()

    assert data == {}


def test_save_dict_writes_valid_json_dict(tmp_path):
    s = _make_storage(tmp_path)

    s.save_dict({"next_id": 2, "items": [{"id": 1, "text": "alma"}]})

    raw = s.path.read_text(encoding="utf-8")
    loaded = json.loads(raw)
    assert isinstance(loaded, dict)
    assert loaded["next_id"] == 2
    assert loaded["items"][0]["text"] == "alma"


def test_roundtrip_save_then_load(tmp_path):
    s = _make_storage(tmp_path)

    original = {"next_id": 5, "items": [
        {"id": 1, "text": "a", "priority": 2, "done": False}]}
    s.save_dict(original)

    data = s.load_dict()

    assert data == original
