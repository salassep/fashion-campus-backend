import sys
import pathlib
import uuid
from helpers import *

@grade
def product_detail_test():
    with safe_init(2):
        sys.path.append(f'{pathlib.Path().resolve()}/Api/Flask')
        from main import app

        app.config.update({"TESTING": True})
        c = app.test_client()

    # Get category data from testing database
    categories = run_query(
        "SELECT id, category_name FROM categories WHERE deleted_at IS NULL LIMIT 1", commit=False
    )

    product_samples = [
        (uuid.uuid4(), "Baju Merah", "description product", [], "used", categories[0]["id"], 1000),
        (uuid.uuid4(), "Celana Jeans", "description product", ["images_p4.png"], "used", categories[0]["id"], 3000)
    ]

    with Scorer(1, "9. Get product details"):

        # Insert data product to testing database
        add_products_to_testing_db(product_samples)

        # get the product
        for id, product_name, description, images, condition, category_id, price in product_samples:
            assert_response(
                c,
                "get",
                f'/products/{id}',
                exp_json = {
                    "success": True,
                    "data": {
                        "id": str(id),
                        "title": product_name,
                        "size": ["S", "M", "L"],
                        "product_detail":  description,
                        "price": price,
                        "images_url": images if images else ["/image/default-product.png"],
                        "category_id": category_id,
                        "category_name": categories[0]["category_name"]
                    }
                },
                exp_code=200,
            )

        # get a product that doesn't exist
        assert_response(
            c,
            "get",
            f'/products/prod2',
            exp_json = {
                "success": False,
                "message": "Product not found"
            },
            exp_code=404,
        )

    # Get token after buyer login
    tokens = sign_in_as_buyer(c)

    # Get user id from buyer
    user_id = run_query(f"SELECT id FROM users WHERE token = '{tokens[0]}'", commit=False)[0]['id']

    # Delete the cart data owned by the buyer
    run_query(f"UPDATE carts SET deleted_at = now() WHERE user_id = '{user_id}'")

    products_to_cart = [
        {
            "id": product_samples[0][0],
            "quantity": 10,
            "size": "M"
        },
        {
            "id": product_samples[1][0],
            "quantity": 5,
            "size": "L"
        }
    ]

    with Scorer(2, "10. Add to cart"):
        # Succesfully added item to cart
        for product in products_to_cart:
            assert_response(
                c,
                "post",
                '/cart',
                headers={"Authentication": tokens[0]},
                json={"id": product['id'], "quantity": product["quantity"], "size": product["size"]},
                exp_json = {
                    "success": True,
                    "message": "Item added to cart"
                },
                exp_code=201,
            )

        # Add item to cart without token    
        assert_response(
            c,
            "post",
            '/cart',
            json={"id": products_to_cart[0]['id'], "quantity": 10, "size": "M"},
            exp_json = {
                "success": False,
                "message": "Token is required"
            },
            exp_code=401,
        )

        # Add item to cart with invalid token
        assert_response(
            c,
            "post",
            '/cart',
            headers={"Authentication": "sdlajhfuagwejfsjdfjhsdfhgsdjaf"},
            json={"id": products_to_cart[0]['id'], "quantity": 10, "size": "M"},
            exp_json = {
                "success": False,
                "message": "Token invalid"
            },
            exp_code=401,
        )

        # Add item to cart with invalid product    
        assert_response(
            c,
            "post",
            '/cart',
            headers={"Authentication": tokens[0]},
            json={"id": "invalid_product", "quantity": 10, "size": "M"},
            exp_json = {
                "success": False,
                "message": "Product not found"
            },
            exp_code=404,
        )

        # Add item to cart with invalid size
        assert_response(
            c,
            "post",
            '/cart',
            headers={"Authentication": tokens[0]},
            json={"id": "invalid_product", "quantity": 10, "size": "XL"},
            exp_json = {
                "success": False,
                "message": "'XL' is not one of ['S', 'M', 'L']"
            },
            exp_code=400,
        )

        # Add quantity in cart
        assert_response(
            c,
            "post",
            '/cart',
            headers={"Authentication": tokens[0]},
            json={"id": products_to_cart[0]['id'], "quantity": 5, "size": "M"},
            exp_json = {
                "success": True,
                "message": "Item added to cart"
            },
            exp_code=201,
        )

    

if __name__ == "__main__":
    highlight("Testing for product detail endpoint...")
    tests = [product_detail_test]

    final_score = 0
    perfect_score = 0
    for test_f in tests:
        total_score, total_weight = test_f()
        final_score += total_score
        perfect_score += total_weight

    perc = round(final_score / perfect_score * 100, 1)
    result = f"{COL.PASS}Test passed! {COL.ENDC}" if perc == 100.0 else f"{COL.FAIL}Test failed! {COL.ENDC}"
    highlight(
        f"{COL.BOLD}YOUR Score for product detail endpoint: {COL.ENDC} "
        + f"{COL.BLUE}{final_score}/{perfect_score} ({perc}%){COL.ENDC} "
        + result
    )

    if perc != 100.0:
        raise Exception()