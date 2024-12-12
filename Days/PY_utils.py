import numpy as np
from numba import jit, cuda
import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor
from typing import List, Set, Tuple, Dict, Any, Optional, Callable, Generator, TypeVar
from dataclasses import dataclass
from collections import defaultdict, deque
import heapq
import networkx as nx
from scipy.spatial import ConvexHull
import itertools
from functools import lru_cache, partial
import re
from pathlib import Path
from typing import List, Dict, Set, Any, Optional, Union, Pattern

T = TypeVar('T')  # Generic type for flexible typing

class ParallelProcessor:
    """Manages parallel processing resources efficiently"""
    def __init__(self, max_workers: Optional[int] = None, use_gpu: bool = False):
        self.max_workers = max_workers or mp.cpu_count()
        self.use_gpu = use_gpu and cuda.is_available()
        self._pool = None
        self._executor = None
    
    def __enter__(self):
        self._pool = mp.Pool(self.max_workers)
        self._executor = ThreadPoolExecutor(max_workers=self.max_workers)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._pool:
            self._pool.close()
            self._pool.join()
        if self._executor:
            self._executor.shutdown()

    def map(self, func: Callable, iterable: List[Any], chunk_size: Optional[int] = None) -> List[Any]:
        """Parallel map with automatic chunking"""
        if self.use_gpu and hasattr(func, 'cuda_kernel'):
            return func.cuda_kernel(iterable)
        return self._pool.map(func, iterable, chunksize=chunk_size)

class GridProcessor:
    """Enhanced grid processing with GPU support"""
    def __init__(self, data: np.ndarray):
        self.data = data
        self.height, self.width = data.shape
        self._cuda_enabled = cuda.is_available()

    @staticmethod
    @jit(nopython=True)
    def _neighbors_orthogonal(y: int, x: int, height: int, width: int) -> List[Tuple[int, int]]:
        """Get orthogonal neighbors (up, down, left, right)"""
        neighbors = []
        for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
            ny, nx = y + dy, x + dx
            if 0 <= ny < height and 0 <= nx < width:
                neighbors.append((ny, nx))
        return neighbors

    @staticmethod
    @jit(nopython=True)
    def _neighbors_diagonal(y: int, x: int, height: int, width: int) -> List[Tuple[int, int]]:
        """Get diagonal neighbors"""
        neighbors = []
        for dy, dx in [(1,1), (1,-1), (-1,1), (-1,-1)]:
            ny, nx = y + dy, x + dx
            if 0 <= ny < height and 0 <= nx < width:
                neighbors.append((ny, nx))
        return neighbors

    def get_neighbors(self, y: int, x: int, diagonal: bool = False) -> List[Tuple[int, int]]:
        """Get all valid neighboring coordinates"""
        neighbors = self._neighbors_orthogonal(y, x, self.height, self.width)
        if diagonal:
            neighbors.extend(self._neighbors_diagonal(y, x, self.height, self.width))
        return neighbors

    def find_regions(self, 
                    condition: Callable[[Any], bool], 
                    diagonal: bool = False,
                    min_size: int = 1) -> List[Set[Tuple[int, int]]]:
        """Find connected regions matching condition"""
        visited = set()
        regions = []
        
        def explore(start: Tuple[int, int]) -> Set[Tuple[int, int]]:
            if start in visited:
                return set()
            
            region = set()
            queue = deque([start])
            
            while queue:
                pos = queue.popleft()
                if pos in visited:
                    continue
                    
                visited.add(pos)
                if condition(self.data[pos]):
                    region.add(pos)
                    for n in self.get_neighbors(*pos, diagonal):
                        if n not in visited:
                            queue.append(n)
            
            return region if len(region) >= min_size else set()
        
        with ThreadPoolExecutor() as executor:
            futures = []
            for y in range(self.height):
                for x in range(self.width):
                    if (y, x) not in visited and condition(self.data[y, x]):
                        futures.append(executor.submit(explore, (y, x)))
            
            regions = [f.result() for f in futures if f.result()]
        
        return regions

class PathFinder:
    """Advanced pathfinding with multiple algorithms"""
    def __init__(self, parallel: bool = True):
        self.parallel = parallel
        self._processor = ParallelProcessor() if parallel else None
    
    @staticmethod
    @lru_cache(maxsize=1024)
    def dijkstra(graph: Dict[T, Dict[T, float]], 
                start: T, 
                end: Optional[T] = None) -> Dict[T, float]:
        """Cached Dijkstra's algorithm implementation"""
        distances = {start: 0}
        pq = [(0, start)]
        visited = set()
        
        while pq:
            current_distance, current = heapq.heappop(pq)
            
            if current in visited:
                continue
                
            visited.add(current)
            if end and current == end:
                break
                
            for neighbor, weight in graph[current].items():
                distance = current_distance + weight
                if neighbor not in distances or distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(pq, (distance, neighbor))
        
        return distances

    def parallel_paths(self, 
                      graph: Dict[T, Dict[T, float]], 
                      sources: List[T], 
                      targets: List[T]) -> Dict[Tuple[T, T], float]:
        """Compute multiple paths in parallel"""
        if not self.parallel:
            return {(s, t): self.dijkstra(graph, s, t).get(t, float('inf'))
                    for s in sources for t in targets}
        
        with self._processor as proc:
            pairs = list(itertools.product(sources, targets))
            results = proc.map(
                partial(lambda p: (p, self.dijkstra(graph, p[0], p[1]).get(p[1], float('inf'))), 
                pairs)
            )
        return dict(results)

