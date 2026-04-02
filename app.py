from flask import Flask, render_template, request, redirect, session
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'greentropics2024'
ADMIN_PASSWORD = 'admin123'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED = {'png', 'jpg', 'jpeg', 'webp'}
VENTURES = ['cocoa', 'palmoil', 'gold', 'diamond', 'teak', 'fruit']
UPLOAD_SECTIONS = ['cocoa', 'palmoil', 'gold', 'diamond', 'teak', 'fruit', 'about', 'hero']

VENTURE_DATA = {
    'cocoa': {
        'title': 'Cocoa',
        'subtitle': 'Plantation Ownership',
        'region': 'Ashanti & Brong-Ahafo Region',
        'description': "Own shares in one of Ghana's most productive cocoa plantations. Ghana supplies over 20% of the world's cocoa — partnering with us means owning a piece of that global supply chain.",
        'hero_image': 'https://images.unsplash.com/photo-1611735341450-74d61e660ad2?w=1600&q=90',
        'overview_title': 'Why Invest in Cocoa?',
        'overview_paragraphs': [
            "Cocoa is one of the world's most traded agricultural commodities, used by global giants including Nestlé, Cadbury, Mars, and Lindt. Ghana's cocoa is internationally recognised as premium quality and commands the highest prices on the global market.",
            "When you invest in GreenTropics Ghana's cocoa plantation, you are buying shares in an active, producing farm. Your share entitles you to a proportional stake in the farm's output. Cocoa is harvested twice a year — in October and March — meaning your investment generates returns on a bi-annual cycle.",
            "Ghana's cocoa industry is regulated by COCOBOD (Ghana Cocoa Board), which guarantees a minimum purchase price for every kilogram harvested. This government-backed price floor means your investment is protected against extreme market downturns.",
            "Global cocoa prices have risen over 60% in the past 3 years due to supply shortages in West Africa. Analysts project continued strong demand as chocolate consumption grows in Asia and the Middle East. Partners in our plantation have historically seen projected annual returns of 60–80% on their initial stake, subject to harvest performance and market conditions."
        ],
        'company_links': [
            {'name': 'Nestlé', 'role': 'World\'s largest cocoa buyer'},
            {'name': 'Cadbury / Mondelez', 'role': 'Premium chocolate manufacturer'},
            {'name': 'Mars Inc.', 'role': 'Global confectionery giant'},
            {'name': 'Ghana COCOBOD', 'role': 'Government price guarantee body'},
            {'name': 'Barry Callebaut', 'role': 'World\'s largest cocoa processor'},
        ],
        'market_stats': [
            {'label': 'Global Cocoa Market Value', 'value': '$13.5 Billion'},
            {'label': 'Ghana Market Share', 'value': '20% of World Supply'},
            {'label': 'Price Growth (3 Years)', 'value': '+60%'},
            {'label': 'Harvests Per Year', 'value': '2 (Oct & Mar)'},
            {'label': 'Projected Annual Return', 'value': '60–80%*'},
            {'label': 'Price Protection', 'value': 'COCOBOD Guaranteed'},
        ],
        'facts': [
            {'label': 'Location', 'value': 'Ashanti & Brong-Ahafo'},
            {'label': 'Crop Type', 'value': 'Theobroma Cacao'},
            {'label': 'Harvest Cycles', 'value': 'Twice per year'},
            {'label': 'Regulatory Body', 'value': 'Ghana COCOBOD'},
            {'label': 'Land Status', 'value': 'Titled & Documented'},
            {'label': 'Export Channel', 'value': 'Licensed Buying Companies'},
        ],
        'tiers': [
            {'name': 'Starter', 'price': '$2,000', 'price_note': 'entry', 'desc': 'Own shares in our cocoa plantation with full documentation and bi-annual harvest returns.', 'featured': False, 'features': ['Signed share partnership agreement', 'Bi-annual harvest profit reports', 'Farm photo & video updates', 'WhatsApp updates from site', '1 acre share allocation', 'Projected return: 60–80% annually*']},
            {'name': 'Growth', 'price': '$5,000', 'price_note': 'entry', 'desc': 'A larger share stake with priority updates, site visit eligibility, and dedicated account contact.', 'featured': True, 'features': ['Everything in Starter', '3 acre share allocation', 'Quarterly video updates', 'Site visit eligibility', 'Dedicated WhatsApp contact', 'Priority harvest reports', 'Projected return: 60–80% annually*']},
            {'name': 'Premium', 'price': '$15,000', 'price_note': 'entry', 'desc': 'Full farm block ownership with maximum documentation, legal support, and annual site visit.', 'featured': False, 'features': ['Everything in Growth', '10 acre block allocation', 'Annual site visit arranged', 'Legal agreement with lawyer review', 'Export documentation access', 'Named on land lease records', 'Projected return: 60–80% annually*']},
        ],
    },
    'palmoil': {
        'title': 'Palm Oil',
        'subtitle': 'Farm Partnership',
        'region': 'Western & Central Region',
        'description': "Invest in shares of Ghana's palm oil industry — one of the most in-demand commodities on earth. Palm oil is found in over 50% of all supermarket products globally.",
        'hero_image': 'https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=1600&q=90',
        'overview_title': 'Why Invest in Palm Oil?',
        'overview_paragraphs': [
            "Palm oil is the world's most widely consumed vegetable oil, found in everything from biscuits and margarine to cosmetics, shampoo, and biodiesel. Global demand exceeds 70 million tonnes per year and continues to grow as populations in Asia and Africa expand.",
            "When you invest in GreenTropics Ghana's palm oil farm, you are buying shares in an active producing farm. Oil palms produce fruit year-round, harvested every 2 months — meaning your investment generates returns 6 times per year. This makes palm oil one of the most consistent income-generating agricultural investments available.",
            "Major global corporations including Unilever, Procter & Gamble, and Nestlé all rely on West African palm oil as a core ingredient in their supply chains. Ghana's stable political environment and fertile soils make it one of the most reliable sources of high-quality palm oil in the world.",
            "Partners in our palm oil farm have historically seen projected annual returns of 65–80% on their initial stake, driven by consistent harvests and strong commodity pricing. With 6 harvest cycles per year, returns are distributed more frequently than most agricultural investments."
        ],
        'company_links': [
            {'name': 'Unilever', 'role': 'World\'s largest palm oil consumer'},
            {'name': 'Procter & Gamble', 'role': 'Major cosmetics & food producer'},
            {'name': 'Nestlé', 'role': 'Global food & beverage giant'},
            {'name': 'Wilmar International', 'role': 'World\'s largest palm oil trader'},
            {'name': 'Ghana EPA', 'role': 'Environmental & production regulator'},
        ],
        'market_stats': [
            {'label': 'Global Palm Oil Market', 'value': '$70 Billion'},
            {'label': 'Annual Global Demand', 'value': '70 Million Tonnes'},
            {'label': 'Harvest Cycles Per Year', 'value': '6 (Every 2 Months)'},
            {'label': 'Products Containing Palm Oil', 'value': '50%+ of Supermarket Items'},
            {'label': 'Projected Annual Return', 'value': '65–80%*'},
            {'label': 'Price Trend', 'value': 'Consistently Rising'},
        ],
        'facts': [
            {'label': 'Location', 'value': 'Western & Central Region'},
            {'label': 'Crop Type', 'value': 'Elaeis Guineensis'},
            {'label': 'Production', 'value': 'Fresh Fruit Bunches (FFB)'},
            {'label': 'Harvest Cycle', 'value': 'Every 2 months'},
            {'label': 'Land Status', 'value': 'Leased & Documented'},
            {'label': 'Market', 'value': 'Local & International'},
        ],
        'tiers': [
            {'name': 'Starter', 'price': '$2,500', 'price_note': 'entry', 'desc': 'Own shares in our palm oil farm with 6 harvest cycles per year and full documentation.', 'featured': False, 'features': ['Signed share partnership agreement', 'Bi-monthly harvest reports', 'Farm photo updates', 'WhatsApp farm updates', '2 acre share allocation', 'Projected return: 65–80% annually*']},
            {'name': 'Growth', 'price': '$6,000', 'price_note': 'entry', 'desc': 'A larger stake with dedicated reporting, site visit eligibility, and weight certificate access.', 'featured': True, 'features': ['Everything in Starter', '5 acre share allocation', 'Quarterly video documentation', 'Site visit eligibility', 'Dedicated WhatsApp contact', 'Weight certificate copies', 'Projected return: 65–80% annually*']},
            {'name': 'Premium', 'price': '$18,000', 'price_note': 'entry', 'desc': 'Full farm block with maximum documentation, legal review, and annual site visit.', 'featured': False, 'features': ['Everything in Growth', '15 acre block allocation', 'Annual site visit arranged', 'Legal agreement with lawyer review', 'Buyer receipt documentation', 'Named on lease records', 'Projected return: 65–80% annually*']},
        ],
    },
    'gold': {
        'title': 'Gold',
        'subtitle': 'Mining Operations',
        'region': 'Upper West & Volta Region',
        'description': "Invest in shares of Ghana's gold mining operations — Africa's largest gold producer. Gold is the world's most trusted store of value and has never been worth zero in human history.",
        'hero_image': 'https://images.unsplash.com/photo-1610375461246-83df859d849d?w=1600&q=90',
        'overview_title': 'Why Invest in Gold?',
        'overview_paragraphs': [
            "Ghana is Africa's largest gold producer and the 6th largest in the world, producing over 130 tonnes of gold per year. Gold has been mined in Ghana for over 1,000 years — the country was historically known as the Gold Coast for good reason. Our licensed small-scale mining operations tap into this centuries-old wealth.",
            "When you invest in GreenTropics Ghana's gold operations, you are buying shares in an active licensed mining concession. Your share entitles you to a proportional stake in the gold produced, which is assayed and sold through the Precious Minerals Marketing Company (PMMC) — Ghana's government gold trading body.",
            "Gold is purchased by the world's largest banks, jewellery manufacturers, and technology companies. Major buyers include the Swiss National Bank, JP Morgan, and global jewellery giants like Tiffany & Co. and Cartier. As a shareholder in our operations, your investment is backed by one of the most universally valued commodities on earth.",
            "Gold prices have risen over 80% in the past 5 years, reaching all-time highs in 2024. With global economic uncertainty driving demand for safe-haven assets, gold investment has never been more attractive. Partners in our operations have historically seen projected annual returns of 70–85% on their initial stake, subject to production output and gold market pricing."
        ],
        'company_links': [
            {'name': 'PMMC Ghana', 'role': 'Government gold trading & assay body'},
            {'name': 'JP Morgan', 'role': 'World\'s largest gold buyer'},
            {'name': 'Swiss National Bank', 'role': 'Major gold reserve holder'},
            {'name': 'Tiffany & Co. / Cartier', 'role': 'Premium jewellery manufacturers'},
            {'name': 'Minerals Commission Ghana', 'role': 'Licensing & regulatory authority'},
        ],
        'market_stats': [
            {'label': 'Ghana Annual Production', 'value': '130+ Tonnes'},
            {'label': 'Global Gold Market', 'value': '$13 Trillion'},
            {'label': 'Gold Price Growth (5 Years)', 'value': '+80%'},
            {'label': 'Ghana World Ranking', 'value': '6th Largest Producer'},
            {'label': 'Projected Annual Return', 'value': '70–85%*'},
            {'label': 'Sales Channel', 'value': 'PMMC Government Body'},
        ],
        'facts': [
            {'label': 'Location', 'value': 'Upper West & Volta Region'},
            {'label': 'Operation Type', 'value': 'Licensed Small-Scale Mining'},
            {'label': 'Regulator', 'value': 'Minerals Commission of Ghana'},
            {'label': 'Sales Channel', 'value': 'PMMC Licensed Dealers'},
            {'label': 'License Status', 'value': 'Valid & Current'},
            {'label': 'Documentation', 'value': 'Assay Certificates Provided'},
        ],
        'tiers': [
            {'name': 'Starter', 'price': '$10,000', 'price_note': 'entry', 'desc': 'Own shares in our licensed gold mining concession with full PMMC documentation.', 'featured': False, 'features': ['Signed share partnership agreement', 'Quarterly production reports', 'Assay certificate copies', 'Site photo documentation', 'Copy of operating license', 'Projected return: 70–85% annually*']},
            {'name': 'Growth', 'price': '$25,000', 'price_note': 'entry', 'desc': 'A larger gold stake with monthly reports, site visit eligibility, and dedicated contact.', 'featured': True, 'features': ['Everything in Starter', 'Monthly production reports', 'Site visit eligibility', 'Dedicated WhatsApp contact', 'Video documentation from site', 'PMMC receipt copies', 'Projected return: 70–85% annually*']},
            {'name': 'Premium', 'price': '$50,000', 'price_note': 'entry', 'desc': 'Major gold stake with full legal documentation, named concession entry, and annual site visit.', 'featured': False, 'features': ['Everything in Growth', 'Named in concession records', 'Annual site visit arranged', 'Legal agreement with lawyer review', 'PMMC sales receipt copies', 'Priority quarterly briefings', 'Projected return: 70–85% annually*']},
        ],
    },
    'diamond': {
        'title': 'Diamond',
        'subtitle': 'Sourcing Operations',
        'region': 'Birim River Basin',
        'description': "Invest in shares of Ghana's certified diamond sourcing operations. Diamonds are among the world's most valuable natural resources — Ghana's Birim River Basin is one of West Africa's richest alluvial diamond regions.",
        'hero_image': 'https://images.unsplash.com/photo-1615486511484-92e172cc4fe0?w=1600&q=90',
        'overview_title': 'Why Invest in Diamonds?',
        'overview_paragraphs': [
            "Diamonds are one of the world's most enduringly valuable commodities. Ghana's Birim River Basin in the Eastern Region has been producing alluvial diamonds since the 1920s and remains one of West Africa's most productive diamond regions. Our sourcing operations are fully certified under the Kimberley Process Certification Scheme (KPCS).",
            "When you invest in GreenTropics Ghana's diamond operations, you are buying shares in an active certified sourcing concession. Your share entitles you to a proportional stake in the diamonds sourced, which are graded and sold through licensed dealers under full KPCS documentation — the international standard that guarantees conflict-free origin.",
            "Diamonds are purchased by the world's most prestigious jewellery houses including De Beers, Tiffany & Co., Cartier, and Graff. Industrial diamonds are also in growing demand from technology manufacturers including Samsung and Intel for use in cutting tools and semiconductor production. This dual market — luxury and industrial — provides strong price support.",
            "Global diamond prices have stabilised after a period of correction and analysts project strong growth driven by demand from India and China. Natural diamonds are increasingly scarce as major mines deplete, making new sourcing operations in Ghana highly attractive. Partners in our operations have historically seen projected annual returns of 65–80% subject to quality of stones sourced and market conditions."
        ],
        'company_links': [
            {'name': 'De Beers Group', 'role': 'World\'s largest diamond company'},
            {'name': 'Tiffany & Co.', 'role': 'Premium jewellery manufacturer'},
            {'name': 'Cartier', 'role': 'Luxury diamond jewellery house'},
            {'name': 'Kimberley Process (KPCS)', 'role': 'International conflict-free certification'},
            {'name': 'Minerals Commission Ghana', 'role': 'Licensing & regulatory authority'},
        ],
        'market_stats': [
            {'label': 'Global Diamond Market', 'value': '$89 Billion'},
            {'label': 'Natural Diamond Scarcity', 'value': 'Increasing Annually'},
            {'label': 'Certification Standard', 'value': 'Kimberley Process (KPCS)'},
            {'label': 'Key Markets', 'value': 'USA, India, China, UAE'},
            {'label': 'Projected Annual Return', 'value': '65–80%*'},
            {'label': 'Industrial Demand', 'value': 'Growing (Tech Sector)'},
        ],
        'facts': [
            {'label': 'Location', 'value': 'Birim River Basin, Eastern Region'},
            {'label': 'Operation Type', 'value': 'Alluvial Diamond Sourcing'},
            {'label': 'Certification', 'value': 'Kimberley Process (KPCS)'},
            {'label': 'Regulator', 'value': 'Minerals Commission of Ghana'},
            {'label': 'Diamond Type', 'value': 'Alluvial / Gem Quality'},
            {'label': 'Documentation', 'value': 'KPCS Certificates Provided'},
        ],
        'tiers': [
            {'name': 'Starter', 'price': '$4,000', 'price_note': 'entry', 'desc': 'Own shares in our certified diamond sourcing concession with full KPCS documentation.', 'featured': False, 'features': ['Signed share partnership agreement', 'Quarterly sourcing reports', 'Kimberley Process certificates', 'Site photo documentation', 'WhatsApp sourcing updates', 'Projected return: 65–80% annually*']},
            {'name': 'Growth', 'price': '$10,000', 'price_note': 'entry', 'desc': 'Larger diamond stake with monthly production logs, site visits, and stone documentation.', 'featured': True, 'features': ['Everything in Starter', 'Monthly production logs', 'Individual stone documentation', 'Site visit eligibility', 'Dedicated WhatsApp contact', 'Video from active sourcing sites', 'Projected return: 65–80% annually*']},
            {'name': 'Premium', 'price': '$30,000', 'price_note': 'entry', 'desc': 'Major stake with full legal documentation, named participation, and annual site visit.', 'featured': False, 'features': ['Everything in Growth', 'Named in sourcing concession', 'Annual site visit arranged', 'Legal agreement with lawyer review', 'Full KPCS export documentation', 'Priority quarterly briefings', 'Projected return: 65–80% annually*']},
        ],
    },
    'teak': {
        'title': 'Teak',
        'subtitle': 'Plantation Ownership',
        'region': 'Brong-Ahafo Region',
        'description': "Own shares in a teak plantation in Ghana — one of the world's most valuable hardwoods. Teak commands premium prices globally and Ghana's climate produces the highest quality timber.",
        'hero_image': 'https://images.unsplash.com/photo-1448375240586-882707db888b?w=1600&q=90',
        'overview_title': 'Why Invest in Teak?',
        'overview_paragraphs': [
            "Teak (Tectona grandis) is one of the most commercially valuable tropical hardwoods in the world. It is prized for its exceptional durability, natural oil content, and resistance to rot and insects. Premium teak sells for $1,500–$3,000 per cubic metre on international markets — significantly more than most other timber species.",
            "When you invest in GreenTropics Ghana's teak plantation, you are buying ownership shares in a specific, GPS-mapped plot of land. Your plot is physically marked with boundary posts and documented in your partnership agreement. Unlike most investments, you can visit and physically see exactly what you own.",
            "Teak is purchased by the world's leading furniture manufacturers, shipbuilders, and luxury interior designers. Major buyers include IKEA suppliers, yacht manufacturers, and luxury hotel chains. As global teak forests deplete due to deforestation, plantation-grown teak from legally managed operations like ours commands increasingly premium prices.",
            "Teak is a long-term investment with interim returns. From year 5 onwards, thinning operations generate income as smaller trees are harvested to allow the main crop to grow. Full harvest at maturity (15–25 years) generates the maximum return. Projected annual returns including thinning income average 50–70% from year 5, with substantially higher returns at full maturity."
        ],
        'company_links': [
            {'name': 'IKEA Suppliers', 'role': 'World\'s largest furniture buyers'},
            {'name': 'Sunseeker / Ferretti', 'role': 'Luxury yacht manufacturers'},
            {'name': 'Four Seasons / Marriott', 'role': 'Luxury hotel interior buyers'},
            {'name': 'Forestry Commission Ghana', 'role': 'Timber licensing authority'},
            {'name': 'Global Timber Exchange', 'role': 'International hardwood market'},
        ],
        'market_stats': [
            {'label': 'Teak Price Per Cubic Metre', 'value': '$1,500–$3,000'},
            {'label': 'Global Teak Demand', 'value': 'Rising (Supply Depleting)'},
            {'label': 'Interim Returns From', 'value': 'Year 5 (Thinning)'},
            {'label': 'Full Maturity', 'value': '15–25 Years'},
            {'label': 'Projected Annual Return', 'value': '50–70%* (From Yr 5)'},
            {'label': 'Land Status', 'value': 'GPS Mapped & Titled'},
        ],
        'facts': [
            {'label': 'Location', 'value': 'Brong-Ahafo Region'},
            {'label': 'Species', 'value': 'Tectona Grandis (Teak)'},
            {'label': 'Maturity Period', 'value': '15-25 years'},
            {'label': 'Interim Yields', 'value': 'From Year 5 (thinning)'},
            {'label': 'Land Status', 'value': 'GPS Mapped & Titled'},
            {'label': 'Market', 'value': 'Global Hardwood Export'},
        ],
        'tiers': [
            {'name': 'Starter', 'price': '$1,500', 'price_note': 'entry', 'desc': 'Own a GPS-mapped teak plot with annual growth reports and thinning income from year 5.', 'featured': False, 'features': ['Signed share partnership agreement', 'Annual growth reports', 'GPS plot documentation', 'Farm photo updates', '0.5 acre teak allocation', 'Projected return: 50–70%* from yr 5']},
            {'name': 'Growth', 'price': '$4,000', 'price_note': 'entry', 'desc': 'A larger teak plot with thinning yield participation and site visit eligibility.', 'featured': True, 'features': ['Everything in Starter', '2 acre teak allocation', 'Thinning yield participation (yr 5+)', 'Site visit eligibility', 'Dedicated WhatsApp contact', 'Bi-annual video updates', 'Projected return: 50–70%* from yr 5']},
            {'name': 'Premium', 'price': '$12,000', 'price_note': 'entry', 'desc': 'Full teak block with named documentation, full harvest rights, and annual site visit.', 'featured': False, 'features': ['Everything in Growth', '8 acre teak block', 'Named on land lease records', 'Annual site visit arranged', 'Legal agreement with lawyer review', 'Full harvest rights at maturity', 'Projected return: 50–70%* from yr 5']},
        ],
    },
    'fruit': {
        'title': 'Fruit',
        'subtitle': 'Farming Partnership',
        'region': 'Eastern & Volta Region',
        'description': "Invest in shares of Ghana's tropical fruit farming operations. Pineapple, mango, and citrus from Ghana are exported to Europe and North America year-round — demand has never been higher.",
        'hero_image': 'https://images.unsplash.com/photo-1619566636858-adf3ef46400b?w=1600&q=90',
        'overview_title': 'Why Invest in Fruit Farming?',
        'overview_paragraphs': [
            "Ghana's tropical fruit sector is one of the fastest-growing agricultural export industries in West Africa. The country's year-round growing climate, fertile soils, and proximity to Tema Port — one of West Africa's busiest export hubs — make it ideal for producing export-grade tropical fruits including MD2 pineapple, Tommy Atkins mango, and Valencia citrus.",
            "When you invest in GreenTropics Ghana's fruit farms, you are buying shares in active producing farms with multiple harvest cycles per year. Pineapple is harvested every 14–16 months, mango twice per year, and citrus year-round. This diversity of crops means your investment generates returns across multiple cycles annually.",
            "Ghana's fruit is purchased by major European supermarket chains including Waitrose, Tesco, and Carrefour, as well as North American importers. The EU's Everything But Arms (EBA) trade agreement gives Ghanaian fruit zero-tariff access to the European market — a significant competitive advantage that supports strong export pricing.",
            "Global demand for tropical fruit is growing at 5–7% per year driven by health trends in Western markets. Partners in our fruit farming operations have historically seen projected annual returns of 55–75% on their initial stake, driven by consistent export demand and Ghana's competitive production costs."
        ],
        'company_links': [
            {'name': 'Waitrose / Tesco', 'role': 'UK premium supermarket buyers'},
            {'name': 'Carrefour', 'role': 'Europe\'s largest supermarket chain'},
            {'name': 'Dole Food Company', 'role': 'World\'s largest fruit producer'},
            {'name': 'Ghana Export Authority', 'role': 'Export licensing & certification'},
            {'name': 'EU EBA Agreement', 'role': 'Zero-tariff EU market access'},
        ],
        'market_stats': [
            {'label': 'Global Tropical Fruit Market', 'value': '$150 Billion'},
            {'label': 'Annual Demand Growth', 'value': '5–7% Per Year'},
            {'label': 'EU Market Access', 'value': 'Zero Tariff (EBA)'},
            {'label': 'Export Port', 'value': 'Tema Port, Ghana'},
            {'label': 'Projected Annual Return', 'value': '55–75%*'},
            {'label': 'Harvest Cycles', 'value': 'Multiple Per Year'},
        ],
        'facts': [
            {'label': 'Location', 'value': 'Eastern & Volta Region'},
            {'label': 'Crops', 'value': 'Pineapple, Mango, Citrus'},
            {'label': 'Export Port', 'value': 'Tema Port, Ghana'},
            {'label': 'Harvest Cycle', 'value': 'Year-round'},
            {'label': 'Standards', 'value': 'International Export Grade'},
            {'label': 'Markets', 'value': 'Europe & North America'},
        ],
        'tiers': [
            {'name': 'Starter', 'price': '$1,500', 'price_note': 'entry', 'desc': 'Own shares in our tropical fruit farm with multiple harvest cycles and export documentation.', 'featured': False, 'features': ['Signed share partnership agreement', 'Quarterly harvest reports', 'Grade certificate copies', 'Farm photo updates', '1 acre share allocation', 'Projected return: 55–75% annually*']},
            {'name': 'Growth', 'price': '$4,500', 'price_note': 'entry', 'desc': 'Larger farm stake with export documentation access and site visit eligibility.', 'featured': True, 'features': ['Everything in Starter', '4 acre share allocation', 'Export documentation copies', 'Site visit eligibility', 'Dedicated WhatsApp contact', 'Quarterly video updates', 'Projected return: 55–75% annually*']},
            {'name': 'Premium', 'price': '$14,000', 'price_note': 'entry', 'desc': 'Full farm block with named documentation, legal review, and annual site visit.', 'featured': False, 'features': ['Everything in Growth', '12 acre block allocation', 'Named on lease records', 'Annual site visit arranged', 'Legal agreement with lawyer review', 'Direct buyer introduction', 'Projected return: 55–75% annually*']},
        ],
    },
}

