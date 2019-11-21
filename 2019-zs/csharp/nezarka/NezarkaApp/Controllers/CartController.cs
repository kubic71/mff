using NezarkaApp.Views;
using NezarkaModels;

namespace NezarkaApp.Controllers
{
    public static class CartController
    {
        public static void Add(int custId, int bookId, ModelStore modelStore)
        {
            Book bookToAdd = modelStore.GetBook(bookId);
            if (bookToAdd == null)
            {
                ViewInvalidRequest.Render();
                return;
            }
            
            ShoppingCart cart = modelStore.GetCustomer(custId).ShoppingCart;
            ShoppingCartItem item = cart.GetItem(bookId);

            if (item == null)
            {
                cart.Items.Add(new ShoppingCartItem {BookId = bookId, Count = 1});
            }
            else
            {
                item.Count += 1;
            }
            
            ViewShoppingCart.Render(custId, modelStore);
        }

        public static void Remove(int custId, int bookId, ModelStore modelStore)
        {
            ShoppingCart cart = modelStore.GetCustomer(custId).ShoppingCart;
            ShoppingCartItem item = cart.GetItem(bookId);
            
            if (item == null)
            {
                ViewInvalidRequest.Render();
                return;
            }

            item.Count -= 1;
            if (item.Count == 0)
            {
                cart.RemoveItem(item);
            }
            
            ViewShoppingCart.Render(custId, modelStore);
        }
        
    }
}