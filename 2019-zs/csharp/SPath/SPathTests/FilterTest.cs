using System.Collections.Generic;
using NUnit.Framework;
using SPath;

namespace Tests
{
    public class FilterTest
    {
     
        string exampleTreeStr = "a a ( b b c ) a ( b b ) x ( y ( z ) )";
        private TreeNode exampleTree;

        [SetUp]
        public void Setup()
        {
            exampleTree = Utils.GetTreeFromString(exampleTreeStr);
        }

        [Test]
        public void TestExample()
        {
            string queryStr = "/";
            List<TreeNode> res = Filter.FilterQuery(new List<TreeNode>() { exampleTree }, GetParsedQuery(queryStr));
            Assert.AreEqual(new List<TreeNode> { exampleTree }, res);

            queryStr = "/a";
            res = Filter.FilterQuery(new List<TreeNode>() { exampleTree }, GetParsedQuery(queryStr));
            Assert.AreEqual(new List<TreeNode> {exampleTree.Children[0], exampleTree.Children[1], exampleTree.Children[2]}, res);
            
            queryStr = "/a/b";
            res = Filter.FilterQuery(new List<TreeNode>() { exampleTree }, GetParsedQuery(queryStr));
            Assert.AreEqual(new List<TreeNode> {exampleTree.Children[1].Children[0], exampleTree.Children[1].Children[1], exampleTree.Children[2].Children[0], exampleTree.Children[2].Children[1]}, res);
            
                
            queryStr = "/a/z";
            res = Filter.FilterQuery(new List<TreeNode>() { exampleTree }, GetParsedQuery(queryStr));
            Assert.AreEqual(new List<TreeNode> {}, res);
            
            
            queryStr = "/a[b]";
            res = Filter.FilterQuery(new List<TreeNode>() { exampleTree }, GetParsedQuery(queryStr));
            Assert.AreEqual(new List<TreeNode> {exampleTree.Children[1], exampleTree.Children[2]}, res);

            queryStr = "/a[b][c]";
            res = Filter.FilterQuery(new List<TreeNode>() { exampleTree }, GetParsedQuery(queryStr));
            Assert.AreEqual(new List<TreeNode> {exampleTree.Children[1]}, res);


            queryStr = "/*[y/z]";
            res = Filter.FilterQuery(new List<TreeNode>() { exampleTree }, GetParsedQuery(queryStr));
            Assert.AreEqual(new List<TreeNode> {exampleTree.Children[3]}, res);


            queryStr = "/a[1]/b[1]";
            res = Filter.FilterQuery(new List<TreeNode>() { exampleTree }, GetParsedQuery(queryStr));
            Assert.AreEqual(new List<TreeNode> {exampleTree.Children[1].Children[1]}, res);


            queryStr = "/*/*/z/../..";
            res = Filter.FilterQuery(new List<TreeNode>() { exampleTree }, GetParsedQuery(queryStr));
            Assert.AreEqual(new List<TreeNode> {exampleTree.Children[3]}, res);
            

            
            
        }

        private Query GetParsedQuery(string queryStr)
        {
            QueryParser parser = new QueryParser(QueryParser.StripFirstForwardSlash(queryStr));
            return parser.ParseQuery();
        }
        
    }
}