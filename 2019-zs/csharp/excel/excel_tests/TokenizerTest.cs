using System.Linq;
using excel_impl;
using NUnit.Framework;

namespace Tests
{
    public class TokenizerTests
    {
        [SetUp]
            public void Setup()
        {
        }

        [Test]
        public void Test1()
        {
            var truth = new string[] {"one", "two", "three"};
            var tokens = Tokenizer.Tokenize("    one   two  three  ");
            Assert.True(tokens.SequenceEqual(truth));
        }
        
        [Test]
        public void Test2()
        {
            var truth = new string[] {"A11*B21", "A11/B2", "3", "B32*A4"};
            var tokens = Tokenizer.Tokenize("      A11*B21 A11/B2  3  B32*A4");
            Assert.True(tokens.SequenceEqual(truth));
        }
    }
}