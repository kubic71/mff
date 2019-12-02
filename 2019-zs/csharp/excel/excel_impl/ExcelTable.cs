using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;

namespace excel_impl
{
    public class TableCell
    {
        public bool evaluated = false;


        public const string INVVAL = "I";
        public const string MISSOP = "M";
        public const string ERROR = "E";
        public const string DIV0 = "D";
        public const string CYCLE = "C";
        public const string FORMULA = "F";

        public string content { get; set; }

        // helper data item used during evaluation
//        public string val { get; set; }
    }

    public class ExcelTable
    {
        private string mainSheet;

        private Dictionary<string, TableData> sheets =
            new Dictionary<string, TableData>();

        public TableCell GetCell(string index)
        {
            string[] parts = index.Split("!");
            string sheetName = parts[0];
            string cellIndex = parts[1];
            return GetCell(cellIndex, sheetName);
        }

        /// <summary>
        /// Get TableCell object
        /// </summary>
        /// <param name="index">index of main or external sheet cell (B23, Sheet1!A32 ... )</param>
        /// <returns>TableCell if this cell appeared in input sheet file or null if cell didn't appear in sheet file, but sheet file does exists (and thus has value of 0)</returns>
        /// <exception cref="SheetFileNotFoundException">When index refers to external sheet and this sheet doesn't exist</exception>
        public TableCell GetCell(string index, string sheetName)
        {
            if (!sheets.ContainsKey(sheetName))
            {
                // Load external sheet
                try
                {
                    Load(sheetName + ".sheet", false);
                }
                catch (Exception ex)
                {
                    if (Utils.IsFileErrorException(ex))
                    {
                        throw new SheetFileNotFoundException();
                    }

                    throw;
                }
            }

            if (sheets[sheetName].ContainsKey(index))
            {
                return sheets[sheetName].GetCell(index);
            }

            return null;
        }

        public TableCell GetCell(int row, int col)
        {
            return GetCell(row, col, mainSheet);
        }

        public TableCell GetCell(int row, int col, string sheetName)
        {
            return GetCell(Utils.GetExcelIndex(row, col), sheetName);
        }

        // load main sheet
        public void Load(string filename)
        {
            Load(filename, true);
        }


        private void Load(string filename, bool isMainSheet)
        {
            TableData sheet = new TableData();
            
            string line;
            StreamReader inputFile = new StreamReader(filename);
            while ((line = inputFile.ReadLine()) != null)
            {
                string[] tokens = Tokenizer.Tokenize(line);
                sheet.AddRow(tokens);
            }

            string sheetIdentifier = filename.Replace(".sheet", "");
            if (isMainSheet)
            {
                mainSheet = sheetIdentifier;
            }

            sheets.Add(sheetIdentifier, sheet);
        }

        /// <summary>
        /// Returns two operands, or null, if formula is invalid
        /// Method already assumes, that formula contains given operator
        /// </summary>
        /// <param name="formula"></param>
        /// <param name="op"></param>
        private static string[] GetOperands(string formula, string op)
        {
            string[] operands = formula.Split(op);

            if (operands.Length == 2 && Utils.IsValidCellKey(operands[0]) && Utils.IsValidCellKey(operands[1]))
            {
                return operands;
            }

            return null;
        }

