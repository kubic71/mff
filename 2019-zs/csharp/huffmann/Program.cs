﻿using System;
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
                
                FileStream outputFile = new FileStream(args[0] + ".huff", FileMode.Create);
                
                outputFile.Write(new byte[]{0x7B, 0x68, 0x75, 0x7C, 0x6D, 0x7D, 0x66, 0x66}); // write header
                huffmannTree.PrintTree(outputFile, true);
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
