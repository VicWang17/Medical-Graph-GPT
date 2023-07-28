from py2neo import Graph, Node, Relationship

#连接数据库
graph = Graph("bolt://localhost:7687", auth=("neo4j", "123456789"))

def data_to_neo(data):
    


    # 创建并存储节点
    nodes = {}
    for node_data in data["nodes"]:
        # 检查数据库中是否已存在具有相同名称的实体节点
        existing_node = graph.nodes.match("Entity", name=node_data["name"]).first()
        if existing_node:
            node = existing_node
        else:
            node = Node("Entity", name=node_data["name"])
            graph.create(node)
        nodes[node_data["name"]] = node

            
    # 创建和存储关系
    for rel_data in data["relationships"]:
        start_node = nodes[rel_data["startNode"]]
        end_node = nodes[rel_data["endNode"]]
        relationship = Relationship(start_node, rel_data["type"], end_node)
        graph.create(relationship)

