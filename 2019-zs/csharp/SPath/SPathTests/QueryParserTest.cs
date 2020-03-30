using NUnit.Framework;
using SPath;

namespace Tests
{
    public class QueryParserTest
    {
        [SetUp]
        public void Setup()
        {
        }

        [Test]
        public void TestParseIndex ()
        {
            string queryStr = "123";
            QueryParser parser = new QueryParser(queryStr);
            Assert.AreEqual(123, parser.ParseInt());
            Assert.True(parser.QueryMatched());
            
            queryStr = "0";
            parser = new QueryParser(queryStr);
            Assert.AreEqual(0, parser.ParseInt());
            Assert.True(parser.QueryMatched());
            
            queryStr = "094";
            parser = new QueryParser(queryStr);
            Assert.AreEqual(0, parser.ParseInt());
            Assert.False(parser.QueryMatched());
            
            queryStr = "   123   ";
            parser = new QueryParser(queryStr);
            Assert.AreEqual(null, parser.ParseInt());
            Assert.False(parser.QueryMatched());

            queryStr = "abc";
            parser = new QueryParser(queryStr);
            Assert.AreEqual(null, parser.ParseInt());
            Assert.False(parser.QueryMatched());

            queryStr = "-123";
            parser = new QueryParser(queryStr);
            Assert.AreEqual(null, parser.ParseInt());
            Assert.False(parser.QueryMatched());
        }
        
        
        [Test]
        public void TestParseWhitespace ()
        {
            string queryStr = "     \n \t   ";
            QueryParser parser = new QueryParser(queryStr);
            parser.SkipWhiteSpace();
            Assert.True(parser.QueryMatched());
            
            queryStr = "       \t   f   \n";
            parser = new QueryParser(queryStr);
            parser.SkipWhiteSpace();
            Assert.False(parser.QueryMatched());
            
            // whitespace + number test 
            queryStr = "     \t  \n   94    \t \n ";
            parser = new QueryParser(queryStr);
            parser.SkipWhiteSpace();
            Assert.AreEqual(94, parser.ParseInt());
            parser.SkipWhiteSpace();
            Assert.True(parser.QueryMatched());
        }
        
        [Test]
        public void TestParseID ()
        {
            
            string queryStr = "abc_kocka_Prede";
            QueryParser parser = new QueryParser(queryStr);
            Assert.AreEqual(queryStr, parser.ParseID());
            Assert.True(parser.QueryMatched());
            
            queryStr = "   abc_kocka_Prede";
            parser = new QueryParser(queryStr);
            Assert.AreEqual(null, parser.ParseID());
            Assert.False(parser.QueryMatched());
            
            
            // Query id CAN start with number (and if I understand the instructions correctly, can even BE number)   
            queryStr = "2abcd";
            parser = new QueryParser(queryStr);
            Assert.AreEqual(queryStr, parser.ParseID());
            Assert.True(parser.QueryMatched());
            
            queryStr = "2234";
            parser = new QueryParser(queryStr);
            Assert.AreEqual(queryStr, parser.ParseID());
            Assert.True(parser.QueryMatched());
            
            queryStr = "2234";
            parser = new QueryParser(queryStr);
            Assert.AreEqual(queryStr, parser.ParseID());
            Assert.True(parser.QueryMatched());
            
            queryStr = "abcd[abcd]";
            parser = new QueryParser(queryStr);
            Assert.AreEqual("abcd", parser.ParseID());
            Assert.False(parser.QueryMatched());
            
            queryStr = "Haf/cdf";
            parser = new QueryParser(queryStr);
            Assert.AreEqual("Haf", parser.ParseID());
            Assert.False(parser.QueryMatched());
            
            queryStr = "No space  in ID!";
            parser = new QueryParser(queryStr);
            Assert.AreEqual("No", parser.ParseID());
            Assert.False(parser.QueryMatched());
            
            queryStr = "*";
            parser = new QueryParser(queryStr);
            Assert.AreEqual("*", parser.ParseID());
            Assert.True(parser.QueryMatched());
            
            queryStr = "..";
            parser = new QueryParser(queryStr);
            Assert.AreEqual("..", parser.ParseID());
            Assert.True(parser.QueryMatched());
        }

        [Test]
        public void TestParseNumberPredicate()
        {
            string queryStr = "[ 195  ]";
            QueryParser parser = new QueryParser(queryStr);
            Predicate p = parser.ParsePredicate();
            Assert.True(p is NumberPredicate);
            Assert.AreEqual(195, ((NumberPredicate)p).index);
            Assert.True(parser.QueryMatched());

            queryStr = "[    ]";
            parser = new QueryParser(queryStr);
            Assert.AreEqual(null, parser.ParsePredicate());
            
            queryStr = "[123";
            parser = new QueryParser(queryStr);
            Assert.AreEqual(null, parser.ParsePredicate());

            queryStr = "123]";
            parser = new QueryParser(queryStr);
            Assert.AreEqual(null, parser.ParsePredicate());

            queryStr = "[  \t \n 0 \t \n]";
            parser = new QueryParser(queryStr);
            p = parser.ParsePredicate();
            Assert.True(p is NumberPredicate);
            Assert.AreEqual(0, ((NumberPredicate)p).index);
            Assert.True(parser.QueryMatched());
        }

