using System;
using System.Linq;
using System.Runtime.InteropServices;
using System.Threading;
using System.Xml.Serialization;

namespace ZapoctovyTest
{
    public class InteractiveInterface
    {
        private TypeData data;
        public InteractiveInterface(TypeData data)
        {
            this.data = data;
        }

        // starts interactive mode
        public void Start()
        {
            string line;
            while ((line = Console.ReadLine()) != null)
            {
                if (line.Trim() == "")
                {
                    Console.WriteLine();
                    continue;
                }

                ParseCommandLine(line, out string targetType, out string[] inputTypes);

                string type;
                if ((type = GetFirstUnknownType(targetType, inputTypes)) != null)
                {
                    Console.WriteLine($"Cannot find type {type}");
                    continue;
                }

                
                if (CheckChainRetyping(inputTypes) && data.CanAssign(inputTypes[inputTypes.Length - 1], targetType))
                {
                    Console.WriteLine($"Assignment {targetType} = {inputTypes[0]} is valid");
                }
                else
                {
                    Console.WriteLine($"Assignment {targetType} = {inputTypes[0]} is invalid");
                }
            }
        }

        private bool CheckChainRetyping(string[] inputTypes)
        {
            for (int i = 0; i < inputTypes.Length - 1; i++)
            {
                var from = inputTypes[i];
                var to = inputTypes[i+1];

                if (!data.CanRetype(from, to))
                {
                    Console.WriteLine($"Debub: Cannot retype {from} to {to}");
                    return false;
                }
            }

            return true;
        }

        private string GetFirstUnknownType(string targetType, string[] inputTypes)
        {
            if (!IsTypeKnown(targetType))
                return targetType;

            foreach (var type in inputTypes)
            {
                if (!IsTypeKnown(type))
                    return type;
            }

            return null;
        }

        private TypeNode GetType(string type)
        {
            return data.typeMap[type];
        }

        private bool IsTypeKnown(string type)
        {
            return data.typeMap.ContainsKey(type);
        }
        

        void ParseCommandLine(string line, out string targetType, out string[] inputTypes)
        {
            string[] parts = line.Trim().Split(' ');
            targetType = parts[0];
            inputTypes = parts.Skip(2).Reverse().ToArray();
        } 
    }
}