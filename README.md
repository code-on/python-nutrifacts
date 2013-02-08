python-nutrifacts
=================

Python Client for Nutrifacts API

Usage example:

    import nutrifacts

    nutrifacts.api_domain = 'qa.api.nutrifacts.com'
    nutrifacts.GLN = '111111111111'
    nutrifacts.encryption_key = 'e0d!23f%3cx342e0'

    print nutrifacts.get_product('000011220044', 'en', '1b93a00be242442dd411beeb957210dfca48c8cc')
