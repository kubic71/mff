using System.IO;
using NUnit.Framework;
using SPath;

namespace Tests
{
    public class Tests
    {

        string exampleTree = "a a ( b b c ) a ( b b ) x ( y ( z ) )";
        string exampleTreeWithWhitespace = "     \n\n\na  \n a (\n         \n            b  \n       b \nc    \n    )        \n  a (         b           b ) x ( y ( \nz ) )    \n                  ";
        
        [SetUp]
        public void Setup()
        {
        }

        [Test]
        public void TestExample()
        {
            TestExampleTreeHelper(exampleTree);
        }
        
        [Test]
        public void TestExample2()
        {
            // parser should parse the longest possible sequence that makes sense
            string treeStr = exampleTree + " ( )";
            TestExampleTreeHelper(exampleTree);
        }
        
        [Test]
        public void TestTree4()
        {
            // parser should parse the longest possible sequence that makes sense
            string treeStr = "abcd";
            TreeNode tree = Utils.GetTreeFromString(treeStr);
            Assert.AreEqual(1, tree.Children.Count);
            Assert.AreEqual("abcd", tree.Children[0].ID);
        }
        
        [Test]
        public void TestTree5()
        {
            // parser should parse the longest possible sequence that makes sense
            string treeStr = "a ( c d] ) b c ( d )";
            TreeNode tree = Utils.GetTreeFromString(treeStr);
            Assert.AreEqual(1, tree.Children.Count);
            Assert.AreEqual("a", tree.Children[0].ID);
        }
        
        [Test]
        public void TestTree6()
        {
            // parser should parse the longest possible sequence that makes sense
            string treeStr = "2asd";
            TreeNode tree = Utils.GetTreeFromString(treeStr);
            Assert.AreEqual(null, tree);
        }


        [Test]
        public void TestValid1()
        {
            string treeStr = "                   ";
            StreamReader stream = Utils.GenerateStreamFromString(treeStr);
            TreeParser parser = new TreeParser(stream);
            TreeNode tree = parser.ParseTree();
            Assert.IsFalse(parser.IsParsedTreeValid());
        }
        
        [Test]
        public void TestValid2()
        {
            string treeStr = "  sf as ";
            StreamReader stream = Utils.GenerateStreamFromString(treeStr);
            TreeParser parser = new TreeParser(stream);
            TreeNode tree = parser.ParseTree();
            Assert.IsTrue(parser.IsParsedTreeValid());
        }
        
        [Test]
        public void TestValid3()
        {
            StreamReader stream = Utils.GenerateStreamFromString(exampleTree);
            TreeParser parser = new TreeParser(stream);
            TreeNode tree = parser.ParseTree();
            Assert.IsTrue(parser.IsParsedTreeValid());
        }
        
        [Test]
        public void TestValid4()
        {
            StreamReader stream = Utils.GenerateStreamFromString(exampleTreeWithWhitespace);
            TreeParser parser = new TreeParser(stream);
            TreeNode tree = parser.ParseTree();
            Assert.IsTrue(parser.IsParsedTreeValid());
        }
        
        [Test]
        public void TestValid5()
        {
            StreamReader stream = Utils.GenerateStreamFromString(exampleTree + " ( ) ");
            TreeParser parser = new TreeParser(stream);
            TreeNode tree = parser.ParseTree();
            Assert.IsFalse(parser.IsParsedTreeValid());
        }
        
        [Test]
        public void TestExampleWithWhitespace()
        {

            // should give the same result, no mather the whitespace between tokens
            TestExampleTreeHelper(exampleTreeWithWhitespace);
        }


        private void TestExampleTreeHelper(string exTree)
        {
            TreeNode tree = Utils.GetTreeFromString(exTree);
            Assert.AreEqual(true, tree.IsRoot());
            Assert.AreEqual(4, tree.Children.Count);
            
            Assert.AreEqual("a", tree.Children[0].ID);
            Assert.AreEqual(true, tree.Children[0].IsLeaf());
            
            Assert.AreEqual("a", tree.Children[1].ID);
            Assert.AreEqual(3, tree.Children[1].Children.Count);
            Assert.AreEqual("b", tree.Children[1].Children[0].ID);
            Assert.AreEqual("b", tree.Children[1].Children[1].ID);
            Assert.AreEqual("c", tree.Children[1].Children[2].ID);
            Assert.AreEqual(true, tree.Children[1].Children[0].IsLeaf());
            Assert.AreEqual(true, tree.Children[1].Children[1].IsLeaf());
            Assert.AreEqual(true, tree.Children[1].Children[2].IsLeaf());
            
            Assert.AreEqual(tree.Children[1], tree.Children[1].Children[1].Parent);
            
            Assert.AreEqual("a", tree.Children[2].ID);
            Assert.IsFalse(tree.Children[2].IsLeaf());
            Assert.IsFalse(tree.Children[2].IsRoot());
            Assert.AreEqual(2, tree.Children[2].Children.Count);
            Assert.AreEqual("b", tree.Children[2].Children[0].ID);
            Assert.AreEqual("b", tree.Children[2].Children[1].ID);
            Assert.AreEqual(true, tree.Children[2].Children[0].IsLeaf());
            Assert.AreEqual(true, tree.Children[2].Children[1].IsLeaf());
            
            Assert.AreEqual("x", tree.Children[3].ID);
            Assert.AreEqual(1, tree.Children[3].Children.Count);
            Assert.AreEqual("y", tree.Children[3].Children[0].ID);
            Assert.AreEqual(1, tree.Children[3].Children[0].Children.Count);
            Assert.AreEqual("z", tree.Children[3].Children[0].Children[0].ID);
            Assert.AreEqual(true, tree.Children[3].Children[0].Children[0].IsLeaf());
            
            Assert.AreEqual(tree.Children[3].Children[0], tree.Children[3].Children[0].Children[0].Parent);
            Assert.AreEqual(tree.Children[3], tree.Children[3].Children[0].Parent);
            Assert.AreEqual(tree, tree.Children[3].Parent);
            Assert.AreEqual(null, tree.Parent);
        }
    }
}