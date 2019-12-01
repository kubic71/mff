using System.IO;
using excel_impl;
using NUnit.Framework;

namespace Tests
{
    public class TableLoaderTest
    {



        public static ExcelTable SetupTable1()
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
        public void TestContentTable1()
        {
            ExcelTable table = SetupTable1();
            
            Assert.AreEqual("A11", table.GetCell("Main!A1").content);
            Assert.AreEqual("A11", table.GetCell(1, 1).content);
            Assert.AreEqual("3", table.GetCell("Main!B1").content);
            Assert.AreEqual("3", table.GetCell(1, 2).content);
            Assert.AreEqual("5", table.GetCell("Main!C1").content);
            Assert.AreEqual("5", table.GetCell(1, 3).content);
            Assert.AreEqual("[]", table.GetCell("Main!D1").content);
            Assert.AreEqual("[]", table.GetCell(1,4).content);
            
            Assert.AreEqual("[]", table.GetCell("Main!A2").content);
            Assert.AreEqual("[]", table.GetCell(2, 1).content);
            Assert.AreEqual("[]", table.GetCell("Main!B2").content);
            Assert.AreEqual("[]", table.GetCell(2,2).content);
            Assert.AreEqual("43", table.GetCell("Main!C2").content);
            Assert.AreEqual("43", table.GetCell(2,3).content);
            Assert.AreEqual("B12*B3", table.GetCell("Main!D2").content);
            Assert.AreEqual("B12*B3", table.GetCell(2,4).content);
            
            Assert.AreEqual("[]", table.GetCell("Main!A3").content);
            Assert.AreEqual("[]", table.GetCell(3,1).content);
            Assert.AreEqual("[]", table.GetCell("Main!B3").content);
            Assert.AreEqual("[]", table.GetCell(3,2).content);
            Assert.AreEqual("[]", table.GetCell("Main!C3").content);
            Assert.AreEqual("[]", table.GetCell(3,3).content);
            Assert.AreEqual("[]", table.GetCell("Main!D3").content);
            Assert.AreEqual("[]", table.GetCell(3,4).content);
            
            Assert.AreEqual("[]", table.GetCell("Main!A4").content);
            Assert.AreEqual("[]", table.GetCell(4,1).content);
            Assert.AreEqual(null, table.GetCell("Main!B4"));
            Assert.AreEqual(null, table.GetCell(4,2));
            Assert.AreEqual(null, table.GetCell("Main!AZC3"));
            Assert.AreEqual(null, table.GetCell("Main!AXD1234"));
            
            Assert.AreEqual(null, table.GetCell(-1, 1));
            Assert.AreEqual(null, table.GetCell(3, -100));
            Assert.AreEqual(null, table.GetCell(-342, -341));
            Assert.AreEqual(null, table.GetCell(43, 2));
            Assert.AreEqual(null, table.GetCell(3, 243));

            Assert.IsTrue(table.cols == 4 && table.rows == 4);

        }
    }
}
