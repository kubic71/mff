using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Runtime.CompilerServices;
using System.Xml.Xsl;

namespace huffmann
{
    
    

    class Program
    {

        static void Main(string[] args)
        {
            // check cmd args
            if (args.Length != 1 || args[0] == "")
            {
                Console.WriteLine("Argument Error");
                return;
            }

            
            try
            {
                FileStream fs = new FileStream(args[0], FileMode.Open);
                HuffmannTree huffmannTree = HuffmannTree.BuildTree(fs);
                Console.Write(huffmannTree.GetStringRepresentation());
            }
            
            catch (Exception ex)            
            {
                if (ex is IOException || ex is UnauthorizedAccessException)
                {
                    Console.WriteLine("File Error");
                    return;
                }

                throw;
            }
        }
    }
}
