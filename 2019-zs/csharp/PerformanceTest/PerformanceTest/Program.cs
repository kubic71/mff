using System;
using System.Collections.Generic;
using System.Text;

namespace PerformanceTest
{
    public class TableCell
    {

        public bool evaluated = false;


        public const string INVVAL = "I";
        public const string MISSOP = "M";
        public const string ERROR = "E";
        public const string DIV0 = "D";
        public const string CYCLE = "C";
        public const string FORMULA = "F";
        
        public string content { get; set; }

        // helper data item used during evaluation
//        public string val { get; set; }
    }
    
    
    public struct TableCellStrc
    {

        public bool evaluated;


        public const string INVVAL = "I";
        public const string MISSOP = "M";
        public const string ERROR = "E";
        public const string DIV0 = "D";
        public const string CYCLE = "C";
        public const string FORMULA = "F";
        
        public string content { get; set; }

        // helper data item used during evaluation
//        public string val { get; set; }
    }
    
    class Program
    {
        static void Main(string[] args)
        {
            string mode = "string";
            if (mode == "class") {
            Dictionary<string, TableCell> table = new Dictionary<string, TableCell>();
            for (int i = 0; i < Int32.Parse(args[0]); i++)
            {
                TableCell cell = new TableCell();
                cell.content = i.ToString();
                table[i.ToString()] = cell;
            }

            Console.WriteLine("Press enter to exit...");
            while (true)
            {
            }

            Console.Read();
            }
            else if (mode == "struct")
            {
                Dictionary<string, TableCellStrc> table = new Dictionary<string, TableCellStrc>();
                for (int i = 0; i < Int32.Parse(args[0]); i++)
                {
                    TableCellStrc cell = new TableCellStrc();
                    cell.evaluated = false;
                    cell.content = i.ToString();
                    table[i.ToString()] = cell;
                }

                Console.WriteLine("Press enter to exit...");
                while (true)
                {
                    
                }
            } else if (mode == "list")
            {
                List<TableCell> table = new List<TableCell>();
                for (int i = 0; i < Int32.Parse(args[0]); i++)
                {
                    TableCell cell = new TableCell();
                    cell.content = i.ToString();
                    table.Add(cell);
                }

                Console.WriteLine("Press enter to exit...");
                while (true)
                {
                    
                }
            } else if (mode == "array")
            {
                int n = Int32.Parse(args[0]);
                TableCell[] table = new TableCell[n];
                for (int i = 0; i < n; i++)
                {
                    TableCell cell = new TableCell();
                    cell.content = i.ToString();
                    table[i] = cell;
                }

                Console.WriteLine("Press enter to exit...");
                while (true)
                {
                    
                }
            } else if (mode == "string")
            {
                string str = "";
                int n = Int32.Parse(args[0]);
                TableCell[] table = new TableCell[n];
                for (int i = 0; i < n; i++)
                {
                    str += i.ToString();
                }
                

                Console.WriteLine("Press enter to exit...");
                while (true)
                {
                    
                }
            }
            
            
        }
    }
}