using System;
using NezarkaModels;

namespace NezarkaApp.Views
{
    public static class ViewShoppingCart
    {
        public static void Render(int custId, ModelStore modelStore)
        {
            ViewHeader.Render(custId, modelStore);

            var shoppingCartItems = modelStore.GetCustomer(custId).ShoppingCart.Items;

            if (shoppingCartItems.Count == 0)
            {
                Console.WriteLine("	Your shopping cart is EMPTY.");
            }
            else
            {
                Console.WriteLine("	Your shopping cart:");
                Console.WriteLine("	<table>");
                Console.WriteLine("		<tr>");
                Console.WriteLine("			<th>Title</th>");
                Console.WriteLine("			<th>Count</th>");
                Console.WriteLine("			<th>Price</th>");
                Console.WriteLine("			<th>Actions</th>");
                Console.WriteLine("		</tr>");

                decimal total = 0;
                foreach (var item in shoppingCartItems)
                {
                    var book = modelStore.GetBook(item.BookId);
                    Console.WriteLine("		<tr>");
                    Console.WriteLine("			<td><a href=\"/Books/Detail/" + book.Id.ToString() + "\">" + book.Title +
                                      "</a></td>");
                    Console.WriteLine("			<td>" + item.Count.ToString() + "</td>");
                    
                    Console.WriteLine("			<td>" + (item.Count == 1 ? book.Price.ToString() : item.Count.ToString() + " * " + book.Price.ToString() + " = " +
                                      (item.Count * book.Price).ToString()) + " EUR</td>");
                    Console.WriteLine("			<td>&lt;<a href=\"/ShoppingCart/Remove/" + book.Id.ToString() +
                                      "\">Remove</a>&gt;</td>");
                    Console.WriteLine("		</tr>");

                    total += item.Count * book.Price;
                }

                Console.WriteLine("	</table>");
                Console.WriteLine("	Total price of all items: " + total.ToString() + " EUR");
            }

            Console.WriteLine("</body>");
            Console.WriteLine("</html>");
        }
    }
}