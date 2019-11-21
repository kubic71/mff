using System;
using NezarkaModels;

namespace NezarkaApp.Views
{
    public static class ViewHeader
    {
        public static void Render(int custId, ModelStore modelStore)
        {

            Customer customer = modelStore.GetCustomer(custId);

            Console.WriteLine("<!DOCTYPE html>");
            Console.WriteLine("<html lang=\"en\" xmlns=\"http://www.w3.org/1999/xhtml\">");
            Console.WriteLine("<head>");
            Console.WriteLine("	<meta charset=\"utf-8\" />");
            Console.WriteLine("	<title>Nezarka.net: Online Shopping for Books</title>");
            Console.WriteLine("</head>");
            Console.WriteLine("<body>");
            Console.WriteLine("	<style type=\"text/css\">");
            Console.WriteLine("		table, th, td {");
            Console.WriteLine("			border: 1px solid black;");
            Console.WriteLine("			border-collapse: collapse;");
            Console.WriteLine("		}");
            Console.WriteLine("		table {");
            Console.WriteLine("			margin-bottom: 10px;");
            Console.WriteLine("		}");
            Console.WriteLine("		pre {");
            Console.WriteLine("			line-height: 70%;");
            Console.WriteLine("		}");
            Console.WriteLine("	</style>");
            Console.WriteLine("	<h1><pre>  v,<br />Nezarka.NET: Online Shopping for Books</pre></h1>");
            Console.WriteLine("	" + customer.FirstName + ", here is your menu:");
            Console.WriteLine("	<table>");
            Console.WriteLine("		<tr>");
            Console.WriteLine("			<td><a href=\"/Books\">Books</a></td>");
            Console.WriteLine("			<td><a href=\"/ShoppingCart\">Cart (" + customer.ShoppingCart.Items.Count.ToString() + ")</a></td>");
            Console.WriteLine("		</tr>");
            Console.WriteLine("	</table>");

        }
    }
}