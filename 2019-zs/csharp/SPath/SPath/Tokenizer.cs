using System;
using System.IO;

namespace SPath
{
    public static class Tokenizer
    {
        public static readonly char[] WHITESPACE = new char[] {' ', '\t', '\n'};

        public static string[] Tokenize(StreamReader input)
        {
            return input.ReadToEnd().Split(WHITESPACE, StringSplitOptions.RemoveEmptyEntries);
        }
    }
}