using System;
using System.Collections.Generic;
using System.IO;

namespace excel_impl
{
    public enum Error {OK, INVVAL, MISSOP, FORMULA, DIV0, CYCLE, ERROR};

    
    
    public interface ICell
    {
        bool IsEvaluated();

        int Val { get; set; }
        Error Status { get; set; }
    }

    public class EmptyCell : ICell
    {
        bool ICell.IsEvaluated()
        {
            return true;
        }

        public int Val
        {
            get { return 0; }
            set { throw new NotImplementedException(); }
        }

        public Error Status
        {
            get { return Error.OK; }
            set { throw new NotImplementedException(); }
        }
    }

    public class ValueCell : ICell
    {
        public int Val { get; set; }
        public Error Status { get; set; }

        public bool IsEvaluated()
        {
            return true;
        }
    }

    
    
    public struct Link
    {
        public int sheetHash;
        public int Row;
        public int Col;
    }
    
    public class FormulaCell : ICell
    {
        public static int Divide(int x, int y)
        {
            return x / y;
        }
        
        public static int Add(int x, int y)
        {
            return x + y;
        }
        
        public static int Substract(int x, int y)
        {
            return x - y;
        }
        
        public static int Multiply(int x, int y)
        {
            return x * y;
        }
        
        
        public FormulaCell()
        {
        }
        public const char NO_OP = '0';
        public const int SHEET_RELATIVE = 0;   // hash code of relative link sheetHash
        public bool Evaluated = false;
        public int Val { get; set; }
        public Error Status { get; set; }
        
        public Link[] Operands;
        public char Operator = NO_OP;

        public int GetVal(int v1, int v2)
        {
            switch (Operator) 
            {
                case '+':
                    return v1 + v2;
                case '-':
                    return v1 - v2;
                case '*':
                    return v1 * v2;
                case '/':
                    return v1 / v2;
                default:
                    throw new NotImplementedException();
            }
        }

        public bool IsEvaluated()
        {
            return Evaluated;
        }
    } 
    
    
    
    
    public static class TableFileLoader
    {
        public static TableData Load(string filename, Dictionary<int, string> sheetHashToString)
        {
            TableData sheet = new TableData();
            string line;
            StreamReader inputFile = new StreamReader(filename);
            while ((line = inputFile.ReadLine()) != null)
            {
                string[] tokens = Tokenizer.Tokenize(line);
                ICell[] row = new ICell[tokens.Length];
                for (int i = 0; i < tokens.Length; i++)
                {
                    row[i] = TokenToCell(tokens[i], sheetHashToString);
                }
                
                sheet.AddRow(row);
            }

            return sheet;
        }

        // return EmptyCell, ValueCell or FormulaCell based on string token
        public static ICell TokenToCell(string token, Dictionary<int, string> sheetHashToString)
        {
            // cell needs no further evaluation
            if (token == "[]")
            {
                return new EmptyCell();
            }
            
            
            
            if (Int32.TryParse(token, out int parsed))
            {
                ValueCell cell = new ValueCell();
                cell.Status = Error.OK;
                cell.Val = parsed;
                return cell;
            }

            if (token[0] == '=') // Is some kind of formula
            {
                FormulaCell cell = new FormulaCell();

                
                if (token.Contains('+'))
                {
                    cell.Operator = '+';
                }
                else if (token.Contains('-'))
                {
                    cell.Operator = '-';
                }
                else if (token.Contains('*'))
                {
                    cell.Operator = '*';
                }
                else if (token.Contains('/'))
                {
                    cell.Operator = '/';
                }

                if (cell.Operator == FormulaCell.NO_OP) // formula doesn't contain an operator
                {
                    cell.Status = Error.MISSOP;
                    cell.Evaluated = true;
                    return cell;
                }

                string[] operands = TableFileLoader.GetOperands(token, cell.Operator);
                if (operands == null)
                {
                    // formula syntax error
                    cell.Status = Error.FORMULA;
                    cell.Evaluated = true;
                    return cell;
                }

                cell.Operands = new Link[2];

                for (int i = 0; i < operands.Length; i++)
                {
                    if (operands[i].Contains('!'))
                    {
                        string[] parts = operands[i].Split('!');
                        string addr = parts[1];
                        cell.Operands[i].sheetHash = parts[0].GetHashCode();
                        sheetHashToString[cell.Operands[i].sheetHash] = parts[0];
                        Utils.GetRowColFromAddr(addr, out int row, out int col);
                        cell.Operands[i].Row = row;
                        cell.Operands[i].Col = col;
                    }
                    else
                    {
                        cell.Operands[i].sheetHash = 0;
                        Utils.GetRowColFromAddr(operands[i], out int row, out int col);
                        cell.Operands[i].Row = row;
                        cell.Operands[i].Col = col;
                    } 
                }
                
                return cell;
            }
            
            // not a formula, not an empty cell
            ValueCell invalidCell = new ValueCell();
            invalidCell.Status = Error.INVVAL;
            return invalidCell;
        }
                
        
        /// <summary>
        /// Returns two operands, or null, if formula is invalid
        /// Method already assumes, that formula contains given operator
        /// </summary>
        /// <param name="formula"></param>
        /// <param name="op"></param>
        private static string[] GetOperands(string formula, char op)
        {
            
            string[] operands = formula.Substring(1).Split(op);

            if (operands.Length == 2 && Utils.IsValidCellKey(operands[0]) && Utils.IsValidCellKey(operands[1]))
            {
                return operands;
            }

            return null;
        }
    }
}