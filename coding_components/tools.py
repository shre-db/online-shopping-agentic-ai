__module_name__ = "tools"

__all__ = ['e_commerce_search_aggregator', 'shipping_time_estimator', 'discount_checker', 'competitor_price_comparison', 'return_policy_checker']

"""
This module contains all the mock tools that an agent can access.
"""

import random
from datetime import datetime, timedelta
import datetime
from datetime import datetime as dt

def closest_upcoming_date(day_of_week):
    # Convert the day_of_week string to a lowercase for matching
    day_of_week = day_of_week.lower()
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    if day_of_week not in days:
        raise ValueError("Invalid day of the week. Please provide a valid day of the week.")

    today = datetime.date.today()
    today_weekday = today.weekday()  # Monday is 0 and Sunday is 6
    target_weekday = days.index(day_of_week)

    # Calculate the days until the next target weekday
    days_until = (target_weekday - today_weekday + 7) % 7
    if days_until == 0:
        days_until = 7

    closest_date = today + datetime.timedelta(days=days_until)
    return closest_date.strftime('%Y-%m-%d')

# day_of_week = 'Friday'
# print(f"The closest upcoming {day_of_week} is on {closest_upcoming_date(day_of_week)}")

def e_commerce_search_aggregator(query: str, color: str = None, max_price: float = None, size: str = None):
    """
    Mock implementation of an e-commerce search aggregator.
    This function takes will take search criteria (e.g., iten name, color, price etc) as input and returns a mocked list of products that match the criteria
    
    Parameters:
        query (str): Search term (e.g., "floral skirt").
        color (str, optional): Desired color of the product.
        max_price (float, optional): Maximum budget for the product.
        size (str, optional): Desired size.
    
    Returns:
        List[dict]: A list of matching product dictionaries.
    """
    # Mock dataset of fashion items
    products = [
        {"name": "Floral Skirt", "price": 35.99, "color": "red", "size": "S", "availability": True, "link": "https://example.com/product1"},
        {"name": "Denim Jacket", "price": 79.99, "color": "blue", "size": "M", "availability": True, "link": "https://example.com/product2"},
        {"name": "White Sneakers", "price": 65.00, "color": "white", "size": "8", "availability": True, "link": "https://example.com/product3"},
        {"name": "Black Cocktail Dress", "price": 120.00, "color": "black", "size": "M", "availability": False, "link": "https://example.com/product4"},
        {"name": "Casual T-Shirt", "price": 25.00, "color": "green", "size": "L", "availability": True, "link": "https://example.com/product5"},
        {"name": "Navy Blue Blazer", "price": 115.00, "color": "navy blue", "size": "L", "availability": True, "link": "https://example.com/product6"},
        {"name": "Casual Navy Blazer", "price": 102.00, "color": "navy blue", "size": "L", "availability": True, "link": "https://example.com/product7"},
        {"name": "Classic Leather Loafers", "price": 85.00, "color": "black", "size": "9", "availability": True, "link": "https://example.com/product8"},
        {"name": "Luxury Brown Loafers", "price": 89.00, "color": "brown", "size": "9", "availability": True, "link": "https://example.com/product9"},
    ]
    
    # Filtering logic
    filtered_products = []
    for product in products:
        if query.lower() not in product["name"].lower():
            continue
        if color and product["color"].lower() != color.lower():
            continue
        if max_price and product["price"] > max_price:
            continue
        if size and product["size"].lower() != size.lower():
            continue
        filtered_products.append(product)
    
    return filtered_products if filtered_products else [{"message": "No matching products found."}]

