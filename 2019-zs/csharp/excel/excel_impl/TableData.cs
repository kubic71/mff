using System.Collections.Generic;

namespace excel_impl
{
    public class TableData
    {
        public List<ICell[]> data;

        public List<ICell[]> Rows => data;

        public List<ICell> AllCells                                                         
        {                                                                               
            get
            {
                List<ICell> cells = new List<ICell>();
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

        public void AddRow(ICell[] row)
        {
            data.Add(row);
        }

        public TableData()
        {
            data = new List<ICell[]>();
        }


        public ICell GetCell(string index)
        {
            Utils.GetRowColFromAddr(index, out int row, out int col);
            return GetCell(row, col);
        }

        public ICell GetCell(int row, int col)
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