using System;
using NezarkaModels;

namespace NezarkaApp.Views
{
    public static class ViewBookDetail
    {
        public static void Render(int custId, int bookId, ModelStore modelStore)
        {
            var book = modelStore.GetBook(bookId);
            if (book == null)
            {
                ViewInvalidRequest.Render();
                return;
            }
            
            ViewHeader.Render(custId, modelStore);

            Console.WriteLine("	Book details:");
            Console.WriteLine("	<h2>" + book.Title + "</h2>");
            Console.WriteLine("	<p style=\"margin-left: 20px\">");
            Console.WriteLine("	Author: " + book.Author + "<br />");
            Console.WriteLine("	Price: " + book.Price.ToString() + " EUR<br />");
            Console.WriteLine("	</p>");
            Console.WriteLine("	<h3>&lt;<a href=\"/ShoppingCart/Add/" + book.Id.ToString() + "\">Buy this book</a>&gt;</h3>");
            Console.WriteLine("</body>");
            Console.WriteLine("</html>");
            
        }
    }
}