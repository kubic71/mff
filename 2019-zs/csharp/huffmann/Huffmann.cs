using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

namespace huffmann
{
    class HuffmannTree
    {
        public HuffmannTree Left { get; private set; }
        public HuffmannTree Right { get; private set; }
        public long Weight { get; private set; }
        public byte Symbol { get; private set; }

        public bool IsLeaf()
        {
            return Left == null;
        }

        
        public string GetStringRepresentation()
        {
            // print itself
            if (IsLeaf())
            {
                return $"*{(int) Symbol}:{Weight}";
            }
            else
            {
                string s = $"{Weight} ";
                s += Left.GetStringRepresentation();
                s += " ";
                s += Right.GetStringRepresentation();
                return s;
            }
        }

        /// <summary> returns bool, whether node1 <= node2 </summary> 
        private static bool NodeCompare(HuffmannTree node1, HuffmannTree node2)
        {
            if (node1.Weight != node2.Weight)
            {
                return node1.Weight < node2.Weight;
            }
            else
            {
                if (node1.IsLeaf() && node2.IsLeaf())
                {
                    return node1.Symbol <= node2.Symbol;
                }
                else if (node1.IsLeaf() && !node2.IsLeaf())
                {
                    // leaves are lighter then inner nodes
                    return true;
                }
                else if (!node1.IsLeaf() && node2.IsLeaf())
                {
                    return false;
                }
                else
                {
                    // two inner nodes with the same Weight
                    return true;
                }
            }
        }

        
        /// <summary> insert node into sorted forest while preserving ordering </summary>
        private static void SortInsert(List<HuffmannTree> forest, HuffmannTree node)
        {
            if (forest.Count == 0)
            {
                forest.Add(node);
                return;
            }
            
            int i = 0;
            while (NodeCompare(forest[i], node))
            {
                i++;

                if (i == forest.Count)
                {
                    // node is bigger or equal to the whole forest, it is supposed to be last
                    forest.Add(node);
                    return;
                }
            }

            // forest[i] > node, we want to insert node before i-th forest's node
            forest.Insert(i, node);
        }

        public static HuffmannTree BuildTree(Stream inputStream)
        {
            
            int BUFFER_SIZE = 4096;
            byte[] buffer = new byte[BUFFER_SIZE];
            long[] freq = new long[256];
            int bytesRead;
            while((bytesRead = inputStream.Read(buffer, 0, BUFFER_SIZE)) > 0)
            {
                for (int i = 0; i < bytesRead; i++)
                    freq[buffer[i]] += 1;
            }

            return BuildTree(freq);
        }

        /// <summary>Build huffmann tree from byte frequency array</summary>
        public static HuffmannTree BuildTree(long[] freq)
        {
            List<HuffmannTree> forest = new List<HuffmannTree>();
            for (int i = 0; i < 256; i++)
            {
                if (freq[i] > 0)
                    forest.Add(new HuffmannTree {Left = null, Right = null, Symbol = (byte)i, Weight = freq[i]});
            }

            if (forest.Count == 0)
                return null;

            // initial leaf ordering
            forest = forest.OrderBy(node => node.Weight).ThenBy(node => node.Symbol).ToList();

            
            while (forest.Count > 1)
            {
                HuffmannTree parent = new HuffmannTree();
                parent.Left = forest[0];
                parent.Right = forest[1];
                parent.Weight = parent.Left.Weight + parent.Right.Weight;

                forest.RemoveRange(0, 2);
                SortInsert(forest, parent);
            }

            return forest[0];
        }
    }
}