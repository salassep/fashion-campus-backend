import sys
import pathlib
from helpers import *

@grade
def auth_test():
    with safe_init(2):
        sys.path.append(f'{pathlib.Path().resolve()}/Api/Flask')
        from main import app

        app.config.update({"TESTING": True})
        c = app.test_client()
    
    valid_buyers = [
        {
            "name": "testing",
            "email": f"{get_random_string()}@gmail.com",
            "phone_number": f"0856{get_random_number()}",
            "password": gen_password()
        },
        {
            "name": "testing2",
            "email": f"{get_random_string()}@gmail.com",
            "phone_number": f"0856{get_random_number()}",
            "password": gen_password()
        }
    ]

    valid_admins = [
        {
            "name": "Admin testing",
            "email": f"{get_random_string()}@gmail.com",
            "phone_number": f"0856{get_random_number()}",
            "password": gen_password(),
            "type": "seller",
        },
    ]

    invalid_users = [
        {
            "name": "weird",
            "email": "weird@gmail.com",
            "phone_number": "12387084836769",
            "password": gen_password()
        },
        {
            "name": "weird",
            "email": "weirdgmail.com",
            "phone_number": "085754637231",
            "password": gen_password()
        }
    ]

    with Scorer(1, "4. Sign Up"):
        # Sign up with valid user as buyer
        for user in valid_buyers:
            assert_response(
                c,
                "post",
                "/sign-up",
                json=user,
                exp_json = {
                    "success": True,
                    "message": "success, user created"
                },
                exp_code=201
            )

        # Sign up with valid user as seller
        for user in valid_admins:
            assert_response(
                c,
                "post",
                "/sign-up",
                json=user,
                exp_json = {
                    "success": True,
                    "message": "success, user created"
                },
                exp_code=201
            )

        # Sign up with registered user
        assert_response(
            c,
            "post",
            "/sign-up",
            json=valid_buyers[0],
            exp_json = {
                "success": False,
                "message":  "User with the same name / email / phone already exists"
            },
            exp_code=400
        )

        # Sign up with invalid phone number
        assert_response(
            c,
            "post",
            "/sign-up",
            json=invalid_users[0],
            exp_json = {
                "success": False,
                "message": "Phone number invalid, must Indonesian phone number"
            },
            exp_code=400
        )

        # Sign up with invalid email
        assert_response(
            c,
            "post",
            "/sign-up",
            json=invalid_users[1],
            exp_json = {
                "success": False,
                "message": "Email invalid"
            },
            exp_code=400
        )

    with Scorer(1, "5. Sign in"):
        for user in valid_buyers:
        # Sign in with valid credential as buyers      
            assert_response(
                c,
                "post",
                "/sign-in",
                json={ "email": user["email"], "password": user["password"] },
                exp_json = {
                    "success": True,
                    "user_information": {
                        "name": user["name"],
                        "email": user["email"],
                        "phone_number": user["phone_number"],
                        "type": "buyer"
                    },
                    "token": IsString(),
                    "message": "Login success"
                },
                exp_code=200,
            )

        for user in valid_admins:
        # Sign in with valid credential as admins      
            assert_response(
                c,
                "post",
                "/sign-in",
                json={ "email": user["email"], "password": user["password"] },
                exp_json = {
                    "success": True,
                    "user_information": {
                        "name": user["name"],
                        "email": user["email"],
                        "phone_number": user["phone_number"],
                        "type": "seller"
                    },
                    "token": IsString(),
                    "message": "Login success"
                },
                exp_code=200,
            )

        # Sign in with invalid credential
        assert_response(
            c,
            "post",
            "/sign-in",
            json={ "email": valid_buyers[0]["email"], "password": gen_password() },
            exp_json = {
                "success": False,
                "message": "Wrong credentials"
            },
            exp_code=401,
        )

if __name__ == "__main__":
    highlight("Testing for authentication endpoint...")
    tests = [auth_test]

    final_score = 0
    perfect_score = 0
    for test_f in tests:
        total_score, total_weight = test_f()
        final_score += total_score
        perfect_score += total_weight

    perc = round(final_score / perfect_score * 100, 1)
    result = f"{COL.PASS}Test passed! {COL.ENDC}" if perc == 100.0 else f"{COL.FAIL}Test failed! {COL.ENDC}"
    highlight(
        f"{COL.BOLD}YOUR Score for authentication endpoint: {COL.ENDC} "
        + f"{COL.BLUE}{final_score}/{perfect_score} ({perc}%){COL.ENDC} "
        + result
    )

    if perc != 100.0:
        raise Exception()