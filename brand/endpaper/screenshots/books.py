"""Sample books for the Endpaper screenshots. All text is made up for them."""

import io
import math
import zipfile
from html import escape
from pathlib import Path

import gi

gi.require_version("Pango", "1.0")
gi.require_version("PangoCairo", "1.0")
import cairo
from gi.repository import Pango, PangoCairo

LIGHTHOUSE = {
    "Arrival": [
        "The boat left Ada on the jetty with two crates, a sack of flour and a letter she was not to open until the first of the month. The boatman did not wait to see her climb the path. He had his own weather to think about, and the island was not a place where people lingered.",
        "The lighthouse stood at the top of the rise, white against a sky that could not decide between rain and sun. From below it looked smaller than it had in the drawings her father kept above his desk, and older, as if the wind had been sanding it for a hundred years. It had.",
        "Inside, the keeper's room smelled of paraffin and salt. A kettle sat on the stove, cold. On the table lay the log, open at the last entry: <em>Wind west, moderate. Lamp lit at 5.40. All well.</em> The handwriting was her father's.",
        "She read the line three times before she put her bag down. Then she climbed the hundred and twelve steps to the lantern room, because that was what a keeper did first, and because she did not yet know what else to do.",
        "The lamp was clean. Someone had trimmed the wick and polished the brass, and the great lens turned on its bed of mercury at the lightest touch of her hand. Through the glass the sea went on for ever, grey and patient, and somewhere beyond it was the mainland she had left that morning.",
    ],
    "The Storm": [
        "The barometer had been falling since noon. Ada tapped the glass twice, the way her father used to, as if the needle could be persuaded to change its mind. It never once answered him, and it did not answer her.",
        "By evening the wind stood at nine on the Beaufort scale. It came across the water in long grey sheets, and the old tower answered it with every stone. The windows hummed. Somewhere below, a shutter she had forgotten banged against the wall like a fist on a door.",
        "She lit the lamp at twenty past five, early, because the light was already going. The flame caught, steadied, and grew, and the lens took it and threw it out across the water in four white beams that turned and turned. Whatever else happened tonight, the ships would know where the rocks were.",
        "At eight she made tea and did not drink it. At nine she went up to the lantern room and wiped the salt from the inside of the glass, though there was none. At ten she sat down with the log and wrote the time, the wind and the state of the sea, in a hand that was steadier than she felt.",
        "It was nearly midnight when she saw the other light. It was small and yellow and low on the water, far too low for a ship, and it rose and fell with the swell. She watched it for a long time before she understood that it was a lantern, and that someone was holding it.",
        "She ran down the hundred and twelve steps without counting them. The door fought her and the wind took her breath away, but the path to the cove was the one she had walked a thousand times as a child, and her feet remembered it even when her eyes could not.",
        "On the shingle lay a rowing boat, half full of water, and beside it a man in an oilskin coat who was trying to stand and could not. He looked up when her lamp found his face. \"I saw your light,\" he said, as if that explained everything. Perhaps it did.",
        "She got him up the path somehow, one step at a time, with the storm pushing at their backs. In the keeper's room she wrapped him in every blanket she owned and put the cold tea on the stove again. He was asleep before it boiled.",
        "Ada went back up to the lamp. It was still turning, steady and white, sweeping the dark water where the little yellow light had been. She sat beside it until morning and listened to the tower answer the wind.",
    ],
    "The Letter": [
        "The stranger slept until noon. When he woke he said his name was Elias, that he had been sailing to the mainland, and that he was sorry for the trouble. He did not say why anyone would sail to the mainland in a rowing boat on the worst night of the year.",
        "Ada did not ask. It was the first of the month, and on the shelf above the stove lay the letter she had been told to keep closed until today. She opened it while he ate, and read it twice, and then folded it very small and put it in her pocket.",
        "\"Bad news?\" Elias asked. \"Old news,\" she said. Her father had known about the storm, the letter said. He had known about a great many things, and he had written them all in the log, between the wind and the weather, for whoever came to keep the light after him.",
        "That afternoon she took the log down from the shelf and turned back through the years. The lamp lit, the lamp put out, the ships that passed and the ones that did not. And here and there, in the margin, a small pencilled star.",
    ],
    "Low Tide": [
        "At low tide the island doubled in size. Rocks that were hidden all winter rose out of the water, black and shining, and between them lay pools where small crabs went about their business as if nobody were watching.",
        "Elias walked out with her to the far point, where the old wreck showed its ribs twice a month. He knew the names of the birds and the seaweed, and he knew the lighthouse, too, better than a stranger should. He had been here before, he admitted at last. A long time ago.",
        "\"Your father kept the lamp burning for me once,\" he said. \"All night, in a storm like the last one. I never thanked him.\" Ada thought of the pencilled stars in the margin of the log and did not say anything for a while.",
    ],
    "The Keeper's Log": [
        "The log was not a diary. Her father had been very clear about that. A keeper wrote down what the light did and what the sea did, and nothing about what the keeper thought of either.",
        "And yet. In the margins of thirty years there was a second log, written in pencil and in small stars, and when Ada laid the pages side by side she could read it. Every star was a night when a boat had come in by the light and someone had been glad of it.",
        "She found the night Elias had spoken of. Wind north-west, gale. Lamp lit at 4.55. Small boat seen off the point at 11. And in the margin, a star, and a single word she had not expected from her father: <em>Home.</em>",
    ],
    "Fog": [
        "The fog came in on the last day of the month and did not lift for three days. It filled the cove and climbed the path and pressed against the windows like wet wool, and the lamp turned all day as well as all night, a pale smudge in the white.",
        "When the boat came for Elias, they heard it long before they saw it, the engine knocking somewhere out in the grey. He shook her hand on the jetty and said he would write. She believed him, which surprised her.",
        "That evening Ada lit the lamp at the usual time and wrote in the log. Fog, dense. Lamp lit at 5.30. Boat to the mainland at 3. Then, after a moment, she sharpened the pencil and drew a small star in the margin.",
    ],
}

