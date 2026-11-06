"""Takes the AppStream screenshots of Endpaper with made-up sample books. argv: out folder, light|dark, [only]."""

import json
import os
import shutil
import sys
import tempfile
import time
from pathlib import Path

R = Path("/home/wuebbsy/Development/Endpaper")
HERE = Path(__file__).resolve().parent
OUT = Path(sys.argv[1])
SCHEME = sys.argv[2]
ONLY = sys.argv[3].split(",") if len(sys.argv) > 3 else None
sys.path[:0] = [str(R / "src"), str(HERE)]
os.environ["LANGUAGE"] = "en"
os.environ["LC_ALL"] = "C.UTF-8"
TMP = Path(tempfile.mkdtemp(prefix="shots-", dir=HERE))
LIB = TMP / "Books"
for name, sub in (("XDG_CONFIG_HOME", "c"), ("XDG_DATA_HOME", "d"), ("XDG_CACHE_HOME", "k")):
    os.environ[name] = str(TMP / sub)
    (TMP / sub).mkdir()

import books  # noqa: E402

made = books.build(LIB)

import gi  # noqa: E402

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gio, GLib, Graphene, Gtk  # noqa: E402

from endpaper import config, library  # noqa: E402
from endpaper.main import EndpaperApplication  # noqa: E402
from endpaper.notes import NotesFile  # noqa: E402

config.update(library_path=str(LIB), reader={"theme": "auto"})


def spin(seconds):
    context, end = GLib.MainContext.default(), time.time() + seconds
    while time.time() < end:
        context.iteration(False) or time.sleep(0.003)


def wait_for(condition, seconds=25):
    context, end = GLib.MainContext.default(), time.time() + seconds
    while time.time() < end:
        if condition():
            return True
        context.iteration(False) or time.sleep(0.003)
    return False


def js(reader, script):
    box = {}
    reader._js(script, lambda value: box.update(done=True, value=value))
    wait_for(lambda: box.get("done"), 15)
    return box.get("value")


def shot(window, name):
    if ONLY and name not in ONLY:
        return
    spin(1.2)
    window.unset_state_flags(Gtk.StateFlags.BACKDROP)  # as if the window had the focus
    spin(0.3)
    width, height = window.get_width(), window.get_height()
    scale = 2
    snapshot = Gtk.Snapshot()
    snapshot.scale(scale, scale)
    Gtk.WidgetPaintable(widget=window).snapshot(snapshot, width, height)
    node = snapshot.to_node()
    texture = window.get_renderer().render_texture(node, Graphene.Rect().init(0, 0, width * scale, height * scale))
    suffix = "" if name == "shelf" else f"-{name}"
    path = OUT / f"screenshot{suffix}-{SCHEME}.png"
    texture.save_to_png(str(path))
    print("saved", path.name, texture.get_width(), texture.get_height(), flush=True)


app = EndpaperApplication()
app.set_flags(app.get_flags() | Gio.ApplicationFlags.NON_UNIQUE)


