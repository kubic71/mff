using System;

namespace ZapoctovyTest
{
    class Program
    {
        static void Main(string[] args)
        {
            if (args.Length != 1)
            {
                Console.WriteLine("Usage: Program.exe typesFile");
                return;
            }

            TypeTreeLoader loader = new TypeTreeLoader(args[0]);
            TypeData data = loader.Load();
            if (data == null)
                return;
            
            InteractiveInterface ui = new InteractiveInterface(data);
            ui.Start();
            
            


        }
    }
}