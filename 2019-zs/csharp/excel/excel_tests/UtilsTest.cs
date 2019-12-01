using excel_impl;
using NUnit.Framework;

namespace Tests
{
    public class UtilsTest
    {
        [Test]
        public void ConvertColToNumTest()
        {
            Assert.AreEqual("A", Utils.ConvertNumToCol(1));
            Assert.AreEqual("K", Utils.ConvertNumToCol(11));
            Assert.AreEqual("Z", Utils.ConvertNumToCol(26));
            Assert.AreEqual("AA", Utils.ConvertNumToCol(27));
            Assert.AreEqual("AB", Utils.ConvertNumToCol(28));
            Assert.AreEqual("AZ", Utils.ConvertNumToCol(52));
            Assert.AreEqual("BA", Utils.ConvertNumToCol(53));
            Assert.AreEqual("CA", Utils.ConvertNumToCol(79));
            Assert.AreEqual("ZZ", Utils.ConvertNumToCol(702));
            Assert.AreEqual("AAA", Utils.ConvertNumToCol(703));
            Assert.AreEqual("AAB", Utils.ConvertNumToCol(704));
        }

        /*
        [Test]
        public void ConvertNumToColTest()
        {
            Assert.AreEqual(1, Utils.ConvertColToNum("A"));
            Assert.AreEqual(11, Utils.ConvertColToNum("K"));
            Assert.AreEqual(26, Utils.ConvertColToNum("Z"));
            Assert.AreEqual(27, Utils.ConvertColToNum("AA"));
            Assert.AreEqual(28, Utils.ConvertColToNum("AB"));
            Assert.AreEqual(52, Utils.ConvertColToNum("AZ"));
            Assert.AreEqual(53, Utils.ConvertColToNum("BA"));
            Assert.AreEqual(703, Utils.ConvertColToNum("AAA"));
            Assert.AreEqual(704, Utils.ConvertColToNum("AAB"));
            
        }
        */


        [Test]
        public void IsIntegerTest()
        {
            Assert.IsTrue(Utils.IsInteger("0"));
            Assert.IsTrue(Utils.IsInteger("1"));
            Assert.IsTrue(Utils.IsInteger("10"));
            Assert.IsTrue(Utils.IsInteger("-5657"));
            Assert.IsFalse(Utils.IsInteger(""));
            Assert.IsFalse(Utils.IsInteger("0.0"));
            Assert.IsFalse(Utils.IsInteger("3.14"));
            Assert.IsFalse(Utils.IsInteger("3424324 234324"));
            Assert.IsFalse(Utils.IsInteger("=34"));
            Assert.IsFalse(Utils.IsInteger("auto"));
            Assert.IsFalse(Utils.IsInteger("\n"));
        }

        [Test]
        public void IsValidCellKeyTest()
        {
            Assert.IsTrue(Utils.IsValidCellKey("B132"));
            Assert.IsTrue(Utils.IsValidCellKey("BA104"));
            Assert.IsTrue(Utils.IsValidCellKey("ZZX4"));
            Assert.IsTrue(Utils.IsValidCellKey("F34"));
            Assert.IsFalse(Utils.IsValidCellKey("b123"));
            Assert.IsFalse(Utils.IsValidCellKey("324"));
            Assert.IsFalse(Utils.IsValidCellKey("aB1"));
            Assert.IsFalse(Utils.IsValidCellKey("Ab143"));
            Assert.IsFalse(Utils.IsValidCellKey("AB"));
            Assert.IsFalse(Utils.IsValidCellKey("AB0"));
            Assert.IsFalse(Utils.IsValidCellKey("AB01"));
            Assert.IsFalse(Utils.IsValidCellKey("1B"));
            Assert.IsFalse(Utils.IsValidCellKey("A1B"));
            Assert.IsFalse(Utils.IsValidCellKey("ZZ1b"));
            Assert.IsFalse(Utils.IsValidCellKey(""));
            Assert.IsFalse(Utils.IsValidCellKey("AB-123"));

            // Extension
            Assert.IsTrue(Utils.IsValidCellKey("Sesit!AB34"));
            Assert.IsTrue(Utils.IsValidCellKey("List1!B1"));
            Assert.IsTrue(Utils.IsValidCellKey("test-list!B1"));
            Assert.IsTrue(Utils.IsValidCellKey("test_list!B1"));
            Assert.IsTrue(Utils.IsValidCellKey("List2!A2"));
            Assert.IsTrue(Utils.IsValidCellKey("asbc!B3344"));
            Assert.IsFalse(Utils.IsValidCellKey("!AB34"));
            Assert.IsFalse(Utils.IsValidCellKey("Aser!!AB34"));
            Assert.IsFalse(Utils.IsValidCellKey("Aser!AB"));
        }
    }
}