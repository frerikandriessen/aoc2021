from typing import List, Dict


class Node:
    def __init__(self, name: str) -> None:
        self.name = name
        self.neighbours: List["Node"] = []

    def __repr__(self) -> str:
        return f"{self.name}"


class NodeManager:
    def __init__(self) -> None:
        self.nodes: Dict[str, Node] = {}

    def get_or_create_node(self, node_name: str) -> Node:
        node = self.nodes.get(node_name)
        if node is None:
            node = Node(node_name)
            self.nodes[node_name] = node
        return node

    @staticmethod
    def connect_nodes(node1: Node, node2: Node) -> None:
        node1.neighbours.append(node2)
        node2.neighbours.append(node1)


class PathFinder:
    def __init__(self, data: List[str]) -> None:
        self.paths: List[List[Node]] = []
        self.has_run = False

        nm = NodeManager()
        self.start = None
        for line in data:
            node1_str, node2_str = line.split("-")
            node1 = nm.get_or_create_node(node1_str)
            node2 = nm.get_or_create_node(node2_str)
            nm.connect_nodes(node1, node2)
            if node1.name == "start":
                self.start = node1
            elif node2.name == "start":
                self.start = node2

    def run(self) -> None:
        if self.has_run:
            raise Exception("I have already been run")
        if self.start is None:
            raise Exception("I cannot find a path when the 'start' node is not given")

        self.find_next_step(self.start, [self.start])

        self.has_run = True

    def find_next_step(self, node: Node, path: List[Node]) -> None:
        if node.name == "end":
            self.paths.append(path)
            return

        for neighbour in node.neighbours:
            if neighbour.name.isupper() or path.count(neighbour) == 0:
                new_path = list(path)
                new_path.append(neighbour)
                self.find_next_step(neighbour, new_path)

    @property
    def paths_found(self) -> int:
        return len(self.paths)


class PathFinder2(PathFinder):
    VISITED_TWICE_MARKER = "VISITED_TWICE"

    def find_next_step(self, node: Node, path: List[Node]) -> None:
        if node.name == "end":
            self.paths.append(path)
            return

        for neighbour in node.neighbours:
            if neighbour.name.isupper() or path.count(neighbour) == 0:
                new_path = list(path)
                new_path.append(neighbour)
                self.find_next_step(neighbour, new_path)
            elif path.count(neighbour) == 1 and neighbour.name not in ("end", "start"):
                if path[0].name != self.VISITED_TWICE_MARKER:
                    new_path = [Node(self.VISITED_TWICE_MARKER)] + list(path)
                    new_path.append(neighbour)
                    self.find_next_step(neighbour, new_path)


def q1(data: List[str]) -> int:
    path_finder = PathFinder(data)
    path_finder.run()

    return path_finder.paths_found


def q2(data: List[str]) -> int:
    path_finder = PathFinder2(data)
    path_finder.run()

    return path_finder.paths_found
