from PartA_DinaraKurmangaliyevaSantiagoDelgado.neo4j_connection import conn

# Create GDS projection
create_projection_query = """
CALL gds.graph.project(
    'citation-graph',
    ['Paper'],
    {
        CITES: {
            type: 'CITES',
            orientation: 'NATURAL'
        }
    }
)
"""
try:
    conn.query(create_projection_query, return_result=False)
    print("GDS graph projection created.")
except Exception as e:
    print(f"Failed to create GDS graph projection: {e}")

# Run Node Similarity algorithm
node_similarity_query = """
CALL gds.nodeSimilarity.stream('citation-graph')
YIELD node1, node2, similarity
RETURN gds.util.asNode(node1).title AS Paper1,
       gds.util.asNode(node2).title AS Paper2,
       similarity
ORDER BY similarity DESC
LIMIT 10
"""
try:
    results = conn.query(node_similarity_query)
    print("\nNode Similarity Results:")
    for row in results:
        print(row)
except Exception as e:
    print(f"Failed to run node similarity: {e}")

# Run Dijkstra shortest path
shortest_path_query = """
MATCH (source:Paper), (target:Paper)
WHERE source.title <> target.title
WITH source, target LIMIT 1
CALL gds.shortestPath.dijkstra.stream('citation-graph', {
    sourceNode: id(source),
    targetNode: id(target)
})
YIELD totalCost, nodeIds
RETURN totalCost, [nodeId IN nodeIds | gds.util.asNode(nodeId).title] AS path
"""
try:
    path_result = conn.query(shortest_path_query)
    print("\nShortest Path Example:")
    for row in path_result:
        print(row)
except Exception as e:
    print(f"Failed to find shortest path: {e}")

# Close the connection
conn.close()
print("All graph algorithms completed. Connection closed.")
