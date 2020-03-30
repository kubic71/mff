using System.Collections.Generic;
using System.Linq;

namespace SPath
{
    public static class Filter
    {
        public static List<TreeNode> FilterQuery(List<TreeNode> nodes, Query query)
        {
            if (query == null)
                return nodes;
            
            foreach (Step step in query.steps)
            {
                nodes = FilterStep(nodes, step);
            }

            return nodes;
        }
        
        public static List<TreeNode> FilterStep(List<TreeNode> nodes, Step step)
        {
            nodes = FilterID(nodes, step.ID);
            nodes = RemoveNeighbouringDuplicates(nodes);
            
            foreach (var predicate in step.Predicates)
            {
                List<TreeNode> newNodes = new List<TreeNode>();
                
                if (predicate is NumberPredicate)
                {
                    int index = ((NumberPredicate) predicate).index;
                    if(index < nodes.Count)
                        newNodes.Add(nodes[index]);
                }
                else
                {
                    Query q = ((QueryPredicate) predicate).Query;
                    foreach (var node in nodes)
                    {
                        if (FilterQuery(new List<TreeNode>() {node}, q).Count > 0)
                            newNodes.Add(node);
                    }
                }

                nodes = newNodes;
            }

            return nodes;
        }

        private static List<TreeNode> RemoveNeighbouringDuplicates(List<TreeNode> nodes)
        {
            List<TreeNode> newNodes = new List<TreeNode>();
            TreeNode last = null;
            foreach (var node in nodes)
            {
                if (node != last)
                {
                    newNodes.Add(node);
                    last = node;
                }
            }

            return newNodes;
        }

        public static List<TreeNode> FilterID(List<TreeNode> nodes, string id)
        {
            List<TreeNode> newNodes = new List<TreeNode>();
            foreach (var node in nodes)
            {
                switch (id)
                {
                    case "*":
                        if(node.Children == null)
                            continue;
                        newNodes.AddRange(node.Children);
                        break;
                    
                    case "..":
                        if (node.Parent == null)
                            continue;
                        newNodes.Add(node.Parent);
                        break;
                    default:
                        if(node.Children == null)
                            continue;
                        foreach (var child in node.Children)
                        {
                            if (child.ID == id)
                            {
                                newNodes.Add(child);
                            }                            
                        }
                        break;
                }
            }

            return newNodes;
        }
        
    }
}