def allowed(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED

def get_photos(venture):
    folder = os.path.join(UPLOAD_FOLDER, venture)
    if not os.path.exists(folder):
        return []
    return [f'/static/uploads/{venture}/{f}' for f in os.listdir(folder) if allowed(f)]

def get_pdfs():
    folder = 'static/downloads'
    if not os.path.exists(folder):
        return []
    return [f for f in os.listdir(folder) if f.endswith('.pdf')]

def get_card_photo(venture):
    photos = get_photos(venture)
    if photos:
        return photos[0]
    return VENTURE_DATA[venture]['hero_image']

@app.route('/')
def home():
    photos = {v: get_photos(v) for v in VENTURES}
    card_photos = {v: get_card_photo(v) for v in VENTURES}
    # About section photo
    about_photos = get_photos('about')
    about_img = about_photos[0] if about_photos else 'https://images.unsplash.com/photo-1586771107445-d3ca888129ff?w=900&q=85'
    hero_photos = get_photos('hero')
    hero_img = hero_photos[0] if hero_photos else None
    cert_photos = get_photos('certificates')
    downloadable_pdfs = get_pdfs()
    return render_template('index.html', photos=photos, card_photos=card_photos, about_img=about_img, hero_img=hero_img, cert_photos=cert_photos, downloadable_pdfs=downloadable_pdfs)

@app.route('/venture/<name>')
def venture(name):
    if name not in VENTURES:
        return redirect('/')
    photos = get_photos(name)
    data = VENTURE_DATA[name]
    return render_template('ventures/venture_page.html',
        photos=photos,
        title=data['title'],
        subtitle=data['subtitle'],
        region=data['region'],
        description=data['description'],
        hero_image=data['hero_image'],
        overview_title=data['overview_title'],
        overview_paragraphs=data['overview_paragraphs'],
        company_links=data['company_links'],
        market_stats=data['market_stats'],
        facts=data['facts'],
        tiers=data['tiers'],
    )

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST' and 'password' in request.form:
        if request.form['password'] == ADMIN_PASSWORD:
            session['admin'] = True
        else:
            return render_template('admin/login.html', error='Wrong password')
    if not session.get('admin'):
        return render_template('admin/login.html', error=None)
    photos = {v: get_photos(v) for v in VENTURES}
    about_photos = get_photos('about')
    hero_photos = get_photos('hero')
    downloadable_pdfs = get_pdfs()
    return render_template('admin/dashboard.html', ventures=VENTURES, photos=photos, about_photos=about_photos, hero_photos=hero_photos, downloadable_pdfs=downloadable_pdfs)

@app.route('/admin/upload', methods=['POST'])
def upload():
    if not session.get('admin'):
        return redirect('/admin')
    venture = request.form.get('venture')
    all_sections = VENTURES + ['about', 'hero', 'certificates']
    if venture not in all_sections:
        return redirect('/admin')
    files = request.files.getlist('photos')
    for file in files:
        if file and allowed(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, venture, filename))
    return redirect('/admin')

@app.route('/admin/delete', methods=['POST'])
def delete_photo():
    if not session.get('admin'):
        return redirect('/admin')
    path = request.form.get('path', '').lstrip('/')
    if path.startswith('static/uploads/') and os.path.exists(path):
        os.remove(path)
    return redirect('/admin')

@app.route('/admin/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/admin/upload-pdf', methods=['POST'])
def upload_pdf():
    if not session.get('admin'):
        return redirect('/admin')
    import os
    os.makedirs('static/downloads', exist_ok=True)
    file = request.files.get('pdf')
    if file and file.filename.endswith('.pdf'):
        from werkzeug.utils import secure_filename
        filename = secure_filename(file.filename)
        file.save('static/downloads/' + filename)
    return redirect('/admin')

@app.route('/admin/delete-pdf', methods=['POST'])
def delete_pdf():
    if not session.get('admin'):
        return redirect('/admin')
    filename = request.form.get('filename', '')
    path = 'static/downloads/' + filename
    if os.path.exists(path) and filename.endswith('.pdf'):
        os.remove(path)
    return redirect('/admin')
if __name__ == '__main__':
    app.run(debug=True)
