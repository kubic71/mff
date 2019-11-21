using System;

namespace NezarkaApp.Views
{
    public static class ViewInvalidRequest
    {

        public static void Render()
        {
            Console.WriteLine("<!DOCTYPE html>");
            Console.WriteLine("<html lang=\"en\" xmlns=\"http://www.w3.org/1999/xhtml\">");
            Console.WriteLine("<head>");
            Console.WriteLine("	<meta charset=\"utf-8\" />");
            Console.WriteLine("	<title>Nezarka.net: Online Shopping for Books</title>");
            Console.WriteLine("</head>");
            Console.WriteLine("<body>");
            Console.WriteLine("<p>Invalid request.</p>");
            Console.WriteLine("</body>");
            Console.WriteLine("</html>");
   
        }
    }
}