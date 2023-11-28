import sys
import pathlib
from helpers import *

@grade
def profile_test():
    with safe_init(10):
        sys.path.append(f'{pathlib.Path().resolve()}/Api/Flask')
        from main import app

        app.config.update({"TESTING": True})
        c = app.test_client()
    
    # Get buyer token after login
    tokens = sign_in_as_buyer(c)

    # Get admin token after login
    admin_token = sign_in_as_admin(c)

    with Scorer(1, "21. Get orders"):
        # Get user id from buyer
        user_data = run_query(f"SELECT id, email, name FROM users WHERE token = '{tokens[0]}'", commit=False)[0]

        # Add carts
        product_samples, products_to_cart = add_carts_to_testing_db(user_data["id"])

        # Delete order data from testing database
        run_query(f"UPDATE orders SET deleted_at = now()")

        # Set buyer balance to 100000
        run_query(f"UPDATE users SET balance = 100000 WHERE id = '{user_data['id']}'")

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
            f"SELECT * FROM orders WHERE user_id = '{user_data['id']}' ORDER BY created_at DESC LIMIT 1",
            commit=False
        )[0]

        assert_response(
            c,
            "get",
            "/orders",
            headers={"authentication": admin_token},
            exp_json={
                "success": True,
                "data":[
                    {
                        "id": orders["id"],
                        "user_name": user_data["name"],
                        "created_at": f'{orders["created_at"]:%a, %d %B %Y}',
                        "user_id": user_data["id"],
                        "user_email": user_data["email"],
                        "total": orders["total_order"]
                    }
                ]
            },
            exp_code=200,
        )

    categories = run_query(
        "SELECT id, category_name AS name FROM categories ORDER BY created_at LIMIT 2", 
        commit=False
    )
    product_samples = [
        ("Baju Merah", "description product", [], "used", categories[0]["id"], 1000, categories[0]["name"]),
        ("Celana Jeans", "description product", ["images_p4.png"], "used", categories[1]["id"], 3000, categories[1]["name"])
    ]

    with Scorer(2, "22. Create Product"):
        for product_name, description, images, condition, category_id, price, category_name in product_samples:
            assert_response(
                c,
                "post",
                "/products",
                headers={"authentication": admin_token},
                json={
                    "product_name": product_name,
                    "description": description,
                    "images": images,
                    "condition": condition,
                    "category_id": category_id,
                    "price": price},
                exp_json={
                    "message": "Product added", 
                    'success': True
                },
                exp_code=201,
            )

        products = run_query("SELECT id FROM products ORDER BY created_at DESC LIMIT 2", commit=False)
        product_samples[0] += products[1]["id"],
        product_samples[1] += products[0]["id"],

        # Get product after adding product
        for product_name, description, images, condition, category_id, price, category_name, id in reversed(product_samples):
            assert_response(
                c,
                "get",
                f'/products/{id}',
                exp_json = {
                    "success": True,
                    "data": {
                        "id": id,
                        "category_id": category_id,
                        "category_name": category_name,
                        "title": product_name,
                        "size": ["S", "M", "L"],
                        "product_detail":  description,
                        "price": price,
                        "images_url": images if images else ["/image/default-product.png"]
                    }
                },
                exp_code=200,
            )

    with Scorer(1, "23. Update Product"):
        updated_products = [
            ("Baju Biru", "description product", ["images_p1x.png","images_p2x.png"], "new", categories[0]["id"], 5000)
        ]
        for product_name, description, images, condition, category_id, price in updated_products:
            assert_response(
                c,
                "put",
                "/products",
                headers={"authentication": admin_token},
                json={
                    "product_id":products[0]["id"],
                    "product_name": product_name,
                    "description": description,
                    "images": images,
                    "condition": condition,
                    "category_id": category_id, 
                    "price": price
                },
                exp_json={"message": "Product updated", 'success': True},
                exp_code=201,
            )

            # get the product after update
            assert_response(
                c,
                "get",
                f'/products/{products[0]["id"]}',
                exp_json = {
                    "success": True,
                    "data": {
                        "id": products[0]["id"],
                        "category_id": category_id,
                        "category_name": category_name,
                        "title": product_name,
                        "size": ["S", "M", "L"],
                        "product_detail":  description,
                        "price": price,
                        "images_url": images if images else ["/image/default-product.png"]
                    }
                },
                exp_code=200,
            )
    
    with Scorer(1, "24. Delete Product"):
        assert_response(
            c,
            "delete",
            f"/products/{products[1]['id']}",
            headers={"authentication": admin_token},
            exp_json={"message": "Product deleted", 'success': True},
            exp_code=200,
        )

        # get a product after deleted
        assert_response(
            c,
            "get",
            f'/products/{products[1]["id"]}',
            exp_json = {
                "success": False,
                "message": "Product not found"
            },
            exp_code=404,
        )
    
    # Get category data from testing database
    categories = run_query(
        "SELECT id, category_name as title FROM categories WHERE deleted_at IS NULL", commit=False
    )

    with Scorer(0.5, "24.5. Get Category"):
        # Get categories
        assert_response(
            c,
            "get",
            "/categories",
            exp_json={
                "success": True,
                "data": IsIn(categories, "title")
            },
            exp_code=200,
        )

    new_categories = ['Aksesoris', 'Blackmamba']

    with Scorer(1, "25. Add Category"):
        for category_name in new_categories:
            assert_response(
                c,
                "post",
                "/categories",
                headers={"authentication": admin_token},
                json={"category_name": category_name},
                exp_json={"message": "Category added", 'success': True},
                exp_code=201,
            )

        # Get current category data from testing database
        categories = run_query(
            "SELECT id, category_name as title FROM categories WHERE deleted_at IS NULL ORDER BY created_at DESC",
            commit=False
        )

        # Get categories after add new category
        assert_response(
            c,
            "get",
            "/categories",
            exp_json={
                "success": True,
                "data": IsIn(categories, "title")
            },
            exp_code=200,
        )
    
    update_categories = ["Shoes"]
    with Scorer(1, "26. Update Category"):
        for category_name in update_categories:
            assert_response(
                c,
                "put",
                f"/categories/{categories[0]['id']}",
                headers={"authentication": admin_token},
                json={"category_name": category_name},
                exp_json={"message": "Category updated", 'success': True},
                exp_code=200,
            )
        
        # Get current category data from testing database
        categories = run_query(
            "SELECT id, category_name as title FROM categories WHERE deleted_at IS NULL ORDER BY created_at DESC",
            commit=False
        )

        # Get categories after update category
        assert_response(
            c,
            "get",
            "/categories",
            exp_json={
                "success": True,
                "data": IsIn(categories, "title")
            },
            exp_code=200,
        )
    
    with Scorer(1, "27. Delete Category"):
        assert_response(
            c,
            "delete",
            f"/categories/{categories[0]['id']}",
            headers={"authentication": admin_token},
            exp_json={"message": "Category deleted", 'success': True},
            exp_code=200,
        )

        # Get current category data from testing database
        categories = run_query(
            "SELECT id, category_name as title FROM categories WHERE deleted_at IS NULL ORDER BY created_at DESC",
            commit=False
        )

        # Get categories after delete one category
        assert_response(
            c,
            "get",
            "/categories",
            exp_json={
                "success": True,
                "data": IsMatch(categories, "title")
            },
            exp_code=200,
        )

    run_query("DELETE FROM categories WHERE category_name IN ('Aksesoris', 'Blackmamba', 'Shoes')")

    with Scorer(1, "28. Get Total Sales"):
        total_sales = run_query("SELECT SUM(total_order) AS total FROM orders", commit=False)
        assert_response(
            c,
            "get",
            "/sales",
            headers={"authentication": admin_token},
            exp_json= {
                'success': True,
                "data": {
                    "total": total_sales[0]['total']
                },
            },
            exp_code=200,
        )
    
if __name__ == "__main__":
    highlight("Grading for Admin Page Endpoint...")
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
        f"{COL.BOLD}YOUR Score for Admin Page endpoint: {COL.ENDC} "
        + f"{COL.BLUE}{final_score}/{perfect_score} ({perc}%){COL.ENDC} "
        + result
    )

    if perc != 100.0:
        raise Exception()