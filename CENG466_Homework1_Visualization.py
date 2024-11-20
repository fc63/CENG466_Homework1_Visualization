import subprocess
import sys
import heapq
from collections import deque
try:
    import pygame
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
    import pygame

graph = {
    'A': {'C': 7, 'B': 4},
    'B': {'A': 4, 'C': 2, 'E': 6},
    'C': {'A': 7, 'B': 2, 'D': 3, 'F': 8},
    'D': {'C': 3, 'G': 9},
    'E': {'B': 6, 'F': 5, 'H': 3},
    'F': {'C': 8, 'E': 5, 'G': 1, 'I': 7},
    'G': {'D': 9, 'F': 1, 'J': 6},
    'H': {'E': 3, 'I': 8},
    'I': {'F': 7, 'H': 8, 'J': 4},
    'J': {'G': 6, 'I': 4}
}

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("202011204 CENG 466 – Homework 1 Visualization")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 102, 204)
RED = (204, 0, 0)
GREEN = (0, 204, 0)
YELLOW = (255, 255, 0)
FONT = pygame.font.Font(None, 24)

positions = {
    'A': (400, 100), 'B': (300, 200), 'C': (400, 200), 'D': (500, 200),
    'E': (200, 300), 'F': (400, 300), 'G': (600, 300), 'H': (200, 400),
    'I': (400, 400), 'J': (600, 400)
}

"""
direkt queue mantığı ile keşif yapar ve path belirler. Firts in First Out Algoritması...
en az node'u ziyaret eden path'i bulur. costa bakmaz. path'in node sayısını düşük tutmayı amaçlar
kuyruktaki ilk elemana ilerler. onu da graph değişkenindeki sıralamaya göre alır.
"""
def bfs(graph, start, goal, visited):
    queue = deque([(start, [start], 0)])
    visitedArray = {node: False for node in graph}
    exploration_cost = 0
    steps = []

    while queue:
        (node, path, cost) = queue.popleft()
        if visitedArray[node]:
            continue
        visitedArray[node] = True
        visited.append(node)

        if len(path) > 1:
            exploration_cost += graph[path[-2]][node]

        steps.append((node, path, cost, exploration_cost, visited[:]))

        if node == goal:
            return path, cost, steps

        for neighbor, weight in graph[node].items():
            if not visitedArray[neighbor]:
                queue.append((neighbor, path + [neighbor], cost + weight))

    return None, None, steps

"""
stack veri yapısı mantığı ile hareket eder.
her node'un komşularını LIFO mnatığı ile ziyaret eder.
bu da koddaki graph değişkenindeki sırayla alınır
"""
def dfs(graph, start, goal, visited):
    stack = [(start, [start], 0)]
    visitedArray = {node: False for node in graph}
    exploration_cost = 0
    steps = []

    while stack:
        (node, path, cost) = stack.pop()
        if visitedArray[node]:
            continue
        visitedArray[node] = True
        visited.append(node)

        if len(path) > 1:
            exploration_cost += graph[path[-2]][node]

        steps.append((node, path, cost, exploration_cost, visited[:]))

        if node == goal:
            return path, cost, steps

        for neighbor, weight in graph[node].items():
            if not visitedArray[neighbor]:
                stack.append((neighbor, path + [neighbor], cost + weight))

    return None, None, steps

"""
priotiy queue mantığı ile ilerler
costu en az olan pathi bulur
"""
def ucs(graph, start, goal, visited):
    queue = [(0, start, [start])]
    visitedArray = {node: False for node in graph}
    parent = {node: None for node in graph}
    exploration_cost = 0
    steps = []

    while queue:
        (cost, node, path) = heapq.heappop(queue)
        if visitedArray[node]:
            continue
        visitedArray[node] = True
        visited.append(node)

        if parent[node] is not None:
            for edge_node, edge_cost in graph[parent[node]].items():
                if edge_node == node:
                    exploration_cost += edge_cost
                    break

        steps.append((node, path, cost, exploration_cost, visited[:]))

        if node == goal:
            return path, cost, steps

        for neighbor, weight in graph[node].items():
            if not visitedArray[neighbor]:
                heapq.heappush(queue, (cost + weight, neighbor, path + [neighbor]))
                parent[neighbor] = node

    return None, None, steps