FIELD_QUESTIONS = """<p class="question">Which birds visited your garden this week, and at what time of day?</p>
<textarea id="q1" rows="3" style="width: 100%;"></textarea>"""


def lighthouse_chapters():
    return [(title, paragraphs) for title, paragraphs in LIGHTHOUSE.items()]


def simple_chapters(sections):
    """sections: [(title, [paragraphs])]; each chapter gets its paragraphs twice, for some length."""
    return list(sections)


BOOKS = [
    # category, file, title, author, palette, motif, progress, chapters
    ("Novels", "The Lighthouse Keeper", "Mara Lindqvist", ("#1f3a5f", "#f2c46d", "#f5efe0"), "lighthouse", 0.38,
     lighthouse_chapters()),
    ("Novels", "The Winter Orchard", "Jonas Ferrell", ("#7a2e2e", "#e9d8c4", "#f6efe6"), "tree", 1.0, simple_chapters([
        ("The First Frost", [
            "The orchard was older than the house, and the house was older than anyone could remember. Every winter the trees stood in their rows like patient people waiting for a train, and every spring they were surprised all over again.",
            "Nell walked between them with a lantern in the early dark, counting. Forty-two trees, as there had always been. She knew each one by the shape of its branches against the sky, the way you know a voice on the telephone.",
            "From the top of the hill you could see the sea on a clear day, and at night the lighthouse on the far headland, blinking its slow white signal. Her grandmother said it was counting the trees too, from out there.",
        ]),
        ("Grafting", [
            "In February the old man from the next valley came to teach her grafting. He brought a knife wrapped in oilcloth and a ball of waxed string, and he talked the whole time about apples that nobody grew any more.",
            "\"A tree remembers what you give it,\" he said, binding a pale twig to a dark branch. \"Give it something good, and in five years it will give it back to you. Give it nothing, and it will give you nothing too.\"",
        ]),
    ])),
    ("Novels", "Salt and Cedar", "Ines Calloway", ("#2f5d50", "#d9b26f", "#eef3ee"), "waves", 0.72, simple_chapters([
        ("The Harbor", [
            "The harbor town lived by the tide. When it was out, the boats lay on their sides in the mud like sleeping dogs, and the gulls walked among them looking for breakfast. When it was in, everything floated, and everybody hurried.",
            "Tomas had a cedar workshop at the end of the quay, where he built boats the old way, plank by plank. The smell of the wood carried down the whole street, and the children said you could find his door with your eyes closed.",
            "On stormy nights he left a lamp burning in the window, though the lighthouse on the point did that job far better. \"For the ones who come in late,\" he said, and nobody ever asked him which ones he meant.",
        ]),
        ("Launching", [
            "The new boat went into the water on the first warm day of May. Half the town came down to watch, and the other half pretended not to, from behind their curtains.",
            "She floated. That was the main thing. She floated, and she sat level, and when Tomas stepped aboard she dipped to meet him like a horse that knows its rider.",
        ]),
    ])),
    ("Novels", "A House by the River", "Theo Brandt", ("#d8a48f", "#4a3b52", "#fbf4ef"), "house", 0.0, simple_chapters([
        ("Moving In", [
            "The house by the river had nine rooms, three staircases and a door that opened onto nothing at all, two floors up, where a balcony had once been. The estate agent called it character. The children called it the door to the sky.",
            "They moved in on a wet Tuesday with a van that was too small and a cat that refused to leave its basket. By evening the kitchen was full of boxes and the river had risen to the bottom of the garden, brown and fast and full of opinions.",
        ]),
    ])),
    ("Novels", "The Clockmaker's Daughter", "Clara Weston", ("#3b3355", "#c9a96e", "#f3f0f7"), "clock", 0.15, simple_chapters([
        ("Seven Minutes Fast", [
            "Every clock in the shop ran seven minutes fast, and every customer complained about it, and every customer came back. Her father said it was a kindness. People were always late; this way they were only a little late.",
            "Lotte grew up among the ticking, which never stopped, not even at night. When she went to stay with her aunt in the city she could not sleep for the silence, and lay awake listening for a heartbeat in the walls.",
        ]),
    ])),
    ("Study", "A Field Guide to Garden Birds", "Henrik Moll", ("#e8e1cf", "#5b7553", "#2e3b2c"), "bird", None, simple_chapters([
        ("How to Watch", [
            "The best way to watch birds is to sit still and let them come to you. Choose a place with a view of the feeder and the hedge, bring a cup of tea, and give it a quarter of an hour. Most birds forgive a quiet watcher very quickly.",
            "Keep a notebook. Write down the date, the time and the weather, and then every bird you see, even the ones you are not sure of. After a month you will know your garden better than you ever expected.",
        ]),
        ("The Robin", [
            "The robin is the gardener's companion. It follows the spade for the worms it turns up, and it sings in winter when almost every other bird is silent, a thin, bright song from the top of the hedge.",
            "Robins are fiercely territorial. A male will fight his own reflection in a window for an hour, and a pair will defend their corner of the garden against all comers, however large.",
        ]),
        ("Gulls and Sea Birds", [
            "Near the coast, gardens are visited by gulls, which are cleverer than their reputation. Herring gulls nest on roofs and on the ledges of old buildings; on some islands they nest on the gallery of the lighthouse itself.",
            "Watch for the oystercatcher on the lawn after rain, black and white with an orange bill, probing for worms with great seriousness.",
        ]),
    ])),
    ("Study", "The Quiet Mind", "R. A. Penhallow", ("#f1ece2", "#8c6d4f", "#3a3029"), "circle", 0.55, simple_chapters([
        ("On Attention", [
            "Attention is the rarest and purest form of generosity. To give a book, a person or a single afternoon your whole attention is to give them something that cannot be bought and is seldom offered.",
            "We do not lack time so much as we lack stillness. The hours are there; it is we who are elsewhere, already thinking of the next thing before the present one has had its turn.",
        ]),
        ("On Reading Slowly", [
            "A book read slowly is a different book. The sentences open like rooms, and you find that the author has furnished them with care: a chair by the window, a lamp on the table, a door left a little open.",
            "Mark what moves you. A line in the margin, a word underlined, a short note in your own hand: these are the footprints you leave for the reader you will be in ten years.",
        ]),
    ])),
    ("Study", "Notes on Light and Color", "Paul Arden", ("#f4d35e", "#1d3557", "#1d3557"), "rays", 0.9, simple_chapters([
        ("What Light Is", [
            "Light travels in straight lines until something persuades it otherwise. A glass, a drop of water or the surface of the sea will bend it, split it or turn it back, and most of what we see is light that has been persuaded.",
            "A lighthouse lens is a lesson in persuasion, and the lamp is only half of it. Its rings of glass gather the light of a single flame and bend it into a beam that can be seen twenty miles away, a candle made to shout.",
        ]),
        ("Color", [
            "Color is not in things, strictly speaking, but in the light they give back. A red apple keeps the blue and green for itself and returns only the red, which is perhaps the most generous thing an apple can do.",
        ]),
    ])),
    ("Poetry and Letters", "Small Hours", "Lena Haldane", ("#141b2d", "#9fb4d9", "#e9eef7"), "moon", 0.25, simple_chapters([
        ("Night Watch", [
            "The kettle ticks as it cools.<br/>Somewhere a dog remembers<br/>a bone it never had.",
            "Out on the black water<br/>the lighthouse keeps its counting,<br/>one, and one, and one.",
            "I leave the lamp on<br/>for no one in particular,<br/>which is to say, for you.",
        ]),
        ("Morning", [
            "First the blackbird,<br/>then the milk van,<br/>then the long grey light<br/>that asks for nothing.",
        ]),
    ])),
    ("Poetry and Letters", "Letters from the Coast", "Edith Rowe", ("#5a7d9a", "#f2e8d5", "#f7f4ee"), "gull", 0.6, simple_chapters([
        ("March", [
            "Dearest Anna, the wind has not stopped for four days and I have given up on my hat entirely. The village is very small and very kind, and the baker already knows that I take my bread unsliced.",
            "From my window, by the light of my lamp, I can see the lighthouse on its island, and at night its beam comes round across the ceiling every ten seconds, so regular that I have started to fall asleep counting it, like sheep.",
        ]),
        ("April", [
            "Dearest Anna, the gulls have begun to nest on the roof, and they are not quiet about it. I have been told this is a sign of spring. I have also been told that I will get used to it, which I doubt.",
        ]),
    ])),
]


