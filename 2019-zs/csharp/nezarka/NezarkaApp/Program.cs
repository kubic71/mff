using System;
using System.IO;
using NezarkaApp.Controllers;
using NezarkaModels;

namespace NezarkaApp
{
    class Program
    {
        static void Main(string[] args)
        {
            

            TextReader stdin = new StreamReader(Console.OpenStandardInput(), Console.InputEncoding);
            ModelStore modelStore = ModelStore.LoadFrom(stdin);
            if (modelStore == null)
            {
                Console.WriteLine("Data error.");
                return;
            }
            

            NezarkaDispatcher dispatcher = new NezarkaDispatcher(modelStore);

            string command;
            while((command = stdin.ReadLine()) != null)
            {
                dispatcher.Dispatch(command);
                Console.WriteLine("====");
            }
            
            

        }
    }
}