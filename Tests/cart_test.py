import sys
import pathlib
import uuid 
from helpers import *

@grade
def cart_test():
    with safe_init(4):
        sys.path.append(f'{pathlib.Path().resolve()}/Api/Flask')
        from main import app

        app.config.update({"TESTING": True})
        c = app.test_client()

    # Get token after buyer login
    tokens = sign_in_as_buyer(c)

    # Get user id from buyer
    user_id = run_query(f"SELECT id FROM users WHERE token = '{tokens[0]}'", commit=False)[0]['id']

    carts = None
    product_samples, products_to_cart = add_carts_to_testing_db(user_id)

    with Scorer(0.5, "11. Get user's carts"):
        # Get user carts
        assert_response(
            c,
            "get",
            '/cart',
            headers={"Authentication": tokens[0]},
            exp_json = {
                "success": True,
                "data": [
                    {
                        "id": str(products_to_cart[1]["id"]),
                        "details": {
                            "quantity": products_to_cart[1]["quantity"],
                            "size": products_to_cart[1]["size"],
                        },
                        "price": product_samples[1][6],
                        "image": IsString(),
                        "name": product_samples[1][1]
                    },
                    {
                        "id": str(products_to_cart[0]["id"]),
                        "details": {
                            "quantity": products_to_cart[0]["quantity"],
                            "size": products_to_cart[0]["size"],
                        },
                        "price": product_samples[0][6],
                        "image": IsString(),
                        "name": product_samples[0][1]
                    },
                ]
            },
            exp_code=200,
        )

        # Add quantity in cart
        assert_response(
            c,
            "post",
            '/cart',
            headers={"Authentication": tokens[0]},
            json={"id": products_to_cart[0]['product_id'], "quantity": 5, "size": products_to_cart[0]["size"]},
            exp_json = {
                "success": True,
                "message": "Item added to cart"
            },
            exp_code=201,
        )

        # Get user carts after adding quantity
        response = assert_response(
            c,
            "get",
            '/cart',
            headers={"Authentication": tokens[0]},
            exp_json = {
                "success": True,
                "data": [
                    {
                        "id": str(products_to_cart[1]["id"]),
                        "details": {
                            "quantity": products_to_cart[1]["quantity"],
                            "size": products_to_cart[1]["size"],
                        },
                        "price": product_samples[1][6],
                        "image": IsString(),
                        "name": product_samples[1][1]
                    },
                    {
                        "id": str(products_to_cart[0]["id"]),
                        "details": {
                            "quantity": products_to_cart[0]["quantity"] + 5,
                            "size": products_to_cart[0]["size"],
                        },
                        "price": product_samples[0][6],
                        "image": IsString(),
                        "name": product_samples[0][1]
                    },
                ]
            },
            exp_code=200,
        )

        if response["success"]:
            carts = response["data"]
        
        # Get buyer cart who doesnt have a cart
        assert_response(
            c,
            "get",
            '/cart',
            headers={"Authentication": tokens[1]},
            exp_json = {
                "success": True,
                "data": []
            },
            exp_code=200,
        )
    
    with Scorer(0.5, "12. Get User's Shipping Address"):
        # Delete buyer shipping address from testing database
        run_query(f"UPDATE shipping_addresses SET deleted_at = now() WHERE user_id = '{user_id}'")

        # Get shipping address from buyer who doesnt have an address
        assert_response(
            c,
            "get",
            '/user/shipping_address',
            headers={"Authentication": tokens[1]},
            exp_json = {
                "success": True,
                "data": []
            },
            exp_code=200,
        )

        user_shipping_addresses = [
            (uuid.uuid4(), user_id, 'user 1', "08123", "Cangak, Bodeh", "Pemalang")
        ]

        for id, user_id, name, phone_number, address, city in user_shipping_addresses:
            # Insert buyer shipping address data to testing database
            run_query(
                "INSERT INTO shipping_addresses(id, user_id, name, phone_number, address, city) "\
                f"VALUES('{id}', '{user_id}', '{name}', '{phone_number}', '{address}', '{city}')"
            )
        
            # Get buyer shipping address
            assert_response(
                c,
                "get",
                '/user/shipping_address',
                headers={"Authentication": tokens[0]},
                exp_json = {
                    "success": True,
                    "data": {
                        "id": str(id),
                        "name": name,
                        "phone_number": phone_number,
                        "address": address,
                        "city": city
                    }
                },
                exp_code=200,
            )

    total_price = sum(cart["price"]*cart["details"]["quantity"] for cart in carts)
    total_price_with_shipping_price = None
    with Scorer(2, "13. Get shippping price"):
        # get shipping price for user who have a cart
        response = assert_response(
            c,
            "get",
            '/shipping_price',
            headers={"Authentication": tokens[0]},
            exp_json = {
                "success": True,
                "data": [
                    {
                        "name": "regular",
                        "price": total_price*20//100 if total_price >= 200 else total_price*15//100
                    },
                    {
                        "name": "next day",
                        "price": total_price*25//100 if total_price >= 300 else total_price*20//100
                    }
                ]
            },
            exp_code=200,
        )

        total_price_with_shipping_price = total_price + response["data"][0]["price"]

        # Get shipping price for user who don't have a cart
        assert_response(
            c,
            "get",
            '/shipping_price',
            headers={"Authentication": tokens[1]},
            exp_json = {
                "success": False,
                "message": "Cart empty"
            },
            exp_code=400,
        )

    order_addresses = [("khazim", "628123456789", "Cangak", "Pemalang")]
    with Scorer(1.5, "14. Create Order"):
        # Set buyer balance to 0
        run_query(f"UPDATE users SET balance = 0 WHERE id = '{user_id}'")

        # Create order with insufficient balance
        for name, phone_number, address, city in order_addresses:
            assert_response(
                c,
                "post",
                "/order",
                headers={"authentication": tokens[0]},
                json={
                    'shipping_method': 'regular', 
                    'shipping_address': {
                        'name': name,
                        'phone_number': phone_number,
                        'address': address,
                        'city': city
                    },
                },
                exp_json={'message': 'Need top up', 'success': False},
                exp_code=400,
            )

        # Set buyer balance to 100000
        run_query(f"UPDATE users SET balance = 100000 WHERE id = '{user_id}'")

        # Create order
        for name, phone_number, address, city in order_addresses:
            assert_response(
                c,
                "post",
                "/order",
                headers={"authentication": tokens[0]},
                json={
                    'shipping_method': 'regular', 
                    'shipping_address': {
                        'name': name,
                        'phone_number': phone_number,
                        'address': address,
                        'city': city
                    },
                },
                exp_json={'message': 'Order success', 'success': True},
                exp_code=201,
            )

        # Get user cart after creat order
        assert_response(
            c,
            "get",
            '/cart',
            headers={"Authentication": tokens[0]},
            exp_json = {
                "success": True,
                "data": []
            },
            exp_code=200,
        )

        # Get buyer balance after creating order
        current_balance = 100000-total_price_with_shipping_price
        assert_response(
            c,
            "get",
            "/user/balance",
            headers={"authentication": tokens[0]},
            exp_json={
                'success': True,
                'data': {
                    'balance': current_balance
                },
                'message': f'Your balance : Rp {current_balance}',
            },
            exp_code=200,
        )

    with Scorer(1, "15. Delete Cart Item"):
        product_samples, products_to_cart = add_carts_to_testing_db(user_id)
        
        # Delete cart
        assert_response(
            c,
            "delete",
            f'/cart/{products_to_cart[0]["id"]}',
            headers={"Authentication": tokens[0]},
            exp_json = {
                "success": True,
                "message": "Cart deleted"
            },
            exp_code=200,
        )
        
        # Delete cart with invalid id 
        assert_response(
            c,
            "delete",
            f'/cart/{products_to_cart[0]["id"]}',
            headers={"Authentication": tokens[0]},
            exp_json = {
                "success": False,
                "message": "Cart not found"
            },
            exp_code=404,
        )

        # Get user cart after deleted one cart
        assert_response(
            c,
            "get",
            '/cart',
            headers={"Authentication": tokens[0]},
            exp_json = {
                "success": True,
                "data": [
                    {
                        "id": str(products_to_cart[1]["id"]),
                        "details": {
                            "quantity": products_to_cart[1]["quantity"],
                            "size": products_to_cart[1]["size"],
                        },
                        "price": product_samples[1][6],
                        "image": IsString(),
                        "name": product_samples[1][1]
                    },
                ]
            },
            exp_code=200,
        )
    
if __name__ == "__main__":
    highlight("Testing for cart endpoint...")
    tests = [cart_test]

    final_score = 0
    perfect_score = 0
    for test_f in tests:
        total_score, total_weight = test_f()
        final_score += total_score
        perfect_score += total_weight

    perc = round(final_score / perfect_score * 100, 1)
    result = f"{COL.PASS}Test passed! {COL.ENDC}" if perc == 100.0 else f"{COL.FAIL}Test failed! {COL.ENDC}"
    highlight(
        f"{COL.BOLD}YOUR Score for cart endpoint: {COL.ENDC} "
        + f"{COL.BLUE}{final_score}/{perfect_score} ({perc}%){COL.ENDC} "
        + result
    )

    if perc != 100.0:
        raise Exception()