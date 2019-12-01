using System;

namespace excel_impl
{
    public static class Tokenizer
    {
        public static string[] Tokenize(string line)
        {
            return line.Split(new []{" "}, StringSplitOptions.RemoveEmptyEntries);
        }
    }
}