        private void EvaluateRecursively(TableCell cell, Stack<TableCell> seen, string sheetname)
        {
            if (cell.evaluated) // if cell was evaluated already, skip evaluation
            {
                return;
            }

            // cell needs no further evaluation
            if (Utils.IsInteger(cell.content) || cell.content == "[]")
            {
                cell.evaluated = true;
                return;
            }
            else if (cell.content[0] == '=') // Is some kind of formula
            {
                string formula = cell.content.Substring(1);
                string op = "";

                if (formula.Contains("+"))
                    op = "+";
                else if (formula.Contains("-"))
                    op = "-";
                else if (formula.Contains("*"))
                    op = "*";
                else if (formula.Contains("/"))
                    op = "/";

                if (op == "") // formula doesn't contain an operator
                {
                    cell.content = TableCell.MISSOP;
                    cell.evaluated = true;
                    return;
                }

                string[] operands = ExcelTable.GetOperands(formula, op);
                if (operands == null)
                {
                    // formula syntax error
                    cell.content = TableCell.FORMULA;
                    cell.evaluated = true;
                    return;
                }


                // string values of operands
                List<string> vals = new List<string>();

                // rewrite relative address to absolute address
                for (int i = 0; i < operands.Length; i++)
                {
                    if (!operands[i].Contains("!"))
                    {
                        operands[i] = sheetname + "!" + operands[i];
                    }

                    TableCell operand = GetCell(operands[i]);
                    if (operand == null)
                    {
                        vals.Add("0");
                        continue;
                    }

                    if (seen.Contains(operand))
                    {
                        // Seen stack together with operand contains exactly 1 cycle, operand lies in this cycle
                        // eg. operand = C3  --------------------------->  
                        //     seen = C1 -> C2 -> C3 -> C4 ->  C5       |
                        //                         ^                    V
                        //                         |<--------------------

                        // In this particular case, we would need to flag C3, C4 and C5 as being on a cycle 

                        bool cycleStarted = false;
                        foreach (var cycleCell in seen.Reverse())
                        {
                            if (cycleCell == operand)
                                cycleStarted = true;

                            if (cycleStarted)
                            {
                                cycleCell.content = TableCell.CYCLE;
                                cycleCell.evaluated = true;
                            }
                        }

                        vals.Add("#CYCLE");
                    }
                    else
                    {
                        seen.Push(operand);
                        EvaluateRecursively(operand, seen, operands[i].Split("!")[0]);
                        seen.Pop();
                        vals.Add(operand.content);
                    }
                }

                // Cycle detection can set current cell value to #CYCLE, end evaluation in that case
                if (cell.content == TableCell.CYCLE)
                {
                    return;
                }

                cell.content = ExpressionEvaluator.EvaluateFormula(vals.ToArray(), op);
                cell.evaluated = true;
            }

            else // Not an integer number and not a formula => #INVVAL
            {
                cell.content = TableCell.INVVAL;
                cell.evaluated = true;
            }
        }

        public void Evaluate()
        {
            foreach (var cell in sheets[mainSheet].AllCells)
            {
                Stack<TableCell> seen = new Stack<TableCell>();
                seen.Push(cell);
                EvaluateRecursively(cell, seen, mainSheet);
            }
        }

        public override string ToString()
        {
            MemoryStream ms = new MemoryStream();
            StreamWriter sw = new StreamWriter(ms);

            WriteTo(sw);
            sw.Flush();
            sw.Close();

            return Encoding.ASCII.GetString(ms.ToArray());
        }


        private string StatusRewrite(string content)
        {
            switch (content)
            {
                case TableCell.ERROR:
                    return "#ERROR";
                case TableCell.INVVAL:
                    return "#INVVAL";
                case TableCell.DIV0:
                    return "#DIV0";
                case TableCell.CYCLE:
                    return "#CYCLE";
                case TableCell.MISSOP:
                    return "#MISSOP";
                case TableCell.FORMULA:
                    return "#FORMULA";
                default:
                    return content;
            }
        }

        public void WriteTo(StreamWriter writer)
        {
            var rows = sheets[mainSheet].Rows;
            for(int i = 0; i < rows.Count; i ++)
            {
                var row = rows[i];
                bool lastRow = i == (rows.Count - 1);
                
                for(int j = 0; j < row.Length; j++)
                {
                    bool lastCell = j == (row.Length - 1);
                    TableCell cell = row[j];
                    writer.Write(StatusRewrite(cell.content));
                    if (!lastCell)
                        writer.Write(" ");
                }
                
                if (!lastRow)
                    writer.Write("\n");
            }
        }
    }
}