using System.Collections.Generic;

namespace excel_impl
{
    public class TableData
    {
        private List<TableCell[]> data;

        public List<TableCell[]> Rows => data;

        public List<TableCell> AllCells                                                         
        {                                                                               
            get
            {
                List<TableCell> cells = new List<TableCell>();
                foreach (var row in data)
                {
                    foreach (var cell in row)
                    {
                        cells.Add(cell);
                    }
                }

                return cells;
            }
        }

        public TableData()
        {
            data = new List<TableCell[]>();
        }

        public void AddRow(string[] row)
        {
            TableCell[] cellRow = new TableCell[row.Length];
            for (int i = 0; i < row.Length; i++)
            {
                TableCell cell = new TableCell();
                cell.content = row[i];
                cell.evaluated = false;
                cellRow[i] = cell;
            }
            data.Add(cellRow);
        }

        public TableCell GetCell(string index)
        {
            Utils.GetRowColFromAddr(index, out int row, out int col);
            return GetCell(row, col);
        }

        public TableCell GetCell(int row, int col)
        {
            if (row >= 1 && data.Count >= row && col >= 1 && data[row - 1].Length >= col)
            {
                return data[row - 1][col - 1];
            }

            return null;
        }

        public bool ContainsKey(string index)
        {
            return GetCell(index) != null;
        }
    }
}