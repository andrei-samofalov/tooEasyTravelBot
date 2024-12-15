class SearchConfig:
    sort = [
        "Цена и наш выбор",
        "Оценки гостей",
        "Удаленность от центра",
        "По возрастанию цены",
        "Звездность",
        "Рекомендации"
    ]
    sort_ = [
        {"data": "PRICE_RELEVANT", "text": "Цена и наш выбор"},
        {"data": "REVIEW", "text": "Оценки гостей"},
        {"data": "DISTANCE", "text": "Удаленность от центра"},
        {"data": "PRICE_LOW_TO_HIGH", "text": "По возрастанию цены"},
        {"data": "PROPERTY_CLASS", "text": "Звездность"},
        {"data": "RECOMMENDED", "text": "Рекомендации"}
    ]
    filters = [
        {"data": 'hotelName', "text": 'Filter by hotel name'},
        {"data": 'price', "text": 'Filter by price {"max": 150,"min": 30}'},
        {"data": 'guestRating', "text": 'One of the following : 35 (Good 7+)|40 (Very good 8+)|45 (Wonderful 9+)'},
        {"data": 'accessibility', "text": 'One of the following : 35 (Good 7+)|40 (Very good 8+)|45 (Wonderful 9+)'},

    ]
# filters	object	Specify filters for results.
# filters -> hotelName	string	Filter by hotel name, refer the value of regionNames -> lastSearchName field returned in .../locations/v3/search.
# * "type" must be "HOTEL"
# filters -> price	object	Filter by price. Ex : "price": {"max": 150,"min": 30}
# filters -> guestRating	string	One of the following : 35 (Good 7+)|40 (Very good 8+)|45 (Wonderful 9+)
# Ex : "guestRating": "35"
# filters -> accessibility	array of string	One of the following : SIGN_LANGUAGE_INTERPRETER|STAIR_FREE_PATH|SERVICE_ANIMAL|IN_ROOM_ACCESSIBLE|ROLL_IN_SHOWER|ACCESSIBLE_BATHROOM|ELEVATOR|ACCESSIBLE_PARKING
# Ex : "accessibility": ["SIGN_LANGUAGE_INTERPRETER","STAIR_FREE_PATH"]
# filters -> travelerType	array of string	One of the following : BUSINESS|FAMILY|LGBT
# Ex : "travelerType": ["BUSINESS","FAMILY"]
# filters -> mealPlan	array of string	One of the following : FREE_BREAKFAST|HALF_BOARD|FULL_BOARD|ALL_INCLUSIVE
# Ex : "mealPlan": ["FREE_BREAKFAST","HALF_BOARD"]
# filters -> poi	string	Filter for properties around a point of interest, format is lat,long:regionId. Ex : "poi":"12.223031,109.247187:6115844"
# * Refer destination -> regionId section to get the correct value
# filters -> regionId	string	Filter for properties with neighborhood. The value of neighborhoods -> regionId field returned right in this endpoint
# Ex : "regionId":"553248635976399837"
# filters -> lodging	array of string	One of the following : VILLA|CONDO_RESORT|PENSION|TOWNHOUSE|AGRITOURISM|HOTEL_RESORT|HOLIDAY_PARK|CONDO
# Ex : "lodging": ["VILLA","CONDO_RESORT"]
# filters -> amenities	array of string	One of the following : FREE_AIRPORT_TRANSPORTATION|OCEAN_VIEW|HOT_TUB|PETS|CASINO|SPA_ON_SITE|CRIB|BALCONY_OR_TERRACE|
# PARKING|ELECTRIC_CAR|RESTAURANT_IN_HOTEL|KITCHEN_KITCHENETTE|GYM|POOL|WASHER_DRYER|WATER_PARK|AIR_CONDITIONING|WIFI
# Ex : "amenities": ["FREE_AIRPORT_TRANSPORTATION","OCEAN_VIEW"]
# filters -> star	array of string	One of the following : 10 (1-star hotel)|20 (2-star hotel)|30 (3-star hotel)|40 (4-star hotel)|50 (5-star hotel)
# Ex : "star": ["40","50"]
# filters -> paymentType	array of string	One of the following : FREE_CANCELLATION|PAY_LATER. Ex : "paymentType": ["FREE_CANCELLATION"]
# filters -> bedroomFilter	array of string	One of the following : 0 (Studio)|1|2|3|4. Ex : "bedroomFilter": ["0","1"]
# filters -> availableFilter	string	Only one value : SHOW_AVAILABLE_ONLY. Ex : "availableFilter": "SHOW_AVAILABLE_ONLY"
