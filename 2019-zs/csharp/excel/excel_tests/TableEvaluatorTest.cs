using excel_impl;
using NUnit.Framework;

namespace Tests
{
    public class TableEvaluatorTest
    {
        private static ExcelTable SetupTable1()
        {
            string query = "1 3 4 Příliš žluťoučký kůň úpěl ďábelské ódy\n" +
                           "1 234 []\n" +
                           "10 0 [] 0";
            ExcelTable table = new ExcelTable();
            TestUtils.SaveToFile(query, "Main.sheet");
            table.Load("Main.sheet");
            return table;
        }

        [Test]
        public static void EvaluateTableTest1()
        {
            ExcelTable table = SetupTable1();
            string expected = "1 3 4 #INVVAL #INVVAL #INVVAL #INVVAL #INVVAL #INVVAL\n" +
                              "1 234 []\n" +
                              "10 0 [] 0";
            table.Evaluate();
            Assert.AreEqual(expected, table.ToString());
        }


        private static ExcelTable SetupTable2()
        {
            //A  B C  D
            string query = "[] 3 =B1*A2\n" +
                           "19 =C1+C2 42\n" +
                           "auto\n" +
                           "=B2/A1 =A1-B4 =C2+A4\n" +
                           "=chyba =A1+autobus";

            ExcelTable table = new ExcelTable();
            TestUtils.SaveToFile(query, "Main.sheet");
            table.Load("Main.sheet");
            return table;
        }

        [Test]
        public static void EvaluateTableTest2()
        {
            ExcelTable table = SetupTable2();
            table.Evaluate();
            string expected = "[] 3 57\n" +
                              "19 99 42\n" +
                              "#INVVAL\n" +
                              "#DIV0 #CYCLE #ERROR\n" +
                              "#MISSOP #FORMULA";
            Assert.AreEqual(expected, table.ToString());
        }


        private static ExcelTable SetupTable3()
        {
            string query = "#ERROR #DIV0 #CYCLE #MISSOP #FORMULA #INVVAL";
            ExcelTable table = new ExcelTable();
            TestUtils.SaveToFile(query, "Main.sheet");
            table.Load("Main.sheet");
            return table;
        }

        [Test]
        public static void EvaluateTableTest3()
        {
            ExcelTable table = SetupTable3();
            table.Evaluate();
            string expected = "#INVVAL #INVVAL #INVVAL #INVVAL #INVVAL #INVVAL";

            Assert.AreEqual(expected, table.ToString());
        }

        private static ExcelTable SetupTable4()
        {
            string query = "1 = 3\n";
            ExcelTable table = new ExcelTable();
            TestUtils.SaveToFile(query, "Main.sheet");
            table.Load("Main.sheet");
            return table;
        }

        [Test]
        public static void EvaluateTableTestNewlineAtTheEnd()
        {
            ExcelTable table = SetupTable4();
            table.Evaluate();
            // TODO should output have newline at the end as the input?
            string expected = "1 #MISSOP 3";

            Assert.AreEqual(expected, table.ToString());
        }

        
        

        private static ExcelTable SetupTable5()
        {
            //A  B C  D
            string query = "=A2+A3243 =B2*A3\n" +
                           "=B1*B123 =A2*C3 42\n" +
                           "3";

            ExcelTable table = new ExcelTable();
            TestUtils.SaveToFile(query, "Main.sheet");
            table.Load("Main.sheet");
            return table;
        }

        [Test]
        public static void EvaluateTableTest5()
        {
            ExcelTable table = SetupTable5();
            table.Evaluate();
            string expected = "#ERROR #CYCLE\n" +
                              "#CYCLE #CYCLE 42\n" +
                              "3";
            Assert.AreEqual(expected, table.ToString());
        }
        
        
        
        private static ExcelTable SetupTableCycleSimple()
        {
            //A  B C  D
            string query = "=B1+A123 =A1+A123\n";
            ExcelTable table = new ExcelTable();
            TestUtils.SaveToFile(query, "Main.sheet");
            table.Load("Main.sheet");
            return table;
        }

        [Test]
        public static void EvaluateTableTestCycleSimple()
        {
            ExcelTable table = SetupTableCycleSimple();
            table.Evaluate();
            string expected = "#CYCLE #CYCLE";
            Assert.AreEqual(expected, table.ToString());
        }
    }
}