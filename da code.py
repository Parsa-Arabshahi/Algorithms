import heapq


def load_graph(file):
    graph = {}
    edges = []
    nodes = set()

    with open(file) as f:
        for line in f:

            line = line.strip()

            if not line:
                continue

            a, b, d, t, w, delay = line.split()

            cost = float(d) * float(t) * float(w) + float(delay)

            nodes.add(a)
            nodes.add(b)

            graph.setdefault(a, [])
            graph.setdefault(b, [])

            graph[a].append((b, cost))
            edges.append((a, b, cost))

    return graph, nodes, edges

def has_negative_edge(edges):
    for _, _, cost in edges:
        if cost < 0:
            return True
    return False


def dijkstra(graph, nodes, start):
    dist = {x: float("inf") for x in nodes}
    parent = {x: None for x in nodes}

    dist[start] = 0
    heap = [(0, start)]

    while heap:
        d, u = heapq.heappop(heap)

        if d > dist[u]:
            continue

        for v, cost in graph.get(u, []):

            if dist[v] > d + cost:
                dist[v] = d + cost
                parent[v] = u
                heapq.heappush(heap, (dist[v], v))

    return dist, parent


def bellman_ford(nodes, edges, start):
    dist = {x: float("inf") for x in nodes}
    parent = {x: None for x in nodes}

    dist[start] = 0

    for _ in range(len(nodes) - 1):

        updated = False

        for u, v, cost in edges:

            if dist[u] != float("inf") and dist[v] > dist[u] + cost:
                dist[v] = dist[u] + cost
                parent[v] = u
                updated = True

        if not updated:
            break

    for u, v, cost in edges:
        if dist[u] != float("inf") and dist[v] > dist[u] + cost:
            return None, None, True

    return dist, parent, False


def get_path(parent, start, target):

    if target not in parent:
        return "No Path Found"

    path = []
    cur = target

    while cur is not None:
        path.append(cur)

        if cur == start:
            break

        cur = parent[cur]

    if path[-1] != start:
        return "No Path Found"

    return " -> ".join(reversed(path))


def tsp(graph, nodes, edges, start, targets):

    route = [start]
    current = start
    total = 0

    targets = set(targets)

    use_bellman = has_negative_edge(edges)

    while targets:

        if use_bellman:
            dist, _, cycle = bellman_ford(nodes, edges, current)

            if cycle:
                return None, None

        else:
            dist, _ = dijkstra(graph, nodes, current)

        reachable = [x for x in targets if dist[x] != float("inf")]

        if not reachable:
            return None, None

        nxt = min(reachable, key=lambda x: dist[x])

        total += dist[nxt]
        route.append(nxt)

        current = nxt
        targets.remove(nxt)


    if use_bellman:
        dist, _, cycle = bellman_ford(nodes, edges, current)

        if cycle:
            return None, None

    else:
        dist, _ = dijkstra(graph, nodes, current)

    if dist[start] == float("inf"):
        return None, None

    total += dist[start]
    route.append(start)

    return route, total


graph, nodes, edges = load_graph("map.txt")

mode = input("1-Single Destination\n2-Multiple Destinations\nChoose: ")

negative = has_negative_edge(edges)

if mode == "1":

    start = input("Start node: ")

    if start not in nodes:
        print("Invalid start node")
        exit()

    target = input("Destination node: ")

    if target not in nodes:
        print("Invalid destination node")
        exit()

    if negative:

        dist, parent, cycle = bellman_ford(nodes, edges, start)

        if cycle:
            print("Negative Cycle Found!")
            print("Program stopped.")
        else:
            print("\nBellman-Ford")

            if dist[target] == float("inf"):
                print("No Path Found")
            else:
                print("Path:", get_path(parent, start, target))
                print("Cost:", dist[target])

    else:

        dist, parent = dijkstra(graph, nodes, start)

        print("\nDijkstra")

        if dist[target] == float("inf"):
            print("No Path Found")
        else:
            print("Path:", get_path(parent, start, target))
            print("Cost:", dist[target])

elif mode == "2":

    start = input("Start node: ")

    if start not in nodes:
        print("Invalid start node")
        exit()

    targets = input("Destinations: ").split()
    
    targets = list(dict.fromkeys(targets))
    
    if start in targets:
        targets.remove(start)
        
    if not targets:
        print("No destinations entered.")
        exit()
    
    for t in targets:
        if t not in nodes:
            print("Invalid destination:", t)
            exit()

    if negative:

        _, _, cycle = bellman_ford(nodes, edges, start)

        if cycle:
            print("Negative Cycle Found!")
            print("TSP stopped.")
            exit()

    route, cost = tsp(graph, nodes, edges, start, targets)

    if route is None:
        print("No valid route found.")
    else:
        print("Route:", " -> ".join(route))
        print("Cost:", cost)

else:
    print("Invalid choice")