def go():
    Adw.StyleManager.get_default().set_color_scheme(
        Adw.ColorScheme.FORCE_DARK if SCHEME == "dark" else Adw.ColorScheme.FORCE_LIGHT)
    window = app.get_active_window()
    window.set_default_size(1280, 800)
    shelf = window.shelf
    window.state.collapsed.add("Study")
    shelf.set_root(LIB)
    spin(0.5)
    cards = {card.info.title: card for section in shelf.sections.values() for card in section.cards.values()
             if wait_for(lambda card=card: card.info.key, 10)}
    now = time.time()
    for i, (title, (path, progress)) in enumerate(made.items()):
        if progress:
            window.state.set_position(cards[title].info.key, "epubcfi(/6/4!/4/2)", progress, now - i * 3600)
    shelf.toggle_pin(cards["The Lighthouse Keeper"])
    shelf.toggle_pin(cards["Small Hours"])
    shelf.toggle_reference(cards["A Field Guide to Garden Birds"])
    spin(0.5)
    shelf.refresh_progress()
    wait_for(lambda: not shelf.indexer.busy, 60)
    spin(1)
    shelf.scroller.get_vadjustment().set_value(0)
    shot(window, "shelf")

    # Marks and notes in the open book.
    lighthouse = cards["The Lighthouse Keeper"]
    shelf.open_card(lighthouse)
    reader = window.reader
    wait_for(lambda: reader.opened)
    wait_for(lambda: (js(reader, "endpaper.diagnostics()") or {}).get("cfi"))
    js(reader, "endpaper.goToPassage(1, [1, 0])")  # chapter 2, the heading
    spin(1.5)
    click = lambda selector, word: js(reader, f"endpaper.clickWord({json.dumps(selector)}, {json.dumps(word)})")
    marks = [
        ("yellow", "p:nth-of-type(1)", "tapped", "mind."),
        ("green", "p:nth-of-type(3)", "Whatever", "were."),
        ("blue", "p:nth-of-type(2)", "the", "stone."),
    ]
    for color, selector, first, last in marks:
        reader.mark_buttons[color].set_active(True)
        wait_for(lambda: (js(reader, "endpaper.markState()") or {}).get("marking"))
        click(selector, first)
        wait_for(lambda: (js(reader, "endpaper.markState()") or {}).get("pending"))
        click(selector, last)
        wait_for(lambda: not (js(reader, "endpaper.markState()") or {}).get("pending"))
        spin(0.3)
        reader.mark_buttons[color].set_active(False)
        spin(0.3)
    entries = {e.color: e for e in reader.notes.entries}
    print("marks", [(e.color, e.quote[:30]) for e in reader.notes.entries], flush=True)
    book_path = lighthouse.book.path
    window.navigation.pop()
    wait_for(lambda: window.navigation.get_visible_page() is shelf)
    spin(0.5)
    notes = NotesFile(book_path)
    if "yellow" in entries:
        notes.add_note(entries["yellow"].id, "Her father's habit, the first thing she does **without thinking**. Compare the log in chapter 5.")
    if "green" in entries:
        notes.add_note(entries["green"].id, "The lamp as a promise: the light is for the ships, not for her.")
        notes.add_note(entries["green"].id, "Question for the reading group: *what does she owe the light?*")
    if "blue" in entries:
        notes.add_note(entries["blue"].id, "The tower \u201canswers\u201d the storm. The same word comes back in the last sentence of the chapter.")
    spin(0.3)
    shelf.open_card(lighthouse)
    wait_for(lambda: reader.opened)
    wait_for(lambda: (js(reader, "endpaper.diagnostics()") or {}).get("cfi"))
    spin(1.5)
    reader.notes_split.set_show_sidebar(True)
    spin(1.5)
    shot(window, "notes")
    reader.notes_split.set_show_sidebar(False)
    spin(0.5)

    # Search in the book.
    reader.start_search()
    reader.search_entry.set_text("lamp")
    spin(2.5)
    shot(window, "search")
    reader.search_entry.set_text("")
    reader.split.set_show_sidebar(False)
    spin(0.5)

    # Focus mode.
    js(reader, "endpaper.goToPassage(1, [1, 0])")
    spin(1)
    # Focus mode without full screen, so that the picture has the size of the others.
    if SCHEME == "light":
        reader.theme_follow.set_active(False)
        reader.theme_buttons["sepia"].set_active(True)
    reader.set_focus_mode(True)
    spin(3)
    shot(window, "focus")
    reader.set_focus_mode(False)
    reader.theme_follow.set_active(True)
    spin(1.5)

    # Search in the library.
    window.navigation.pop()
    wait_for(lambda: window.navigation.get_visible_page() is shelf)
    spin(0.5)
    shelf.start_search()
    shelf.search_entry.set_text("lamp")
    spin(2.5)
    shot(window, "library-search")

    window.close()
    app.quit()


app.connect("activate", lambda _a: GLib.timeout_add(500, lambda: (go(), False)[1]))
app.run(None)
shutil.rmtree(TMP, ignore_errors=True)
