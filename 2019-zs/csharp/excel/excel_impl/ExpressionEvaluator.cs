using System;
using System.Linq;

namespace excel_impl
{
    public class ExpressionEvaluator
    {
        public static string EvaluateFormula(string[] vals, string op)
        {
            for (int i = 0; i < vals.Length; i++)
            {
                if (vals[i] == "[]")
                {
                    vals[i] = "0";
                }
            }
            
            // At least one operand doesn't have valid value or cannot be computed (eg. is on a cycle)
            if (vals.Contains(TableCell.INVVAL) || vals.Contains(TableCell.ERROR) || vals.Contains(TableCell.DIV0) ||
                vals.Contains(TableCell.MISSOP) || vals.Contains(TableCell.FORMULA) || vals.Contains(TableCell.CYCLE))
            {
                return TableCell.ERROR;
            }

            if (op == "/" && vals[1] == "0")
                return TableCell.DIV0;

            

            int x0 = Int32.Parse(vals[0]);
            int x1 = Int32.Parse(vals[1]);

            if (op == "+")
                return (x0 + x1).ToString();
            if (op == "-")
                return (x0 - x1).ToString();
            if (op == "*")
                return (x0 * x1).ToString();
            if (op == "/")
                return (x0 / x1).ToString();


            // shouldn't happen
            throw new DivideByZeroException();
            return null;
        }
    }
}