# --- Covers ---------------------------------------------------------------------------------

W, H = 600, 900


def _rgb(hexcolor):
    hexcolor = hexcolor.lstrip("#")
    return tuple(int(hexcolor[i:i + 2], 16) / 255 for i in (0, 2, 4))


def _text(cr, text, font, size, color, y, width=W - 120, align=Pango.Alignment.CENTER, spacing=0):
    layout = PangoCairo.create_layout(cr)
    desc = Pango.FontDescription.from_string(f"{font} {size}")
    layout.set_font_description(desc)
    layout.set_width(int(width * Pango.SCALE))
    layout.set_alignment(align)
    layout.set_wrap(Pango.WrapMode.WORD)
    if spacing:
        attrs = Pango.AttrList()
        attrs.insert(Pango.attr_letter_spacing_new(int(spacing * Pango.SCALE)))
        layout.set_attributes(attrs)
    layout.set_text(text, -1)
    cr.set_source_rgb(*_rgb(color))
    cr.move_to((W - width) / 2, y)
    PangoCairo.show_layout(cr, layout)
    return layout.get_pixel_size()[1]


def _motif(cr, motif, ink, accent):
    cx, cy = W / 2, 560
    cr.set_source_rgb(*_rgb(accent))
    if motif == "lighthouse":
        for side in (-1, 1):
            beam = cairo.LinearGradient(cx, 0, cx + side * 300, 0)
            beam.add_color_stop_rgba(0, *_rgb(accent), 0.55)
            beam.add_color_stop_rgba(1, *_rgb(accent), 0.0)
            cr.set_source(beam)
            cr.move_to(cx, 470); cr.line_to(cx + side * 300, 395); cr.line_to(cx + side * 300, 525); cr.close_path()
            cr.fill()
        cr.set_source_rgb(*_rgb(accent))
        cr.move_to(cx - 26, 700); cr.line_to(cx - 16, 490); cr.line_to(cx + 16, 490); cr.line_to(cx + 26, 700)
        cr.close_path(); cr.fill()
        cr.rectangle(cx - 22, 455, 44, 30); cr.fill()
        cr.move_to(cx - 26, 455); cr.line_to(cx, 430); cr.line_to(cx + 26, 455); cr.close_path(); cr.fill()
        cr.set_source_rgba(1, 1, 1, 0.9); cr.rectangle(cx - 12, 461, 24, 18); cr.fill()
        _waves(cr, 700, accent, 0.5)
    elif motif == "tree":
        cr.set_line_width(10); cr.set_line_cap(cairo.LINE_CAP_ROUND)
        _branch(cr, cx, 720, -math.pi / 2, 120, 6)
        cr.move_to(90, 722); cr.line_to(W - 90, 722); cr.set_line_width(3); cr.stroke()
    elif motif == "waves":
        cr.move_to(cx - 10, 330); cr.line_to(cx - 10, 470); cr.line_to(cx - 100, 470); cr.close_path(); cr.fill()
        cr.move_to(cx + 5, 350); cr.line_to(cx + 5, 470); cr.line_to(cx + 70, 470); cr.close_path(); cr.fill()
        cr.move_to(cx - 110, 485); cr.line_to(cx + 110, 485); cr.line_to(cx + 80, 510); cr.line_to(cx - 80, 510)
        cr.close_path(); cr.fill()
        for i in range(5):
            _waves(cr, 520 + i * 40, accent, 1 - i * 0.15, amplitude=14)
    elif motif == "house":
        cr.move_to(cx - 110, 640); cr.line_to(cx - 110, 520); cr.line_to(cx, 430); cr.line_to(cx + 110, 520)
        cr.line_to(cx + 110, 640); cr.close_path(); cr.fill()
        cr.set_source_rgb(*_rgb(ink))
        for x, y in ((cx - 70, 540), (cx + 30, 540)):
            cr.rectangle(x, y, 40, 40); cr.fill()
        cr.rectangle(cx - 18, 590, 36, 50); cr.fill()
        _waves(cr, 690, accent, 0.8, amplitude=8)
    elif motif == "clock":
        cr.set_line_width(8); cr.new_sub_path(); cr.arc(cx, cy - 20, 130, 0, 2 * math.pi); cr.stroke()
        for i in range(12):
            a = i * math.pi / 6
            cr.set_line_width(6 if i % 3 == 0 else 3)
            cr.move_to(cx + 105 * math.cos(a), cy - 20 + 105 * math.sin(a))
            cr.line_to(cx + 118 * math.cos(a), cy - 20 + 118 * math.sin(a)); cr.stroke()
        cr.set_line_width(7); cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.move_to(cx, cy - 20); cr.line_to(cx + 45, cy - 75); cr.stroke()
        cr.move_to(cx, cy - 20); cr.line_to(cx - 10, cy - 110); cr.stroke()
    elif motif == "bird":
        cr.new_sub_path(); cr.arc(cx, cy, 80, 0, 2 * math.pi); cr.fill()
        cr.new_sub_path(); cr.arc(cx + 70, cy - 70, 45, 0, 2 * math.pi); cr.fill()
        cr.move_to(cx + 110, cy - 75); cr.line_to(cx + 140, cy - 68); cr.line_to(cx + 110, cy - 60); cr.close_path(); cr.fill()
        cr.move_to(cx - 70, cy + 10); cr.line_to(cx - 170, cy - 30); cr.line_to(cx - 80, cy + 50); cr.close_path(); cr.fill()
        cr.set_source_rgb(*_rgb("#c8553d")); cr.new_sub_path(); cr.arc(cx + 35, cy - 20, 48, 0, 2 * math.pi); cr.fill()
        cr.set_source_rgb(*_rgb(ink)); cr.new_sub_path(); cr.arc(cx + 80, cy - 78, 6, 0, 2 * math.pi); cr.fill()
        cr.set_source_rgb(*_rgb(accent)); cr.set_line_width(5)
        cr.move_to(cx - 200, cy + 92); cr.line_to(cx + 200, cy + 92); cr.stroke()
    elif motif == "circle":
        cr.set_line_width(3)
        for r in (140, 110, 80):
            cr.new_sub_path(); cr.arc(cx, cy - 20, r, 0, 2 * math.pi); cr.stroke()
        cr.new_sub_path(); cr.arc(cx, cy - 20, 40, 0, 2 * math.pi); cr.fill()
    elif motif == "rays":
        for i in range(16):
            a = i * math.pi / 8
            cr.move_to(cx, cy - 20)
            cr.arc(cx, cy - 20, 220, a, a + math.pi / 16); cr.close_path(); cr.fill()
        cr.set_source_rgb(*_rgb("#f4d35e")); cr.new_sub_path(); cr.arc(cx, cy - 20, 70, 0, 2 * math.pi); cr.fill()
    elif motif == "moon":
        cr.new_sub_path(); cr.arc(cx + 30, cy - 40, 100, 0, 2 * math.pi); cr.fill()
        cr.set_source_rgb(*_rgb("#141b2d")); cr.new_sub_path(); cr.arc(cx + 75, cy - 70, 92, 0, 2 * math.pi); cr.fill()
        cr.set_source_rgb(*_rgb(accent))
        for x, y, r in ((150, 430, 4), (420, 650, 3), (200, 690, 2.5), (470, 460, 3), (110, 600, 2)):
            cr.new_sub_path(); cr.arc(x, y, r, 0, 2 * math.pi); cr.fill()
    elif motif == "gull":
        cr.set_line_width(7); cr.set_line_cap(cairo.LINE_CAP_ROUND)
        for x, y, s in ((cx - 60, cy - 40, 1.2), (cx + 90, cy - 100, 0.8), (cx + 20, cy + 40, 0.6)):
            cr.move_to(x - 70 * s, y); cr.curve_to(x - 40 * s, y - 40 * s, x - 10 * s, y - 30 * s, x, y)
            cr.curve_to(x + 10 * s, y - 30 * s, x + 40 * s, y - 40 * s, x + 70 * s, y); cr.stroke()
        _waves(cr, 700, accent, 0.8, amplitude=10)


