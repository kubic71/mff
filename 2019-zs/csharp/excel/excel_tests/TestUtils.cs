using System.IO;

namespace Tests
{
    public static class TestUtils
    {
        public static void SaveToFile(string content, string filename)
        {
            StreamWriter writer = new StreamWriter(filename);
            writer.Write(content);
            writer.Close();
        }
    }
}