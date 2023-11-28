import sys
import pathlib
from helpers import *

@grade
def profile_test():
    with safe_init(5):
        sys.path.append(f'{pathlib.Path().resolve()}/Api/Flask')
        from main import app

        app.config.update({"TESTING": True})
        c = app.test_client()
    
    # Get buyer token after login
    tokens = sign_in_as_buyer(c)

    # Get buyer data from testing database
    users = run_query(
        f"SELECT * FROM users WHERE token IN ('{tokens[0]}', '{tokens[1]}') ORDER BY created_at",
        commit=False
    )

    with Scorer(1, "16. User Details"):
        # Get user details
        for index, token in enumerate(tokens):
            assert_response(
                c,
                "get",
                "/user",
                headers={"authentication": token},
                exp_json={'data': {
                    "name": users[index]["name"],
                    "email": users[index]["email"],
                    "phone_number": users[index]["phone_number"]
                }, 'success': True},
                exp_code=200,
            )

    new_shipping_addresses = [("user baru", "081233333333", "Jl. xxxxx", "banished city")]
    with Scorer(1, "17. Change Shipping Address"):
        # Change shipping adresses
        for name, phone_number, address, city in new_shipping_addresses:
            assert_response(
                c,
                "post",
                "/user/shipping_address",
                headers={"authentication": tokens[0]},
                json={"name": name, "phone_number":  phone_number, "address":  address, "city":  city},
                exp_json={
                    'data': {
                        "name": name, 
                        "phone_number":  phone_number, 
                        "address":  address, 
                        "city":  city
                    }, 'success': True},
                exp_code=201,
            )
    
    # Set buyer balance to 0
    run_query(f"UPDATE users SET balance = 0 WHERE token = '{tokens[0]}'")

    balance = 100000

    with Scorer(1, "18. Topup User Balance"):
        # Top up buyer balance
        assert_response(
            c,
            "post",
            "/user/balance",
            headers={"authentication": tokens[0]},
            json={"amount": balance},
            exp_json={"message": "Top Up balance success", "balance": balance, 'success': True},
            exp_code=201,
        )
    
    with Scorer(1, "19. Get User Balance"):
        # Get user balance
        assert_response(
            c,
            "get",
            "/user/balance",
            headers={"authentication": tokens[0]},
            exp_json={'data': {'balance': balance}, 'message': f'Your balance : Rp {balance}', 'success': True},
            exp_code=200,
        )

        # Get user balance that never topup
        assert_response(
            c,
            "get",
            "/user/balance",
            headers={"authentication": tokens[1]},
            exp_json={'data': {'balance': 0}, 'message': f'Your balance : Rp {0}', 'success': True},
            exp_code=200,
        )
        
    with Scorer(0.5, "19.5. Get user's shipping address"):
        # Get shipping address from buyer
        for name, phone_number, address, city in new_shipping_addresses:  
            assert_response(
                c,
                "get",
                '/user/shipping_address',
                headers={"Authentication": tokens[0]},
               exp_json={
                    'data': {
                        "id": IsString(),
                        "name": name, 
                        "phone_number": phone_number, 
                        "address":  address, 
                        "city":  city
                    }, 'success': True},
                exp_code=200,
            )

    with Scorer(1, "20. Get User Order"):
        # Get user id from buyer
        user_id = run_query(f"SELECT id FROM users WHERE token = '{tokens[0]}'", commit=False)[0]['id']

        # Add carts
        product_samples, products_to_cart = add_carts_to_testing_db(user_id)

        # Delete orders from buyer
        run_query(f"UPDATE orders SET deleted_at = now() WHERE user_id = '{user_id}'")

        # Set buyer balance to 100000
        run_query(f"UPDATE users SET balance = 100000 WHERE id = '{user_id}'")

        order_addresses = [
            ('user 1', f'0856{get_random_number()}', "Cangak, Bodeh", "Pemalang")
        ]

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

        # Get latest order from buyer
        orders = run_query(
            f"SELECT * FROM orders WHERE user_id = '{user_id}' ORDER BY created_at DESC LIMIT 1",
            commit=False
        )[0]

        # Get user order
        assert_response(
            c,
            "get",
            "/user/order",
            headers={"authentication": tokens[0]},
            exp_json={
                'success': True,
                'data': [
                    {
                        "id": orders["id"],
                        "created_at": f'{orders["created_at"]:%a, %d %B %Y}',
                        "products": [
                            {
                                "id": IsString(),
                                "details": {
                                    "quantity": products_to_cart[0]["quantity"],
                                    "size": products_to_cart[0]["size"]
                                },
                                "price": product_samples[0][6] * products_to_cart[0]["quantity"],
                                "image": IsString(),
                                "name": product_samples[0][1]
                            },
                            {
                                "id": IsString(),
                                "details": {
                                    "quantity": products_to_cart[1]["quantity"],
                                    "size": products_to_cart[1]["size"]
                                },
                                "price": product_samples[1][6] * products_to_cart[1]["quantity"],
                                "image": IsString(),
                                "name": product_samples[1][1]
                            },
                        ],
                        "shipping_method": "regular",
                        "status": "Waiting",
                        "shipping_address": {
                            "name": order_addresses[0][0],
                            "phone_number": order_addresses[0][1],
                            "address": order_addresses[0][2],
                            "city": order_addresses[0][3],
                        }
                    }
                ]
            },
            exp_code=200,
        )
    
if __name__ == "__main__":
    highlight("Grading for Profile Page Endpoint...")
    tests = [profile_test]

    final_score = 0
    perfect_score = 0
    for test_f in tests:
        total_score, total_weight = test_f()
        final_score += total_score
        perfect_score += total_weight

    perc = round(final_score / perfect_score * 100, 1)
    result = f"{COL.PASS}Test passed! {COL.ENDC}" if perc == 100.0 else f"{COL.FAIL}Test failed! {COL.ENDC}"
    highlight(
        f"{COL.BOLD}YOUR Score for Profile Page endpoint: {COL.ENDC} "
        + f"{COL.BLUE}{final_score}/{perfect_score} ({perc}%){COL.ENDC} "
        + result
    )

    if perc != 100.0:
        raise Exception()