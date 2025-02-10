import time
import base64
import streamlit as st
import textwrap
from tools import *
from system_prompt import system_prompt

response_parts = []

def process_user_query(user_query: str):
    """
    Determines which tools to invoke based on the user's query.
    
    Parameters:
        user_query (str): The natural language input from the user.

    Returns:
        str: The agent's response.
    """
    global response_parts
    response_parts = []  # Collects different parts of the final response

    # 1. Product Search + Price Constraint
    if "find" in user_query.lower() and "$" in user_query:
        # Extract details -> use mock parsing logic
        product = "floral skirt"  # This is a placeholder since we aren't using an actual model.
        max_price = 40
        size = "S"
        
        search_results = e_commerce_search_aggregator(query=product, max_price=max_price, size=size)
        discount_checker_result = discount_checker(base_price=search_results[0]['price'], promo_code='SAVE10')
        
        ai_reasoning = textwrap.dedent(f"""
            **THOUGHT**: The user wants a floral skirt under ${max_price} in size {size}. They also want to know if it is in stock and whether they can apply the discount code "SAVE10".

            I need to:
            1. Search for available products that meet the criteria
            2. Check if the item is in stock
            3. Verify if the discount code applies

            **ACTION**:  
            ```python
            e_com_search_aggregator(query="floral skirt", max_price=40, size="S")
            ```

            **OBSERVATION**:  
            `{search_results}`

            **THOUGHT**:  
            I found one product under ${max_price} that is in stock right now. Now I need to check if the discount code "SAVE10" applies to it.

            **ACTION**:  
            ```python
            discount_checker(base_price=35.99, promo_code='SAVE10')
            ```

            **OBSERVATION**:  
            `{discount_checker_result}`

            **THOUGHT**:  
            I have all the necessary information, I'll now answer the user.

            **RESPONSE**:  
            Here is the only option for Floral Skirt under ${max_price} in size {size}:
            * {search_results[0]["name"]} - ${search_results[0]['price']} (In stock)
            * Link: {search_results[0]['link']}
            * Good news! You can use the 'SAVE10' discount code, bringing the final price down to ${discount_checker_result['final_price']}!
        """)
        response_parts.append(ai_reasoning)

    # 2. Shipping Time Estimation
    if "white sneakers" in user_query.lower() or not st.session_state.sneaker_session_state:
        location = None  # Setting an initial value
        if user_query in ['USA', 'Canada', 'Europe', 'Asia', 'Australia', 'Other']:
            location = user_query
        product = "white sneakers"
        delivery_date = "Friday"
        size = "8"
        max_price = 70
        second_half = []

        if location is None or st.session_state.sneaker_session_state:
            search_results = e_commerce_search_aggregator(query=product, max_price=max_price, size=size)
            ai_reasoning = textwrap.dedent(f"""
                **THOUGHT**: The user wants white sneakers in size 8 for under $70. Additionally, they need the item to arrive by Friday.

                I need to:
                1. Search for sneakers that match the price and size criteria.
                2. Check if these items can be delivered by the deadline.

                **ACTION**:
                ```python
                e_com_search_aggregator(query="white sneakers", color="white", max_price=70, size="8")
                ```

                **OBSERVATION**:
                `{search_results}`

                **THOUGHT**: I found an item that fits the criteria. Now, I need to check if it can be delivered by Friday. Wait a second! The user didn't specify the destination which is necessary.
                I need to ask the user where the product should be delivered to.

                **RESPONSE**:
                I found one option for white sneakers under ${max_price} in size 8. To determine the shipping feasibility by {delivery_date}, could you please specify a destination?
            """)

            response_parts.append(ai_reasoning)
            st.session_state.sneaker_session_state = False
        else:
            shipping_feasblty = shipping_time_estimator(destination=location, desired_date=delivery_date)
            ai_reasoning = textwrap.dedent(f"""
                **THOUGHT**: Great! The destination is now known. I need to determine the shipping feasibility.

                **ACTION**: 
                ```python
                shipping_time_estimator(destination={location}, desired_date={delivery_date})
                ```

                **OBSERVATION**: `{shipping_feasblty}`

                **THOUGHT**: The item is available and can arrive by Friday. I'll now present the final response.

                **RESPONSE**:
                Here’s an option that meets your criteria:  
                **Classic White Sneakers** - $65.99 (In stock)  
                [View Here](https://example.com/sneakers1)  

                Estimated Delivery: {delivery_date}  
                Shipping Cost: ${shipping_feasblty['shipping_cost']}
            """)

            second_half.append(ai_reasoning)
            response_parts.append(ai_reasoning)
            

    # 4. Competitor Price Comparison
    if "any better deals" in user_query.lower():
        product = "casual denim jacket"
        current_price = 80
        product_prices = competitor_price_comparison(product_name=product)
        price_comparison = product_prices['competitor_prices']

        ai_reasoning = textwrap.dedent(f"""
            **THOUGHT**: The user has found a casual denim jacket priced at ${current_price} on siteA.
            To determine if there's a better deal, I need to:
            1. Search for the same product across competitor sites.
            2. Compare the listed prices.
            3. Present the best available price.

            **ACTION**:
            ```python
            competitor_price_comparison(product_name={product})
            ```

            **OBSERVATION**:
            [
            `{price_comparison}`
            ]

            **THOUGHT**: I found competitor listings for the same jacket.
            - SiteM offers the best price at ${price_comparison[0]['price']} (cheaper than ${price_comparison[1]['price']}).
            - SiteX has it for ${price_comparison[2]['price']} (Not significantly lower).
            - SiteB is more expensive at ${price_comparison[1]['price']}.

            **RESPONSE**:
            I found a better deal!
            Casual Denim Jacket - ${price_comparison[0]['price']} (Cheaper than ${current_price})
            Available at SiteM: [Buy Here](https://example.com/siteM_jacket)

            Other options:
            - ${price_comparison[2]['price']} at SiteX ([view](https://example.com/siteX_jacket))
            - ${price_comparison[1]['price']} at SiteB ([view](https://example.com/siteB_jacket))
        """)


        response_parts.append(ai_reasoning)

    # 5. Return Policy Checking
    if "accept returns" in user_query.lower():
        site = "StoreB"  # Extract from query

        return_policy = return_policy_checker(site_name=site)

        ai_reasoning = textwrap.dedent(f"""
            **THOUGHT**: The user wants to buy a cocktail dress from SiteB but only if returns are hassle-free.
            To determine this, I need to:
            1. Retrieve SiteB's return policy.
            2. Analyze whether it qualifies as "hassle-free."
            3. Respond to the user accordingly.

            **ACTION**:
            ```python
            return_policy_checker(site={site})
            ```

            **OBSERVATION**:
            [
            `{return_policy}`
            ]

            **THOUGHT**:
            - The return window is 30 days, which is reasonable.
            - Returns are allowed if the item is unworn and has tags attached.
            - There is a $5 restocking fee, which may be an inconvenience.

            Since there is a small fee but the overall process is straightforward, I would classify this as 'mostly hassle-free' but not entirely free of restrictions.

            **RESPONSE**:
            SiteB allows returns within 30 days as long as the dress is unworn and has its original tags attached.
            However, there is a $5 restocking fee for processing the return.

            Would you still like to proceed with this purchase?
        """)

        
        response_parts.append(ai_reasoning)

    if "stylish outfit" in user_query.lower():
        location = 'Canada'
        blazer = ["navy blue blazer", "casual navy blazer"]
        blazer_max_price = 120
        shoes = ["classic leather loafers", "luxury brown loafers"]
        shoes_max_price = 90

        # Simulation of getting multiple entries as a response from e_commerce_search_aggregator API.
        search_agg_upwr_response = [e_commerce_search_aggregator(query=item, max_price=blazer_max_price) for item in blazer]
        search_agg_shoes_response = [e_commerce_search_aggregator(query=item, max_price=shoes_max_price) for item in shoes]

        # Simulation of getting multiple entries as a response from competitor price analysis API.
        cmpttr_price_resp_blazer = competitor_price_comparison(product_name='blazer')['competitor_prices']
        cmpttr_price_resp_loafers = competitor_price_comparison(product_name='loafers')['competitor_prices']

        # Simulation of shipping feasibility
        shipping_fesblty_blazer = [shipping_time_estimator(destination=location, desired_date='Friday', product=item) for item in blazer]
        shipping_fesblty_loafers = [shipping_time_estimator(destination=location, desired_date='Friday', product=item) for item in shoes]

        # Simulate Checking discounts
        discount_blazer = discount_checker(base_price=105, promo_code="FASHION20")
        discount_loafers = discount_checker(base_price=85, promo_code="FASHION20")

        # Simulate Checking the return policies
        return_polc_blazer = return_policy_checker(site_name='StoreX')['return_policy']
        return_polc_loafers = return_policy_checker(site_name='StoreB')['return_policy']

        ai_reasoning = textwrap.dedent(f"""
            **THOUGHT**:
            - The user needs a navy blue blazer (under $120) and leather loafers (under $90).
            - They need fast shipping (arrive by Friday).
            - They want the best deal (price comparison + discounts).
            - They want hassle-free returns in case of sizing issues.

            Let me devise an action plan...
            1. Search for matching products.
            2. Compare prices across competitors.
            3. Check shipping feasibility for both items.
            4. Apply potential discount codes.
            5. Confirm return policies before finalizing recommendations.

            **ACTION**:
            ```python
            e_commerce_search_aggregator(query='navy blue blazer', max_price={blazer_max_price})
            ```

            **OBSERVATION**:
            [
            `{search_agg_upwr_response}`
            ]

            **THOUGHT**: Found two potential matches.
            1. {search_agg_upwr_response[0][0]['name']} - ${search_agg_upwr_response[0][0]['price']}
            2. {search_agg_upwr_response[1][0]['name']} - ${search_agg_upwr_response[1][0]['price']}

            **ACTION**:
            ```python
            e_commerce_search_aggregator(query='leather loafers', max_price={shoes_max_price})
            ```

            **OBSERVATION**:
            [
            `{search_agg_shoes_response}`
            ]

            **THOUGHT**: Found two potential matches for leather loafers as well.
            1. {search_agg_shoes_response[0][0]['name']} - ${search_agg_shoes_response[0][0]['price']}
            2. {search_agg_shoes_response[1][0]['name']} - ${search_agg_shoes_response[1][0]['price']}

            Great! In the worst case, we have two options for each item that are within the user's budget. I think it's a good idea to explore a bit for better deals. I'll now perform a competitor price comparison.

            **ACTION**:
            ```python
            competitor_price_comparison(product_name='navy blue blazer')
            ```

            **OBSERVATION**:
            [
            `{cmpttr_price_resp_blazer}`
            ]

            **THOUGHT**:
            - SiteM: ${cmpttr_price_resp_blazer[0]['price']} 
            - SiteB: ${cmpttr_price_resp_blazer[1]['price']} (Current Price)
            - SiteX: ${cmpttr_price_resp_blazer[2]['price']} (Better Price!)

            **ACTION**:
            ```python
            competitor_price_comparison(product_name='Classic Leather Loafers')
            ```

            **OBSERVATION**:
            [
            `{cmpttr_price_resp_loafers}`
            ]

            **THOUGHT**:
            - SiteM: ${cmpttr_price_resp_loafers[0]['price']} 
            - SiteB: ${cmpttr_price_resp_loafers[1]['price']} (Current site is the cheapest!)
            - SiteX: ${cmpttr_price_resp_loafers[2]['price']}

            Next, I'll check shipping feasibility. Looks like the user has allowed location access; the location is Canada.

            **ACTION**:
            ```python
            shipping_time_estimator(destination='Canada', desired_date='Friday', product='navy blue blazer')
            ```

            **OBSERVATION**:
            [
            `{shipping_fesblty_blazer}`
            ]

            **THOUGHT**:
            - {shipping_fesblty_blazer[0]['product']} - Available, arrives by Friday
            - {shipping_fesblty_blazer[1]['product']} - Hmmm, 9 days! Cannot be delivered by Friday

            **ACTION**:
            ```python
            shipping_time_estimator(destination='Canada', desired_date='Friday', product='Classic Leather Loafers')
            ```

            **OBSERVATION**:
            [
            `{shipping_fesblty_loafers}`
            ]

            **THOUGHT**:
            - {shipping_fesblty_loafers[0]['product']} - Available, arrives by Friday
            - {shipping_fesblty_loafers[1]['product']} - Available, arrives by Friday

            So far, there is one available option for the navy blue blazer and two for the leather loafers.

            Next, I'll explore the fourth step in the action plan I created earlier.

            **ACTION**:
            ```python
            discount_checker(base_price=105, promo_code="FASHION20")
            ```

            **OBSERVATION**:
            [
            `{discount_blazer}`
            ]

            **THOUGHT**: Promocode applied. Price optimized from $105 to ${discount_blazer['final_price']} for the blazer.

            **ACTION**:
            ```python
            discount_checker(base_price=85, promo_code="FASHION20")
            ```

            **OBSERVATION**:
            [
            `{discount_loafers}`
            ]

            **THOUGHT**: Promocode applied. Price reduced from $85 to ${discount_loafers['final_price']} for the loafers.

            Finally, I'll check the return policies for both the blazer and the loafers.

            **ACTION**:
            ```python
            return_policy_checker(site_name='Site X')
            ```

            **OBSERVATION**:
            [
            `{return_polc_blazer}`
            ]

            **THOUGHT**:
            Blazer: 45-day free returns for members! 30 days for non-members.

            **ACTION**:
            ```python
            return_policy_checker(site_name='Site B')
            ```

            **OBSERVATION**:
            [
            `{return_polc_loafers}`
            ]

            **THOUGHT**:
            Loafers: 30-day return acceptance provided items are unworn and tags are in place. $5 return fee is applicable.

            Now that I have the full information, I'll respond to the user.

            **RESPONSE**:
            Here's your outfit, optimized for price, shipping, and returns!

            1. **Navy Blue Blazer** - ${discount_blazer['final_price']} (after discount)
                - Best price from Site X (was ${cmpttr_price_resp_blazer[2]['price']})
                - Arrives by Friday
                - 45-day free returns

            2. **Classic Leather Loafers** - ${discount_loafers['final_price']} (after discount)
                - Best price from current site ${cmpttr_price_resp_loafers[1]['price']}
                - Arrives by Friday
                - 30-day return policy with a $5 restocking fee.

            Would you like me to proceed with checkout?
        """)
        response_parts.append(ai_reasoning)

    # Final response formatting
    if response_parts:
        return "\n".join(response_parts)
    else:
        return "I'm not sure how to help with that. Can you clarify your request?"

