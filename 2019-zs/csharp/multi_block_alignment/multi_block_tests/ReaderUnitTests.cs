using System.IO;
using System.Text;
using NUnit.Framework;
using MultiBlockAlignment;

namespace MultiBlockAlignment.Tests
{
    public class Tests
    {
        private string Test1Text = "Hello world!";
        
        [SetUp]
        public void Setup()
        {
            var f = new StreamWriter("test1.in");
            f.Write(Test1Text);
            f.Close();
            
        }

        [Test]
        public void Test1()
        {
            string[] files = new string[] {"test1.in"};
            IReader reader = new MultifileReader(files);


            Assert.AreEqual(Test1Text + " ", readWholeReader(reader));
        }
        
        
        [Test]
        public void Test2()
        {
            string[] files = new string[] {"test1.in", "test1.in", "test1.in"};
            IReader reader = new MultifileReader(files);


            Assert.AreEqual(Test1Text + " " + Test1Text + " " + Test1Text + " ", readWholeReader(reader));
        }
        
        [Test]
        public void Test3()
        {
            string[] files = new string[] {"test1.in", "doesnt_exist", "test1.in"};
            IReader reader = new MultifileReader(files);


            Assert.AreEqual(Test1Text + " " + Test1Text + " ", readWholeReader(reader));
        }
        
        
        [Test]
        public void Test4()
        {
            string[] files = new string[] {"doesnt_exist", "doesnt_exist", "doesnt_exist"};
            IReader reader = new MultifileReader(files);


            Assert.AreEqual(" ", readWholeReader(reader));
        }
        
        [Test]
        public void Test5()
        {
            string[] files = new string[] {"doesnt_exist"};
            IReader reader = new MultifileReader(files);


            Assert.AreEqual(" ", readWholeReader(reader));
        }
        
        [Test]
        public void Test6()
        {
            string[] files = new string[] {"01.in"};
            IReader reader = new MultifileReader(files);


            Assert.AreEqual("If a train station is where the train stops, what is a work station? \n ", readWholeReader(reader));
        }
        
        
        
        
        
        


        private string readWholeReader(IReader reader)
        {
            StringBuilder output = new StringBuilder();
            while (!reader.EndOfStream)
            {
                char c = (char)reader.ReadChar();
                output.Append((char) c);
            }

            return output.ToString();
        }
    }
}