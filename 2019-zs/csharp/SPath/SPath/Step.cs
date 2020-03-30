using System.Collections.Generic;

namespace SPath
{
    public class Step
    {
        public string ID { get; set; }
        public List<Predicate> Predicates = new List<Predicate>();
    }
}