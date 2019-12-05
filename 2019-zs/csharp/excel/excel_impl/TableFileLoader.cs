using System;
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

    
    public interface ILink
    {
        int Row { get; set; }
        int Col { get; set;  }
    }
    
    public class RelativeLink : ILink
    {
        public int Row { get; set; }
        public int Col { get; set; }
    }
    
    public class AbsoluteLink : ILink
    {
        public string SheetName;
        public int Row { get; set; }
        public int Col { get; set; }
    }
    
    public class FormulaCell : ICell
    {
        public int GetVal(int x, int y)
        {
            switch (Operation) 
            {
                case '+':
                    return x + y;
                case '-':
                    return x - y;
                case '*':
                    return x * y;
                case '/':
                    return x / y;
                default:
                    throw new NotImplementedException();
            }
        } 
        
        
        public FormulaCell()
        {
        }

        public bool Evaluated = false;
        public int Val { get; set; }
        public Error Status { get; set; }
        
        public ILink[] Operands;
        public char Operation = '0'; 

        public bool IsEvaluated()
        {
            return Evaluated;
        }
    } 
    
    
    
    
    public static class TableFileLoader
    {
        public static TableData Load(string filename)
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
                    row[i] = TokenToCell(tokens[i]);
                }
                
                sheet.AddRow(row);
            }

            return sheet;
        }

        // return EmptyCell, ValueCell or FormulaCell based on string token
        public static ICell TokenToCell(string token)
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
                string formula = token.Substring(1);
                Func<int, int ,int> op = null;
                FormulaCell cell = new FormulaCell();

                
                if (formula.Contains('+')) {
                    cell.Operation = '+';
                }
                else if (formula.Contains("-")) {
                    cell.Operation = '-';
                }
                else if (formula.Contains("*")) {
                    cell.Operation = '*';
                }
                else if (formula.Contains("/"))
                {
                    cell.Operation = '/';
                }

                if (cell.Operation == '0') // formula doesn't contain an operator
                {
                    cell.Status = Error.MISSOP;
                    cell.Evaluated = true;
                    return cell;
                }

                string[] operands = TableFileLoader.GetOperands(formula, cell.Operation);
                if (operands == null)
                {
                    // formula syntax error
                    cell.Status = Error.FORMULA;
                    cell.Evaluated = true;
                    return cell;
                }

                ILink[] links = new ILink[2];
                
                for (int i = 0; i < operands.Length; i++)
                {
                    if (operands[i].Contains('!'))
                    {
                        string[] parts = operands[i].Split('!');
                        string addr = parts[1];
                        AbsoluteLink link = new AbsoluteLink();
                        link.SheetName = parts[0];
                        Utils.GetRowColFromAddr(addr, out int row, out int col);
                        link.Row = row;
                        link.Col = col;
                        links[i] = link;
                    }
                    else
                    {
                        RelativeLink link = new RelativeLink();
                        Utils.GetRowColFromAddr(operands[i], out int row, out int col);
                        link.Row = row;
                        link.Col = col;
                        links[i] = link;
                    } 
                }

                cell.Operands = links;
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
            string[] operands = formula.Split(op);

            if (operands.Length == 2 && Utils.IsValidCellKey(operands[0]) && Utils.IsValidCellKey(operands[1]))
            {
                return operands;
            }

            return null;
        }
    }
}