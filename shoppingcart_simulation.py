import time , signal

shop_cart={}
members={}

# welcome
def mainmenu():
    header("WELCOME XYZ SHOP")
    print()
    print()

#Header and message
def header(text):
    print("\n"+"="*50)
    print(text.center(50))
    print("="*50)
def message(text):
    print("•", text)

#products
def pcomponent():
    component={
            "cpu":5000,
            "ram":2000,
            "gpu":10000,
            "motherboard":5000,
            "psu":2500,
            "disk":600,
    }
    return component
def pcequipment():
    equipment={
             "mouse":600,
             "keyboard":500,
             "microphone":200,
             "webcam":300,
             "headphone":300,
             "speakers":150,
             "monitor":5000
    }
    return equipment
def videogames():
    games={
        "minecraft":300,
        "elden ring":400,
        "god of war":600,
        "far cry":200,
        "diablo iv":500
    }
    return games
def listproduct(active,header_name="PRODUCT"):
    header(header_name)
    for product,price in active.items():
        print(f" {product:<25} {price:<7} $")
    print("="*50)

#menus
def categories():
    header("Categories")
    message("[C] PC Components")
    message("[E] PC Equipment")
    message("[G] PC Games")
    message("[Q] GO Back ")
def menu():
    header("MENU")
    print("[S] Shopping")
    print("[P] Show ShoppingCart")
    print("[B] Delete Product")
    print("[D] Empty the ShoppingCart")
    print("[O] Payment")
    print("[M] More Info")
    print("[Q] Quit")
#shopping
def shopping():
    mainmenu()
    products={"c":pcomponent(),"e":pcequipment(),"g":videogames()}
    while True:
        menu()
        choice_Menu = input("Your Choice: ").lower()

        if choice_Menu=="s":
            while True:
                categories()
                category_ = input("Enter Choice: ").lower()
                if category_=="q":
                    message("Return to menu")
                    break
                if category_ not in products:
                    message(f"Category not found,please try again.")
                    continue
                active=products[category_]
                while True: #add product
                    listproduct(active,"PRODUCTS")
                    add_Product=input("Add Product (Q: Return To Menu): ").lower()
                    if add_Product=="q":
                        break
                        #return to menu
                    if add_Product in active:
                        addcart(add_Product,active[add_Product])
                        message(f"Added {add_Product} to shopping cart.")
                    else:
                        message("Product not found,please try again.")
        elif choice_Menu=="p":
            showshopcart()
        elif choice_Menu=="b":
            if not shop_cart:
                header("REMOVE CART")
                message("Shopping cart is empty.")
                continue
            header("REMOVE PRODUCT")
            remove_product=input("Remove Product (Q: Return To Menu): ").lower()

            if remove_product=="q":
                message("Return to menu")
                continue
            else:
                removecart(remove_product)
        elif choice_Menu=="d":
            emptycart()
        elif choice_Menu=="o":
            payment_ok=payment()
            if payment_ok:
                break
            else:
                continue
        elif choice_Menu=="m":
                moreinfo()
        elif choice_Menu=="q":
            message("Goodbye...")
            break

#shopping cart control
def showshopcart():
    if not shop_cart:
        header("SHOPPING CART")
        message("Shopping cart is empty.")
        return

    header("SHOPPING CART")
    grand_total = 0

    for product, info in shop_cart.items():
        pricing = info["price"]
        quantity = info["quantity"]
        line_total = pricing * quantity
        grand_total += line_total
        print(f" {product:<15}  {quantity:<4} = {line_total:<7} $")

    print("="*50)
    print(f"Total: {grand_total:<7} $")
def addcart(product_name: str,price: int):
    if product_name in shop_cart:
        shop_cart[product_name]["quantity"]+=1
    else:
        shop_cart[product_name] = {"price":price,"quantity":1}
def removecart(product_name: str):
    if product_name not in shop_cart:
        message("Product not in cart.")
        return
    shop_cart[product_name]["quantity"]-=1

    if shop_cart[product_name]["quantity"]<=0:
        del shop_cart[product_name]
        message(f"Removed {product_name} from cart.")
    else:
        message(f"Reduced {product_name} from cart.")
def emptycart():
    if not shop_cart:
        message("Shopping cart is empty")
        return
    else:
        shop_cart.clear()
        message("Shopping cart is cleared")
def totalprice():
    return sum(item["price"]*item["quantity"] for item in shop_cart.values())

#payment
class TimeoutError(Exception):
    pass
def alarm_handler(signum, frame):
    raise TimeoutError