def draw_edges(graph):
    for node, neighbors in graph.items():
        for neighbor, weight in neighbors.items():
            pygame.draw.line(screen, BLACK, positions[node], positions[neighbor], 2)
            mid_point = ((positions[node][0] + positions[neighbor][0]) // 2,
                         (positions[node][1] + positions[neighbor][1]) // 2)
            weight_text = FONT.render(str(weight), True, BLACK)
            screen.blit(weight_text, mid_point)

def draw_nodes():
    for node, pos in positions.items():
        pygame.draw.circle(screen, BLUE if node == 'A' else RED if node == 'J' else WHITE, pos, 20)
        pygame.draw.circle(screen, BLACK, pos, 20, 2)
        node_text = FONT.render(node, True, BLACK)
        screen.blit(node_text, (pos[0] - 10, pos[1] - 10))

def visualize_steps(steps, step_index):
    draw_nodes()

    for i, (node, path, cost, exploration_cost, visited_nodes) in enumerate(steps[:step_index + 1]):
        color = GREEN if i == step_index else BLUE
        pygame.draw.circle(screen, color, positions[node], 20)
        node_text = FONT.render(node, True, BLACK)
        screen.blit(node_text, (positions[node][0] - 10, positions[node][1] - 10))

    if step_index == len(steps) - 1:
        for node in steps[-1][1]:
            pygame.draw.circle(screen, YELLOW, positions[node], 20)
            node_text = FONT.render(node, True, BLACK)
            screen.blit(node_text, (positions[node][0] - 10, positions[node][1] - 10))

    total_cost_text = f"Path: {' -> '.join(steps[step_index][1])} | Total Cost: {steps[step_index][2]}"
    path_text = FONT.render(total_cost_text, True, BLACK)
    visited_nodes_text = f"Visited Nodes: {' -> '.join(visited_nodes)}"
    visited_text = FONT.render(visited_nodes_text, True, BLACK)

    pygame.draw.rect(screen, WHITE, (0, HEIGHT - 60, WIDTH, 60))
    screen.blit(path_text, (10, HEIGHT - 50))
    screen.blit(visited_text, (10, HEIGHT - 30))

    exploration_cost_text = f"Exploration Cost: {steps[step_index][3]}"
    exploration_text = FONT.render(exploration_cost_text, True, BLACK)
    screen.blit(exploration_text, (WIDTH - 250, HEIGHT - 30))

def choose_algorithm():
    screen.fill(WHITE)

    title = FONT.render("Choose an algorithm: Press 1 for BFS, 2 for DFS, 3 for UCS", True, BLACK)
    title2 = FONT.render("Controls: ", True, BLACK)
    control1 = FONT.render("Right Arrow: Take 1 step forward.", True, BLACK)
    control2 = FONT.render("Left Arrow: Take 1 step back.", True, BLACK)

    screen.blit(title, (WIDTH // 2 - 200, HEIGHT // 2 - 20))
    screen.blit(title2, (WIDTH // 2 - 150, HEIGHT // 2 + 20))
    screen.blit(control1, (WIDTH // 2 - 150, HEIGHT // 2 + 50))
    screen.blit(control2, (WIDTH // 2 - 150, HEIGHT // 2 + 80))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    visited = []
                    return bfs(graph, 'A', 'J', visited), "BFS"
                elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    visited = []
                    return dfs(graph, 'A', 'J', visited), "DFS"
                elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    visited = []
                    return ucs(graph, 'A', 'J', visited), "UCS"

def main():
    result, algorithm_name = choose_algorithm()
    path, cost, steps = result
    clock = pygame.time.Clock()
    step_index = 0

    while True:
        screen.fill(WHITE)
        draw_edges(graph)
        visualize_steps(steps, step_index)

        algorithm_text = FONT.render(f"Algorithm: {algorithm_name}", True, BLACK)
        screen.blit(algorithm_text, (10, 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and step_index < len(steps) - 1:
                    step_index += 1
                elif event.key == pygame.K_LEFT and step_index > 0:
                    step_index -= 1

        pygame.display.flip()
        clock.tick(10)

main()