def _waves(cr, y, color, alpha, amplitude=10):
    cr.set_source_rgba(*_rgb(color), alpha)
    cr.set_line_width(5)
    cr.move_to(60, y)
    for x in range(60, W - 60, 60):
        cr.curve_to(x + 15, y - amplitude, x + 45, y + amplitude, x + 60, y)
    cr.stroke()


def _branch(cr, x, y, angle, length, depth):
    if depth == 0:
        return
    x2, y2 = x + length * math.cos(angle), y + length * math.sin(angle)
    cr.set_line_width(depth * 2.2)
    cr.move_to(x, y); cr.line_to(x2, y2); cr.stroke()
    _branch(cr, x2, y2, angle - 0.45, length * 0.72, depth - 1)
    _branch(cr, x2, y2, angle + 0.4, length * 0.7, depth - 1)


def cover(title, author, palette, motif) -> bytes:
    background, accent, ink = palette
    surface = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    cr = cairo.Context(surface)
    cr.set_source_rgb(*_rgb(background)); cr.paint()
    text_color = ink if sum(_rgb(background)) > 1.8 else "#f7f4ee"
    if sum(_rgb(background)) <= 1.8:
        ink = background
    _text(cr, author.upper(), "Noto Sans Medium", 15, text_color, 92, spacing=3)
    _text(cr, title, "C059 Bold", 38, text_color, 140)
    _motif(cr, motif, ink, accent)
    cr.set_source_rgb(*_rgb(accent)); cr.set_line_width(2)
    cr.move_to(W / 2 - 40, 810); cr.line_to(W / 2 + 40, 810); cr.stroke()
    out = io.BytesIO()
    surface.write_to_png(out)
    return out.getvalue()


