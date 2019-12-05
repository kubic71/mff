using System.Collections.Generic;
using System.IO;
using excel_impl;
using NUnit.Framework;

namespace Tests
{
    public class TableLoaderTest
    {



        public static TableData SetupTable1()
        {
            //A  B C  D
            string query = " A11 3 5 [] \n" + // 1
                           "=B12*B3 =2rs5 =34*BAc\n" + // 2
                           " []  [] \n";   // 3
                           
            TestUtils.SaveToFile(query, "Main.sheet");
            Dictionary<int, string> hashToString  = new Dictionary<int, string>();
            return TableFileLoader.Load("Main.sheet", hashToString);
        }

        [Test]
        public void TestContentTable1()
        {
            TableData table = SetupTable1();
            
            Assert.AreEqual(Error.INVVAL, table.GetCell(1, 1).Status);
            Assert.AreEqual(3, table.GetCell(1, 2).Val);
            Assert.AreEqual(Error.OK, table.GetCell(1, 2).Status);
            Assert.AreEqual(true, table.GetCell(1, 2).IsEvaluated());
            Assert.AreEqual(0, table.GetCell(1, 4).Val);
            Assert.AreEqual(Error.OK, table.GetCell(1, 4).Status);
            
            
            Assert.AreEqual(Error.OK, table.GetCell(2, 1).Status);
            Assert.AreEqual(Error.MISSOP, table.GetCell(2, 2).Status);
            Assert.AreEqual(Error.FORMULA, table.GetCell(2, 3).Status);
        }
        
        public static TableData SetupTable2()
        {
            string query = "=B12*B3";
            TestUtils.SaveToFile(query, "Main.sheet");
            Dictionary<int, string> hashToString  = new Dictionary<int, string>();
            return TableFileLoader.Load("Main.sheet", hashToString);
        }

        [Test]
        public void TestContentTable2()
        {
            TableData table = SetupTable2();

            Assert.AreEqual(Error.OK, table.GetCell(1, 1).Status);

        }
        
    }
    
    
}
