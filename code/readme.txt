1. 先求出Nodes潜在朋友（2度朋友，3度朋友）
2. 根据Local methods(Common neighbors/Jaccard's coefficient/Adamic Adar/Preferential attactment)方法分别算出潜在边的权值
3. 加权处理算出潜在边的最终权值
4. 每个节点按Train/Test集合中与之关联的边的比例取潜在边的数量 
5. 利用deepwalk/line等图嵌入工具计算Top K相似的点连边
6. 二者取交集