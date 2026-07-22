"""Script interactiu per visualitzar el comportament de NetworkXGraph pas a pas.

Executa:
    python test/visualize_mock_graph.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cvcdocdb.networkx_graph import NetworkXGraph
from cvcdocdb.base import Node, Relation
from cvcdocdb.drm_entities import IndividuPadro, LlocPadro


def separator(title: str) -> None:
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")


def main() -> None:
    print("Visualització del comportament de NetworkXGraph (NetworkX)")
    print("=" * 70)

    # ===================================================================
    # 1. Node CRUD — inserció i actualització
    # ===================================================================
    separator("1. NODE CRUD: inserció i actualització amb pk compost")

    graph = NetworkXGraph()

    a = Node(
        pk={"nom": "Caldes dEstrac", "any": 1905},
        main_label="LlocPadro",
        estat="inserit",
    )
    id_a = graph.insertNode(a, replace=True)
    print(f"  Node A creat amb ID: {id_a}")
    print(f"  {graph.debug()}")

    b = Node(
        pk={"nom": "Caldes dEstrac", "any": 1905},
        main_label="LlocPadro",
        estat="actualitzat",
    )
    id_b = graph.insertNode(b, replace=False, update=True)
    print(f"  Node B actualitzat amb ID: {id_b} (mateix que A? {id_a == id_b})")
    print(f"  {graph.debug()}")

    graph.close()

    # ===================================================================
    # 2. IndividuPadro — inserció múltiple
    # ===================================================================
    separator("2. INDIVIDUPADRO: inserció de 3 nodes individuals")

    graph = NetworkXGraph()

    a = IndividuPadro(pk=1, nom="Oriol", cognom1="Ramos", edat=18, alternative_labels="TEST")
    b = IndividuPadro(pk=2, nom="Sergio", cognom1="Ramos", ofici="fuster", alternative_labels="TEST")
    c = IndividuPadro(pk=3, nom="Pere", cognom1="Fuster", edat="50", alternative_labels="TEST")

    id_a = graph.insertNode(a, replace=True)
    id_b = graph.insertNode(b, replace=False, update=True)
    id_c = graph.insertNode(c, replace=False, update=False)

    print(f"  Oriol:   ID={id_a}")
    print(f"  Sergio:  ID={id_b}")
    print(f"  Pere:    ID={id_c}")
    print(f"  Total nodes: {len(graph.get_nodes())}")
    print(f"  {graph.debug()}")

    graph.close()

    # ===================================================================
    # 3. Relacions — creació i validació FK
    # ===================================================================
    separator("3. RELACIONS: creació amb validació FK")

    graph = NetworkXGraph()

    src = Node(pk={"nom": "NodeA"}, main_label="LlocPadro")
    dst = Node(pk={"nom": "NodeB"}, main_label="LlocPadro")

    graph.insertNode(src, replace=True)
    graph.insertNode(dst, replace=True)
    print(f"  Nodes inserits: {sorted(graph.get_nodes())}")
    print(f"  {graph.debug()}")

    rel = Relation(src, dst, "CONNECTS")
    graph.insertRelation(rel)
    print(f"  Relació CONNECTS creada")
    print(f"  {graph.debug()}")

    # FK violation — src no inserit
    print("\n  --- FK VIOLATION: src no inserit ---")
    bad_src = Node(pk={"nom": "Missing"}, main_label="LlocPadro")
    rel_bad = Relation(bad_src, dst, "CONNECTS")
    try:
        graph.insertRelation(rel_bad)
    except RuntimeError as e:
        print(f"  ERROR: {e}")

    graph.close()

    # ===================================================================
    # 4. ON DELETE RESTRICT
    # ===================================================================
    separator("4. ON DELETE RESTRICT: no es pot esborrar node amb arestes")

    graph = NetworkXGraph()

    node_a = Node(pk={"id": 1}, main_label="TestNode")
    node_b = Node(pk={"id": 2}, main_label="TestNode")
    graph.insertNode(node_a, replace=True)
    graph.insertNode(node_b, replace=True)
    graph.insertRelation(Relation(node_a, node_b, "LINKS"))

    print(f"  Abans d'esborrar: {len(graph.get_nodes())} nodes, {len(graph.get_edges())} arestes")
    print(f"  {graph.debug()}")

    try:
        graph.deleteNode(node_a, detach=False)
    except RuntimeError as e:
        print(f"  ERROR RESTRICT: {e}")
    print(f"  Després de RESTRICT: {len(graph.get_nodes())} nodes, {len(graph.get_edges())} arestes")

    graph.close()

    # ===================================================================
    # 5. ON DELETE CASCADE
    # ===================================================================
    separator("5. ON DELETE CASCADE: esborrar node elimina les arestes")

    graph = NetworkXGraph()

    a = Node(pk={"id": 1}, main_label="TestNode")
    b = Node(pk={"id": 2}, main_label="TestNode")
    c = Node(pk={"id": 3}, main_label="TestNode")
    graph.insertNode(a, replace=True)
    graph.insertNode(b, replace=True)
    graph.insertNode(c, replace=True)
    graph.insertRelation(Relation(a, b, "LINKS"))
    graph.insertRelation(Relation(b, c, "LINKS"))

    print(f"  Abans: {len(graph.get_nodes())} nodes, {len(graph.get_edges())} arestes")
    print(f"  {graph.debug()}")

    graph.deleteNode(a, detach=True)
    print(f"  Després d'esborrar A (cascade): {len(graph.get_nodes())} nodes, {len(graph.get_edges())} arestes")
    print(f"  {graph.debug()}")

    graph.close()

    # ===================================================================
    # 6. ON DELETE CASCADE en cadena
    # ===================================================================
    separator("6. ON DELETE CASCADE: cadena A→B→C, esborrar A")

    graph = NetworkXGraph()

    a = Node(pk={"id": 1}, main_label="TestNode")
    b = Node(pk={"id": 2}, main_label="TestNode")
    c = Node(pk={"id": 3}, main_label="TestNode")
    graph.insertNode(a, replace=True)
    graph.insertNode(b, replace=True)
    graph.insertNode(c, replace=True)
    graph.insertRelation(Relation(a, b, "LINKS"))
    graph.insertRelation(Relation(b, c, "LINKS"))

    print(f"  Abans: {len(graph.get_nodes())} nodes, {len(graph.get_edges())} arestes")
    print(f"  {graph.debug()}")

    graph.deleteNode(a, detach=True)
    print(f"  Després d'esborrar A: {len(graph.get_nodes())} nodes, {len(graph.get_edges())} arestes")
    print(f"  (B→C es manté, només A→B s'elimina)")
    print(f"  {graph.debug()}")

    graph.close()

    # ===================================================================
    # 7. ON DELETE CASCADE amb múltiples arestes
    # ===================================================================
    separator("7. ON DELETE CASCADE: node amb múltiples arestes sortint")

    graph = NetworkXGraph()

    a = Node(pk={"id": 1}, main_label="TestNode")
    b = Node(pk={"id": 2}, main_label="TestNode")
    c = Node(pk={"id": 3}, main_label="TestNode")
    graph.insertNode(a, replace=True)
    graph.insertNode(b, replace=True)
    graph.insertNode(c, replace=True)
    graph.insertRelation(Relation(a, b, "LINKS"))
    graph.insertRelation(Relation(a, c, "LINKS"))

    print(f"  Abans: {len(graph.get_nodes())} nodes, {len(graph.get_edges())} arestes")
    print(f"  {graph.debug()}")

    graph.deleteNode(a, detach=True)
    print(f"  Després d'esborrar A: {len(graph.get_nodes())} nodes, {len(graph.get_edges())} arestes")
    print(f"  (B i C queden com a nodes independents)")
    print(f"  {graph.debug()}")

    graph.close()

    # ===================================================================
    # 8. ON DELETE SET NULL
    # ===================================================================
    separator("8. ON DELETE SET NULL: esborrar node sense cascada als veïns")

    graph = NetworkXGraph()

    a = Node(pk={"id": 1}, main_label="TestNode")
    b = Node(pk={"id": 2}, main_label="TestNode")
    c = Node(pk={"id": 3}, main_label="TestNode")
    graph.insertNode(a, replace=True)
    graph.insertNode(b, replace=True)
    graph.insertNode(c, replace=True)
    graph.insertRelation(Relation(a, b, "LINKS"))
    graph.insertRelation(Relation(a, c, "LINKS"))

    print(f"  Abans: {len(graph.get_nodes())} nodes, {len(graph.get_edges())} arestes")
    print(f"  {graph.debug()}")

    graph.deleteNode(a, detach=True, on_delete="set_null")
    print(f"  Després SET NULL d'A: {len(graph.get_nodes())} nodes, {len(graph.get_edges())} arestes")
    print(f"  (B i C es mantenen, només s'eliminen les arestes)")
    print(f"  {graph.debug()}")

    graph.close()

    # ===================================================================
    # 9. ON DELETE SET NULL sense cascada
    # ===================================================================
    separator("9. ON DELETE SET NULL: cadena A→B→C, esborrar B")

    graph = NetworkXGraph()

    a = Node(pk={"id": 1}, main_label="TestNode")
    b = Node(pk={"id": 2}, main_label="TestNode")
    c = Node(pk={"id": 3}, main_label="TestNode")
    graph.insertNode(a, replace=True)
    graph.insertNode(b, replace=True)
    graph.insertNode(c, replace=True)
    graph.insertRelation(Relation(a, b, "LINKS"))
    graph.insertRelation(Relation(b, c, "LINKS"))

    print(f"  Abans: {len(graph.get_nodes())} nodes, {len(graph.get_edges())} arestes")
    print(f"  {graph.debug()}")

    graph.deleteNode(b, detach=True, on_delete="set_null")
    print(f"  Després SET NULL de B: {len(graph.get_nodes())} nodes, {len(graph.get_edges())} arestes")
    print(f"  (A i C es mantenen, NO hi ha cascada)")
    print(f"  {graph.debug()}")

    graph.close()

    # ===================================================================
    # 10. ON UPDATE CASCADE (update=True)
    # ===================================================================
    separator("10. ON UPDATE CASCADE: update=True manté les arestes")

    graph = NetworkXGraph()

    a = Node(pk={"id": 1}, main_label="TestNode", name="original", count=1)
    b = Node(pk={"id": 2}, main_label="TestNode", name="other")
    graph.insertNode(a, replace=True)
    graph.insertNode(b, replace=True)
    graph.insertRelation(Relation(a, b, "LINKS"))

    print(f"  Abans d'update: {len(graph.get_nodes())} nodes, {len(graph.get_edges())} arestes")
    print(f"  {graph.debug()}")

    a_updated = Node(pk={"id": 1}, main_label="TestNode", name="updated", count=1)
    graph.insertNode(a_updated, update=True)
    print(f"  Després d'update: {len(graph.get_nodes())} nodes, {len(graph.get_edges())} arestes")
    print(f"  (les arestes es mantenen)")
    print(f"  {graph.debug()}")

    graph.close()

    # ===================================================================
    # 11. ON UPDATE CASCADE (replace=True)
    # ===================================================================
    separator("11. ON UPDATE CASCADE: replace=True elimina les arestes")

    graph = NetworkXGraph()

    a = Node(pk={"id": 1}, main_label="TestNode", name="old", count=1)
    b = Node(pk={"id": 2}, main_label="TestNode", name="other")
    graph.insertNode(a, replace=True)
    graph.insertNode(b, replace=True)
    graph.insertRelation(Relation(a, b, "LINKS"))

    print(f"  Abans de replace: {len(graph.get_nodes())} nodes, {len(graph.get_edges())} arestes")
    print(f"  {graph.debug()}")

    a_new = Node(pk={"id": 1}, main_label="TestNode", name="new", count=99)
    graph.insertNode(a_new, replace=True)
    print(f"  Després de replace: {len(graph.get_nodes())} nodes, {len(graph.get_edges())} arestes")
    print(f"  (les arestes s'eliminen, node rep nou ID)")
    print(f"  {graph.debug()}")

    graph.close()

    print(f"\n{'='*70}")
    print("  Visualització completada!")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()
