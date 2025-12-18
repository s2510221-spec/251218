# ==========================================
# 1. 데이터 정의 (도시 간 연결 정보와 거리)
# ==========================================
graph = {
    "서울": {"천안": 85, "원주": 87, "인천": 27},
    "인천": {"서울": 27, "수원": 42},
    "천안": {"서울": 85, "대전": 48, "논산": 60, "수원": 55},
    "수원": {"인천": 42, "천안": 55, "서울": 35},
    "원주": {"서울": 87, "강릉": 110, "제천": 35},
    "강릉": {"원주": 110, "포항": 160},
    "대전": {"천안": 48, "대구": 120, "광주": 140},
    "논산": {"천안": 60, "전주": 35, "광주": 90},
    "대구": {"대전": 120, "포항": 70, "부산": 95, "제천": 100},
    "제천": {"원주": 35, "대구": 100, "안동": 60},
    "안동": {"제천": 60, "포항": 80},
    "포항": {"강릉": 160, "안동": 80, "대구": 70, "부산": 100},
    "광주": {"대전": 140, "논산": 90, "순천": 60},
    "순천": {"광주": 60, "부산": 130},
    "전주": {"논산": 35, "대구": 130},
    "부산": {"대구": 95, "포항": 100, "순천": 130}
}

# ==========================================
# 2. 최단 거리 알고리즘 (Dijkstra 구현)
# ==========================================
def find_shortest_path(graph, start, end):
    # 초기화: 모든 도시의 거리를 무한대(매우 큰 수)로 설정
    distances = {node: float('inf') for node in graph}
    distances[start] = 0  # 시작점은 거리가 0
    
    # 경로 추적을 위한 딕셔너리 (어디서 왔는지 기록)
    previous_nodes = {node: None for node in graph}
    
    # 방문하지 않은 도시 목록
    unvisited = list(graph.keys())

    while unvisited:
        # 1. 방문하지 않은 도시 중 가장 가까운 도시 찾기
        current_node = None
        min_dist = float('inf')
        
        for node in unvisited:
            if distances[node] < min_dist:
                min_dist = distances[node]
                current_node = node
        
        # 더 이상 갈 곳이 없거나 도착점에 도달했으면 중단
        if current_node is None or current_node == end:
            break
            
        # 2. 현재 도시에서 갈 수 있는 이웃 도시들 확인
        neighbors = graph[current_node]
        for neighbor, weight in neighbors.items():
            # 새로운 거리 계산 (지금까지 온 거리 + 이웃까지 거리)
            new_distance = distances[current_node] + weight
            
            # 더 빠른 길을 발견하면 정보 갱신
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous_nodes[neighbor] = current_node # 어디서 왔는지 기록
        
        # 방문 완료 처리
        unvisited.remove(current_node)

    # ==========================================
    # 3. 경로 역추적 (도착점 -> 시작점)
    # ==========================================
    path = []
    current = end
    
    # 거리가 무한대라면 길이 없는 것
    if distances[end] == float('inf'):
        return None, None

    while current is not None:
        path.append(current)
        current = previous_nodes[current]
    
    # 역순으로 담겼으므로 다시 뒤집기 (시작 -> 끝)
    path.reverse()
    
    return path, distances[end]

# ==========================================
# 4. 실행 및 테스트
# ==========================================
print("🗺️ AI 네비게이션 시스템 가동")
print("-" * 30)

start_city = "서울"
end_city = "부산"

# 함수 실행
path, total_dist = find_shortest_path(graph, start_city, end_city)

if path:
    print(f"🚩 출발: {start_city}")
    print(f"🏁 도착: {end_city}")
    print(f"🛣️ 최단 경로: {' -> '.join(path)}")
    print(f"📏 총 거리: {total_dist}km")
else:
    print("❌ 경로를 찾을 수 없습니다.")
