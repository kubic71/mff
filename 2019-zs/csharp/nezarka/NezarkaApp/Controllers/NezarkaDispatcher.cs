using System;
using NezarkaApp.Views;
using NezarkaModels;

namespace NezarkaApp.Controllers
{
    public class NezarkaDispatcher
    {
        private string WEBSITE_NAME = "http://www.nezarka.net/"; 
        private ModelStore modelStore;

        public NezarkaDispatcher(ModelStore modelStore)
        {
            this.modelStore = modelStore;
        }

        public void Dispatch(string request)
        {
            try
            {
                string[] tokens = request.Split(' ');
                int custId = Int32.Parse(tokens[1]);
                string action = tokens[2];
                if (tokens[0] != "GET" || !customerExists(custId) || tokens.Length != 3 || !action.StartsWith(WEBSITE_NAME))
                    throw new InvalidRequestException();
                
                // strip http://www.nezarka.net/ from request
                action = action.Substring(WEBSITE_NAME.Length, action.Length - WEBSITE_NAME.Length);
                string[] act_list = action.Split('/');
                
                if (act_list.Length == 1 && act_list[0] == "Books")
                {
                    // http://www.nezarka.net/Books
                    ViewBooks.Render(custId, modelStore);
                    
                } else if (act_list.Length == 3 && act_list[0] == "Books" && act_list[1] == "Detail")
                {
                    // http://www.nezarka.net/Books/Detail/_Book_Id_
                    ViewBookDetail.Render(custId, Int32.Parse(act_list[2]), modelStore);
                    
                } else if (act_list.Length == 1 && act_list[0] == "ShoppingCart")
                {
                    // http://www.nezarka.net/ShoppingCart
                    ViewShoppingCart.Render(custId, modelStore);
                    
                } else if (act_list.Length == 3 && act_list[0] == "ShoppingCart" && act_list[1] == "Add")
                {
                    // http://www.nezarka.net/ShoppingCart/Add/_BookId_
                    CartController.Add(custId, Int32.Parse(act_list[2]), modelStore);

                } else if (act_list.Length == 3 && act_list[0] == "ShoppingCart" && act_list[1] == "Remove")
                {
                    // http://www.nezarka.net/ShoppingCart/Remove/_BookId_
                    CartController.Remove(custId, Int32.Parse(act_list[2]), modelStore);
                } else
                {
                    ViewInvalidRequest.Render();
                }
                
            }
            catch (Exception ex)
            {
                
                if (ex is InvalidRequestException || ex is FormatException || ex is IndexOutOfRangeException)
                {
                    ViewInvalidRequest.Render();
                }
                else
                {
                    throw;
                }
            }
        }

        private bool customerExists(int custID)
        {
            if (modelStore.GetCustomer(custID) == null)
                return false;
            return true;
        }
    }
}