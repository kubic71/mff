using System;
using System.IO;
using System.Text;
using NUnit.Framework;
using MultiBlockAlignment;

namespace MultiBlockAlignment.Tests
{
    public class AlignerUnitTests
    {
        [SetUp]
        public void Setup()
        {
            Console.WriteLine("Copy ex{n}.out files to compile directory!");
        }

        [Test]
        public void Test1()
        {
            // Batch.exe --highlight-spaces 01.in ex01.out 17
        
            string[] files = new string[] {"01.in"};
            IReader reader = new MultifileReader(files);
            Aligner aligner = new Aligner(reader, "ex01_actual.out", 17, true);
            aligner.Process();
            
            Assert.AreEqual(ReadFile("ex01.out"), ReadFile("ex01_actual.out"));
        }
        
        [Test]
        public void Test2()
        {
            // Batch.exe --highlight-spaces 01.in 01.in 01.in ex02.out 17    
        
            string[] files = new string[] {"01.in", "01.in", "01.in"};
            IReader reader = new MultifileReader(files);
            Aligner aligner = new Aligner(reader, "ex02_actual.out", 17, true);
            aligner.Process();
            
            Assert.AreEqual(ReadFile("ex02.out"), ReadFile("ex02_actual.out"));
        }
        
        [Test]
        public void Test3()
        {
            // Batch.exe --highlight-spaces xx.in xx.in xx.in 01.in xx.in xx.in ex08.out 80
        
            string[] files = new string[] {"xx.in", "xx.in", "xx.in", "01.in", "xx.in", "xx.in"};
            IReader reader = new MultifileReader(files);
            Aligner aligner = new Aligner(reader, "ex08_actual.out", 80, true);
            aligner.Process();
            
            Assert.AreEqual(ReadFile("ex08.out"), ReadFile("ex08_actual.out"));
        }
        
        [Test]
        public void Test4()
        {
            // Batch.exe --highlight-spaces xx.in xx.in xx.in 01.in xx.in xx.in ex08.out 80
            string[] files = new string[] {"01.in", "01.in", "01.in"};
            IReader reader = new MultifileReader(files);
            Aligner aligner = new Aligner(reader, "ex12_actual.out", 17, false);
            aligner.Process();
            Assert.AreEqual(ReadFile("ex12.out"), ReadFile("ex12_actual.out"));
            
        }


        private string ReadFile(string filename)
        {
            StringBuilder output = new StringBuilder();
            StreamReader f = new StreamReader(filename);

            while (!f.EndOfStream)
            {
                output.Append(f.Read());
            }

            return output.ToString();
            
            f.Close();
        }
    }
}