def timed_input(prompt, timeout_sec):
    signal.signal(signal.SIGALRM, alarm_handler)
    signal.alarm(timeout_sec)
    try:
        return input(prompt)
    finally:
        signal.alarm(0)
def payment():
    if not shop_cart:
        header("SHOPPING CART")
        message("Shopping cart is empty. Please add a product.")
        return False

    header("PAYMENT")
    message("You have 60 seconds to complete the payment.")

    start = time.time()

    try:
        remaining = 60 - int(time.time() - start)
        if remaining <= 0:
            raise TimeoutError
        card = timed_input("Card Numbers (16 digits): ", remaining).replace(" ", "")

        if not (card.isdigit() and len(card) == 16):
            message("Invalid card number. Please try again.")
            return False

        remaining = 60 - int(time.time() - start)
        if remaining <= 0:
            raise TimeoutError
        expiry = timed_input("Date (MM/YY): ", remaining).strip()

        if len(expiry) != 5 or expiry[2] != "/":
            message("Invalid month/year format. Please try again.")
            return False

        month, year = expiry.split("/")
        if not (month.isdigit() and year.isdigit() and 1 <= int(month) <= 12):
            message("Invalid expiration date. Please try again.")
            return False

        remaining = 60 - int(time.time() - start)
        if remaining <= 0:
            raise TimeoutError
        cvv = timed_input("CVV (3 digits): ", remaining).strip()

        if not (cvv.isdigit() and len(cvv) == 3):
            message("Invalid CVV. Please try again.")
            return False

        message("PAYMENT SUCCESSFULL")

        print()
        shoppingreceipt()
        return True


    except TimeoutError:
        header("TIMEOUT!")
        message("Time expired. Returning to menu.")
        return False
def shoppingreceipt():
    header("SHOPPING RECEIPT")

    grand_total = 0

    for product, info in shop_cart.items():
        price = info["price"]
        quantity = info["quantity"]
        line_total = price * quantity
        grand_total += line_total

        print(f"{product:<15} x {quantity:<3} = {line_total:<7} $")

    print("=" * 50)
    print(f"TOTAL: {grand_total:<7} $")
    print("=" * 50)
    print()
    header(time.strftime("Date: %d.%m.%Y  Time: %H:%M:%S"))

#sign up / sign in / login
def signup():
    header("SIGNUP")
    while True:
        username = input("Username(Min length 4 ): ")
        password = input("Password(Min length 4 ): ")
        if len(username) < 4 or len(password) < 4:
            message("Invalid nickname or password.Please try again.")
            continue
        if username in members:
            message("Nickname was taken. Please try again.")
            continue
        members[username] = password
        message("Signup successful.")
        break
def signin():
    if not members:
        header("SIGNIN")
        message("No members found.")
        return
    header("SIGNIN")
    while True:
        username = input("username: ")
        password = input("Password: ")
        if username in members and members[username] == password:
            message("Signin successful.")
            message(f"Welcome {username}.")
            return True
        message("Wrong username or password.")
        sign_choice = input("Would you like to sign up? (Y/N) and (Q: Quit): ").lower()
        if sign_choice == "y":
            signup()
        elif sign_choice == "q":
            message("Quitting.")
            message("Goodbye.")
            return False
        # "n" or others: the loop continues
def login():
    while True:
        header("LOGIN")
        options = input("[U] Sign up [S] Sign in [Q] Quit : ").lower()
        if options == "u":
            signup()
        elif options == "s":
            if signin():
                shopping()
                break
        elif options == "q":
            message("Goodbye.")
            break
        else:
            message("Invalid option. Please try again.")

#information
def moreinfo():
        header("MORE INFO")
        message("Program: XYZ Shopping Cart Simulation")
        message("Version: 1.0")
        message("Developer: Batuhan Tuna")
        message("Language: Python")
        message("Modules: time, signal")
        print()

        message("DATA MODELS USED:")
        message("- Product Model:")
        message("  Products are stored as dictionaries with name-price pairs.")
        message("  Example: {'cpu': 5000, 'ram': 2000}")

        message("- Shopping Cart Model:")
        message("  Cart is a dictionary that stores product details.")
        message("  Each product keeps price and quantity information.")
        message("  Example: {'cpu': {'price':5000, 'quantity':2}}")

        message("- User Model:")
        message("  Users are stored in a dictionary as username-password pairs.")
        message("  Example: {'batuhan': '1234'}")

        message("- Payment Model:")
        message("  Payment inputs are validated using rules and exceptions.")
        message("  signal.alarm() is used to limit input time to 60 seconds.")

#start app
login()