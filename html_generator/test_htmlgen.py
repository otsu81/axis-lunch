from html_generator import HTMLGenerator

menus = {
    "Paolos": {
        "mon": "PASTA AL POLLO E FUNGHI 95 KR\nPASTA PUTANESCA 95 KR\nPIZZA SALAMI FINOCCHIONA 95 KR\nPIZZA CAPRICCIOSA 95 KR\nPIZZA SICILIANA 95 KR",
        "tue": "PASTA SALSICCIA AL SUGO 95 KR\nPASTA ZUCCHINI 95 KR\nPIZZA DI SALUMI MISTI 95 KR\nPIZZA BOSCAIOLA 95 KR\nPIZZA CON ZUCCA 95 KR",
        "wed": "PASTA BOLOGNESE 95 KR\nPASTA POMMODORINI E PINOLI 95 KR\nPIZZA CALABRESE 95 KR\nPIZZA DI PARMA 95 KR\nPIZZA CON BARBABIETOLA ROSSA 95 KR",
        "thu": "PASTA SALMONE AFFUMICATO 95 KR\nPASTA ALLA VELLUTATA DI FUNGHI 95 KR\nPIZZA QUATTRO STAGIONI 95 KR\nPIZZA CON ANATTRA 95 KR\nPIZZA CON MOZZARELLA DI BUFFALO 95 KR",
        "fri": "PASTA ALLA CARBONARA 95 KR\nPASTA ALLA NORMA 95 KR\nPIZZA CON BRESAOLA 95 KR\nPurjol\u00f6k\nPIZZA CON PANCETTA 95 KR\nPIZZA CAPRINHA 95 KR"
    },
    "Pieplow": {
        "mon": "Casarecce pasta, spicy tomato sauce with `Nduja. Served with burrata & parmesan\nCasarecce pasta, spicy tomato sauce. Served with burrata & parmesan",
        "tue": "Pannbiff with potato cake, fried onion, cucumber & creamed gravy\nGF\nVegetarian pirogi with mixed salad & blue cheese cr\u00e8me\nLF",
        "wed": "Chipotle glazed brisket with potato salad, summer vegetables & steak sauce\nGF\nVegetarian lasagna with tomato salad & rocket salad",
        "thu": "Chili chicken with glass noodle salad, mango, coriander, beansprouts, lime & spring onion\nLF\nChili quorn filets with glass noodle salad, mango, coriander, beansprouts, lime & spring onion\nLF",
        "fri": "Closed \u2013 Happy Midsummer"
    }
}

for r in menus:
    for d in menus[r]:
        menus[r][d] = menus[r][d].replace('\n', '</p><p>')

grnr = HTMLGenerator(
        menus,
        index_template_path='html_templates/index_template.html',
        menu_template_path='html_templates/row_template.html',
        output_path='sandbox/index.html'
    )


grnr.make_html()

# print(grnr.make_restaurant_row('paolos', menu['Paolos']))