def shipping_time_estimator(destination: str, desired_date: str, product: str=None):
    """
    Mock implementation of a shipping time estimator.
    This function estimates the shipping feasibility, cost, and delivery date based on user location, desired date and product.
    
    Parameters:
        destination (str): The user's shipping location.
        desired_date (str): Desired delivery date in 'YYYY-MM-DD' format.
        product (str): The product involved in the shipping.
    
    Returns:
        dict: Shipping feasibility, cost, and estimated delivery date.
    """
    if product == "casual navy blazer":
        return {
        "product": product,
        "destination": destination,
        "estimated_delivery_date": "delivery takes 9 days",
        "desired_delivery_date": desired_date,
        "feasible": False,
        "shipping_cost": 8.99
    }

    formatted_desired_date = closest_upcoming_date(desired_date)
    
    # Mock transit times in days based on region
    shipping_times = {
        "USA": 3,
        "Canada": 5,
        "Europe": 7,
        "Asia": 10,
        "Australia": 12,
        "Other": 15
    }
    
    # Mock shipping costs based on region
    shipping_costs = {
        "USA": 5.99,
        "Canada": 8.99,
        "Europe": 12.99,
        "Asia": 15.99,
        "Australia": 18.99,
        "Other": 25.00
    }
    
    # Determine estimated delivery time
    region = destination if destination in shipping_times else None
    if region is None:
        return "Couldn't estimate shipping time, Please specify a destination."
    transit_days = shipping_times[region]
    estimated_delivery = dt.today() + timedelta(days=transit_days)
    # print(estimated_delivery)
    # exit()
    
    # Parse desired delivery date
    try:
        desired_delivery = dt.strptime(formatted_desired_date, "%Y-%m-%d")
        # print(desired_delivery)
        # exit()
    except ValueError:
        return {"error": "Invalid date format. Use 'YYYY-MM-DD'."}
    
    # Check if delivery is feasible
    is_feasible = desired_delivery >= estimated_delivery
    cost = shipping_costs[region]
    
    return {
        "product": product,
        "destination": destination,
        "estimated_delivery_date": estimated_delivery.strftime("%Y-%m-%d"),
        "desired_delivery_date": desired_date,
        "feasible": is_feasible,
        "shipping_cost": cost
    }

def discount_checker(base_price: float, promo_code: str):
    """
    Validates and applies discount or promo codes to calculate final prices.

    Mock promo codes with discount percentages:
    SAVE10: 10% discount
    FASHION20: 20% discount
    WELCOME5: 5% discount for first-time users
    VIP30: 30% discount for VIP customers 
    
    Parameters:
        base_price (float): The original price of the product.
        promo_code (str): The discount code provided by the user.
    
    Returns:
        dict: Contains the final price after discount, applied discount percentage, and validity status.
    """
    promo_codes = {
        "SAVE10": 10,
        "FASHION20": 20,
        "WELCOME5": 5,
        "VIP30": 30
    }
    
    # Check if the promo code is valid
    if promo_code in promo_codes:
        discount_percent = promo_codes[promo_code]
        discount_amount = (discount_percent / 100) * base_price
        final_price = round(base_price - discount_amount, 2)
        # print(base_price, final_price)
        # exit()
        return {
            "valid_code": True,
            "promo_code": promo_code,
            "discount_percent": discount_percent,
            "final_price": final_price
        }
    else:
        return {
            "valid_code": False,
            "promo_code": promo_code,
            "discount_percent": 0,
            "final_price": base_price
        }

def competitor_price_comparison(product_name: str):
    """
    Mock implementation of a competitor price comparison tool. Compares prices for a given product across multiple online stores.

    Parameters:
        product_name (str): The name of the product to compare prices for.

    Returns:
        dict: A dictionary containing the product name and a list of competitor prices.
    """
    # Mock competitor price data
    competitor_prices = {
        "floral skirt": [
            {"site": "StoreM", "price": 38.99},
            {"site": "StoreB", "price": 35.50},
            {"site": "StoreX", "price": 40.00}
        ],
        "white sneakers": [
            {"site": "StoreM", "price": 68.00},
            {"site": "StoreB", "price": 72.50},
            {"site": "StoreX", "price": 70.00}
        ],
        "casual denim jacket": [
            {"site": "StoreM", "price": 75.99},
            {"site": "StoreB", "price": 80.00},
            {"site": "StoreX", "price": 78.50}
        ],
        "blazer": [
            {"site": "StoreM", "price": 110.00},
            {"site": "StoreB", "price": 115.00},
            {"site": "StoreX", "price": 105.00}
        ],
        "loafers": [
            {"site": "StoreM", "price": 88.00},
            {"site": "StoreB", "price": 85.00},
            {"site": "StoreX", "price": 86.00}
        ]
    }

    # Get competitor prices if the product exists
    prices = competitor_prices.get(product_name.lower(), [])

    return {
        "product_name": product_name,
        "competitor_prices": prices
    }

def return_policy_checker(site_name: str):
    """
    Retrieves the return poilcy details for a specified e-commerce site.

    Parameters:
        site_name (str): The name of the e-commerce site.

    Returns:
        dict: A dictionary containing the site name and its return policy details.
    """
    return_policies = {
        "StoreA": "14-day return window. Refunds processed within 7 business days.",
        "StoreB": "Returns accepted within 30 days. Items must be unworn with tags attached. A return fee of $5 is applicable",
        "StoreX": "Free returns within 45 days for members, 30 days for non-members.",
        "StoreM": "Final sale items cannot be returned. Standard returns within 21 days."
    }

    # Get return policy if available
    policy = return_policies.get(site_name, "Return policy details are unavailable for this site.")

    return {
        "site_name": site_name,
        "return_policy": policy
    }
