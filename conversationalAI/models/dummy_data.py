class DummyData:

    # Method to get products
    def getProducts(gender, skinType, hairType):

        menDrySkinProducts = [
            {'ProductID': 1, 'Name': "L'ORÉAL PARIS MEN EXPERT HYDRA INTENSIVE 24H FACE CREAM", 'Skin Type': 'Dry',
             'Gender': 'Man', 'Size': '50ML', 'Price': 10.09},
            {'ProductID': 2, 'Name': 'NIVEA MEN SENSITIVE COOLING AFTERSHAVE BALSEM', 'Skin Type': 'Dry',
             'Gender': 'Man', 'Size': '100ML', 'Price': 9.99},
        ]

        menSensitiveSkinProducts = [
            {'ProductID': 3, 'Name': "NIVEA MEN SENSITIVE STUBBLE MOISTURISER CRÈME",
             'Skin Type': 'Sensitive', 'Gender': 'Man', 'Size': '50ML', 'Price': 13.49},
            {'ProductID': 4, 'Name': "L'ORÉAL PARIS MEN EXPERT HYDRA SENSITIVE MOISTURIZING FACIAL CARE",
             'Skin Type': 'Sensitive', 'Gender': 'Man', 'Size': '50ML', 'Price': 15.15}
        ]

        womenDrySkinProducts = [
            {'ProductID': 1, 'Name': "DIADERMINE HYDRA NUTRITION DAY CREAM", 'Skin Type': 'Dry',
             'Gender': 'Woman', 'Size': '50ML', 'Price': 10.49},
            {'ProductID': 2, 'Name': 'OLAY WOMEN REGENERIST PERFUME-FREE NIGHT CREAM', 'Skin Type': 'Dry',
             'Gender': 'Woman', 'Size': '50ML', 'Price': 37.99},
        ]

        womenSensitiveSkinProducts = [
            {'ProductID': 3, 'Name': "NIVEA ESSENTIALS RESTORATIVE NIGHT CREAM",
             'Skin Type': 'Sensitive', 'Gender': 'Woman', 'Size': '50ML', 'Price': 11.49},
            {'ProductID': 4, 'Name': "GARNIER SKIN ACTIVE BOTANICAL DAY CREAM WITH ROSE WATER",
             'Skin Type': 'Sensitive', 'Gender': 'Woman', 'Size': '50ML', 'Price': 7.05}
        ]

        menDryHairProducts = [
            {'ProductID': 5, 'Name': "ALPECIN HYBRID CAFFEINE SHAMPOO", 'Hair Type': 'Dry', 'Gender': 'Man',
             'Size': '250ML', 'Price': 7.69},
            {'ProductID': 6, 'Name': "Schwarzkopf Repair & Care Shampoo", 'Hair Type': 'Dry', 'Gender': 'Both',
             'Size': '400ML', 'Price': 2.59}
        ]

        menNormalHairProducts = [
            {'ProductID': 7, 'Name': "NIVEA MEN STRONG POWER SHAMPOO", 'Hair Type': 'Normal', 'Gender': 'Man',
             'Size': '250ML', 'Price': 3.79},
            {'ProductID': 8, 'Name': "John Frieda Frizz Ease Dream Curls Shampoo", 'Hair Type': 'Normal',
             'Gender': 'Man', 'Size': '250ML', 'Price': 11.99}
        ]

        womenDryHairProducts = [
            {'ProductID': 5, 'Name': "GARNIER LOVING BLENDS ARGAN & CAMELLIA OIL SUBLIME MASK", 'Hair Type': 'Dry', 'Gender': 'Women',
             'Size': '300ML', 'Price': 6.79},
            {'ProductID': 6, 'Name': "KRUIDVAT ARGAN OIL & CARE HAIR OIL", 'Hair Type': 'Dry', 'Gender': 'Woman',
             'Size': '150ML', 'Price': 2.59}
        ]

        womenNormalHairProducts = [
            {'ProductID': 7, 'Name': "HAIRWONDER HAIR REPAIR CREAM", 'Hair Type': 'Normal', 'Gender': 'Woman',
             'Size': '150ML', 'Price': 9.09},
            {'ProductID': 8, 'Name': "ANDRÉLON INTENSE SUMMER BLONDE SHAMPOO", 'Hair Type': 'Normal',
             'Gender': 'Woman', 'Size': '300ML', 'Price': 4.49}
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

        print(products)
        return products
