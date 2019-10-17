using System;
using System.IO;

namespace _1
{

    class Reader
    {
        string str;
        int index;
        public Reader(string str)
        {
            this.str = str;
            index = 0;
        }

        bool isSpace(char s)
        {
            return s == ' ' || s == '\t' || s == '\n';
        }

        public string get_word()
        {
            if (index >= str.Length)
            {
                return null;
            }

            string word = "";

            // skip spaces
            while (isSpace(str[index]))
            {
                index++;
                if (index >= str.Length)
                {
                    return null;
                }
            }

            while (!isSpace(str[index]))
            {
                word += str[index];
                index++;

                if (index >= str.Length)
                {
                    return word;
                }
            }

            return word;
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            if (args.Length != 1)
            {
                Console.WriteLine("Argument Error");
                return;
            }


            try
            {
                using (StreamReader file = new StreamReader(args[0]))
                {
                    int counter = 0;
                    string ln;

                    while ((ln = file.ReadLine()) != null)
                    {

                        Reader reader = new Reader(ln);
                        string word = reader.get_word();

                        while (word != null)
                        {
                            // Console.WriteLine(word);
                            counter++;
                            word = reader.get_word();
                        }
                    }

                    file.Close();

                    Console.WriteLine(counter);
                }
            } catch (IOException) {
                Console.WriteLine("File Error");
            }
        }
    }
}
