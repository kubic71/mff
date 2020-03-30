namespace ZapoctovyTest
{
    public class TypeNode
    {
        public string Name { get; set; }
        public TypeNode Predecessor { get; set; }
        public int LineDeclared { get; set; }
        
    }
}