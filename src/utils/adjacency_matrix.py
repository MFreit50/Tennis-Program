from typing import List, Dict, Tuple, Union

class AdjacencyMatrix:
    def __init__(self, vertices: List[Union[str, int]]) -> None:
        """
        Initialize an adjacency matrix for the given list of vertices.

        Args:
            vertices (List[Union[str, int]]): A list of vertices to create the adjacency matrix.
        """
        self.adjacency_matrix: Dict[Union[str, int], Dict[Union[str, int], int]] = {
            v: {u: 0 for u in vertices} for v in vertices
        }
        
    # Utility Functions
    def has_edge(self, vertex1: Union[str, int], vertex2: Union[str, int]) -> bool:
        """
        Check if an edge exists between two vertices.

        Args:
            vertex1 (Union[str, int]): The first vertex.
            vertex2 (Union[str, int]): The second vertex.

        Returns:
            bool: True if the edge exists, False otherwise.
        """
        return vertex1 in self.adjacency_matrix and vertex2 in self.adjacency_matrix
    
    def has_vertex(self, vertex: Union[str, int]) -> bool:
        """
        Check if a vertex exists in the matrix.

        Args:
            vertex (Union[str, int]): The vertex to check.

        Returns:
            bool: True if the vertex exists, False otherwise.
        """
        return vertex in self.adjacency_matrix
    
    def get_edge(self, vertex1: Union[str, int], vertex2: Union[str, int]) -> int:
        """
        Get the weight of the edge between two vertices.

        Args:
            vertex1 (Union[str, int]): The first vertex.
            vertex2 (Union[str, int]): The second vertex.

        Returns:
            int: The weight of the edge.

        Raises:
            ValueError: If the edge is invalid.
        """
        if self.has_edge(vertex1, vertex2):
            return self.adjacency_matrix[vertex1][vertex2]
        else:
            raise ValueError("Invalid Edge")
        
    def get_all_edges(self) -> List[Tuple[Union[str, int], Union[str, int], int]]:
        """
        Get a list of all edges in the adjacency matrix.

        Returns:
            List[Tuple[Union[str, int], Union[str, int], int]]: A list of edges in the form (vertex1, vertex2, weight).
        """
        edges = []
        for i in self.adjacency_matrix:
            for j in self.adjacency_matrix:
                if i != j:
                    edges.append((i, j, self.adjacency_matrix[i][j]))
        return edges
    
    def get_edges_of_vertex(self, vertex: Union[str, int]) -> List[Tuple[Union[str, int], Union[str, int], int]]:
        """
        Get all edges connected to a vertex.

        Args:
            vertex (Union[str, int]): The vertex whose edges are to be retrieved.

        Returns:
            List[Tuple[Union[str, int], Union[str, int], int]]: A list of edges in the form (vertex, adjacent_vertex, weight).

        Raises:
            ValueError: If the vertex is invalid.
        """
        if not self.has_vertex(vertex):
            raise ValueError("Invalid Vertex")

        edges = []
        for adjacent_vertex, weight in self.adjacency_matrix[vertex].items():
            edges.append((vertex, adjacent_vertex, weight))
        return edges
    
    # Edge Functions
    def update_edge(self, vertex1: Union[str, int], vertex2: Union[str, int], weight: int) -> None:
        """
        Update the weight of an edge between two vertices.

        Args:
            vertex1 (Union[str, int]): The first vertex.
            vertex2 (Union[str, int]): The second vertex.
            weight (int): The new weight of the edge.

        Raises:
            ValueError: If the edge is invalid.
        """
        if self.has_edge(vertex1, vertex2):
            self.adjacency_matrix[vertex1][vertex2] = weight
            self.adjacency_matrix[vertex2][vertex1] = weight
        else:
            raise ValueError("Invalid Edge")

    def increment_edge(self, vertex1: Union[str, int], vertex2: Union[str, int]) -> None:
        """
        Increment the weight of an edge between two vertices by 1.

        Args:
            vertex1 (Union[str, int]): The first vertex.
            vertex2 (Union[str, int]): The second vertex.

        Raises:
            ValueError: If the edge is invalid.
        """
        if self.has_edge(vertex1, vertex2):
            self.adjacency_matrix[vertex1][vertex2] += 1
        else:
            raise ValueError("Invalid Edge")
    
    def increment_edge_list(self, vertices: List[Union[str, int]]) -> None:
        """
        Increment the weights of all edges in a list of vertices.

        Args:
            vertices (List[Union[str, int]]): A list of vertices to increment edges for.
        """
        for vertex1 in vertices:
            for vertex2 in vertices:
                self.increment_edge(vertex1, vertex2)

    def remove_edge(self, vertex1: Union[str, int], vertex2: Union[str, int]) -> None:
        """
        Remove an edge between two vertices by setting its weight to 0.

        Args:
            vertex1 (Union[str, int]): The first vertex.
            vertex2 (Union[str, int]): The second vertex.

        Raises:
            ValueError: If the edge is invalid.
        """
        if self.has_edge(vertex1, vertex2):
            self.adjacency_matrix[vertex1][vertex2] = 0
            self.adjacency_matrix[vertex2][vertex1] = 0
        else:
            raise ValueError("Invalid Edge")
        
    # Vertex Functions
    def add_vertex(self, new_vertex: Union[str, int]) -> bool:
        """
        Add a new vertex to the adjacency matrix.

        Args:
            new_vertex (Union[str, int]): The new vertex to add.

        Returns:
            bool: True if the vertex was added successfully, False if it already exists.
        """
        if not self.has_vertex(new_vertex):
            for vertex in self.adjacency_matrix:
                self.adjacency_matrix[vertex][new_vertex] = 0
            self.adjacency_matrix[new_vertex] = {vertex: 0 for vertex in self.adjacency_matrix}
            return True
        
        return False
    
    def remove_vertex(self, vertex_to_remove: Union[str, int]) -> bool:
        """
        Remove a vertex and its associated edges from the adjacency matrix.

        Args:
            vertex_to_remove (Union[str, int]): The vertex to remove.

        Returns:
            bool: True if the vertex was removed successfully, False if it doesn't exist.
        """
        if self.has_vertex(vertex_to_remove):
            for vertex in self.adjacency_matrix:
                del self.adjacency_matrix[vertex][vertex_to_remove]
            del self.adjacency_matrix[vertex_to_remove]
            return True
        
        return False
    
    def __str__(self) -> str:
        """
        Get a string representation of the adjacency matrix.

        Returns:
            str: A string representation of the adjacency matrix.
        """
        string = ''
        for vertex, edges in self.adjacency_matrix.items():
            string += (f"{vertex}:\t{edges}\n")
        return string