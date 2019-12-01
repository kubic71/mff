using System.IO;
using System.Text;
using excel_impl;
using NUnit.Framework;

namespace Tests
{
    public class TableWriterTest
    {
        
        private static ExcelTable SetupTable1()
        {
            //A  B C  D
            string query = " A11 3 5 [] \n" +        // 1
                           " []  [] 43 B12*B3\n" +   // 2
                           " []  []  []   [] \n" +   // 3
                           " [] ";                   // 4

            ExcelTable table = new ExcelTable();
            TestUtils.SaveToFile(query, "Main.sheet");
            table.Load("Main.sheet");
            return table;
        }


        [Test]
        public void TestWriterTable1()
        {
            ExcelTable table1 = SetupTable1();
            
            MemoryStream ms = new MemoryStream();
            StreamWriter sw = new StreamWriter(ms);
            
            table1.WriteTo(sw);
            sw.Flush();
            sw.Close();

            string s = Encoding.ASCII.GetString(ms.ToArray());
            string expected = "A11 3 5 []\n" +
                              "[] [] 43 B12*B3\n" +
                              "[] [] [] []\n" +
                              "[]";
            
            Assert.AreEqual(expected, s);
        }

        private static ExcelTable SetupTable2()
        {
            //A  B C  D
            string query = "    \n" +        // 1
                           " [] \n" +   // 2
                           " 3 4 \n" +   // 3
                           " 5 =B23 ";                   // 4

            ExcelTable table = new ExcelTable();
            TestUtils.SaveToFile(query, "Main.sheet");
            table.Load("Main.sheet");
            return table;
        }
        
        [Test]
        public void TestWriterTable2()
        {
            ExcelTable table1 = SetupTable2();
            
            MemoryStream ms = new MemoryStream();
            StreamWriter sw = new StreamWriter(ms);
            
            table1.WriteTo(sw);
            sw.Flush();
            sw.Close();

            string s = Encoding.ASCII.GetString(ms.ToArray());
            string expected = "\n" +
                              "[]\n" +
                              "3 4\n" +
                              "5 =B23";
            
            Assert.AreEqual(expected, s);
        }
    }
}