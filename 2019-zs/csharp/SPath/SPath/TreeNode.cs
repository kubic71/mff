using System.Collections.Generic;
using System.Text;

namespace SPath
{
    public class TreeNode
    {
        public bool OutputThisNode = false;
        public string ID { get; set; }
        public TreeNode Parent { get; set; }
        
        public int Index { get; set; } 
        public List<TreeNode> Children { get; set; }
        

        public bool IsLeaf()
        {
            return this.Children == null || this.Children.Count == 0;
        }
        
        public bool IsRoot()
        {
            return Parent == null;
        }

        
        // add path from node to root to path-list 
        private void GetPathFromRoot(TreeNode node, List<TreeNode> path)
        {
            if (node != null)
            {
                path.Add(node);
                GetPathFromRoot(node.Parent, path);
            }
        }
        
        public List<TreeNode> GetPathFromRoot()
        {
            List<TreeNode> path = new List<TreeNode>();
            path.Add(this);
            GetPathFromRoot(this.Parent, path);
            path.Reverse();
            return path;
        }

        public override string ToString()
        {
            var path = GetPathFromRoot();

            StringBuilder sb = new StringBuilder();
            foreach (var node in path)
            {
                if (!node.IsRoot())
                {
                    sb.Append($"/{node.ID}({node.Index})");
                }
            }

            if (sb.Length == 0)
            {
                return "/";
            }
            
            return sb.ToString();
        }
    }
}