using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;

namespace excel_impl
{
 
    public class ExcelTable
    {
        private string mainSheet;

        private Dictionary<string, TableData> sheets =
            new Dictionary<string, TableData>();
        
        private Dictionary<int, string> sheetHashToString = new Dictionary<int, string>();

        /// <summary>
        /// Get ICell object
        /// </summary>
        /// <returns>ICell if this cell appeared in input sheet file or null if cell didn't appear in sheet file, but sheet file does exists (and thus has value of 0)</returns>
        /// <exception cref="SheetFileNotFoundException">When index refers to external sheet and this sheet doesn't exist</exception>
        public ICell GetCell(int row, int col, int sheetHash)
        {
            string sheetName = sheetHashToString[sheetHash];
            
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
            
            // returns null when cell doesn't exist in given sheet
            return sheets[sheetName].GetCell(row, col);
        }

        // load main sheet
        public void Load(string filename)
        {
            Load(filename, true);
        }
       
        public void Load(string filename, bool isMainSheet)
        {
            TableData sheet = TableFileLoader.Load(filename, sheetHashToString);
            string sheetIdentifier = filename.Replace(".sheet", "");
            sheetHashToString[sheetIdentifier.GetHashCode()] = sheetIdentifier;
            if (isMainSheet)
                mainSheet = sheetIdentifier;

            sheets.Add(sheetIdentifier, sheet);
        }

        private void EvaluateRecursively(ICell cell, Stack<ICell> seen, int sheetHash)
        {
            if (cell.IsEvaluated()) // if cell was evaluated already, skip evaluation
                return;

            if (cell is FormulaCell)
            {
                FormulaCell formulaCell = (FormulaCell) cell;
                // string values of operands

                List<int> vals = new List<int>();
                // rewrite relative address to absolute address
                foreach(Link link in formulaCell.Operands)
                {
                    ICell operandCell;
                    int newSheetHash;

                    if (link.sheetHash != FormulaCell.SHEET_RELATIVE)   // absolute link
                    {
                        // can fail if sheetfile doesn't exist
                        try
                        {
                            operandCell = GetCell(link.Row, link.Col, link.sheetHash);
                        } catch (Exception ex)
                        {
                            if (ex is SheetFileNotFoundException)
                            {
                                formulaCell.Evaluated = true;
                                formulaCell.Status = Error.ERROR;
                                return;
                            }
                            throw;
                        }
                        newSheetHash = link.sheetHash;
                    }
                    else
                    {
                        operandCell = GetCell(link.Row, link.Col, sheetHash);
                        newSheetHash = sheetHash;
                    }

                    if (operandCell == null)
                    {
                        vals.Add(0);
                        continue;
                    }


                    if (seen.Contains(operandCell))
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
                            if (cycleCell == operandCell)
                                cycleStarted = true;

                            if (cycleStarted)
                            {
                                cycleCell.Status = Error.CYCLE;
                                ((FormulaCell) cycleCell).Evaluated = true;
                            }
                        }
                    }
                    else
                    {
                        seen.Push(operandCell);
                        EvaluateRecursively(operandCell, seen, newSheetHash);
                        seen.Pop();
                        
                        // Cycle detection can set current cell value to #CYCLE, end evaluation in that case
                        if (formulaCell.Status == Error.CYCLE)
                        {
                            return;
                        }

                        if (operandCell.Status != Error.OK)
                        {
                            formulaCell.Evaluated = true;
                            formulaCell.Status = Error.ERROR;
                            return;
                        }
                        
                        vals.Add(operandCell.Val);
                    }
                }


                try
                {
                    formulaCell.Val = formulaCell.GetVal(vals[0], vals[1]);
                    formulaCell.Evaluated = true;
                }
                catch (Exception e)
                {
                    if (e is DivideByZeroException)
                    {
                        formulaCell.Status = Error.DIV0;
                        formulaCell.Evaluated = true;
                    }
                }
            }
            
            
            // shouldn't happen
        }

        public void Evaluate()
        {
            foreach (var row in sheets[mainSheet].data)
            {
                foreach (var cell in row)
                {
                    Stack<ICell> seen = new Stack<ICell>();
                    seen.Push(cell);
                    EvaluateRecursively(cell, seen, mainSheet.GetHashCode());
                }
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


        private string StatusRewrite(Error status)
        {
            switch (status)
            {
                case Error.ERROR:
                    return "#ERROR";
                case Error.INVVAL:
                    return "#INVVAL";
                case Error.DIV0:
                    return "#DIV0";
                case Error.CYCLE:
                    return "#CYCLE";
                case Error.MISSOP:
                    return "#MISSOP";
                case Error.FORMULA:
                    return "#FORMULA";
                default:
                    return null;
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
                    ICell cell = row[j];

                    if (cell is EmptyCell)
                    {
                        writer.Write("[]");
                    } else 
                    {
                        if(cell.Status == Error.OK)
                            writer.Write(cell.Val);
                        else
                        {
                            writer.Write(StatusRewrite(cell.Status));
                        }
                    }
                    
                    if (!lastCell)
                        writer.Write(" ");
                }
                
                if (!lastRow)
                    writer.Write("\n");
            }
        }
    }
}