st.set_page_config(page_title="Shoppin'", page_icon=":strawberry", initial_sidebar_state='collapsed')

css_model_init = '''
<style>
.model-init {
    font-size: 15px;
    color: #888888;
}
</style>
'''
st.markdown(css_model_init, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>🍓 ShoppinGPT</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Lezz go Shoppin'</h4>", unsafe_allow_html=True)

st.markdown('')
st.markdown('')
st.markdown('')
st.markdown('')
st.markdown('')
st.markdown('')
st.markdown("<h3 style='text-align: center;'>What do you want to shop today?</h3>", unsafe_allow_html=True)

# State management for chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []
    st.session_state.first_half = None
    st.session_state.sneaker_session_state = True

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)

# Function to simulate streaming response by line
def generate_response(prompt):
    response = process_user_query(prompt)
    # Dedent the full response to remove any extra indentation
    response = textwrap.dedent(response)
    # Stream line-by-line to preserve markdown structure
    for line in response.splitlines(keepends=True):
        yield line
        time.sleep(0.1)

# User input area
if prompt := st.chat_input("Type your message here"):
    if st.session_state.sneaker_session_state:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt, unsafe_allow_html=True)

        with st.chat_message("assistant"):
            response_container = st.empty()
            response = ""
            for chunk in generate_response(prompt):
                response += chunk
                response_container.markdown(response, unsafe_allow_html=True)
        # Add assistant message to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

if prompt in ['USA', 'Canada', 'Europe', 'Asia', 'Australia', 'Other']:
    with st.chat_message("assistant"):
        response_container = st.empty()
        response = ""
        for chunk in generate_response(prompt):
            response += chunk
            response_container.markdown(response, unsafe_allow_html=True)
            
    # Add assistant message to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.clear()

st.markdown('')
st.markdown('')
st.markdown('')
st.markdown('***')
