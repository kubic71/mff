using System.IO;
using System.Text;
using SPath;

namespace Tests
{
    public static class Utils
    {
        public static StreamReader GenerateStreamFromString(string value)
        {
            return new StreamReader(new MemoryStream(Encoding.UTF8.GetBytes(value ?? "")), Encoding.UTF8);
        }
        
        public static TreeNode GetTreeFromString(string treeStr)
        {
            StreamReader stream = Utils.GenerateStreamFromString(treeStr);
            TreeParser parser = new TreeParser(stream);
            TreeNode tree = parser.ParseTree();
            return tree;
        }
    }
}