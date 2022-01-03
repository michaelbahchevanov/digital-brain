class DummyData:

    # Method to get products
    def getProducts(gender, skinType, hairType):

        menDrySkinProducts = [
            {'ProductID': 1, 'Name': "L'ORÉAL PARIS MEN EXPERT HYDRA INTENSIVE 24H FACE CREAM", 'Skin Type': 'Dry',
             'Gender': 'Man', 'Size': '50ML', 'Price': 10.09},
            {'ProductID': 2, 'Name': 'OLAY WOMEN REGENERIST PERFUME-FREE NIGHT CREAM', 'Skin Type': 'Dry',
             'Gender': 'Woman', 'Size': '50ML', 'Price': 37.99},
        ]

        menSensitiveSkinProducts = [
            {'ProductID': 3, 'Name': "BIODERMAL FACE WASH FACIAL CLEANSING FOR ALL SKIN TYPES",
             'Skin Type': 'Sensitive', 'Gender': 'Both', 'Size': '150ML', 'Price': 13.99},
            {'ProductID': 4, 'Name': "L'ORÉAL PARIS MEN EXPERT HYDRA SENSITIVE MOISTURIZING FACIAL CARE",
             'Skin Type': 'Sensitive', 'Gender': 'Man', 'Size': '50ML', 'Price': 15.15}
        ]

        womenDrySkinProducts = [
            {'ProductID': 1, 'Name': "L'ORÉAL PARIS MEN EXPERT HYDRA INTENSIVE 24H FACE CREAM", 'Skin Type': 'Dry',
             'Gender': 'Man', 'Size': '50ML', 'Price': 10.09},
            {'ProductID': 2, 'Name': 'OLAY WOMEN REGENERIST PERFUME-FREE NIGHT CREAM', 'Skin Type': 'Dry',
             'Gender': 'Woman', 'Size': '50ML', 'Price': 37.99},
        ]

        womenSensitiveSkinProducts = [
            {'ProductID': 3, 'Name': "BIODERMAL FACE WASH FACIAL CLEANSING FOR ALL SKIN TYPES",
             'Skin Type': 'Sensitive', 'Gender': 'Both', 'Size': '150ML', 'Price': 13.99},
            {'ProductID': 4, 'Name': "L'ORÉAL PARIS MEN EXPERT HYDRA SENSITIVE MOISTURIZING FACIAL CARE",
             'Skin Type': 'Sensitive', 'Gender': 'Man', 'Size': '50ML', 'Price': 15.15}
        ]

        menDryHairProducts = [
            {'ProductID': 5, 'Name': "Andrélon Special Keratine Repair Shampoo", 'Hair Type': 'Dry', 'Gender': 'Women',
             'Size': '300ML', 'Price': 5.49},
            {'ProductID': 6, 'Name': "Schwarzkopf Repair & Care Shampoo", 'Hair Type': 'Dry', 'Gender': 'Both',
             'Size': '400ML', 'Price': 2.59}
        ]

        menNormalHairProducts = [
            {'ProductID': 7, 'Name': "Kruidvat Sensation Tropical Shampoo", 'Hair Type': 'Normal', 'Gender': 'Both',
             'Size': '500ML', 'Price': 0.99},
            {'ProductID': 8, 'Name': "John Frieda Frizz Ease Dream Curls Shampoo", 'Hair Type': 'Normal',
             'Gender': 'Man', 'Size': '250ML', 'Price': 11.99}
        ]

        womenDryHairProducts = [
            {'ProductID': 5, 'Name': "Andrélon Special Keratine Repair Shampoo", 'Hair Type': 'Dry', 'Gender': 'Women',
             'Size': '300ML', 'Price': 5.49},
            {'ProductID': 6, 'Name': "Schwarzkopf Repair & Care Shampoo", 'Hair Type': 'Dry', 'Gender': 'Both',
             'Size': '400ML', 'Price': 2.59}
        ]

        womenNormalHairProducts = [
            {'ProductID': 7, 'Name': "Kruidvat Sensation Tropical Shampoo", 'Hair Type': 'Normal', 'Gender': 'Both',
             'Size': '500ML', 'Price': 0.99},
            {'ProductID': 8, 'Name': "John Frieda Frizz Ease Dream Curls Shampoo", 'Hair Type': 'Normal',
             'Gender': 'Man', 'Size': '250ML', 'Price': 11.99}
        ]

        products = []

        if skinType == "dry" and gender == "man":
            products.append(menDrySkinProducts)
        elif skinType == "sensitive" and gender == "man":
            products.append(menSensitiveSkinProducts)
        elif skinType == "dry" and gender == "woman":
            products.append(womenDrySkinProducts)
        elif skinType == "sensitive" and gender == "woman":
            products.append(womenSensitiveSkinProducts)

        if hairType == "dry" and gender == "man":
            products.append(menDryHairProducts)
        elif hairType == "normal" and gender == "man":
            products.append(menNormalHairProducts)
        if hairType == "dry" and gender == "woman":
            products.append(womenDryHairProducts)
        elif hairType == "normal" and gender == "woman":
            products.append(womenNormalHairProducts)

        return products
