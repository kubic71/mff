using System;
using System.Collections.Generic;
using System.Security.Cryptography.X509Certificates;

namespace ZapoctovyTest
{
    public class TypeData
    {
        public Dictionary<string, TypeNode> typeMap { get; set; }
        public TypeNode tree { get; set; }

        public bool CanAssign(string from, string to)
        {
            // from = Y ; to = X
            // X = Y <=> X == Y || X is Predecessor of Y
            return from == to || IsPredecessor(from, to); 
        }

        public bool IsPredecessor(string type, string predecessor)
        {
            TypeNode current = typeMap[type];
            while (true)
            {
                if (current.Name == predecessor)
                    return true;

                if (current.Predecessor == null)
                {
                    return false;
                }

                current = current.Predecessor;
            }
        }

        public bool CanRetype(string from, string to)
        {
            return from == to || CanAssign(to, from) || IsPredecessor(from, to);
        }
        
    }
}