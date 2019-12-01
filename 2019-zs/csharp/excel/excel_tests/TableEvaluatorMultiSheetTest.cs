using System.IO;
using excel_impl;
using NUnit.Framework;

namespace Tests
{
    public static class TableEvaluatorMultiSheetTest
    {
        private static ExcelTable SetupTables1()
        {
            //A  B C  D
            string mainTable = "1 =A2+A1\n" +
                               "-10 =List1!B1*List1!A1 =A1+List3!A10";
            string sheet1 = "=B1*A2 3 \n" +
                            "4     1 \n";
            string sheet2 = "1000 23";
            string sheet3 = "[]";

            TestUtils.SaveToFile(mainTable, "Main.sheet");
            TestUtils.SaveToFile(sheet1, "List1.sheet");
            TestUtils.SaveToFile(sheet2, "List2.sheet");
            TestUtils.SaveToFile(sheet3, "List3.sheet");


            ExcelTable table = new ExcelTable();
            table.Load("Main.sheet");


            return table;
        }

        [Test]
        public static void EvaluateTableTest1()
        {
            ExcelTable table = SetupTables1();
            table.Evaluate();
            string expected = "1 -9\n" +
                              "-10 36 1";
            Assert.AreEqual(expected, table.ToString());
        }
        
        private static ExcelTable SetupTablesCycle()
        {
            //A  B C  D
            string mainTable = "=List1!A1+A123\n";
            string sheet1 = "=List2!A1+B234 \n";
            string sheet2 = "=List3!A1+B3432";
            string sheet3 = "=Main!A1+A123";

            TestUtils.SaveToFile(mainTable, "Main.sheet");
            TestUtils.SaveToFile(sheet1, "List1.sheet");
            TestUtils.SaveToFile(sheet2, "List2.sheet");
            TestUtils.SaveToFile(sheet3, "List3.sheet");


            ExcelTable table = new ExcelTable();
            table.Load("Main.sheet");
            return table;
        }

        [Test]
        public static void EvaluateTableTestCycle()
        {
            ExcelTable table = SetupTablesCycle();
            table.Evaluate();
            string expected = "#CYCLE";
            Assert.AreEqual(expected, table.ToString());
        }
    }
}