# --- EPUB -------------------------------------------------------------------------------------

CSS = """
body { margin: 0; }
h1 { font-weight: normal; font-size: 1.6em; margin: 0.8em 0 1.4em; }
h1 .number { display: block; font-size: 0.55em; letter-spacing: 0.2em; text-transform: uppercase; opacity: 0.6; margin-bottom: 0.4em; }
p { margin: 0; text-indent: 1.4em; }
h1 + p { text-indent: 0; }
p.question { text-indent: 0; font-style: italic; margin-top: 1em; }
.poem p { text-indent: 0; margin-bottom: 1em; }
"""


def typeset(text):
    """Curly quotes and apostrophes, as a printed book has them."""
    import re
    text = re.sub(r'"([^"]*)"', "\u201c\\1\u201d", text)
    return text.replace("'", "\u2019")


def make_book(path: Path, title, author, palette, motif, chapters, identifier, extra=None):
    items, spine, toc = [], [], []
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml",
                   '<?xml version="1.0"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
                   '<rootfiles><rootfile full-path="OEBPS/p.opf" media-type="application/oebps-package+xml"/></rootfiles></container>')
        z.writestr("OEBPS/style.css", CSS)
        items.append('<item id="css" href="style.css" media-type="text/css"/>')
        poem = motif == "moon"
        for n, (chapter, paragraphs) in enumerate(chapters, 1):
            body = "".join(f"<p>{typeset(p)}</p>" for p in paragraphs)
            if extra and n == 1:
                body += extra
            if poem:
                body = f'<div class="poem">{body}</div>'
            html = ('<?xml version="1.0" encoding="utf-8"?>\n'
                    '<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">'
                    f'<head><title>{escape(chapter)}</title><link rel="stylesheet" href="style.css"/></head>'
                    f'<body><h1><span class="number">Chapter {n}</span>{escape(chapter)}</h1>{body}</body></html>')
            z.writestr(f"OEBPS/ch{n}.xhtml", html)
            items.append(f'<item id="c{n}" href="ch{n}.xhtml" media-type="application/xhtml+xml"/>')
            spine.append(f'<itemref idref="c{n}"/>')
            toc.append(f'<li><a href="ch{n}.xhtml">{escape(chapter)}</a></li>')
        z.writestr("OEBPS/nav.xhtml",
                   '<?xml version="1.0"?><html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">'
                   f'<head><title>Contents</title></head><body><nav epub:type="toc"><ol>{"".join(toc)}</ol></nav></body></html>')
        items.append('<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>')
        z.writestr("OEBPS/cover.png", cover(title, author, palette, motif))
        items.append('<item id="cov" href="cover.png" media-type="image/png" properties="cover-image"/>')
        z.writestr("OEBPS/p.opf",
                   '<?xml version="1.0"?><package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="i">'
                   f'<metadata xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:identifier id="i">{identifier}</dc:identifier>'
                   f"<dc:title>{escape(title)}</dc:title><dc:creator>{escape(author)}</dc:creator><dc:language>en</dc:language></metadata>"
                   f'<manifest>{"".join(items)}</manifest><spine>{"".join(spine)}</spine></package>')


def build(library: Path) -> dict:
    """The books in their categories; returns {title: (path, progress)}."""
    made = {}
    for i, (category, title, author, palette, motif, progress, chapters) in enumerate(BOOKS):
        folder = library / category
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / f"{title}.epub"
        extra = FIELD_QUESTIONS if motif == "bird" else None
        make_book(path, title, author, palette, motif, chapters, f"urn:endpaper-sample:{i}", extra)
        made[title] = (path, progress)
    return made


if __name__ == "__main__":
    import sys
    out = Path(sys.argv[1])
    for category, title, author, palette, motif, *_ in BOOKS:
        (out / f"{title}.png").write_bytes(cover(title, author, palette, motif))
