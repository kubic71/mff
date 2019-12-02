using System;
using System.IO;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text.RegularExpressions;

namespace excel_impl
{
    public class Utils
    {
        /// <summary>
        ///  Converts column index to Excel-like index (AB, BCZ...)
        /// Indexed from 1, eg. A is 1, B is 2...
        /// </summary>
        /// <param name="column"></param>
        /// <returns></returns>
        public static string ConvertNumToCol(int columnNumber)
        {
            int dividend = columnNumber;
            string columnName = "";
            int modulo;

            while (dividend > 0)
            {
                modulo = (dividend - 1) % 26;
                columnName = Convert.ToChar(65 + modulo).ToString() + columnName;
                dividend = (int) ((dividend - modulo) / 26);
            }

            return columnName;
        }


        public static int ConvertColToNum(string columnName)
        {
            int sum = 0;
            for (int i = 0; i < columnName.Length; i++)
            {
                sum *= 26;
                sum += (columnName[i] - 'A' + 1);
            }
            return sum;
        }
        
        public static StreamReader GenerateStreamReaderFromString(string s)
        {
            var stream = new MemoryStream();
            var writer = new StreamWriter(stream);
            writer.Write(s);
            writer.Flush();
            stream.Position = 0;
            return new StreamReader(stream);
        }

        public static string GetExcelIndex(int row, int col)
        {
            return ConvertNumToCol(col) + row.ToString();
        }


        public static void GetRowColFromAddr(string addr, out int row, out int col)
        {
            string[] addrParts = SplitAddress(addr);
            col = ConvertColToNum(addrParts[0]);
            row = Int32.Parse(addrParts[1]);
        }

        public static bool IsValidCellKey(string key)
        {
            var regex = new Regex(@"^[A-Z]+[1-9][0-9]*$");
            var regex2 = new Regex(@"^[A-Za-z0-9_-]+![A-Z]+[1-9][0-9]*$");
            return regex.Match(key).Success || regex2.Match(key).Success;
        }


        public static bool IsFileErrorException(Exception ex)
        {
            return ex is FileNotFoundException ||
                   ex is IOException ||
                   ex is UnauthorizedAccessException ||
                   ex is System.Security.SecurityException;
        }

        /// <summary>
        /// Given Excel-like address (eg. A34, BC9), return column and row separated, eg. ["A", "34"] or ["BC", "9"] 
        /// </summary>
        public static string[] SplitAddress(string addr)
        {
            int i = 0;
            while (true)
            {
                if ('0' <= addr[i] && addr[i] <= '9')
                {
                    break;
                }

                i++;
            }

            return new string[] {addr.Substring(0, i), addr.Substring(i, addr.Length - i)};
        }

        public static bool IsInteger(string n)
        {
            return Int32.TryParse(n, out int parsed);
        }
    }
}