        [Test]
        public void TestParseQueryPredicate()
        {
            string queryStr = "[  someID  ]";
            QueryParser parser = new QueryParser(queryStr);
            Predicate p = parser.ParsePredicate();
            Assert.True(p is QueryPredicate);
            Assert.AreEqual("someID", ((QueryPredicate)p).Query.steps[0].ID);
            Assert.True(parser.QueryMatched());
            
            // Nested Predicate 
            queryStr = "[  someID/ ..  [33] / alfa ]";
            parser = new QueryParser(queryStr);
            p = parser.ParsePredicate();
            Assert.True(p is QueryPredicate);
            Query predQuery = ((QueryPredicate) p).Query;
            Assert.AreEqual(3, predQuery.steps.Count);
            Assert.AreEqual("someID", predQuery.steps[0].ID);
            Assert.AreEqual("..", predQuery.steps[1].ID);
            Assert.AreEqual(1, predQuery.steps[1].Predicates.Count);
            Assert.True(predQuery.steps[1].Predicates[0] is NumberPredicate);
            Assert.AreEqual(33, ((NumberPredicate)predQuery.steps[1].Predicates[0]).index);
            Assert.AreEqual("alfa", predQuery.steps[2].ID);
            Assert.True(parser.QueryMatched());
        }

        [Test]
        public void TestParseStep()
        {
            string queryStr = "   wer   \t \n    ";
            QueryParser parser = new QueryParser(queryStr);
            Step step = parser.ParseStep();
            Assert.True(step != null);
            Assert.AreEqual("wer", step.ID);
            Assert.AreEqual(0, step.Predicates.Count);
            Assert.True(parser.QueryMatched());
            
            queryStr = "   wer  abc   ";
            parser = new QueryParser(queryStr);
            step = parser.ParseStep();
            Assert.True(step != null);
            Assert.AreEqual("wer", step.ID);
            Assert.AreEqual(0, step.Predicates.Count);
            Assert.False(parser.QueryMatched());
            
            queryStr = "   idagain  [1] [ 23 ] [ 5 4 ]  ";
            parser = new QueryParser(queryStr);
            step = parser.ParseStep();
            Assert.True(step != null);
            Assert.AreEqual("idagain", step.ID);
            Assert.AreEqual(2, step.Predicates.Count);
            Assert.True(step.Predicates[0] is NumberPredicate && step.Predicates[1] is NumberPredicate);
            Assert.AreEqual(1, ((NumberPredicate)step.Predicates[0]).index);
            Assert.AreEqual(23, ((NumberPredicate)step.Predicates[1]).index);
            Assert.False(parser.QueryMatched());
            
            queryStr = "   idagain  [1] [ 23 ] [ this/is/query ]  ";
            parser = new QueryParser(queryStr);
            step = parser.ParseStep();
            Assert.True(step != null);
            Assert.AreEqual("idagain", step.ID);
            Assert.AreEqual(3, step.Predicates.Count);
            Assert.True(step.Predicates[0] is NumberPredicate && step.Predicates[1] is NumberPredicate && step.Predicates[2] is QueryPredicate);
            Assert.AreEqual(1, ((NumberPredicate)step.Predicates[0]).index);
            Assert.AreEqual(23, ((NumberPredicate)step.Predicates[1]).index);

            Query q = ((QueryPredicate) step.Predicates[2]).Query;
            Assert.AreEqual(3, q.steps.Count);
            Assert.AreEqual("this", q.steps[0].ID);
            Assert.AreEqual(0, q.steps[0].Predicates.Count);
            Assert.AreEqual("is", q.steps[1].ID);
            Assert.AreEqual("query", q.steps[2].ID);
            
            Assert.True(parser.QueryMatched());

        }


        [Test]
        public void TestParseQuery()
        {
            string queryStr = " / not_allowed ";
            QueryParser parser = new QueryParser(queryStr);
            Assert.AreEqual(null, parser.ParseQuery());

            queryStr = "/starting/with/backslash";
            parser = new QueryParser(queryStr);
            Assert.AreEqual(null, parser.ParseQuery());

            // backslash only
            queryStr = "/";
            parser = new QueryParser(queryStr);
            Assert.AreEqual(null, parser.ParseQuery());

            queryStr = "   /   ";
            parser = new QueryParser(queryStr);
            Assert.AreEqual(null, parser.ParseQuery());
            
            queryStr = " id123  /   ";
            parser = new QueryParser(queryStr);
            Query q = parser.ParseQuery();
            Assert.AreEqual(1, q.steps.Count);
            Assert.AreEqual("id123", q.steps[0].ID);

            queryStr = "abcd / a b c";
            parser = new QueryParser(queryStr);
            q = parser.ParseQuery();
            Assert.AreEqual(2, q.steps.Count);
            Assert.AreEqual("abcd", q.steps[0].ID);
            Assert.AreEqual("a", q.steps[1].ID);
            
            queryStr = "     ";
            parser = new QueryParser(queryStr);
            Assert.AreEqual(null, parser.ParseQuery());
            Assert.False(parser.QueryMatched());
            
            queryStr = "";
            parser = new QueryParser(queryStr);
            Assert.AreEqual(null, parser.ParseQuery());
            Assert.True(parser.QueryMatched());
            
            queryStr = "abd/ /sdf";
            parser = new QueryParser(queryStr);
            q = parser.ParseQuery();
            Assert.AreEqual(1, q.steps.Count );
            Assert.AreEqual("abd", q.steps[0].ID);
            Assert.False(parser.QueryMatched());
        }

        [Test]
        public void TestQuerySlashStripper()
        {
            Assert.AreEqual("abcd/cdter[1]", QueryParser.StripFirstForwardSlash("/abcd/cdter[1]"));
            Assert.AreEqual("  something / d234 / sfd", QueryParser.StripFirstForwardSlash("   /  something / d234 / sfd"));
            Assert.AreEqual("", QueryParser.StripFirstForwardSlash("/"));
            Assert.AreEqual(" ahoj/svete ", QueryParser.StripFirstForwardSlash(" ahoj/svete "));
        }
    }
}