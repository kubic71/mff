using NUnit.Framework;
using SPath;

namespace Tests
{
    public class QueryTest
    {
        string exampleTreeStr = "a a ( b b c ) a ( b b ) x ( y ( z ) )";
        private TreeNode exampleTree;

        [SetUp]
        public void Setup()
        {
            exampleTree = Utils.GetTreeFromString(exampleTreeStr);
        }
        
        
        [Test]
        public void TestPathToString()
        {
            Assert.AreEqual("/", exampleTree.ToString());
            Assert.AreEqual("/a(2)", exampleTree.Children[2].ToString());
            Assert.AreEqual("/a(1)/c(2)", exampleTree.Children[1].Children[2].ToString());
            Assert.AreEqual("/x(3)/y(0)/z(0)", exampleTree.Children[3].Children[0].Children[0].ToString());
        }
    }
}