class Geometry:
    """Enhanced geometry utilities"""
    @staticmethod
    @jit(nopython=True)
    def manhattan_distance(p1: Tuple[int, ...], p2: Tuple[int, ...]) -> int:
        """N-dimensional Manhattan distance"""
        return sum(abs(a - b) for a, b in zip(p1, p2))
    
    @staticmethod
    @jit(nopython=True)
    def euclidean_distance_squared(p1: Tuple[float, ...], p2: Tuple[float, ...]) -> float:
        """N-dimensional Euclidean distance squared"""
        return sum((a - b) ** 2 for a, b in zip(p1, p2))

    @staticmethod
    def convex_hull(points: List[Tuple[float, ...]]) -> List[Tuple[float, ...]]:
        """Compute convex hull of N-dimensional points"""
        if len(points) < 3:
            return points
        hull = ConvexHull(np.array(points))
        return [points[i] for i in hull.vertices]

class Parser:
    """Robust input parsing with multiple formats and validation"""
    
    def __init__(self, strip: bool = True, filter_empty: bool = True):
        self.strip = strip
        self.filter_empty = filter_empty
        self._regex_cache: Dict[str, Pattern] = {}
    
    def load_file(self, day: Union[int, str]) -> str:
        """Load input file for given day"""
        day = str(day).zfill(2)
        path = Path(__file__).parent.parent / 'Data' / f'{day}.txt'
        return path.read_text().strip() if self.strip else path.read_text()

    def lines(self, text: str) -> List[str]:
        """Split text into lines with optional filtering"""
        lines = text.splitlines()
        if self.strip:
            lines = [line.strip() for line in lines]
        if self.filter_empty:
            lines = [line for line in lines if line]
        return lines

    def numbers(self, text: str, 
               negative: bool = True, 
               as_type: type = int) -> List[Union[int, float]]:
        """Extract all numbers from text"""
        pattern = r'-?\d+\.?\d*' if negative else r'\d+\.?\d*'
        return [as_type(n) for n in re.findall(pattern, text)]

    def parse_grid(self, 
                  text: str, 
                  as_type: type = str,
                  separator: str = '') -> np.ndarray:
        """Parse 2D grid from text"""
        lines = self.lines(text)
        if separator:
            grid = [line.split(separator) for line in lines]
        else:
            grid = [[char for char in line] for line in lines]
            
        try:
            return np.array(grid, dtype=as_type)
        except ValueError as e:
            raise ValueError(f"Could not parse grid as {as_type}: {e}")

    def parse_groups(self, 
                    text: str, 
                    separator: str = '\n\n') -> List[str]:
        """Split text into groups by separator"""
        groups = text.split(separator)
        if self.strip:
            groups = [g.strip() for g in groups]
        if self.filter_empty:
            groups = [g for g in groups if g]
        return groups

    def parse_with_regex(self, 
                        text: str, 
                        pattern: str, 
                        as_dict: bool = True,
                        flags: int = re.MULTILINE) -> List[Union[Dict[str, str], tuple]]:
        """
        Parse text using regex pattern
        Returns list of dicts (if named groups) or tuples (if unnamed groups)
        """
        if pattern not in self._regex_cache:
            self._regex_cache[pattern] = re.compile(pattern, flags)
            
        regex = self._regex_cache[pattern]
        matches = regex.finditer(text)
        
        if as_dict:
            return [m.groupdict() for m in matches]
        return [m.groups() for m in matches]

    def parse_key_value(self, 
                       text: str,
                       item_sep: str = '\n',
                       key_value_sep: str = ':',
                       as_type: Optional[type] = None) -> Dict[str, Any]:
        """Parse key-value pairs from text"""
        result = {}
        items = text.split(item_sep)
        
        for item in items:
            if key_value_sep not in item:
                continue
            key, value = item.split(key_value_sep, 1)
            if self.strip:
                key = key.strip()
                value = value.strip()
            if as_type:
                try:
                    value = as_type(value)
                except ValueError:
                    continue
            result[key] = value
            
        return result

    @staticmethod
    def extract_ints(text: str) -> List[int]:
        """Quick helper for common case of extracting integers"""
        return [int(n) for n in re.findall(r'-?\d+', text)]

    @staticmethod
    def extract_words(text: str) -> List[str]:
        """Extract words using common pattern"""
        return re.findall(r'[a-zA-Z]+', text)

    def parse_graph(self, 
                   text: str, 
                   directed: bool = False,
                   weighted: bool = False) -> Dict[str, Dict[str, float]]:
        """
        Parse graph structure from text
        Format: "node1 -> node2,node3" or "node1 -> node2(5),node3(10)" for weighted
        """
        graph: Dict[str, Dict[str, float]] = defaultdict(dict)
        
        for line in self.lines(text):
            if '->' not in line:
                continue
                
            source, targets = line.split('->', 1)
            source = source.strip()
            
            for target in targets.split(','):
                target = target.strip()
                weight = 1.0
                
                if weighted and '(' in target:
                    target, weight_str = target.split('(')
                    weight = float(weight_str.rstrip(')'))
                
                graph[source][target] = weight
                if not directed:
                    graph[target][source] = weight
                    
        return dict(graph)

    def __call__(self, text: str) -> List[str]:
        """Default behavior: split into lines"""
        return self.lines(text)