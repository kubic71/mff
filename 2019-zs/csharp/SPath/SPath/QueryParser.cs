using System;
using System.Linq;
using System.Text;

namespace SPath
{
    /**
     * Parse queries without forward slash (/)
     * possible forward slash should be removed before executing parser
     *
     * Empty queries are not parsed!
     * 
     * Parsing grammar:
     * query : step , '/' , query | step
     * step : [space], ID , [space], { predicate , [space] }
     * predicate : '[', [space] , ( index | query ) , [space] , ']'
     * ID : 
     */


    public class QueryParser
    {
        private static readonly char[] FORBIDDEN_ID_CHARS = new char[]{
            '/', '[', ']', ' ', '\n', '\t'
        };

        private string queryStr;
        private int index;
        private Query query;
        
        public QueryParser(string queryStr)
        {
            this.queryStr = queryStr;
            index = 0;
            query = new Query();
        }

        private bool IndexOutOfRange()
        {
            return index >= queryStr.Length;
        }


        public void SkipWhiteSpace()
        {
            while (true)
            {
                if (IndexOutOfRange() || !Char.IsWhiteSpace(queryStr[index]))
                {
                    return;
                }

                index++;
            }            
        }
        
        public bool ParseChar(char c)
        {
            if (IndexOutOfRange() || queryStr[index] != c)
            {
                return false;
            }

            index++;
            return true;
        }

        public string ParseID()
        {
             
            StringBuilder sb = new StringBuilder();
            while (true)
            {
                if (IndexOutOfRange() || FORBIDDEN_ID_CHARS.Contains(queryStr[index]))
                {
                    break;
                }
                
                sb.Append(queryStr[index]);
                index++;
            }

            if (sb.Length == 0)
            {
                return null;
            }

            return sb.ToString();
        }

        public int? ParseInt()
        {
            // Ambiguity: Is positive integer starting with 0 valid? eg. 00023
            // We suppose it is not!
            
            if (IndexOutOfRange())
                return null;

            if (queryStr[index] == '0')
            {
                index++;
                return 0;
            }

            string intStr = "";
            while (true)
            {
                if (IndexOutOfRange() || !Char.IsDigit(queryStr[index]))
                {
                    break;
                }

                intStr += queryStr[index];
                index++;
            }

            if (intStr == "")
            {
                return null;
            }
            return int.Parse(intStr);
        }

        /// <summary>
        ///`Returns true when query string was fully matched
        /// Do not call before calling some Parse method
        /// </summary>
        public bool QueryMatched()
        {
            return index == queryStr.Length;
        }


        public Predicate ParsePredicate()
        {
            // predicate : '[', [space] , ( index | query ) , [space] , ']'
            int startBacktrack = index;
            if(!ParseChar('['))
                return null;
            
            SkipWhiteSpace();
            
            // try to parse number first
            int? predicateIndex = ParseInt();
            Predicate predicate;
            if (predicateIndex == null)
            {
                Query q = ParseQuery();
                if (q == null)
                {
                    index = startBacktrack;
                    return null;
                }
                else
                {
                    predicate = new QueryPredicate();
                    ((QueryPredicate) predicate).Query = q;
                }
            }
            else
            {
                predicate = new NumberPredicate();
                ((NumberPredicate) predicate).index = predicateIndex.Value;
            }
            
            SkipWhiteSpace();
            if (!ParseChar(']'))
            {
                index = startBacktrack;
                return null;
            }

            return predicate;
        }
        

        public Step ParseStep()
        {
            // step : [space], ID , [space], { predicate , [space] }

            int backtrack = index;
            SkipWhiteSpace();
            string ID = ParseID();
            if (ID == null)
            {
                index = backtrack;
                return null;
            }
            SkipWhiteSpace();
            
            Step step = new Step();
            step.ID = ID;

            Predicate p;
            while (true)
            {
                if ((p = ParsePredicate()) == null)
                {
                    break;
                }
                step.Predicates.Add(p);
                SkipWhiteSpace();
            }

            return step;
        }

        public Query ParseQuery()
        {
            Step step = ParseStep();
            if (step == null)
            {
                return null;
            }
            else
            {
                // step, '/', query
                int backtrack = index;
                Query queryRest;
                if (ParseChar('/') && (queryRest = ParseQuery())!=null )
                {
                    queryRest.steps.Insert(0, step);
                    return queryRest;
                }

                index = backtrack;
                // step
                Query oneStepQuery = new Query();
                oneStepQuery.steps.Add(step);
                return oneStepQuery;
            }
        }


        public static string StripFirstForwardSlash(string qStr)
        {
            int i = 0;
            while (true)
            {
                if (i >= qStr.Length)
                    return "";
                
                if (!Char.IsWhiteSpace(qStr[i]))
                {
                    if (qStr[i] == '/')
                    {
                        // skip it
                        return qStr.Substring(i + 1);
                    }
                    else
                    {
                        return qStr.Substring(i);
                    }
                }

                i++;
            }
        }
    }
}