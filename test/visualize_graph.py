"""Script per generar un GIF animat de la creació i esborrat de nodes i arestes.

Cada operació segueix el patró PRE → OP:
  PRE: construeix l'estat base del graf
  OP:  executa l'operació real (inserció, esborrat, actualització)
  RESULT: retorna metadades per al renderitzat (highlight, deleted, etc.)

Executa:
    python test/visualize_graph.py

El GIF es guarda a test/output/animation.gif
"""

import sys
import os
import shutil
import math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PIL import Image, ImageDraw, ImageFont
from drm.mock_graph import MockGraph
from drm.entities import IndividuPadro, LlocPadro, Atribut
from drm.base import Node, Relation, WeakNode


OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
FPS = 0.5  # 1 frame cada 2 segons → transicions molt lentest
NODE_COLORS = {
    "IndividuPadro": "#4fc3f7",
    "LlocPadro": "#81c784",
    "TestNode": "#ffb74d",
    "Document": "#fff176",
    "Section": "#a1887f",
    "Page": "#90caf9",
    "DocumentPart": "#a5d6a7",
    "Valor": "#f06292",
}


# ── helpers ──────────────────────────────────────────────────────────

def _font(size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
    except (OSError, IOError):
        return ImageFont.load_default()


def _text_size(draw: ImageDraw.ImageDraw, text: str, font) -> tuple[int, int]:
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def _draw_box(
    draw: ImageDraw.ImageDraw,
    x1: int, y1: int, x2: int, y2: int,
    fill: str | None, outline: str = "#333", width: int = 1,
) -> None:
    draw.rectangle([x1, y1, x2, y2], fill=fill, outline=outline, width=width)


def _draw_node(
    draw: ImageDraw.ImageDraw,
    cx: int, cy: int,
    label: str, pk: str,
    fill: str,
    highlight: bool = False,
    deleted: bool = False,
    font: ImageFont.FreeTypeFont | None = None,
) -> None:
    """Draw an ellipse node. If deleted=True, draw with red strike-through."""
    if font is None:
        font = _font(13)
    font_pk = _font(10)

    tw, th = _text_size(draw, label, font)
    pw, ph = _text_size(draw, f"({pk})", font_pk)
    box_w = max(tw, pw) + 20
    box_h = th + ph + 14

    left = cx - box_w // 2
    top = cy - box_h // 2
    right = cx + box_w // 2
    bottom = cy + box_h // 2

    if deleted:
        draw.ellipse([left, top, right, bottom],
                      fill="#ffcccc", outline="#ff0000", width=3)
        draw.line([(left, top), (right, bottom)], fill="#ff0000", width=2)
        draw.line([(right, top), (left, bottom)], fill="#ff0000", width=2)
        font_del = _font(11)
        lw, _ = _text_size(draw, "ELIMINAT", font_del)
        _draw_box(draw, cx - lw // 2 - 6, cy - box_h // 2 - 20,
                  cx + lw // 2 + 6, cy - box_h // 2 - 6, fill="#ffcccc", outline="#ff0000")
        draw.text((cx - lw // 2, cy - box_h // 2 - 18), "ELIMINAT", fill="#cc0000", font=font_del)
    elif highlight:
        draw.ellipse([left - 3, top - 3, right + 3, bottom + 3],
                      fill=fill, outline="#ff0000", width=3)
    else:
        draw.ellipse([left, top, right, bottom],
                      fill=fill, outline="#333333", width=1)

    draw.text((cx - tw // 2, cy - th // 2 - 3), label, fill="#000000", font=font)
    draw.text((cx - pw // 2, cy + th // 2), f"({pk})", fill="#333333", font=font_pk)


def _draw_edge(
    draw: ImageDraw.ImageDraw,
    x1: int, y1: int,
    x2: int, y2: int,
    rel_type: str,
    deleted: bool = False,
    font: ImageFont.FreeTypeFont | None = None,
) -> None:
    """Draw a directed arrow. If deleted=True, draw in red."""
    if font is None:
        font = _font(11)
    dx = x2 - x1
    dy = y2 - y1
    dist = math.sqrt(dx * dx + dy * dy)
    if dist == 0:
        return

    offset = 60
    ux, uy = dx / dist, dy / dist
    sx, sy = x1 + ux * offset, y1 + uy * offset
    ex, ey = x2 - ux * offset, y2 - uy * offset

    color = "#cc0000" if deleted else "#333333"
    draw.line([(sx, sy), (ex, ey)], fill=color, width=2)

    arrow = 10
    angle = math.atan2(ey - sy, ex - sx)
    ax1 = ex - arrow * math.cos(angle - 0.4)
    ay1 = ey - arrow * math.sin(angle - 0.4)
    ax2 = ex - arrow * math.cos(angle + 0.4)
    ay2 = ey - arrow * math.sin(angle + 0.4)
    draw.polygon([(ex, ey), (ax1, ay1), (ax2, ay2)], fill=color)

    mx, my = (sx + ex) // 2, (sy + ey) // 2
    lw, _ = _text_size(draw, rel_type, font)
    bg = "#ffcccc" if deleted else "white"
    _draw_box(draw, mx - lw // 2 - 4, my - 8, mx + lw // 2 + 4, my + 8, fill=bg)
    draw.text((mx - lw // 2, my - 7), rel_type, fill=color, font=font)


def _draw_text_block(
    draw: ImageDraw.ImageDraw,
    x: int, y: int,
    lines: list[str],
    font: ImageFont.FreeTypeFont | None = None,
    bg: str = "#f5f5f5",
) -> int:
    """Draw a text block with a light background box. Returns box height."""
    if font is None:
        font = _font(12)
    padding = 6
    line_h = font.size + 4

    max_w = max(_text_size(draw, l, font)[0] for l in lines)
    total_h = len(lines) * line_h

    _draw_box(draw, x - padding, y - padding,
              x + max_w + padding, y + total_h + padding, fill=bg)

    for i, line in enumerate(lines):
        draw.text((x, y + i * line_h), line, fill="#222222", font=font)
    return total_h


# ── graph state reader ───────────────────────────────────────────────

def _read_graph_state(
    graph: MockGraph,
    positions: dict[int, tuple[int, int]],
    highlight_new: set[int] | None = None,
    deleted_nodes: set[int] | None = None,
    deleted_edges: set[tuple[int, int]] | None = None,
) -> tuple[list[tuple[int, str, str]], list[tuple[int, int, str]]]:
    """Read actual graph state and return (nodes, edges) for rendering."""
    del_nodes = deleted_nodes or set()
    del_edges = deleted_edges or set()
    highlight = highlight_new or set()

    nodes = []
    for nid in graph.get_nodes():
        if nid not in positions:
            continue
        attrs = graph.get_node_attrs(nid)
        if attrs is None:
            continue
        label = attrs.get("main_label", "Unknown")
        pk = attrs.get("pk", {})
        pk_str = str(pk)
        nodes.append((nid, label, pk_str))

    edges = []
    for src, dst, rtype in graph.get_edges():
        if src in positions and dst in positions:
            edges.append((src, dst, rtype))

    return nodes, edges


# ── frame builder ────────────────────────────────────────────────────

def _render_frame(
    step_num: int,
    title: str,
    graph: MockGraph,
    positions: dict[int, tuple[int, int]],
    nodes: list[tuple[int, str, str]],
    edges: list[tuple[int, int, str]],
    highlight_new: set[int] | None = None,
    explanation: str | None = None,
    deleted_nodes: set[int] | None = None,
    deleted_edges: set[tuple[int, int]] | None = None,
) -> None:
    """Render one frame from the actual graph state."""
    W, H = 1000, 700
    img = Image.new("RGB", (W, H), "white")
    draw = ImageDraw.Draw(img)

    font = _font(13)
    font_bold = _font(15)
    font_expl = _font(12)

    # Title bar
    _draw_box(draw, 0, 0, W, 32, fill="#263238")
    draw.text((12, 3), f"Step {step_num}: {title}", fill="white", font=font_bold)

    # Explanation box
    expl_y = 42
    if explanation:
        expl_lines = explanation.split("\n")
        _draw_text_block(draw, 14, expl_y, expl_lines, font=font_expl, bg="#e8f5e9")
        expl_h = len(expl_lines) * (font_expl.size + 4) + 12
        expl_y += expl_h + 6

    del_nodes = deleted_nodes or set()
    del_edges = deleted_edges or set()
    highlight = highlight_new or set()

    # Edges first
    for src_id, dst_id, rel_type in edges:
        if src_id in positions and dst_id in positions:
            is_del = (src_id, dst_id) in del_edges
            _draw_edge(draw,
                       positions[src_id][0], positions[src_id][1],
                       positions[dst_id][0], positions[dst_id][1],
                       rel_type, deleted=is_del, font=font)

    # Nodes
    for nid, label, pk in nodes:
        fill = NODE_COLORS.get(label, "#e0e0e0")
        hl = nid in highlight
        is_del = nid in del_nodes
        _draw_node(draw, positions[nid][0], positions[nid][1],
                   label, pk, fill, highlight=hl, deleted=is_del, font=font)

    png_path = os.path.join(OUTPUT_DIR, f"frame_{step_num:03d}.png")
    img.save(png_path)
    print(f"  [{step_num:3d}] {title:55s} → frame_{step_num:03d}.png")


# ── operation functions ──────────────────────────────────────────────
# Pattern: PRE (build base state) → OP (execute operation) → RESULT
# Each scenario gets a fresh MockGraph, so ops must build state from scratch.

def _op_insert_lloc_padro(graph: MockGraph) -> dict:
    """Step 1: Insert a LlocPadro node."""
    # PRE: insert node
    node = LlocPadro(pk={"nom": "Caldes dEstrac", "any": 1905})
    graph.insertNode(node, replace=True)
    return {"highlight_new": {node.neo4j_id}}


def _op_update_lloc_padro(graph: MockGraph) -> dict:
    """Step 2: Update the LlocPadro node (replace)."""
    # PRE: insert node (same PK, triggers update)
    node = LlocPadro(pk={"nom": "Caldes dEstrac", "any": 1905})
    graph.insertNode(node, replace=True)
    return {"highlight_new": set()}


def _op_insert_individu(graph: MockGraph) -> dict:
    """Step 3: Insert an IndividuPadro with dependencies."""
    # PRE: insert IndividuPadro (auto-creates Valor nodes + edges)
    ind = IndividuPadro(pk=1, nom="Oriol", cognom1="Ramos", cognom2="Perez")
    graph.insertNode(ind, replace=True)
    return {"highlight_new": {1, 2, 3, 4}}


def _op_delete_individu(graph: MockGraph) -> dict:
    """Step 4: Delete the IndividuPadro (cascade)."""
    # PRE: insert full state
    ind = IndividuPadro(pk=1, nom="Oriol", cognom1="Ramos", cognom2="Perez")
    graph.insertNode(ind, replace=True)
    # OP: delete with cascade
    graph.deleteNode(ind, detach=True)
    return {"deleted_nodes": {1}, "deleted_edges": {(1, 2), (1, 3), (1, 4)}}


def _op_delete_orphan_valors(graph: MockGraph) -> dict:
    """Step 5: Delete orphan Valor nodes."""
    # PRE: insert full state, delete individu (cascade leaves orphan Valors)
    ind = IndividuPadro(pk=1, nom="Oriol", cognom1="Ramos", cognom2="Perez")
    graph.insertNode(ind, replace=True)
    graph.deleteNode(ind, detach=True)
    # OP: delete remaining Valor nodes
    for nid in list(graph.get_nodes()):
        attrs = graph.get_node_attrs(nid)
        if attrs and attrs.get("main_label") == "Valor":
            graph.deleteNode(Node(neo4j_id=nid), detach=False)
    return {"deleted_nodes": {2, 3, 4}, "deleted_edges": set()}


def _op_insert_individu_ramos(graph: MockGraph) -> dict:
    """Step 6: Insert first IndividuPadro (Oriol Ramos)."""
    # PRE: insert IndividuPadro with Valor dependencies
    ind = IndividuPadro(pk=1, nom="Oriol", cognom1="Ramos")
    graph.insertNode(ind, replace=True)
    return {"highlight_new": {1, 3, 4}}


def _op_insert_individu_fuster(graph: MockGraph) -> dict:
    """Step 7: Insert second IndividuPadro (Oriol Fuster), sharing 'Oriol' Valor."""
    # PRE: insert second IndividuPadro (shares Valor node 3)
    ind = IndividuPadro(pk=2, nom="Oriol", cognom1="Fuster")
    graph.insertNode(ind, replace=True)
    return {"highlight_new": {2, 5}}


def _op_insert_test_nodes(graph: MockGraph) -> dict:
    """Step 8: Insert two TestNodes."""
    # PRE: insert two nodes
    a = Node(pk={"nom": "NodeA"}, main_label="TestNode")
    b = Node(pk={"nom": "NodeB"}, main_label="TestNode")
    graph.insertNode(a, replace=True)
    graph.insertNode(b, replace=True)
    return {"highlight_new": {1, 2}}


def _op_insert_connects(graph: MockGraph) -> dict:
    """Step 9: Create CONNECTS relation (insert nodes + relation)."""
    # PRE: insert nodes
    a = Node(pk={"nom": "NodeA"}, main_label="TestNode")
    b = Node(pk={"nom": "NodeB"}, main_label="TestNode")
    graph.insertNode(a, replace=True)
    graph.insertNode(b, replace=True)
    # OP: create relation
    graph.insertRelation(Relation(a, b, "CONNECTS"))
    return {"highlight_new": set()}


def _op_fk_violation(graph: MockGraph) -> dict:
    """Step 10: Show FK violation scenario (graph unchanged from step 9)."""
    # No-op: graph already has state from step 9
    return {"highlight_new": set()}


def _op_insert_link_a_b(graph: MockGraph) -> dict:
    """Step 11: Insert two nodes and a LINKS relation."""
    # PRE: insert nodes
    a = Node(pk={"id": 1}, main_label="TestNode")
    b = Node(pk={"id": 2}, main_label="TestNode")
    graph.insertNode(a, replace=True)
    graph.insertNode(b, replace=True)
    # OP: create relation
    graph.insertRelation(Relation(a, b, "LINKS"))
    return {"highlight_new": {1, 2}}


def _op_delete_a_restrict(graph: MockGraph) -> dict:
    """Step 12: Try to delete A without detach (RESTRICT)."""
    # PRE: insert full state
    a = Node(pk={"id": 1}, main_label="TestNode")
    b = Node(pk={"id": 2}, main_label="TestNode")
    graph.insertNode(a, replace=True)
    graph.insertNode(b, replace=True)
    graph.insertRelation(Relation(a, b, "LINKS"))
    # OP: try delete (will fail with RuntimeError)
    try:
        graph.deleteNode(a, detach=False)
    except RuntimeError:
        pass
    return {"highlight_new": set()}


def _op_delete_a_cascade(graph: MockGraph) -> dict:
    """Step 13: Delete A with cascade."""
    # PRE: insert full state
    a = Node(pk={"id": 1}, main_label="TestNode")
    b = Node(pk={"id": 2}, main_label="TestNode")
    graph.insertNode(a, replace=True)
    graph.insertNode(b, replace=True)
    graph.insertRelation(Relation(a, b, "LINKS"))
    # OP: delete A with cascade
    graph.deleteNode(a, detach=True)
    return {"deleted_nodes": {1}, "deleted_edges": {(1, 2)}}


def _op_insert_chain(graph: MockGraph) -> dict:
    """Step 14: Insert A→B→C chain."""
    # PRE: insert nodes and relations
    a = Node(pk={"id": 1}, main_label="TestNode")
    b = Node(pk={"id": 2}, main_label="TestNode")
    c = Node(pk={"id": 3}, main_label="TestNode")
    graph.insertNode(a, replace=True)
    graph.insertNode(b, replace=True)
    graph.insertNode(c, replace=True)
    graph.insertRelation(Relation(a, b, "LINKS"))
    graph.insertRelation(Relation(b, c, "LINKS"))
    return {"highlight_new": {1, 2, 3}}


def _op_delete_a_chain(graph: MockGraph) -> dict:
    """Step 15: Delete A from the chain."""
    # PRE: insert full chain
    a = Node(pk={"id": 1}, main_label="TestNode")
    b = Node(pk={"id": 2}, main_label="TestNode")
    c = Node(pk={"id": 3}, main_label="TestNode")
    graph.insertNode(a, replace=True)
    graph.insertNode(b, replace=True)
    graph.insertNode(c, replace=True)
    graph.insertRelation(Relation(a, b, "LINKS"))
    graph.insertRelation(Relation(b, c, "LINKS"))
    # OP: delete A
    graph.deleteNode(a, detach=True)
    return {"deleted_nodes": {1}, "deleted_edges": {(1, 2)}}


def _op_insert_multi_edges(graph: MockGraph) -> dict:
    """Step 16: Insert A with two outgoing edges."""
    # PRE: insert nodes and relations
    a = Node(pk={"id": 1}, main_label="TestNode")
    b = Node(pk={"id": 2}, main_label="TestNode")
    c = Node(pk={"id": 3}, main_label="TestNode")
    graph.insertNode(a, replace=True)
    graph.insertNode(b, replace=True)
    graph.insertNode(c, replace=True)
    graph.insertRelation(Relation(a, b, "LINKS"))
    graph.insertRelation(Relation(a, c, "LINKS"))
    return {"highlight_new": {1, 2, 3}}


def _op_delete_a_multi(graph: MockGraph) -> dict:
    """Step 17: Delete A with multiple outgoing edges."""
    # PRE: insert full state
    a = Node(pk={"id": 1}, main_label="TestNode")
    b = Node(pk={"id": 2}, main_label="TestNode")
    c = Node(pk={"id": 3}, main_label="TestNode")
    graph.insertNode(a, replace=True)
    graph.insertNode(b, replace=True)
    graph.insertNode(c, replace=True)
    graph.insertRelation(Relation(a, b, "LINKS"))
    graph.insertRelation(Relation(a, c, "LINKS"))
    # OP: delete A
    graph.deleteNode(a, detach=True)
    return {"deleted_nodes": {1}, "deleted_edges": {(1, 2), (1, 3)}}


def _op_insert_set_null(graph: MockGraph) -> dict:
    """Step 18: Insert nodes for SET NULL test."""
    # PRE: insert nodes and relations
    a = Node(pk={"id": 1}, main_label="TestNode")
    b = Node(pk={"id": 2}, main_label="TestNode")
    c = Node(pk={"id": 3}, main_label="TestNode")
    graph.insertNode(a, replace=True)
    graph.insertNode(b, replace=True)
    graph.insertNode(c, replace=True)
    graph.insertRelation(Relation(a, b, "LINKS"))
    graph.insertRelation(Relation(a, c, "LINKS"))
    return {"highlight_new": {1, 2, 3}}


def _op_delete_set_null(graph: MockGraph) -> dict:
    """Step 19: Delete A with SET NULL."""
    # PRE: insert full state
    a = Node(pk={"id": 1}, main_label="TestNode")
    b = Node(pk={"id": 2}, main_label="TestNode")
    c = Node(pk={"id": 3}, main_label="TestNode")
    graph.insertNode(a, replace=True)
    graph.insertNode(b, replace=True)
    graph.insertNode(c, replace=True)
    graph.insertRelation(Relation(a, b, "LINKS"))
    graph.insertRelation(Relation(a, c, "LINKS"))
    # OP: delete A with set_null
    graph.deleteNode(a, detach=True, on_delete="set_null")
    return {"deleted_nodes": {1}, "deleted_edges": {(1, 2), (1, 3)}}


def _op_insert_document(graph: MockGraph) -> dict:
    """Step 20: Insert a Document node."""
    # PRE: insert document
    doc = Node(pk={"id": 1}, main_label="Document")
    graph.insertNode(doc, replace=True)
    return {"highlight_new": {1}}


def _op_insert_weak_child(graph: MockGraph) -> dict:
    """Step 21: Insert first WeakNode child."""
    # PRE: insert parent
    doc = Node(pk={"id": 1}, main_label="Document")
    graph.insertNode(doc, replace=True)
    # OP: insert WeakNode child
    part = WeakNode(doc, pk={"sub_id": 1}, main_label="DocumentPart")
    graph.insertNode(part, insert_parent=True)
    return {"highlight_new": {2}}


def _op_insert_weak_child2(graph: MockGraph) -> dict:
    """Step 22: Insert second WeakNode child."""
    # PRE: insert parent and first child
    doc = Node(pk={"id": 1}, main_label="Document")
    graph.insertNode(doc, replace=True)
    graph.insertNode(WeakNode(doc, pk={"sub_id": 1}, main_label="DocumentPart"), insert_parent=True)
    # OP: insert second child
    part2 = WeakNode(doc, pk={"sub_id": 2}, main_label="DocumentPart")
    graph.insertNode(part2, insert_parent=True)
    return {"highlight_new": {3}}


def _op_insert_nesting_chain(graph: MockGraph) -> dict:
    """Step 23: Insert Document for nesting."""
    # PRE: insert document
    doc = Node(pk={"id": 1}, main_label="Document")
    graph.insertNode(doc, replace=True)
    return {"highlight_new": {1}}


def _op_insert_nesting_section(graph: MockGraph) -> dict:
    """Step 24: Insert Section (WeakNode of Document)."""
    # PRE: insert parent
    doc = Node(pk={"id": 1}, main_label="Document")
    graph.insertNode(doc, replace=True)
    # OP: insert WeakNode child
    sec = WeakNode(doc, pk={"section": 1}, main_label="Section")
    graph.insertNode(sec, insert_parent=True)
    return {"highlight_new": {2}}


def _op_insert_nesting_page(graph: MockGraph) -> dict:
    """Step 25: Insert Page (WeakNode of Section)."""
    # PRE: insert parent chain
    doc = Node(pk={"id": 1}, main_label="Document")
    graph.insertNode(doc, replace=True)
    sec = WeakNode(doc, pk={"section": 1}, main_label="Section")
    graph.insertNode(sec, insert_parent=True)
    # OP: insert grandchild WeakNode
    pg = WeakNode(sec, pk={"page": 1}, main_label="Page")
    graph.insertNode(pg, insert_parent=True)
    return {"highlight_new": {3}}


def _op_delete_nesting_document(graph: MockGraph) -> dict:
    """Step 26: Delete Document from nesting chain."""
    # PRE: insert full nesting chain
    doc = Node(pk={"id": 1}, main_label="Document")
    graph.insertNode(doc, replace=True)
    sec = WeakNode(doc, pk={"section": 1}, main_label="Section")
    graph.insertNode(sec, insert_parent=True)
    pg = WeakNode(sec, pk={"page": 1}, main_label="Page")
    graph.insertNode(pg, insert_parent=True)
    # OP: delete Document (cascade removes outgoing edges)
    graph.deleteNode(doc, detach=True)
    return {"deleted_nodes": {1}, "deleted_edges": {(1, 2)}}


def _op_insert_update_test(graph: MockGraph) -> dict:
    """Step 27: Insert A→B for UPDATE/REPLACE test."""
    # PRE: insert nodes and relation
    a = Node(pk={"id": 1}, main_label="TestNode")
    b = Node(pk={"id": 2}, main_label="TestNode")
    graph.insertNode(a, replace=True)
    graph.insertNode(b, replace=True)
    graph.insertRelation(Relation(a, b, "LINKS"))
    return {"highlight_new": {1, 2}}


def _op_update_a(graph: MockGraph) -> dict:
    """Step 28: Update A (not replace)."""
    # PRE: insert full state
    a = Node(pk={"id": 1}, main_label="TestNode")
    b = Node(pk={"id": 2}, main_label="TestNode")
    graph.insertNode(a, replace=True)
    graph.insertNode(b, replace=True)
    graph.insertRelation(Relation(a, b, "LINKS"))
    # OP: update A in place (same ID, new attributes)
    a = Node(pk={"id": 1}, main_label="TestNode", nom="nou_nom")
    graph.insertNode(a, update=True)
    return {"highlight_new": set()}


def _op_replace_a(graph: MockGraph) -> dict:
    """Step 29: Replace A (creates new ID, loses edge)."""
    # PRE: insert full state
    a = Node(pk={"id": 1}, main_label="TestNode")
    b = Node(pk={"id": 2}, main_label="TestNode")
    graph.insertNode(a, replace=True)
    graph.insertNode(b, replace=True)
    graph.insertRelation(Relation(a, b, "LINKS"))
    # OP: replace A (delete old + create new with same PK but different ID)
    a = Node(pk={"id": 1}, main_label="TestNode", nom="nou_nom")
    graph.insertNode(a, replace=True)
    return {"deleted_nodes": {1}, "deleted_edges": {(1, 2)}}


def _op_insert_doc_doc(graph: MockGraph) -> dict:
    """Step 30: Insert Document DOC-001."""
    # PRE: insert document
    doc = Node(pk={"doc": "DOC-001"}, main_label="Document")
    graph.insertNode(doc, replace=True)
    return {"highlight_new": {1}}


def _op_insert_pages(graph: MockGraph) -> dict:
    """Step 31: Insert Page 1 and Page 2."""
    # PRE: insert parent
    doc = Node(pk={"doc": "DOC-001"}, main_label="Document")
    graph.insertNode(doc, replace=True)
    # OP: insert WeakNode children
    p1 = WeakNode(doc, pk={"page": 1}, main_label="Page")
    graph.insertNode(p1, insert_parent=True)
    p2 = WeakNode(doc, pk={"page": 2}, main_label="Page")
    graph.insertNode(p2, insert_parent=True)
    return {"highlight_new": {2, 3}}


def _op_delete_page1(graph: MockGraph) -> dict:
    """Step 32: Delete Page 1."""
    # PRE: insert full state
    doc = Node(pk={"doc": "DOC-001"}, main_label="Document")
    graph.insertNode(doc, replace=True)
    p1 = WeakNode(doc, pk={"page": 1}, main_label="Page")
    graph.insertNode(p1, insert_parent=True)
    p2 = WeakNode(doc, pk={"page": 2}, main_label="Page")
    graph.insertNode(p2, insert_parent=True)
    # OP: delete Page 1
    graph.deleteNode(p1, detach=True)
    return {"deleted_nodes": {2}, "deleted_edges": {(1, 2)}}


# ── scenario definitions ─────────────────────────────────────────────

SCENARIOS = [
    # 1. NODE CRUD
    {
        "title": "Node A inserit",
        "step": 1,
        "positions": {1: (500, 400)},
        "nodes": [(1, "LlocPadro", "{'nom': 'Caldes dEstrac', 'any': 1905}")],
        "edges": [],
        "op": _op_insert_lloc_padro,
        "explanation": "Codi:\n  node = LlocPadro(pk={'nom': 'Caldes dEstrac', 'any': 1905})\n\n"
                       "Es crea un node LlocPadro amb PK composta per 'nom' i 'any'.",
    },
    {
        "title": "Node B actualitza A (mateix ID)",
        "step": 2,
        "positions": {1: (500, 400)},
        "nodes": [(1, "LlocPadro", "{'nom': 'Caldes dEstrac', 'any': 1905}")],
        "edges": [],
        "op": _op_update_lloc_padro,
        "explanation": "Codi:\n  node = LlocPadro(pk={'nom': 'Caldes dEstrac', 'any': 1905})\n\n"
                       "S'intenta inserir un node amb la mateixa PK. "
                       "Com que ja existeix, es fa UPDATE: esborra i recrea amb nous atributs.",
    },

    # 2. INDIVIDUADRO amb dependencies
    {
        "title": "IndividuPadro inserit: nom=Oriol, cognom1=Ramos, cognom2=Perez",
        "step": 3,
        "positions": {
            1: (250, 400), 2: (650, 250), 3: (650, 400), 4: (650, 550),
        },
        "nodes": [
            (1, "IndividuPadro", "{'id': 1}"),
            (2, "Valor", "{'name': 'Oriol'}"),
            (3, "Valor", "{'name': 'Ramos'}"),
            (4, "Valor", "{'name': 'Perez'}"),
        ],
        "edges": [
            (1, 2, "HAS_NOM"), (1, 3, "HAS_COGNOM1"), (1, 4, "HAS_COGNOM2"),
        ],
        "op": _op_insert_individu,
        "explanation": "Codi:\n  ind = IndividuPadro(pk=1, nom='Oriol', cognom1='Ramos', cognom2='Perez')\n\n"
                       "IndividuPadro té be_value_properties = ('nom', 'cognom1', 'cognom2').\n"
                       "MockGraph equival a Neo4jGraph: AUTOMÀTICAMENT es generen:\n"
                       "  - 1 node Valor per cada propietat string\n"
                       "  - 1 aresta HAS_NOM / HAS_COGNOM1 / HAS_COGNOM2 per connectar-los\n"
                       "Tot es crea en un sol pas: node + Valor nodes + arestes.",
    },
    {
        "title": "Esborrar IndividuPadro Oriol Ramos Perez",
        "step": 4,
        "positions": {
            1: (250, 400), 2: (650, 250), 3: (650, 400), 4: (650, 550),
        },
        "nodes": [
            (1, "IndividuPadro", "{'id': 1}"),
            (2, "Valor", "{'name': 'Oriol'}"),
            (3, "Valor", "{'name': 'Ramos'}"),
            (4, "Valor", "{'name': 'Perez'}"),
        ],
        "edges": [
            (1, 2, "HAS_NOM"), (1, 3, "HAS_COGNOM1"), (1, 4, "HAS_COGNOM2"),
        ],
        "op": _op_delete_individu,
        "explanation": "Codi:\n  ind.delete(on_delete='cascade')\n\n"
                       "1. Es marca l'IndividuPadro com a ELIMINAT\n"
                       "2. Es marquen les arestes sortint com a ELIMINADES\n"
                       "3. S'esborra l'IndividuPadro i les seves arestes\n"
                       "4. Els nodes Valor queden al graf però sense arestes connectades",
    },
    {
        "title": "Esborrar nodes Valor orfes (sense arestes)",
        "step": 5,
        "positions": {
            1: (250, 400), 2: (650, 250), 3: (650, 400), 4: (650, 550),
        },
        "nodes": [],
        "edges": [],
        "op": _op_delete_orphan_valors,
        "explanation": "Els nodes Valor no tenen cap aresta sortint → cascade només "
                       "esborra les arestes entrant.\n"
                       "Els nodes Valor queden orfes al graf.\n"
                       "Nota: si un Valor està connectat a un altre IndividuPadro "
                       "(veure escenari 3), NO s'esborra.",
    },

    # 3. Atributs compartits
    {
        "title": "Oriol Ramos → 'Oriol', 'Ramos', 'Perez'",
        "step": 6,
        "positions": {
            1: (150, 450), 2: (150, 250), 3: (600, 450), 4: (600, 300), 5: (600, 150),
        },
        "nodes": [
            (1, "IndividuPadro", "{'id': 1}"),
            (2, "IndividuPadro", "{'id': 2}"),
            (3, "Valor", "{'name': 'Oriol'}"),
            (4, "Valor", "{'name': 'Ramos'}"),
            (5, "Valor", "{'name': 'Fuster'}"),
        ],
        "edges": [
            (1, 3, "HAS_NOM"), (1, 4, "HAS_COGNOM1"),
        ],
        "op": _op_insert_individu_ramos,
        "explanation": "Codi:\n  ind1 = IndividuPadro(pk=1, nom='Oriol', cognom1='Ramos')\n"
                       "  ind2 = IndividuPadro(pk=2, nom='Oriol', cognom1='Fuster')\n\n"
                       "IndividuPadro utilitza be_value() per crear nodes Valor.\n"
                       "Si el mateix valor ja existeix, es reutilitza (no es duplica).",
    },
    {
        "title": "Oriol Fuster → 'Oriol', 'Fuster', 'Perez'",
        "step": 7,
        "positions": {
            1: (150, 450), 2: (150, 250), 3: (600, 450), 4: (600, 300), 5: (600, 150),
        },
        "nodes": [
            (1, "IndividuPadro", "{'id': 1}"),
            (2, "IndividuPadro", "{'id': 2}"),
            (3, "Valor", "{'name': 'Oriol'}"),
            (4, "Valor", "{'name': 'Ramos'}"),
            (5, "Valor", "{'name': 'Fuster'}"),
        ],
        "edges": [
            (1, 3, "HAS_NOM"), (1, 4, "HAS_COGNOM1"),
            (2, 3, "HAS_NOM"), (2, 5, "HAS_COGNOM1"),
        ],
        "op": _op_insert_individu_fuster,
        "explanation": "El node Valor {'name': 'Oriol'} ja existeix → es reutilitza.\n"
                       "Oriol Ramos i Oriol Fuster comparteixen el node Valor 'Oriol'.\n"
                       "Cada IndividuPadro té les seves pròpies arestes HAS_NOM/HAS_COGNOM.",
    },

    # 4. RELACIONS FK validation
    {
        "title": "NodeA i NodeB inserits",
        "step": 8,
        "positions": {1: (250, 400), 2: (750, 400)},
        "nodes": [
            (1, "TestNode", "{'nom': 'NodeA'}"),
            (2, "TestNode", "{'nom': 'NodeB'}"),
        ],
        "edges": [],
        "op": _op_insert_test_nodes,
        "explanation": "Codi:\n  a = TestNode(pk={'nom': 'NodeA'})\n"
                       "  b = TestNode(pk={'nom': 'NodeB'})\n\n"
                       "S'intenta crear una relació: a.connects_to(b)",
    },
    {
        "title": "Relació CONNECTS: A → B",
        "step": 9,
        "positions": {1: (250, 400), 2: (750, 400)},
        "nodes": [
            (1, "TestNode", "{'nom': 'NodeA'}"),
            (2, "TestNode", "{'nom': 'NodeB'}"),
        ],
        "edges": [(1, 2, "CONNECTS")],
        "op": _op_insert_connects,
        "explanation": "La clau forana es valida: NodeA existeix al graf.\n"
                       "L'aresta CONNECTS es crea correctament.",
    },
    {
        "title": "FK VIOLATION: src Missing no es pot inserir",
        "step": 10,
        "positions": {1: (250, 400), 2: (750, 400)},
        "nodes": [
            (1, "TestNode", "{'nom': 'NodeA'}"),
            (2, "TestNode", "{'nom': 'NodeB'}"),
        ],
        "edges": [(1, 2, "CONNECTS")],
        "op": lambda g: {"highlight_new": set()},  # No-op, graph already has state
        "explanation": "Codi:\n  missing = TestNode(pk={'nom': 'Missing'})\n"
                       "  missing.connects_to(b)\n\n"
                       "Error! Missing no existeix al graf → FK violation.\n"
                       "No es poden crear nodes que depenen d'altres que no existeixen.",
    },

    # 5. ON DELETE RESTRICT
    {
        "title": "A→B creat amb LINKS",
        "step": 11,
        "positions": {1: (250, 400), 2: (750, 400)},
        "nodes": [
            (1, "TestNode", "{'id': 1}"),
            (2, "TestNode", "{'id': 2}"),
        ],
        "edges": [(1, 2, "LINKS")],
        "op": _op_insert_link_a_b,
        "explanation": "Codi:\n  a = TestNode(pk={'id': 1})\n"
                       "  b = TestNode(pk={'id': 2})\n"
                       "  a.connects_to(b)\n\n"
                       "S'intenta esborrar A: a.delete()",
    },
    {
        "title": "RESTRICT: A no s'esborra (té arestes sortint)",
        "step": 12,
        "positions": {1: (250, 400), 2: (750, 400)},
        "nodes": [
            (1, "TestNode", "{'id': 1}"),
            (2, "TestNode", "{'id': 2}"),
        ],
        "edges": [(1, 2, "LINKS")],
        "op": _op_delete_a_restrict,
        "explanation": "Error! A té arestes sortint → RESTRICT.\n"
                       "No es pot esborrar un node que té relacions actives.",
    },
    {
        "title": "CASCADE: A esborrat + totes les seves arestes",
        "step": 13,
        "positions": {1: (250, 400), 2: (750, 400)},
        "nodes": [
            (2, "TestNode", "{'id': 2}"),
        ],
        "edges": [],
        "op": _op_delete_a_cascade,
        "explanation": "Codi:\n  a.delete(on_delete='cascade')\n\n"
                       "1. Es marca A com a ELIMINAT (X vermella)\n"
                       "2. Es marquen les arestes SORTINT d'A com a ELIMINADES\n"
                       "3. S'esborra A i les seves arestes del graf\n"
                       "4. B queda al graf però sense arestes",
    },

    # 6. ON DELETE CASCADE en cadena
    {
        "title": "Cadena A→B→C",
        "step": 14,
        "positions": {1: (150, 400), 2: (500, 400), 3: (850, 400)},
        "nodes": [
            (1, "TestNode", "{'id': 1}"),
            (2, "TestNode", "{'id': 2}"),
            (3, "TestNode", "{'id': 3}"),
        ],
        "edges": [(1, 2, "LINKS"), (2, 3, "LINKS")],
        "op": _op_insert_chain,
        "explanation": "Codi:\n  a.connects_to(b)\n  b.connects_to(c)\n\n"
                       "Cadena de dependències: A → B → C",
    },
    {
        "title": "Esborrar A: només A→B desapareix, B→C sobreviu",
        "step": 15,
        "positions": {1: (150, 400), 2: (500, 400), 3: (850, 400)},
        "nodes": [
            (2, "TestNode", "{'id': 2}"),
            (3, "TestNode", "{'id': 3}"),
        ],
        "edges": [(2, 3, "LINKS")],
        "op": _op_delete_a_chain,
        "explanation": "a.delete(on_delete='cascade')\n\n"
                       "1. Es marca A com a ELIMINAT\n"
                       "2. Es marca l'aresta A→B com a ELIMINADA\n"
                       "3. S'esborra A i l'aresta A→B\n"
                       "4. B→C sobreviu perquè no depèn d'A",
    },

    # 7. ON DELETE CASCADE múltiples
    {
        "title": "A→B i A→C",
        "step": 16,
        "positions": {1: (150, 400), 2: (700, 550), 3: (700, 250)},
        "nodes": [
            (1, "TestNode", "{'id': 1}"),
            (2, "TestNode", "{'id': 2}"),
            (3, "TestNode", "{'id': 3}"),
        ],
        "edges": [(1, 2, "LINKS"), (1, 3, "LINKS")],
        "op": _op_insert_multi_edges,
        "explanation": "A té dues arestes sortint: A→B i A→C",
    },
    {
        "title": "Esborrar A: B i C queden independents",
        "step": 17,
        "positions": {1: (150, 400), 2: (700, 550), 3: (700, 250)},
        "nodes": [
            (2, "TestNode", "{'id': 2}"),
            (3, "TestNode", "{'id': 3}"),
        ],
        "edges": [],
        "op": _op_delete_a_multi,
        "explanation": "a.delete(on_delete='cascade')\n\n"
                       "1. Es marca A com a ELIMINAT\n"
                       "2. Es marquen totes les arestes SORTINT d'A com a ELIMINADES\n"
                       "3. S'esborra A i ambdues arestes\n"
                       "4. B i C queden al graf com a nodes independents",
    },

    # 8. ON DELETE SET NULL
    {
        "title": "A→B i A→C amb SET NULL",
        "step": 18,
        "positions": {1: (150, 400), 2: (700, 550), 3: (700, 250)},
        "nodes": [
            (1, "TestNode", "{'id': 1}"),
            (2, "TestNode", "{'id': 2}"),
            (3, "TestNode", "{'id': 3}"),
        ],
        "edges": [(1, 2, "LINKS"), (1, 3, "LINKS")],
        "op": _op_insert_set_null,
        "explanation": "Codi:\n  a.delete(on_delete='set_null')\n\n"
                       "Esborra A però manté B i C al graf sense les arestes.",
    },
    {
        "title": "SET NULL: A esborrat, B i C queden sense arestes",
        "step": 19,
        "positions": {1: (150, 400), 2: (700, 550), 3: (700, 250)},
        "nodes": [
            (2, "TestNode", "{'id': 2}"),
            (3, "TestNode", "{'id': 3}"),
        ],
        "edges": [],
        "op": _op_delete_set_null,
        "explanation": "B i C queden al graf però sense cap aresta.\n"
                       "A diferència de CASCADE, SET NULL no propaga l'esborrat.\n"
                       "Només s'esborra el node eliminat i les seves arestes.",
    },

    # 9. WeakNode parent-child
    {
        "title": "Document inserit",
        "step": 20,
        "positions": {1: (250, 500), 2: (750, 400), 3: (750, 200)},
        "nodes": [
            (1, "Document", "{'id': 1}"),
        ],
        "edges": [],
        "op": _op_insert_document,
        "explanation": "Codi:\n  doc = Node(pk={'id': 1}, main_label='Document')\n\n"
                       "Node normal amb PK simple {'id': 1}.",
    },
    {
        "title": "WeakNode inserit: Document HAS DocumentPart",
        "step": 21,
        "positions": {1: (250, 500), 2: (750, 400), 3: (750, 200)},
        "nodes": [
            (1, "Document", "{'id': 1}"),
            (2, "DocumentPart", "{'id': 1, 'sub_id': 1}"),
        ],
        "edges": [(1, 2, "HAS")],
        "op": _op_insert_weak_child,
        "explanation": "Codi:\n  part = WeakNode(parent=doc, pk={'sub_id': 1}, main_label='DocumentPart')\n\n"
                       "WeakNode hereta la PK del parent i la combina:\n"
                       "PK composta = {'id': 1, 'sub_id': 1}",
    },
    {
        "title": "Segon fill: Document HAS 2 parts",
        "step": 22,
        "positions": {1: (250, 500), 2: (750, 400), 3: (750, 200)},
        "nodes": [
            (1, "Document", "{'id': 1}"),
            (2, "DocumentPart", "{'id': 1, 'sub_id': 1}"),
            (3, "DocumentPart", "{'id': 1, 'sub_id': 2}"),
        ],
        "edges": [(1, 2, "HAS"), (1, 3, "HAS")],
        "op": _op_insert_weak_child2,
        "explanation": "Codi:\n  part2 = WeakNode(parent=doc, pk={'sub_id': 2}, main_label='DocumentPart')\n\n"
                       "Cada DocumentPart té una PK composta única:\n"
                       "{'id': 1, 'sub_id': 1} i {'id': 1, 'sub_id': 2}",
    },

    # 10. WeakNode nesting
    {
        "title": "Document inserit",
        "step": 23,
        "positions": {1: (150, 550), 2: (500, 400), 3: (850, 250)},
        "nodes": [
            (1, "Document", "{'id': 1}"),
        ],
        "edges": [],
        "op": _op_insert_nesting_chain,
        "explanation": "Codi:\n  doc = Node(pk={'id': 1}, main_label='Document')\n"
                       "  sec = WeakNode(parent=doc, pk={'section': 1}, main_label='Section')\n"
                       "  pg  = WeakNode(parent=sec, pk={'page': 1}, main_label='Page')\n\n"
                       "Cadena de WeakNode: Document → Section → Page",
    },
    {
        "title": "Section inserida (WeakNode de Document)",
        "step": 24,
        "positions": {1: (150, 550), 2: (500, 400), 3: (850, 250)},
        "nodes": [
            (1, "Document", "{'id': 1}"),
            (2, "Section", "{'id': 1, 'section': 1}"),
        ],
        "edges": [(1, 2, "HAS")],
        "op": _op_insert_nesting_section,
        "explanation": "PK Section = {'id': 1, 'section': 1}\n"
                       "Hereta 'id' del parent Document.",
    },
    {
        "title": "Page inserida (WeakNode de Section)",
        "step": 25,
        "positions": {1: (150, 550), 2: (500, 400), 3: (850, 250)},
        "nodes": [
            (1, "Document", "{'id': 1}"),
            (2, "Section", "{'id': 1, 'section': 1}"),
            (3, "Page", "{'id': 1, 'section': 1, 'page': 1}"),
        ],
        "edges": [(1, 2, "HAS"), (2, 3, "HAS")],
        "op": _op_insert_nesting_page,
        "explanation": "PK Page = {'id': 1, 'section': 1, 'page': 1}\n"
                       "Hereta 'id' de Document i 'section' de Section.\n"
                       "La PK és la unió de TOTES les PK dels avantpassats.",
    },
    {
        "title": "Esborrar Document: cascade elimina arestes entrants i sortint",
        "step": 26,
        "positions": {1: (150, 550), 2: (500, 400), 3: (850, 250)},
        "nodes": [
            (2, "Section", "{'id': 1, 'section': 1}"),
            (3, "Page", "{'id': 1, 'section': 1, 'page': 1}"),
        ],
        "edges": [(2, 3, "HAS")],
        "op": _op_delete_nesting_document,
        "explanation": "doc.delete(on_delete='cascade')\n\n"
                       "1. Es marca Document com a ELIMINAT\n"
                       "2. S'esborra l'aresta SORTINT de Document (Document→Section)\n"
                       "3. També s'esborren les arestes ENTRANTS (si n'hi hagués)\n"
                       "4. Section→Page sobreviu perquè no surt del node eliminat\n"
                       "5. Section i Page queden al graf però orfes (sense parent)",
    },

    # 11. ON UPDATE CASCADE
    {
        "title": "A→B creat",
        "step": 27,
        "positions": {1: (250, 400), 2: (750, 400)},
        "nodes": [
            (1, "TestNode", "{'id': 1}"),
            (2, "TestNode", "{'id': 2}"),
        ],
        "edges": [(1, 2, "LINKS")],
        "op": _op_insert_update_test,
        "explanation": "Codi:\n  a = TestNode(pk={'id': 1})\n"
                       "  b = TestNode(pk={'id': 2})\n"
                       "  a.connects_to(b)",
    },
    {
        "title": "UPDATE A: node actualitzat, arestes es mantenen",
        "step": 28,
        "positions": {1: (250, 400), 2: (750, 400)},
        "nodes": [
            (1, "TestNode", "{'id': 1}"),
            (2, "TestNode", "{'id': 2}"),
        ],
        "edges": [(1, 2, "LINKS")],
        "op": _op_update_a,
        "explanation": "Codi:\n  a.update(nom='nou_nom')\n\n"
                       "UPDATE modifica el node en el mateix ID.\n"
                       "Les arestes es mantenen intactes.",
    },
    {
        "title": "REPLACE A: node esborrat amb cascade, nova ID",
        "step": 29,
        "positions": {1: (250, 400), 2: (750, 400)},
        "nodes": [
            (2, "TestNode", "{'id': 2}"),
        ],
        "edges": [],
        "op": _op_replace_a,
        "explanation": "Codi:\n  a.replace(nom='nou_nom')\n\n"
                       "1. REPLACE crida deleteNode(detach=True, propagation=True)\n"
                       "2. Es marca A com a ELIMINAT\n"
                       "3. Es marca l'aresta A→B com a ELIMINADA\n"
                       "4. REPLACE esborra A i crea un node nou amb ID diferent\n"
                       "5. L'aresta original apunta a l'ID antic → es perd",
    },

    # 12. WeakNode PK compostes integritat
    {
        "title": "Document DOC-001 inserit",
        "step": 30,
        "positions": {1: (250, 500), 2: (750, 400), 3: (750, 200)},
        "nodes": [
            (1, "Document", "{'doc': 'DOC-001'}"),
        ],
        "edges": [],
        "op": _op_insert_doc_doc,
        "explanation": "Codi:\n  doc = Node(pk={'doc': 'DOC-001'}, main_label='Document')\n"
                       "  p1 = WeakNode(parent=doc, pk={'page': 1}, main_label='Page')\n"
                       "  p2 = WeakNode(parent=doc, pk={'page': 2}, main_label='Page')\n\n"
                       "Cada Page hereta 'doc' del parent Document.",
    },
    {
        "title": "Page 1 i Page 2 inserides (PK: doc+page)",
        "step": 31,
        "positions": {1: (250, 500), 2: (750, 400), 3: (750, 200)},
        "nodes": [
            (1, "Document", "{'doc': 'DOC-001'}"),
            (2, "Page", "{'doc': 'DOC-001', 'page': 1}"),
            (3, "Page", "{'doc': 'DOC-001', 'page': 2}"),
        ],
        "edges": [(1, 2, "HAS"), (1, 3, "HAS")],
        "op": _op_insert_pages,
        "explanation": "PK Page 1 = {'doc': 'DOC-001', 'page': 1}\n"
                       "PK Page 2 = {'doc': 'DOC-001', 'page': 2}\n"
                       "Les PK compostes garanteixen unicitat.",
    },
    {
        "title": "Esborrar Page 1: Page 2 sobreviu",
        "step": 32,
        "positions": {1: (250, 500), 2: (750, 400), 3: (750, 200)},
        "nodes": [
            (1, "Document", "{'doc': 'DOC-001'}"),
            (3, "Page", "{'doc': 'DOC-001', 'page': 2}"),
        ],
        "edges": [(1, 3, "HAS")],
        "op": _op_delete_page1,
        "explanation": "p1.delete(on_delete='cascade')\n\n"
                       "1. Es marca Page 1 com a ELIMINAT\n"
                       "2. Es marca l'aresta Document→Page1 com a ELIMINADA\n"
                       "3. S'esborra Page 1 i la seva aresta\n"
                       "4. Page 2 sobreviu perquè és un node independent",
    },
]


def separator(title: str) -> None:
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")


# ── main ─────────────────────────────────────────────────────────────

def main() -> None:
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)

    print("Generant GIF animat del graf")
    print("=" * 70)

    for sc in SCENARIOS:
        separator(sc["title"])

        # Create a fresh graph for each scenario
        graph = MockGraph()

        # Execute the operation (PRE + OP)
        op_result = sc["op"](graph)

        # Read actual graph state
        nodes, edges = _read_graph_state(
            graph, sc["positions"],
            highlight_new=op_result.get("highlight_new"),
            deleted_nodes=op_result.get("deleted_nodes"),
            deleted_edges=op_result.get("deleted_edges"),
        )

        # Render the frame
        _render_frame(
            step_num=sc["step"],
            title=sc["title"],
            graph=graph,
            positions=sc["positions"],
            nodes=nodes,
            edges=edges,
            highlight_new=op_result.get("highlight_new"),
            explanation=sc.get("explanation"),
            deleted_nodes=op_result.get("deleted_nodes"),
            deleted_edges=op_result.get("deleted_edges"),
        )

        graph.close()

    # Generate GIF
    gif_path = os.path.join(OUTPUT_DIR, "animation.gif")
    png_files = sorted([
        os.path.join(OUTPUT_DIR, f"frame_{i:03d}.png")
        for i in range(1, 33)
    ])

    print(f"\nGenerant GIF: {gif_path}")
    images = [Image.open(f) for f in png_files]
    images[0].save(
        gif_path,
        save_all=True,
        append_images=images[1:],
        duration=1000 // FPS,
        loop=0,
        optimize=True,
    )

    gif_size = os.path.getsize(gif_path)
    print(f"  GIF generat: {gif_size / 1024:.0f} KB ({len(png_files)} frames, {FPS} FPS)")

    # Clean up PNG frames
    for f in png_files:
        os.remove(f)
    print(f"  Frames PNG eliminats")

    print(f"\n{'='*70}")
    print(f"  Visualització completada! animation.gif")
    print(f"{'='*70}")
    print(f"\nFitxers a {OUTPUT_DIR}/")
    print()


if __name__ == "__main__":
    main()
