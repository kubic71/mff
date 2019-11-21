using System;
using System.Collections.Generic;
using System.Text;

using System.IO;

namespace NezarkaModels
{
	//
	// Model
	//

	public class ModelStore {
		private List<Book> books = new List<Book>();
		private List<Customer> customers = new List<Customer>();

		public IList<Book> GetBooks() {
			return books;
		}

		public Book GetBook(int id) {
			return books.Find(b => b.Id == id);
		}

		public Customer GetCustomer(int id) {
			return customers.Find(c => c.Id == id);
		}


		public static ModelStore LoadFrom(TextReader reader) {
			var store = new ModelStore();

			try {
				if (reader.ReadLine() != "DATA-BEGIN") {
					return null;
				}
				while (true) {
					string line = reader.ReadLine();
					if (line == null) {
						return null;
					} else if (line == "DATA-END") {
						break;
					}

					
					string[] tokens = line.Split(';');
					switch (tokens[0]) {
						case "BOOK":
							
							Book book = new Book
							{
								Id = int.Parse(tokens[1]), Title = tokens[2], Author = tokens[3],
								Price = decimal.Parse(tokens[4])
							};
							if (book.Id < 0 || book.Price < 0 || tokens.Length != 5) 
							{
								return null;
							}

							store.books.Add(book);

							break;
						case "CUSTOMER":
							Customer cust = new Customer
							{
								Id = int.Parse(tokens[1]), FirstName = tokens[2], LastName = tokens[3]
							};

							if (cust.Id < 0 || tokens.Length != 4)
							{
								return null;
							}
							store.customers.Add(cust);
							break;
						case "CART-ITEM":
							var customer = store.GetCustomer(int.Parse(tokens[1]));
							if (customer == null) {
								return null;
							}

							ShoppingCartItem item = new ShoppingCartItem
							{
								BookId = int.Parse(tokens[2]), Count = int.Parse(tokens[3])
							};

							if (store.GetBook(item.BookId) == null || item.Count < 0)
								return null;

							customer.ShoppingCart.Items.Add(item);
							break;
						default:
							return null;
					}
				}
			} catch (Exception ex) {
				if (ex is FormatException || ex is IndexOutOfRangeException) {
					return null;
				}
				throw;
			}

			return store;
		}
	}

	public class Book {
		public int Id { get; set; }
		public string Title { get; set; }
		public string Author { get; set; }
		public decimal Price { get; set; }
	}

	public class Customer {
		private ShoppingCart shoppingCart;

		public int Id { get; set; }
		public string FirstName { get; set; }
		public string LastName { get; set; }

		public ShoppingCart ShoppingCart {
			get {
				if (shoppingCart == null) {
					shoppingCart = new ShoppingCart();
				}
				return shoppingCart;
			}
			set {
				shoppingCart = value;
			}
		}
	}

	public class ShoppingCartItem {
		public int BookId { get; set; }
		public int Count { get; set; }
	}

	public class ShoppingCart {
		public int CustomerId { get; set; }
		public List<ShoppingCartItem> Items = new List<ShoppingCartItem>();

		public ShoppingCartItem GetItem(int bookId)
		{
			return Items.Find(it => it.BookId == bookId);
		}
		
		public void RemoveItem(ShoppingCartItem item)
		{
			Items.Remove(item);
		}
		
	}
}
