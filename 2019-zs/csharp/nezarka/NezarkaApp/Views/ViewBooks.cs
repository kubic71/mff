using System;
using NezarkaModels;

namespace NezarkaApp.Views
{
    public static class ViewBooks
    {
        public static void Render(int custId, ModelStore modelStore)
        {
            ViewHeader.Render(custId, modelStore);
            
            Console.WriteLine("	Our books for you:");
            Console.WriteLine("	<table>");


            var books = modelStore.GetBooks();
            for (int i = 0; i < books.Count; i++)
            {
                var book = books[i];
                // start new row
                if (i % 3 == 0)
                {
                    // end last row
                    if (i != 0)
                        Console.WriteLine("		</tr>");

                    Console.WriteLine("		<tr>");   
                }
                
                Console.WriteLine("			<td style=\"padding: 10px;\">");
                Console.WriteLine("				<a href=\"/Books/Detail/" + book.Id.ToString() + "\">" + book.Title + "</a><br />");
                Console.WriteLine("				Author: " + book.Author + "<br />");
                Console.WriteLine("				Price: " + book.Price.ToString() + " EUR &lt;<a href=\"/ShoppingCart/Add/" + book.Id.ToString() + "\">Buy</a>&gt;");
                Console.WriteLine("			</td>");

            }

            if (books.Count > 0)
            {
                // end last row
                Console.WriteLine("		</tr>");
            }


            Console.WriteLine("	</table>");
            Console.WriteLine("</body>");
            Console.WriteLine("</html>");

        }
    }
}