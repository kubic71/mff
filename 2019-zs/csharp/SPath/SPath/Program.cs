using System;
using System.Collections.Generic;
using System.IO;

namespace SPath
{
    class ParsedTreeInvalidException : Exception
    {
        public ParsedTreeInvalidException(string msg) : base(msg)
        {
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            StreamReader input = new StreamReader("data.in");
            TreeParser treeParser = new TreeParser(input);
            TreeNode tree = treeParser.ParseTree();

            if (!treeParser.IsParsedTreeValid())
            {
                // What to do here?
                throw new ParsedTreeInvalidException("Parsed data in data.in is invalid!");
            }

            StreamReader queryFile = new StreamReader("query.in");
            StreamWriter outputFile = new StreamWriter("results.out");

            var queryParser = new QueryParser(QueryParser.StripFirstForwardSlash(queryFile.ReadLine()));
            var query = queryParser.ParseQuery();

            foreach (var node in Filter.FilterQuery(new List<TreeNode>() {tree}, query))
            {
                outputFile.WriteLine(node.ToString());
            }
            
            input.Close();
            queryFile.Close();
            outputFile.Close();
        }
    }
}