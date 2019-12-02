using System;
using System.IO;
using System.Text;

namespace excel_impl
{
    class Program
    {
        public static void ExecuteExcel(string[] args)
        {
            if (args.Length != 2)
            {
                Console.WriteLine("Argument Error");
                return;
            }

            try
            {
                ExcelTable table = new ExcelTable();
                table.Load(args[0]);

                table.Evaluate();

                
                StreamWriter writer = new StreamWriter(args[1]);
                table.WriteTo(writer);
                writer.Close();
            }
            catch (Exception ex)
            {
                if (Utils.IsFileErrorException(ex))
                {
                    Console.WriteLine("File Error");
                    return;
                }

                throw;
            }
            
            
        }

        static void Main(string[] args)
        {
            ExecuteExcel(args);
        }
    }
}