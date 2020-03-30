using System;
using System.Collections.Generic;
using System.IO;

namespace SPath
{

    public class NotParsedYetException : Exception
    {
        public NotParsedYetException(string message) : base(message)
        {
        }
    } 

    public class TreeParser
    {

        private string[] tokens;
        private int index;
        private bool parsedYet;
        
        public TreeParser(StreamReader inputStream)
        {
            tokens = Tokenizer.Tokenize(inputStream);
            index = 0;
            parsedYet = false;
        }

        private bool IndexOutOfRange()
        {
            // index never gets negative
            return index >= tokens.Length;
        }

        private string ParseID()
        {
            if (IndexOutOfRange()) return null;
            
            string token = tokens[index];
            if (!token.Contains('/') && !token.Contains('*') && !token.Contains('[') && !token.Contains(']')
                && !token.Contains('(') && !token.Contains(')') && !Char.IsDigit(token[0])) {
                index++;
                return token;
            }

            return null;
        }

        private bool ParseString(string s)
        {
            if (IndexOutOfRange()) return false;
            if (tokens[index] == s)
            {
                index++;
                return true;
            }

            return false;
        }
        
        private TreeNode ParseRootedTree()
        {
            string id = ParseID();
            if (id == null)
            {
                return null;
            }

            int backtrack = index;
            // Tree
            TreeNode root;            
            if (ParseString("(") && ((root = ParseTree()) != null) && ParseString(")"))
            {
                root.ID = id;
                return root;
            }

            index = backtrack;
            // Leaf
            root = new TreeNode();
            root.ID = id;
            return root;
        }


        public bool IsParsedTreeValid()
        {
            if (!parsedYet)
            {
                throw new NotParsedYetException("Tree was not yet parsed!");
            }
        
            return index == tokens.Length && tokens.Length > 0;
        }

        public TreeNode ParseTree()
        {
            parsedYet = true;
            
            TreeNode tree = new TreeNode();
            tree.Children = new List<TreeNode>();

            TreeNode rootedTree;
            int index = 0;
            while(true)
            {
                rootedTree = ParseRootedTree();
                if (rootedTree == null)
                {
                    break;
                }

                rootedTree.Index = index;
                tree.Children.Add(rootedTree);
                rootedTree.Parent = tree;

                index++;
            }

            if (tree.Children.Count == 0)
            {
                return null;
            }

            return tree;
        }
    }
}

// Parsing Grammar:
// RootedTree : ID, '(', Tree, ')' | ID
// Tree: RootedTree { RootedTree }