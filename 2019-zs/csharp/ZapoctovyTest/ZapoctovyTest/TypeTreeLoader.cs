using System;
using System.Collections.Generic;
using System.IO;

namespace ZapoctovyTest
{
    public class TypeTreeLoader
    {
        private TypeNode typeTree;
        private StreamReader inputStream;
        private Dictionary<string, TypeNode> typeMap; 
        private int lineNumber;
        private int errors;
        
        public TypeTreeLoader(string fileName)
        {    
            typeTree = new TypeNode();
            typeTree.Name = "Object";
            
            inputStream = new StreamReader(fileName);
            errors = 0;
            
            typeMap = new Dictionary<string, TypeNode>();
            typeMap.Add("Object", typeTree);
            
        }
        

        public TypeData Load()
        {
            string line;
            lineNumber = 1;
            while ((line = inputStream.ReadLine()) != null)
            {
                ProcessLine(line);
                lineNumber++;
            }

            inputStream.Close();

            PrintNumberOfErrors();
            
            TypeData data = new TypeData();
            data.tree = typeTree;
            data.typeMap = typeMap;

            if (errors > 0)
            {
                return null;
            }
            return data;
        }

        private void PrintNumberOfErrors()
        {
            if (errors > 0)
            {
                Console.WriteLine($"{errors} errors. Stopping.");
            }
        }

        private bool CheckTypeAlreadyExists(string typeName)
        {
            if (typeMap.ContainsKey(typeName))
            {
                TypeNode type = typeMap[typeName];
                Console.WriteLine($"{lineNumber}: Duplicate type {type.Name}. First declared on line {type.LineDeclared}");
                errors += 1;
                return true;
            }
            else
            {
                return false;
            }
        }

        private bool CheckBaseTypeAlreadyExists(string baseName)
        {
            if (typeMap.ContainsKey(baseName))
            {
                return true;
            }
            else
            {
                Console.WriteLine($"{lineNumber}: Non existing base type {baseName}");
                errors += 1;
                return false;
            }
        }


        private void AddType(string typeName)
        {
            AddType(typeName, "Object");
        }
        private void AddType(string typeName, string predName)
        {
            TypeNode node = new TypeNode();
            node.LineDeclared = lineNumber;
            node.Name = typeName;
            node.Predecessor = typeMap[predName];
            typeMap.Add(typeName, node);
        }


        private void ProcessLine(string line)
        {
            if (line.Contains(":"))
            {
                string[] parts = line.Split(':');
                string typeName = parts[0].Trim();
                string predName = parts[1].Trim();
                
                if (!CheckTypeAlreadyExists(typeName) && CheckBaseTypeAlreadyExists(predName))
                {
                    AddType(typeName, predName);
                }
            }
            else
            {
                string typeName = line.Trim();
                
                if (!CheckTypeAlreadyExists(typeName))
                {
                    AddType(typeName);
                }
            }
        }
    }
}